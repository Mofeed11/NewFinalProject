import Panel from "../common/Panel";

function nodeLabel(node) {
  if (typeof node === "number") return `s${node}`;
  return String(node);
}

function createLayout(nodes, width, height) {
  const map = new Map();
  const centerX = width / 2;
  const centerY = height / 2;
  const radius = Math.min(width, height) * 0.36;
  const total = Math.max(nodes.length, 1);

  nodes.forEach((node, index) => {
    const angle = (Math.PI * 2 * index) / total;
    map.set(node, {
      x: centerX + radius * Math.cos(angle),
      y: centerY + radius * Math.sin(angle),
    });
  });

  return map;
}

export default function TopologyPanel({ topology, loading, error, lastUpdated }) {
  const nodes = topology?.nodes || [];
  const links = topology?.links || [];
  const width = 520;
  const height = 300;
  const positions = createLayout(nodes, width, height);

  return (
    <Panel
      title="Topology"
      subtitle="Switch nodes and discovered directed links from Ryu"
    >
      {loading ? <p className="muted">Loading topology...</p> : null}
      {error ? <p className="error">{error}</p> : null}

      <div className="kpi-row">
        <div>
          <span className="kpi-label">Nodes</span>
          <strong>{nodes.length}</strong>
        </div>
        <div>
          <span className="kpi-label">Links</span>
          <strong>{links.length}</strong>
        </div>
        <div>
          <span className="kpi-label">Last Update</span>
          <strong className="small">
            {lastUpdated ? new Date(lastUpdated).toLocaleTimeString() : "-"}
          </strong>
        </div>
      </div>

      <div className="topology-canvas-wrap">
        <svg
          className="topology-canvas"
          viewBox={`0 0 ${width} ${height}`}
          preserveAspectRatio="xMidYMid meet"
          role="img"
          aria-label="Live topology graph"
        >
          <defs>
            <marker
              id="arrow"
              viewBox="0 0 10 10"
              refX="8"
              refY="5"
              markerWidth="5"
              markerHeight="5"
              orient="auto-start-reverse"
            >
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#76c5ff" />
            </marker>
          </defs>

          {links.map((link, idx) => {
            const src = positions.get(link.src);
            const dst = positions.get(link.dst);
            if (!src || !dst) return null;
            return (
              <g key={`edge-${idx}`}>
                <line
                  x1={src.x}
                  y1={src.y}
                  x2={dst.x}
                  y2={dst.y}
                  stroke="#5b8eb8"
                  strokeWidth="1.6"
                  markerEnd="url(#arrow)"
                  opacity="0.85"
                />
              </g>
            );
          })}

          {nodes.map((node) => {
            const point = positions.get(node);
            if (!point) return null;
            return (
              <g key={`node-${node}`}>
                <circle
                  cx={point.x}
                  cy={point.y}
                  r="13"
                  fill="#122338"
                  stroke="#9ed4ff"
                  strokeWidth="2"
                />
                <text
                  x={point.x}
                  y={point.y + 4}
                  textAnchor="middle"
                  className="topology-node-label"
                >
                  {nodeLabel(node)}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Source</th>
              <th>Destination</th>
              <th>Port</th>
            </tr>
          </thead>
          <tbody>
            {links.map((link, idx) => (
              <tr key={`${link.src}-${link.dst}-${idx}`}>
                <td>{nodeLabel(link.src)}</td>
                <td>{nodeLabel(link.dst)}</td>
                <td>{link.port}</td>
              </tr>
            ))}
            {links.length === 0 ? (
              <tr>
                <td colSpan={3} className="muted">
                  No links yet. Start Mininet and wait for discovery.
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </Panel>
  );
}
