# src/controller.py
import json

from webob import Response
from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import (
    MAIN_DISPATCHER,
    DEAD_DISPATCHER,
    set_ev_cls,
    CONFIG_DISPATCHER,
)
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4, tcp, udp, arp
from ryu.topology import event, switches
from ryu.topology.api import get_switch, get_link
from ryu.lib import hub

import time
import os
import numpy as np
import joblib
import pandas as pd
import networkx as nx
from itertools import islice

# Constants for classes (0=VoIP, 1=Video, 2=HTTP, 3=FTP, 4=DNS, 5=Background)
CLASS_NAMES = {0: "VoIP", 1: "Video", 2: "HTTP", 3: "FTP", 4: "DNS", 5: "Background"}
PACKETS_TO_COLLECT = 10  # Number of packets before classification
K_PATHS = 3  # Number of paths to consider for RL
NUM_QUEUES = 3  # 0=High, 1=Medium, 2=Best Effort
CLASS_TO_QUEUE = {
    0: 0,  # VoIP    -> High
    1: 0,  # Video   -> High
    2: 1,  # HTTP    -> Medium
    3: 1,  # FTP     -> Medium
    4: 2,  # DNS     -> Best Effort
    5: 2,  # Background -> Best Effort
}
QOS_FLOW_PRIORITY = 10
QOS_CONTROLLER_INSTANCE_NAME = "qos_controller_app"


class QoSDashboardController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(QoSDashboardController, self).__init__(req, link, data, **config)
        self.qos_app = data[QOS_CONTROLLER_INSTANCE_NAME]

    def _json_response(self, payload):
        body = json.dumps(payload, indent=2, default=str)
        resp = Response(
            content_type="application/json; charset=utf-8", body=body.encode("utf-8")
        )
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return resp

    def _options_response(self):
        resp = Response(status=200)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return resp

    @route("qos_topology", "/api/topology", methods=["GET", "OPTIONS"])
    def topology(self, req, **kwargs):
        if req.method == "OPTIONS":
            return self._options_response()
        return self._json_response(self.qos_app.get_topology_snapshot())

    @route("qos_flows", "/api/flows", methods=["GET", "OPTIONS"])
    def flows(self, req, **kwargs):
        if req.method == "OPTIONS":
            return self._options_response()
        return self._json_response(self.qos_app.get_flows_snapshot())

    @route("qos_qos", "/api/qos", methods=["GET", "OPTIONS"])
    def qos(self, req, **kwargs):
        if req.method == "OPTIONS":
            return self._options_response()
        return self._json_response(self.qos_app.get_qos_snapshot())

    @route("qos_rl", "/api/rl", methods=["GET", "OPTIONS"])
    def rl(self, req, **kwargs):
        if req.method == "OPTIONS":
            return self._options_response()
        return self._json_response(self.qos_app.get_rl_snapshot())


class QLearningAgent:
    """Tabular Q-Learning Agent for SDN QoS Routing"""

    def __init__(
        self,
        num_actions=K_PATHS * NUM_QUEUES,
        alpha=0.1,
        gamma=0.9,
        epsilon=1.0,
        min_epsilon=0.1,
        decay=0.995,
    ):
        self.q_table = {}
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.decay = decay

    def get_q_values(self, state):
        if state not in self.q_table:
            self.q_table[state] = [0.0] * self.num_actions
        return self.q_table[state]

    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.num_actions)  # Explore
        q_values = self.get_q_values(state)
        return np.argmax(q_values)  # Exploit

    def update(self, state, action, reward, next_state):
        q_values = self.get_q_values(state)
        next_q_values = self.get_q_values(next_state)
        best_next_action = np.argmax(next_q_values)

        # Q-Learning Formula
        td_target = reward + self.gamma * next_q_values[best_next_action]
        td_error = td_target - q_values[action]
        q_values[action] += self.alpha * td_error

        # Decay epsilon
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.decay


class QoSController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {"wsgi": WSGIApplication}

    def __init__(self, *args, **kwargs):
        super(QoSController, self).__init__(*args, **kwargs)
        wsgi = kwargs["wsgi"]
        self.mac_to_port = {}
        self.datapaths = {}
        self.net = nx.DiGraph()

        self.ip_to_dpid = {}
        self.mac_to_dpid = {}

        self.flow_tracker = {}
        self.classified_flows = set()

        self.link_utilization = {}
        self.prev_port_stats = {}
        self.stats_interval = 5

        self.flow_stats = {}
        self.current_delay_level = 0

        QOS_TARGETS = {
            0: {"max_delay": 0.15, "max_jitter": 0.03, "max_loss": 0.01},
            1: {"max_delay": 0.40, "max_jitter": 0.05, "max_loss": 0.01},
            2: {"max_delay": 1.00, "max_jitter": 0.10, "max_loss": 0.05},
            3: {"max_delay": 2.00, "max_jitter": 0.20, "max_loss": 0.05},
            4: {"max_delay": 0.50, "max_jitter": 0.05, "max_loss": 0.01},
            5: {"max_delay": 5.00, "max_jitter": 0.50, "max_loss": 0.10},
        }
        self.qos_targets = QOS_TARGETS

        # RL Agent initialization
        self.rl_agent = QLearningAgent()

        # Load ML Model
        model_path = os.path.join(os.path.dirname(__file__), "../data/dt_model.pkl")
        if os.path.exists(model_path):
            self.logger.info("Loading Decision Tree Model from %s", model_path)
            self.clf = joblib.load(model_path)
        else:
            self.logger.error(
                "Model file not found! Please run train_classifier.py first."
            )
            self.clf = None

        self.monitor_thread = hub.spawn(self._monitor)

        wsgi.register(QoSDashboardController, {QOS_CONTROLLER_INSTANCE_NAME: self})

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Install table-miss flow entry
        # We specify NO MATCH (meaning it matches everything)
        # Action is to send it to the controller (OFPP_CONTROLLER)
        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)
        ]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(
                datapath=datapath,
                buffer_id=buffer_id,
                priority=priority,
                match=match,
                instructions=inst,
            )
        else:
            mod = parser.OFPFlowMod(
                datapath=datapath, priority=priority, match=match, instructions=inst
            )
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.info("Register datapath: %016x", datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.info("Unregister datapath: %016x", datapath.id)
                del self.datapaths[datapath.id]

    @set_ev_cls(event.EventSwitchEnter)
    def get_topology_data(self, ev):
        switch_list = get_switch(self, None)
        switches_dp = [switch.dp.id for switch in switch_list]
        self.net.add_nodes_from(switches_dp)

        links_list = get_link(self, None)
        for link in links_list:
            self.net.add_edge(link.src.dpid, link.dst.dpid, port=link.src.port_no)
            self.net.add_edge(link.dst.dpid, link.src.dpid, port=link.dst.port_no)

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(5)

    def _request_stats(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)
        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        dpid = ev.msg.datapath.id
        flow_data = []
        for stat in ev.msg.body:
            if stat.priority >= QOS_FLOW_PRIORITY:
                flow_data.append(
                    {
                        "packet_count": stat.packet_count,
                        "byte_count": stat.byte_count,
                        "duration_sec": stat.duration_sec,
                        "duration_nsec": stat.duration_nsec,
                    }
                )
        self.flow_stats[dpid] = flow_data

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        dpid = ev.msg.datapath.id
        for stat in ev.msg.body:
            port_no = stat.port_no
            key = (dpid, port_no)

            rx_bytes = stat.rx_bytes
            tx_bytes = stat.tx_bytes
            rx_pkts = stat.rx_packets
            tx_pkts = stat.tx_packets
            rx_errs = stat.rx_errors
            tx_errs = stat.tx_errors

            if key in self.prev_port_stats:
                prev = self.prev_port_stats[key]
                dt = self.stats_interval
                tx_speed = (tx_bytes - prev["tx_bytes"]) * 8 / (dt * 1e6)
                rx_speed = (rx_bytes - prev["rx_bytes"]) * 8 / (dt * 1e6)
                self.link_utilization[key] = {
                    "tx_mbps": max(0, tx_speed),
                    "rx_mbps": max(0, rx_speed),
                    "rx_errors": rx_errs - prev["rx_errors"],
                    "tx_errors": tx_errs - prev["tx_errors"],
                    "rx_packets": rx_pkts,
                    "tx_packets": tx_pkts,
                }

            self.prev_port_stats[key] = {
                "rx_bytes": rx_bytes,
                "tx_bytes": tx_bytes,
                "rx_errors": rx_errs,
                "tx_errors": tx_errs,
            }

        self._update_delay_level()

    def k_shortest_paths(self, src, dst, k=K_PATHS):
        try:
            return list(islice(nx.shortest_simple_paths(self.net, src, dst), k))
        except nx.NetworkXNoPath:
            return []

    def _update_delay_level(self):
        if not self.link_utilization:
            self.current_delay_level = 0
            return
        avg_util = np.mean(
            [v["tx_mbps"] + v["rx_mbps"] for v in self.link_utilization.values()]
        )
        if avg_util > 12:
            self.current_delay_level = 2
        elif avg_util > 6:
            self.current_delay_level = 1
        else:
            self.current_delay_level = 0

    def get_rl_state(self, class_id):
        if not self.link_utilization:
            return (class_id, 0, self.current_delay_level)
        avg_util = np.mean(
            [v["tx_mbps"] + v["rx_mbps"] for v in self.link_utilization.values()]
        )
        if avg_util > 12:
            util_level = 2
        elif avg_util > 6:
            util_level = 1
        else:
            util_level = 0
        return (class_id, util_level, self.current_delay_level)

    def compute_reward(self, class_id, path):
        if not path or len(path) < 2:
            return -10.0
        targets = self.qos_targets.get(class_id, self.qos_targets[5])
        reward = 5.0
        total_errors = 0
        for i in range(len(path) - 1):
            for dpid, port in [(path[i], None), (path[i + 1], None)]:
                for key, util in self.link_utilization.items():
                    if key[0] == dpid:
                        total_errors += util.get("rx_errors", 0) + util.get(
                            "tx_errors", 0
                        )
        if total_errors > 0:
            reward -= total_errors * 2
        avg_util = (
            np.mean(
                [v["tx_mbps"] + v["rx_mbps"] for v in self.link_utilization.values()]
            )
            if self.link_utilization
            else 0
        )
        if avg_util > 16:
            reward -= 3.0
        elif avg_util < 6:
            reward += 3.0
        return max(-10.0, min(10.0, reward))

    def get_topology_snapshot(self):
        def _int_node(value):
            try:
                return int(value)
            except (TypeError, ValueError):
                return value

        return {
            "nodes": sorted(_int_node(node) for node in self.net.nodes),
            "links": [
                {
                    "src": _int_node(src),
                    "dst": _int_node(dst),
                    "port": data.get("port"),
                }
                for src, dst, data in self.net.edges(data=True)
            ],
        }

    def get_flows_snapshot(self):
        flows = []
        for flow_key, tracker in self.flow_tracker.items():
            flows.append(
                {
                    "flow_key": list(flow_key),
                    "class_id": tracker.get("class_id"),
                    "class_name": CLASS_NAMES.get(tracker.get("class_id"), "Unknown"),
                    "packets_collected": len(tracker.get("packets", [])),
                    "classified": tracker.get("class_id") is not None,
                }
            )
        return {"flows": flows}

    def get_qos_snapshot(self):
        return {
            "stats_interval": self.stats_interval,
            "link_utilization": [
                {
                    "dpid": int(dpid),
                    "port": int(port),
                    **values,
                }
                for (dpid, port), values in self.link_utilization.items()
            ],
            "qos_targets": self.qos_targets,
        }

    def get_rl_snapshot(self):
        return {
            "epsilon": self.rl_agent.epsilon,
            "min_epsilon": self.rl_agent.min_epsilon,
            "q_table_size": len(self.rl_agent.q_table),
            "current_delay_level": self.current_delay_level,
            "states": [
                {
                    "state": list(state),
                    "q_values": q_values,
                }
                for state, q_values in list(self.rl_agent.q_table.items())[:50]
            ],
        }

    def _extract_classify_and_route(self, flow_key, tracker, src_dpid, dst_dpid, msg):
        timestamps = tracker["timestamps"]
        sizes = tracker["packets"]

        duration = timestamps[-1] - timestamps[0]
        total_packets = len(sizes)
        total_bytes = sum(sizes)
        mean_pkt_size = np.mean(sizes)
        std_pkt_size = np.std(sizes)

        iats = np.diff(timestamps)
        mean_iat = np.mean(iats) if len(iats) > 0 else 0
        std_iat = np.std(iats) if len(iats) > 0 else 0

        proto, sport, dport = flow_key[4], flow_key[2], flow_key[3]
        pkt_size_ratio = (
            np.mean(sizes[:5]) / mean_pkt_size if mean_pkt_size > 0 else 1.0
        )

        features = [
            [
                duration,
                total_packets,
                total_bytes,
                mean_pkt_size,
                std_pkt_size,
                mean_iat,
                std_iat,
                proto,
                sport,
                dport,
                pkt_size_ratio,
            ]
        ]

        if self.clf:
            feature_names = [
                "duration",
                "total_packets",
                "total_bytes",
                "mean_pkt_size",
                "std_pkt_size",
                "mean_iat",
                "std_iat",
                "protocol",
                "src_port",
                "dst_port",
                "pkt_size_ratio",
            ]
            df = pd.DataFrame(features, columns=feature_names)
            pred_class = self.clf.predict(df)[0]
            tracker["class_id"] = pred_class

            self.logger.info(
                "CLASSIFIED FLOW %s -> Class %s", flow_key, CLASS_NAMES.get(pred_class)
            )

            # --- RL Routing Decision ---
            state = self.get_rl_state(pred_class)
            action_idx = self.rl_agent.get_action(state)

            # Decode Action: Action = (Path_Index * NUM_QUEUES) + Queue_Index
            path_idx = action_idx // NUM_QUEUES
            queue_idx = action_idx % NUM_QUEUES

            self.logger.info(
                "RL Decision -> Path %d, Queue %d (Epsilon: %.2f)",
                path_idx,
                queue_idx,
                self.rl_agent.epsilon,
            )

            # Proceed to map routing via QoS manager
            # This logic will calculate the physical path and insert OpenFlow Rules
            paths = self.k_shortest_paths(src_dpid, dst_dpid)
            if paths:
                safe_path_idx = min(path_idx, len(paths) - 1)
                selected_path = paths[safe_path_idx]
                queue_id = CLASS_TO_QUEUE.get(pred_class, NUM_QUEUES - 1)
                self._install_path(selected_path, flow_key, queue_id, msg)

                self.logger.info(
                    "INSTALLED ROUTE: Flow %s | Path %s | Queue %d (%s)",
                    flow_key,
                    selected_path,
                    queue_id,
                    ["High", "Medium", "BestEffort"][queue_id],
                )

                reward = self.compute_reward(pred_class, selected_path)
                self.logger.info("RL Reward: %.2f for flow %s", reward, flow_key)
            else:
                self.logger.warning(
                    "No path found between %s and %s", src_dpid, dst_dpid
                )
                reward = -10.0

            # Update the Q-Learning Agent so Epsilon decays and it "learns"
            next_state = self.get_rl_state(pred_class)
            self.rl_agent.update(state, action_idx, reward, next_state)

    def _install_path(self, path, flow_key, queue_idx, msg):
        self.logger.info(
            "Installing path %s with Queue %d for flow %s", path, queue_idx, flow_key
        )
        if len(path) < 2:
            self.logger.warning("Path too short to install: %s", path)
            return

        src_ip, dst_ip, src_port, dst_port, proto = flow_key

        for i in range(len(path) - 1):
            current_dpid = path[i]
            next_dpid = path[i + 1]

            if current_dpid not in self.datapaths:
                self.logger.warning("Datapath %s not found, skipping", current_dpid)
                continue

            edge_data = self.net.get_edge_data(current_dpid, next_dpid)
            if edge_data is None:
                self.logger.warning(
                    "No edge between %s and %s, skipping", current_dpid, next_dpid
                )
                continue

            out_port = edge_data["port"]
            datapath = self.datapaths[current_dpid]
            parser = datapath.ofproto_parser

            match = parser.OFPMatch(
                eth_type=0x0800,
                ipv4_src=src_ip,
                ipv4_dst=dst_ip,
                ip_proto=proto,
                tp_src=src_port,
                tp_dst=dst_port,
            )

            actions = [parser.OFPActionOutput(out_port)]
            if queue_idx < NUM_QUEUES:
                actions = [parser.OFPActionSetQueue(queue_idx)] + actions

            inst = [
                parser.OFPInstructionActions(
                    datapath.ofproto.OFPIT_APPLY_ACTIONS, actions
                )
            ]

            mod = parser.OFPFlowMod(
                datapath=datapath,
                priority=QOS_FLOW_PRIORITY,
                match=match,
                instructions=inst,
                idle_timeout=300,
                hard_timeout=600,
            )
            datapath.send_msg(mod)

        self._install_reverse_path(path, flow_key, queue_idx)

    def _install_reverse_path(self, path, flow_key, queue_idx):
        src_ip, dst_ip, src_port, dst_port, proto = flow_key
        reverse_path = list(reversed(path))

        for i in range(len(reverse_path) - 1):
            current_dpid = reverse_path[i]
            next_dpid = reverse_path[i + 1]

            if current_dpid not in self.datapaths:
                continue

            edge_data = self.net.get_edge_data(current_dpid, next_dpid)
            if edge_data is None:
                continue

            out_port = edge_data["port"]
            datapath = self.datapaths[current_dpid]
            parser = datapath.ofproto_parser

            match = parser.OFPMatch(
                eth_type=0x0800,
                ipv4_src=dst_ip,
                ipv4_dst=src_ip,
                ip_proto=proto,
                tp_src=dst_port,
                tp_dst=src_port,
            )

            actions = [parser.OFPActionOutput(out_port)]
            if queue_idx < NUM_QUEUES:
                actions = [parser.OFPActionSetQueue(queue_idx)] + actions

            inst = [
                parser.OFPInstructionActions(
                    datapath.ofproto.OFPIT_APPLY_ACTIONS, actions
                )
            ]

            mod = parser.OFPFlowMod(
                datapath=datapath,
                priority=QOS_FLOW_PRIORITY,
                match=match,
                instructions=inst,
                idle_timeout=300,
                hard_timeout=600,
            )
            datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match["in_port"]

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        if eth.ethertype == 0x88CC:  # LLDP
            return

        dst = eth.dst
        src = eth.src
        dpid = datapath.id

        self.mac_to_dpid[src] = dpid

        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        if ip_pkt:
            self.ip_to_dpid[ip_pkt.src] = dpid

            tcp_pkt = pkt.get_protocol(tcp.tcp)
            udp_pkt = pkt.get_protocol(udp.udp)

            src_port = 0
            dst_port = 0
            proto = ip_pkt.proto

            if tcp_pkt:
                src_port = tcp_pkt.src_port
                dst_port = tcp_pkt.dst_port
            elif udp_pkt:
                src_port = udp_pkt.src_port
                dst_port = udp_pkt.dst_port

            if src_port != 0 and dst_port != 0:
                flow_key = (ip_pkt.src, ip_pkt.dst, src_port, dst_port, proto)

                if flow_key not in self.flow_tracker:
                    self.flow_tracker[flow_key] = {
                        "packets": [],
                        "timestamps": [],
                        "class_id": None,
                    }
                    self.logger.info("NEW FLOW DETECTED: %s", str(flow_key))

                tracker = self.flow_tracker[flow_key]
                if (
                    tracker["class_id"] is None
                    and len(tracker["packets"]) < PACKETS_TO_COLLECT
                ):
                    tracker["packets"].append(len(msg.data))
                    tracker["timestamps"].append(time.time())

                    if len(tracker["packets"]) % 2 == 0:
                        self.logger.info(
                            "Collecting packet %d/%d for flow %s",
                            len(tracker["packets"]),
                            PACKETS_TO_COLLECT,
                            str(flow_key),
                        )

                    if len(tracker["packets"]) == PACKETS_TO_COLLECT:
                        dst_dpid = self.ip_to_dpid.get(ip_pkt.dst, dpid)
                        if dst_dpid == dpid and ip_pkt.src != ip_pkt.dst:
                            self.logger.warning(
                                "Unknown destination DPID for %s, using current dpid",
                                ip_pkt.dst,
                            )
                        self._extract_classify_and_route(
                            flow_key, tracker, dpid, dst_dpid, msg
                        )
                        self.classified_flows.add(flow_key)

        # Base L2 Learning Forwarding (for initial setup)
        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # --- FIX: Do NOT install flow rules immediately for L2 traffic. ---
        # If we install a flow rule on the first packet, the switch handles
        # packets 2-10 directly, and the controller NEVER sees them to classify!
        # For now, let the controller forward packets until classification is done.

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )
        datapath.send_msg(out)
