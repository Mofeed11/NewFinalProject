# Dashboard Agent Guide (Ryu-Integrated)

This file guides any future coding agent to build and maintain the dashboard in `dashboard/` so it works with the current SDN project backend (`src/controller.py`).

## Current Dashboard Analysis

- Frontend stack is **Create React App** (CRA), not Next.js.
- Active entry is `src/App.js` (because `src/index.js` imports `./App`).
- `src/App.jsx` is an older/alternate implementation and is currently unused.
- `src/App.js` is a very large monolithic file and is tightly coupled to **old POX-style** endpoints under `/topo/*`.
- `package.json` has `"proxy": "http://localhost:8000"`, which is for POX and does not match the current Ryu REST API on port `8080`.
- Current backend now exposes read-only Ryu endpoints:
  - `/api/topology`
  - `/api/flows`
  - `/api/qos`
  - `/api/rl`
- Conclusion: the current UI is feature-rich, but endpoint contracts are mismatched with the active backend.

## Integration Truth (Backend Contract)

Use these endpoints as source of truth:

1. `GET /api/topology`
   - Returns: `{ nodes: [...], links: [{ src, dst, port }] }`
2. `GET /api/flows`
   - Returns: `{ flows: [{ flow_key, class_id, class_name, packets_collected, classified }] }`
3. `GET /api/qos`
   - Returns: `{ stats_interval, link_utilization: [...], qos_targets }`
4. `GET /api/rl`
   - Returns: `{ epsilon, min_epsilon, q_table_size, current_delay_level, states }`

These are currently read-only; do not assume write endpoints exist.

## Required Runtime Rules

- Run Ryu in virtualenv:
  - `source /home/mohammed/ryu-env/bin/activate`
  - `ryu-manager src/controller.py --observe-links`
- Run Mininet as root (outside `ryu-env`):
  - `sudo mn -c && sudo python3 scripts/topology.py`
- Run frontend as user `mohammed` (not root):
  - `cd dashboard && npm start`

## Dashboard Build Plan (Do In Order)

1. Keep CRA baseline (do not migrate framework during integration pass).
2. Create a small API layer (`src/api/client.js`) with base URL:
   - `REACT_APP_API_BASE=http://127.0.0.1:8080`
3. Replace direct `fetch("/topo/..." )` calls with the 4 `/api/*` endpoints.
4. Build focused Ryu views first:
   - Topology
   - Flows + class distribution
   - QoS link utilization
   - RL progress (epsilon, q-table size, sample states)
5. Add polling with safe intervals:
   - topology/flows every 2s
   - qos/rl every 3-5s
6. Handle empty data gracefully (controller running before traffic starts).
7. Only after stable integration, add advanced UI features.

## Recommended Frontend Structure

- `src/api/client.js`
- `src/hooks/usePolling.js`
- `src/components/topology/TopologyPanel.jsx`
- `src/components/flows/FlowTable.jsx`
- `src/components/qos/QosPanel.jsx`
- `src/components/rl/RlPanel.jsx`
- `src/pages/Dashboard.jsx`

## Migration Notes From Current `App.js`

- Keep visual style ideas, but avoid carrying over POX-only features that require non-existent endpoints (alerts/test launcher/cmdlog actions).
- If a section depends on unavailable backend writes, mark it as `coming soon` instead of failing requests.
- Do not silently fallback to `localhost:8000`; backend is on `8080`.

## Definition of Done

- Dashboard starts with `npm start` and no critical runtime errors.
- All 4 `/api/*` calls succeed and render live values.
- UI remains responsive with polling enabled for at least 10 minutes.
- Works on desktop and mobile widths.
- No root-required frontend commands.

## Common Pitfalls

- Port conflict (`8080` already in use).
- Mininet not started -> topology links may be empty.
- No traffic generated -> flows/qos may look empty even when integration is correct.
- CORS issues if requests are sent to wrong host/port.

## Optional Next Backlog

- Add backend endpoints for alerts/tests/actions only after read-only dashboard is stable.
- Split monolithic `src/App.js` into domain components.
- Add e2e checks for API contract drift.
