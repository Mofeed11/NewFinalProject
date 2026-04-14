const API_BASE = (
  process.env.REACT_APP_API_BASE || "http://127.0.0.1:8080"
).replace(/\/$/, "");

async function request(path) {
  const started = performance.now();
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status} on ${path}`);
  }
  const data = await response.json();
  const latencyMs = performance.now() - started;
  return { data, latencyMs };
}

export function getTopology() {
  return request("/api/topology");
}

export function getFlows() {
  return request("/api/flows");
}

export function getQos() {
  return request("/api/qos");
}

export function getRl() {
  return request("/api/rl");
}

export { API_BASE };
