import Panel from "../common/Panel";

export default function QosPanel({ qosData, loading, error, lastUpdated }) {
  const linkUtilization = qosData?.link_utilization || [];
  const targets = qosData?.qos_targets || {};

  const avgTx =
    linkUtilization.length > 0
      ? linkUtilization.reduce((sum, e) => sum + Number(e.tx_mbps || 0), 0) /
        linkUtilization.length
      : 0;
  const avgRx =
    linkUtilization.length > 0
      ? linkUtilization.reduce((sum, e) => sum + Number(e.rx_mbps || 0), 0) /
        linkUtilization.length
      : 0;

  return (
    <Panel title="QoS" subtitle="Live link utilization snapshots and QoS targets">
      {loading ? <p className="muted">Loading QoS metrics...</p> : null}
      {error ? <p className="error">{error}</p> : null}

      <div className="kpi-row">
        <div>
          <span className="kpi-label">Stats Interval</span>
          <strong>{qosData?.stats_interval || 0}s</strong>
        </div>
        <div>
          <span className="kpi-label">Ports Observed</span>
          <strong>{linkUtilization.length}</strong>
        </div>
        <div>
          <span className="kpi-label">Avg TX / RX</span>
          <strong className="small">{avgTx.toFixed(2)} / {avgRx.toFixed(2)} Mbps</strong>
        </div>
        <div>
          <span className="kpi-label">Last Update</span>
          <strong className="small">
            {lastUpdated ? new Date(lastUpdated).toLocaleTimeString() : "-"}
          </strong>
        </div>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>DPID</th>
              <th>Port</th>
              <th>TX (Mbps)</th>
              <th>RX (Mbps)</th>
              <th>TX Errors</th>
              <th>RX Errors</th>
            </tr>
          </thead>
          <tbody>
            {linkUtilization.map((entry) => (
              <tr key={`${entry.dpid}-${entry.port}`}>
                <td className="mono">{entry.dpid}</td>
                <td>{entry.port}</td>
                <td>{Number(entry.tx_mbps || 0).toFixed(2)}</td>
                <td>{Number(entry.rx_mbps || 0).toFixed(2)}</td>
                <td>{entry.tx_errors || 0}</td>
                <td>{entry.rx_errors || 0}</td>
              </tr>
            ))}
            {linkUtilization.length === 0 ? (
              <tr>
                <td colSpan={6} className="muted">
                  No utilization samples yet. Wait for stats polling under traffic.
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>

      <details>
        <summary>QoS class targets</summary>
        <pre className="mono small">{JSON.stringify(targets, null, 2)}</pre>
      </details>
    </Panel>
  );
}
