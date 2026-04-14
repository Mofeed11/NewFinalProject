import { useMemo, useState } from "react";
import { API_BASE, getFlows, getQos, getRl, getTopology } from "../api/client";
import StatCard from "../components/common/StatCard";
import TopologyPanel from "../components/topology/TopologyPanel";
import FlowPanel from "../components/flows/FlowPanel";
import QosPanel from "../components/qos/QosPanel";
import RlPanel from "../components/rl/RlPanel";
import usePolling from "../hooks/usePolling";

function useApiState() {
  return useState({
    data: null,
    loading: true,
    error: null,
    latencyMs: null,
    lastUpdated: null,
  });
}

export default function Dashboard() {
  const [topology, setTopology] = useApiState();
  const [flows, setFlows] = useApiState();
  const [qos, setQos] = useApiState();
  const [rl, setRl] = useApiState();

  usePolling(async () => {
    try {
      const result = await getTopology();
      setTopology({
        data: result.data,
        loading: false,
        error: null,
        latencyMs: result.latencyMs,
        lastUpdated: Date.now(),
      });
    } catch (err) {
      setTopology((prev) => ({
        data: prev.data,
        loading: false,
        error: err.message,
        latencyMs: prev.latencyMs,
        lastUpdated: prev.lastUpdated,
      }));
    }
  }, 2000, []);

  usePolling(async () => {
    try {
      const result = await getFlows();
      setFlows({
        data: result.data,
        loading: false,
        error: null,
        latencyMs: result.latencyMs,
        lastUpdated: Date.now(),
      });
    } catch (err) {
      setFlows((prev) => ({
        data: prev.data,
        loading: false,
        error: err.message,
        latencyMs: prev.latencyMs,
        lastUpdated: prev.lastUpdated,
      }));
    }
  }, 2000, []);

  usePolling(async () => {
    try {
      const result = await getQos();
      setQos({
        data: result.data,
        loading: false,
        error: null,
        latencyMs: result.latencyMs,
        lastUpdated: Date.now(),
      });
    } catch (err) {
      setQos((prev) => ({
        data: prev.data,
        loading: false,
        error: err.message,
        latencyMs: prev.latencyMs,
        lastUpdated: prev.lastUpdated,
      }));
    }
  }, 4000, []);

  usePolling(async () => {
    try {
      const result = await getRl();
      setRl({
        data: result.data,
        loading: false,
        error: null,
        latencyMs: result.latencyMs,
        lastUpdated: Date.now(),
      });
    } catch (err) {
      setRl((prev) => ({
        data: prev.data,
        loading: false,
        error: err.message,
        latencyMs: prev.latencyMs,
        lastUpdated: prev.lastUpdated,
      }));
    }
  }, 4000, []);

  const endpointHealth = useMemo(
    () => [
      {
        name: "/api/topology",
        ok: !topology.error,
        latencyMs: topology.latencyMs,
        lastUpdated: topology.lastUpdated,
      },
      {
        name: "/api/flows",
        ok: !flows.error,
        latencyMs: flows.latencyMs,
        lastUpdated: flows.lastUpdated,
      },
      {
        name: "/api/qos",
        ok: !qos.error,
        latencyMs: qos.latencyMs,
        lastUpdated: qos.lastUpdated,
      },
      {
        name: "/api/rl",
        ok: !rl.error,
        latencyMs: rl.latencyMs,
        lastUpdated: rl.lastUpdated,
      },
    ],
    [
      topology.error,
      topology.latencyMs,
      topology.lastUpdated,
      flows.error,
      flows.latencyMs,
      flows.lastUpdated,
      qos.error,
      qos.latencyMs,
      qos.lastUpdated,
      rl.error,
      rl.latencyMs,
      rl.lastUpdated,
    ]
  );

  const status = useMemo(() => {
    const hasError = topology.error || flows.error || qos.error || rl.error;
    return hasError ? "degraded" : "connected";
  }, [topology.error, flows.error, qos.error, rl.error]);

  const avgLatency = useMemo(() => {
    const values = endpointHealth
      .map((item) => item.latencyMs)
      .filter((v) => typeof v === "number");
    if (values.length === 0) return 0;
    return values.reduce((a, b) => a + b, 0) / values.length;
  }, [endpointHealth]);

  const latestUpdate = useMemo(() => {
    const values = endpointHealth
      .map((item) => item.lastUpdated)
      .filter((v) => typeof v === "number");
    if (values.length === 0) return null;
    return Math.max(...values);
  }, [endpointHealth]);

  return (
    <main className="dashboard-root">
      <header className="dashboard-header">
        <div>
          <h1>SDN QoS-Aware Dashboard</h1>
          <p>
            Integrated with Ryu REST API at <code>{API_BASE}</code>
          </p>
        </div>
        <span className={`status-pill ${status}`}>{status.toUpperCase()}</span>
      </header>

      <section className="api-health">
        <div className="api-health-header">
          <h3>API Health</h3>
          <span className="muted small">
            Avg latency: {avgLatency.toFixed(1)} ms
            {latestUpdate
              ? ` | Last update: ${new Date(latestUpdate).toLocaleTimeString()}`
              : ""}
          </span>
        </div>
        <div className="api-health-grid">
          {endpointHealth.map((ep) => (
            <div className="api-item" key={ep.name}>
              <span className={`api-dot ${ep.ok ? "ok" : "bad"}`} />
              <code>{ep.name}</code>
              <span className="muted small">
                {typeof ep.latencyMs === "number"
                  ? `${ep.latencyMs.toFixed(1)} ms`
                  : "-"}
              </span>
            </div>
          ))}
        </div>
      </section>

      <section className="stats-grid">
        <StatCard
          label="Topology Nodes"
          value={(topology.data?.nodes || []).length}
          hint="switch graph nodes"
        />
        <StatCard
          label="Topology Links"
          value={(topology.data?.links || []).length}
          hint="directed link entries"
        />
        <StatCard
          label="Tracked Flows"
          value={(flows.data?.flows || []).length}
          hint="flow tracker size"
        />
        <StatCard
          label="RL Epsilon"
          value={Number(rl.data?.epsilon ?? 0).toFixed(4)}
          hint="exploration rate"
        />
        <StatCard
          label="Avg API Latency"
          value={`${avgLatency.toFixed(1)} ms`}
          hint="across active endpoints"
        />
      </section>

      <section className="panels-grid">
        <TopologyPanel
          topology={topology.data}
          loading={topology.loading}
          error={topology.error}
          lastUpdated={topology.lastUpdated}
        />
        <FlowPanel
          flowsData={flows.data}
          loading={flows.loading}
          error={flows.error}
          lastUpdated={flows.lastUpdated}
        />
        <QosPanel
          qosData={qos.data}
          loading={qos.loading}
          error={qos.error}
          lastUpdated={qos.lastUpdated}
        />
        <RlPanel
          rlData={rl.data}
          loading={rl.loading}
          error={rl.error}
          lastUpdated={rl.lastUpdated}
        />
      </section>
    </main>
  );
}
