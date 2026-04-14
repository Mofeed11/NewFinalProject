import Panel from "../common/Panel";

export default function FlowPanel({ flowsData, loading, error, lastUpdated }) {
  const flows = flowsData?.flows || [];

  const classCounts = flows.reduce((acc, flow) => {
    const key = flow.class_name || "Unknown";
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});

  return (
    <Panel title="Flows" subtitle="Tracked and classified flow state from controller memory">
      {loading ? <p className="muted">Loading flows...</p> : null}
      {error ? <p className="error">{error}</p> : null}

      <div className="kpi-row kpi-wrap">
        <div>
          <span className="kpi-label">Total Flows</span>
          <strong>{flows.length}</strong>
        </div>
        <div>
          <span className="kpi-label">Classified</span>
          <strong>{flows.filter((f) => f.classified).length}</strong>
        </div>
        <div>
          <span className="kpi-label">Last Update</span>
          <strong className="small">
            {lastUpdated ? new Date(lastUpdated).toLocaleTimeString() : "-"}
          </strong>
        </div>
      </div>

      <div className="chips">
        {Object.entries(classCounts).map(([name, count]) => (
          <span className="chip" key={name}>
            {name}: {count}
          </span>
        ))}
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Flow Key</th>
              <th>Class</th>
              <th>Packets Collected</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {flows.map((flow, idx) => (
              <tr key={idx}>
                <td className="mono">{Array.isArray(flow.flow_key) ? flow.flow_key.join(" | ") : "-"}</td>
                <td>{flow.class_name || "Unknown"}</td>
                <td>{flow.packets_collected}</td>
                <td>{flow.classified ? "Classified" : "Collecting"}</td>
              </tr>
            ))}
            {flows.length === 0 ? (
              <tr>
                <td colSpan={4} className="muted">
                  No tracked flows yet. Generate traffic (VoIP/HTTP/FTP/etc.) to populate this table.
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </Panel>
  );
}
