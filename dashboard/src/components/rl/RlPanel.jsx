import Panel from "../common/Panel";

function formatState(state) {
  if (!Array.isArray(state)) return "-";
  return `class=${state[0]}, util=${state[1]}, delay=${state[2]}`;
}

export default function RlPanel({ rlData, loading, error, lastUpdated }) {
  const states = rlData?.states || [];

  const epsilon = Number(rlData?.epsilon ?? 0);
  const minEpsilon = Number(rlData?.min_epsilon ?? 0);
  const progress = minEpsilon > 0 ? Math.min(100, ((1 - epsilon) / (1 - minEpsilon)) * 100) : 0;

  return (
    <Panel title="RL Agent" subtitle="Q-learning runtime state from controller memory">
      {loading ? <p className="muted">Loading RL data...</p> : null}
      {error ? <p className="error">{error}</p> : null}

      <div className="kpi-row kpi-wrap">
        <div>
          <span className="kpi-label">Epsilon</span>
          <strong>{Number(rlData?.epsilon ?? 0).toFixed(4)}</strong>
        </div>
        <div>
          <span className="kpi-label">Min Epsilon</span>
          <strong>{Number(rlData?.min_epsilon ?? 0).toFixed(4)}</strong>
        </div>
        <div>
          <span className="kpi-label">Q-Table States</span>
          <strong>{rlData?.q_table_size || 0}</strong>
        </div>
        <div>
          <span className="kpi-label">Delay Level</span>
          <strong>{rlData?.current_delay_level ?? 0}</strong>
        </div>
        <div>
          <span className="kpi-label">Learning Progress</span>
          <strong>{progress.toFixed(1)}%</strong>
        </div>
        <div>
          <span className="kpi-label">Last Update</span>
          <strong className="small">
            {lastUpdated ? new Date(lastUpdated).toLocaleTimeString() : "-"}
          </strong>
        </div>
      </div>

      <div className="progress-track" aria-label="RL epsilon decay progress">
        <div className="progress-fill" style={{ width: `${progress}%` }} />
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>State</th>
              <th>Q Values</th>
            </tr>
          </thead>
          <tbody>
            {states.map((s, idx) => (
              <tr key={idx}>
                <td className="mono">{formatState(s.state)}</td>
                <td className="mono small">{Array.isArray(s.q_values) ? s.q_values.map((v) => Number(v).toFixed(3)).join(", ") : "-"}</td>
              </tr>
            ))}
            {states.length === 0 ? (
              <tr>
                <td colSpan={2} className="muted">
                  No learned states yet. Generate classified traffic to populate Q-table.
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </Panel>
  );
}
