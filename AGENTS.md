# OpenCode Context: SDN QoS-Aware Routing Project

This project combines Software-Defined Networking (Ryu + Mininet), Machine Learning (Decision Tree for traffic classification), and Reinforcement Learning (Q-learning for routing). 

## Current Phase: Dashboard Development
The goal is to build a modern dashboard to visualize the network state, RL agent progress, and traffic classifications.

### Architecture
- **Backend (SDN Controller):** Python 3.9 using the Ryu framework. The controller must expose data via a Ryu REST API (`ryu.app.wsgi.WSGIApplication`).
- **Frontend (Dashboard):** React / Next.js.
- **Emulator:** Mininet (custom 14-switch, 8-host tree topology).

### Development Constraints & Permissions (Crucial)
1. **Ryu Controller Environment:** Ryu MUST be run inside its dedicated virtual environment located at `/home/mohammed/ryu-env/`. 
   - *Activation:* `source /home/mohammed/ryu-env/bin/activate`
   - *Command:* `ryu-manager src/controller.py --observe-links`
2. **Mininet Environment:** Mininet MUST be run as `root` in the main system environment (outside the `ryu-env`).
   - *Command:* `sudo mn -c && sudo python3 scripts/topology.py`
3. **Next.js Frontend:** The frontend should be run as the standard user (`mohammed`), likely using `npm run dev` in a new `dashboard` directory. Do NOT run npm commands as root.

### Required REST API Endpoints (To be implemented in Ryu)
The dashboard needs real-time data directly from controller memory. Future agents should implement these endpoints in `src/controller.py` or a dedicated API module:
- `/api/topology` - List of switches, hosts, and active links.
- `/api/flows` - Current active flows and their ML classifications (VoIP, Video, etc.).
- `/api/qos` - Real-time delay, jitter, loss, and throughput metrics per class.
- `/api/rl` - Current Q-table state, latest rewards, and current Epsilon decay value.
- `/api/simulation/start` - (Optional) Webhook to trigger `scripts/traffic_generator.py` for testing from the UI.

### Common Pitfalls
- **Traffic Generator:** The synthetic traffic generator (`scripts/traffic_generator.py`) must have a server running (`--server`) on the destination host before TCP traffic (FTP/HTTP) is sent. 
- **Flow Bidirectionality:** A single TCP test generates two OpenFlow tracks (forward and reverse ACK). The dashboard should handle or group these gracefully.
- **Port Conflicts:** Ryu's default REST API runs on port 8080. Ensure the Next.js dev server runs on 3000 to avoid conflicts. Enable CORS in the Ryu REST app so Next.js can fetch data.