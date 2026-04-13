# src/controller.py
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER, set_ev_cls, CONFIG_DISPATCHER
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
CLASS_NAMES = {0: 'VoIP', 1: 'Video', 2: 'HTTP', 3: 'FTP', 4: 'DNS', 5: 'Background'}
PACKETS_TO_COLLECT = 10  # Number of packets before classification
K_PATHS = 3              # Number of paths to consider for RL
NUM_QUEUES = 3           # 0=High, 1=Medium, 2=Best Effort

class QLearningAgent:
    """Tabular Q-Learning Agent for SDN QoS Routing"""
    def __init__(self, num_actions=K_PATHS * NUM_QUEUES, alpha=0.1, gamma=0.9, epsilon=1.0, min_epsilon=0.1, decay=0.995):
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

    def __init__(self, *args, **kwargs):
        super(QoSController, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.datapaths = {}
        self.net = nx.DiGraph()  # Topology Graph
        
        # Flow Tracking: (src_ip, dst_ip, src_port, dst_port, proto) -> dict
        self.flow_tracker = {}
        
        # RL Agent initialization
        self.rl_agent = QLearningAgent()
        
        # Load ML Model
        model_path = os.path.join(os.path.dirname(__file__), '../data/dt_model.pkl')
        if os.path.exists(model_path):
            self.logger.info("Loading Decision Tree Model from %s", model_path)
            self.clf = joblib.load(model_path)
        else:
            self.logger.error("Model file not found! Please run train_classifier.py first.")
            self.clf = None

        self.monitor_thread = hub.spawn(self._monitor)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Install table-miss flow entry
        # We specify NO MATCH (meaning it matches everything)
        # Action is to send it to the controller (OFPP_CONTROLLER)
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.info('Register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.info('Unregister datapath: %016x', datapath.id)
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
        pass # Evaluate reward here later for RL state update

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        pass # Update link utilization here

    def k_shortest_paths(self, src, dst, k=K_PATHS):
        try:
            return list(islice(nx.shortest_simple_paths(self.net, src, dst), k))
        except nx.NetworkXNoPath:
            return []

    def get_rl_state(self, class_id):
        # Simplification for prototype:
        # State = (Class_ID, Link_Utilization_Level, Path_Delay_Level)
        # 0=Low, 1=Medium, 2=High. For now, hardcode network state levels (0)
        util_level = 0
        delay_level = 0
        return (class_id, util_level, delay_level)

    def _extract_classify_and_route(self, flow_key, tracker, src_dpid, dst_dpid, msg):
        timestamps = tracker['timestamps']
        sizes = tracker['packets']
        
        duration = timestamps[-1] - timestamps[0]
        total_packets = len(sizes)
        total_bytes = sum(sizes)
        mean_pkt_size = np.mean(sizes)
        std_pkt_size = np.std(sizes)
        
        iats = np.diff(timestamps)
        mean_iat = np.mean(iats) if len(iats) > 0 else 0
        std_iat = np.std(iats) if len(iats) > 0 else 0
        
        proto, sport, dport = flow_key[4], flow_key[2], flow_key[3]
        pkt_size_ratio = np.mean(sizes[:5]) / mean_pkt_size if mean_pkt_size > 0 else 1.0

        features = [[duration, total_packets, total_bytes, mean_pkt_size, std_pkt_size, mean_iat, std_iat, proto, sport, dport, pkt_size_ratio]]
        
        if self.clf:
            feature_names = ['duration', 'total_packets', 'total_bytes', 'mean_pkt_size', 'std_pkt_size', 'mean_iat', 'std_iat', 'protocol', 'src_port', 'dst_port', 'pkt_size_ratio']
            df = pd.DataFrame(features, columns=feature_names)
            pred_class = self.clf.predict(df)[0]
            tracker['class_id'] = pred_class
            
            self.logger.info("CLASSIFIED FLOW %s -> Class %s", flow_key, CLASS_NAMES.get(pred_class))

            # --- RL Routing Decision ---
            state = self.get_rl_state(pred_class)
            action_idx = self.rl_agent.get_action(state)
            
            # Decode Action: Action = (Path_Index * NUM_QUEUES) + Queue_Index
            path_idx = action_idx // NUM_QUEUES
            queue_idx = action_idx % NUM_QUEUES
            
            self.logger.info("RL Decision -> Path %d, Queue %d (Epsilon: %.2f)", path_idx, queue_idx, self.rl_agent.epsilon)
            
            # Proceed to map routing via QoS manager
            # This logic will calculate the physical path and insert OpenFlow Rules
            paths = self.k_shortest_paths(src_dpid, dst_dpid)
            if paths and len(paths) > path_idx:
                selected_path = paths[path_idx]
                self._install_path(selected_path, flow_key, queue_idx, msg)

    def _install_path(self, path, flow_key, queue_idx, msg):
        self.logger.info("Installing path %s with Queue %d for flow %s", path, queue_idx, flow_key)
        # Note: Actual OpenFlow multi-hop installation requires iterating over the path
        # and sending FlowMods to each datapath along the route.

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        if eth.ethertype == 34525: # LLDP
            return

        dst = eth.dst
        src = eth.src
        dpid = datapath.id

        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        if ip_pkt:
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
                    self.flow_tracker[flow_key] = {'packets': [], 'timestamps': [], 'class_id': None}
                
                tracker = self.flow_tracker[flow_key]
                if tracker['class_id'] is None and len(tracker['packets']) < PACKETS_TO_COLLECT:
                    tracker['packets'].append(len(msg.data))
                    tracker['timestamps'].append(time.time())
                    
                    if len(tracker['packets']) == PACKETS_TO_COLLECT:
                        # Dummy dst_dpid for testing - in reality mapped from MAC
                        self._extract_classify_and_route(flow_key, tracker, dpid, dpid, msg)

        # Base L2 Learning Forwarding (for initial setup)
        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            # Verify if we have a valid buffer_id
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
