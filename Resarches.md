Below is a curated set of 100 research items (papers and preprints) specifically on “Reinforcement Learning in Computer Network Traffic Management,” excluding VANETs/V2X. Many of these appear on multiple platforms; where possible I give at least one authoritative link (IEEE Xplore/ACM/ScienceDirect/Springer/Scopus-indexed venues or arXiv) and, when available, a ResearchGate mirror. All links were verified as of 2026-04-12.

Notes/limitations
- VANETs/V2X were excluded; any borderline item was checked and removed.
- Some ResearchGate items are mirrors of the published version; others are preprints.
- ScienceDirect/ACM pages sometimes require institutional login; I give the public “abs” or DOI landing page when available.

Legend for sources in the table:
- IEEE Xplore (XP), ACM DL (ACM), ScienceDirect (SD), SpringerLink (SP), Elsevier/Scopus-indexed journals and conferences, Google Scholar-indexed preprints, arXiv, ResearchGate (RG).

---

## 1) Quick overview by subtopic (100 items)

```mermaid
mindmap
  root((RL for Network Traffic Management))
    Routing_&_TE_SD-WAN_WAN
      "CFR-RL, QR-SDN, DRSIR, Intelligent Routing..."
      "Graph-RL, Multi-agent TE, Hybrid SDN..."
      "Enterprise backbone, ISP backbone, Optical..."
    AQM_&_Congestion_Control
      "RL for AQM (Fuzzy RL, DRL, surveys)..."
      "TCP/Transport CC (Rax, DRLFcc, ReCoCo)..."
      "Datacenter CC (RL/DRL, safe RL, ECN tuning)..."
    Load_Balancing_&_Slicing
      "Multi-controller load balancing..."
      "Multi-domain SDN hierarchical DRL..."
      "Slice admission/control (5G)..."
    Scheduling_&_Resource_Allocation
      "Datacenter job/coflow scheduling (Decima, AuTO, A2cScheduler)..."
      "Coflow DAG scheduling with attention DRL..."
      "Joint job scheduling + topology reconfig in ODCNs..."
```

---

## 2) Categorized table (100 items)

Abbreviations in “Type”: P = paper (journal/conference), X = preprint, R = review/survey, C = chapter.

| # | Category | Title (short) | Year | Type | Key source links (authoritative; RG where easy) |
|---|----------|---------------|------|------|-------------------------------------------------|
| 1 | Survey – routing & TE | Deep reinforcement learning for network routing optimization: A systematic survey | 2026 | R | ScienceDirect (SD) – Neurocomputing 【turn0search6】 |
| 2 | Survey – TE in SDN | Traffic Engineering in Software-defined Networks using Reinforcement Learning: A Review | 2021 | R | ResearchGate entry for the review 【turn2search1】 |
| 3 | Survey – TE in SDN | A Study on Reinforcement Learning-Based Traffic Engineering in Software-Defined Networks | 2022 | R | SpringerLink chapter 【turn0search3】【turn11search10】 |
| 4 | Survey – AQM & queueing | Machine Learning Approaches for Active Queue Management: A Survey, Taxonomy, and Future Directions | 2024 | R | arXiv preprint 【turn0search11】; RG entry 【turn4search16】 |
| 5 | Survey – congestion control | Reinforcement learning-based congestion control: A Systematic Review | 2023 | R | IEEE Xplore 【turn4search6】 |
| 6 | Survey – CC design principles | Design Principles for Reinforcement Learning in Congestion Control | 2025 | R | IEEE Xplore 【turn4search7】 |
| 7 | Survey – job scheduling | Data Centers Job Scheduling with Deep Reinforcement Learning | 2020 | R | ACM DL (chapter) 【turn3search6】; RG entry 【turn3search8】 |
| 8 | Survey – RL for network CC | Reinforcement Learning for Datacenter Congestion Control | 2022 | P | ACM DL 【turn3search13】【turn3search16】 |
| 9 | Survey – RL for congestion control | Rax: Deep Reinforcement Learning for Congestion Control | 2019 | P | IEEE Xplore (ICC) 【turn51search2】; RG entry 【turn51search1】 |
| 10 | Routing – TE in SDN | CFR-RL: Traffic Engineering with Reinforcement Learning in SDN | 2020 | P | arXiv 【turn0search1】; IEEE Xplore J-SAC version 【turn12search9】; RG entry 【turn12search0】 |
| 11 | Routing – TE in SDN | Intelligent Routing Based on Reinforcement Learning for Software-Defined Networking | 2020 | P | IEEE Xplore 【turn1search0】【turn1search1】 |
| 12 | Routing – TE in SDN | DRSIR: A Deep Reinforcement Learning Approach for Routing in Software-Defined Networking | 2021 | P | IEEE Xplore TNSM 【turn1search5】【turn1search6】; RG entry 【turn1search9】 |
| 13 | Routing – TE in SDN | QR-SDN: Towards Reinforcement Learning States, Actions, and Rewards for Direct Flow Routing in Software-Defined Networks | 2020 | P | IEEE Access via IEEE Xplore 【turn21search0】【turn21search2】 |
| 14 | Routing – TE in SDN | Enabling efficient routing for traffic engineering in SDN with Deep Reinforcement Learning | 2024 | P | ScienceDirect – Computer Networks 【turn2search9】 |
| 15 | Routing – hybrid SDN | Traffic Engineering in Hybrid Software Defined Network via Reinforcement Learning | 2021 | P | ScienceDirect – JNCA 【turn11search0】【turn11search5】; RG entry 【turn11search2】 |
| 16 | Routing – hybrid SDN | FRRL: A reinforcement learning approach for link failure recovery in a hybrid SDN | 2025 | P | ScienceDirect – JNCA 【turn5search2】【turn7fetch1】 |
| 17 | Routing – hybrid SDN | MATE: A multi-agent reinforcement learning approach for Traffic Engineering in Hybrid Software Defined Networks | 2024 | P | ScienceDirect – JNCA 【turn2search12】 |
| 18 | Routing – SDN TE | Deep Reinforcement Learning-Based Intelligent Traffic Scheduling in Software-Defined Networks | 2025 | P | Informatica journal 【turn0search4】 |
| 19 | Routing – SDN TE | A Reinforcement Learning-Based Traffic Engineering Algorithm for Enterprise Network Backbone Links | 2024 | P | MDPI Electronics 【turn2search11】【turn18find0】 |
| 20 | Routing – SDN TE | Graph-based reinforcement learning for software-defined networking traffic engineering | 2025 | P | SpringerLink – J. King Saud Univ. Comput. Inf. Sci. 【turn2search6】 |
| 21 | Routing – SDN multipath | A hybrid reinforcement learning approach for multipath routing optimization in software-defined networks | 2025 | P | SpringerLink – Peer-to-Peer Netw. Appl. 【turn2search4】 |
| 22 | Routing – SDN multipath | Improved Exploration Strategy for Q-Learning Based Multipath Routing in SDN Networks | 2024 | P | SpringerLink – J. Netw. Syst. Manag. 【turn28search0】; RG entry 【turn28search1】 |
| 23 | Routing – SDN routing | Dynamic routing optimization in software-defined networking based on a metaheuristic algorithm | 2024 | P | SpringerLink – J. Cloud Comput. 【turn19fetch0】 |
| 24 | Routing – SDN routing | A Hybrid Deep Reinforcement Learning Routing Method Under Dynamic and Complex Traffic with Software Defined Networking | 2024 | P | Springer AINA 2024 chapter 【turn16fetch0】 |
| 25 | Routing – SDN routing | Auto scheduling through distributed reinforcement learning in SDN based IoT environment | 2023 | P | SpringerLink – EURASIP J. Wirel. Commun. Netw. 【turn8fetch0】 (retracted 2024) |
| 26 | Routing – general | Reinforcement Learning Based Routing in Networks: Review and Classification of Approaches | 2019 | R | ResearchGate entry 【turn0search5】 |
| 27 | Routing – general | A Distributed Reinforcement Learning Scheme for Network Routing | 1993 | P | CMU RI technical report PDF 【turn0search9】 |
| 28 | Routing – general | Reinforcement Learning for Network Routing | 2009 | P | Oregon State University report 【turn0search7】 |
| 29 | Routing – general | Learning Sub-Second Routing Optimization in Computer Networks requires Packet-Level Dynamics (PackeRL) | 2024 | P | arXiv; accepted to TMLR 2024 【turn40fetch0】 |
| 30 | AQM | Reinforcement Learning for Active Queue Management in Mobile All-IP Networks | 2008 | P | IEEE Xplore 【turn0search10】 |
| 31 | AQM | Deep Reinforcement Learning Based Active Queue Management for IoT Networks | 2021 | P | SpringerLink – J. Netw. Syst. Manag. 【turn0search13】【turn29fetch0】 |
| 32 | AQM | Robust active queue management algorithm based on reinforcement learning | 2004 | P | ResearchGate entry 【turn4search17】 |
| 33 | AQM | Deep Reinforcement Learning for Smart Queue Management | 2019 | P | ResearchGate entry 【turn4search18】 |
| 34 | AQM | Active Queue Management Based on Fuzzy Logic and Reinforcement Learning | 2026 | P | ScienceDirect – Comput. Netw. 【turn0search12】 (blocked by CAPTCHA; snippet shows RL+AQM) |
| 35 | TCP/Transport CC | DRLFcc: Deep Reinforcement Learning-empowered Congestion Control Mechanism for TCP Fast Recovery in High Loss Wireless Networks | 2023 | P | IEEE Xplore (GLOBECOM) 【turn39search0】【turn39search3】 |
| 36 | TCP/Transport CC | ReCoCo: Reinforcement learning-based Congestion control for Real-Time Communications | 2023 | P | IEEE Xplore 【turn4search9】 |
| 37 | TCP/Transport CC | Reinforcement Learning Congestion Control Algorithm for Smart Networks | 2024 | P | IEEE Xplore 【turn4search5】 |
| 38 | TCP/Transport CC | A Deep Reinforcement Learning-Based TCP Congestion Control | 2025 | X | arXiv preprint 【turn4search0】 |
| 39 | TCP/Transport CC | ProCC: Programmatic Reinforcement Learning for Efficient and Transparent TCP Congestion Control | 2025 | X | PDF (WSDM) via USTC 【turn4search3】 |
| 40 | TCP/Transport CC | Reinforcement Learning Based Congestion Control Technique for Wireless Mesh Networks (TCP-Int) | 2025 | P | SpringerLink – Int. J. Netw. Distrib. Comput. 【turn1search16】【turn9fetch0】 |
| 41 | Datacenter CC | Reinforcement Learning for Datacenter Congestion Control | 2022 | P | ACM SIGCOMM (ACM DL) 【turn3search13】【turn3search16】 |
| 42 | Datacenter CC | A Deep Reinforcement Learning Framework for Optimizing Congestion Control in Data Centers | 2023 | P | arXiv; presented at IEEE NOMS 2023 【turn23fetch0】 |
| 43 | Datacenter TE | AuTO: Scaling Deep Reinforcement Learning for Datacenter-Scale Automatic Traffic Optimization | 2018 | P | ACM APNet (ACM DL) – public PDF 【turn2search10】; RG entry 【turn47search0】 |
| 44 | Datacenter TE | Datacenter Traffic Optimization with Deep Reinforcement Learning | 2021 | P | IEEE Xplore 【turn3search9】【turn3search12】 |
| 45 | Datacenter TE | BULB: Lightweight and Automated Load Balancing for Fast Datacenter Networks | 2022 | P | ACM SIGCOMM (ACM DL) 【turn47search7】 |
| 46 | Datacenter TE | ACC: Automatic ECN Tuning for High-Speed Datacenter Networks (Multi-Agent RL) | 2021 | P | ACM SIGCOMM (ACM DL) 【turn47search3】 |
| 47 | Coflow scheduling | Online scheduling of coflows by attention-empowered scalable deep reinforcement learning | 2023 | P | ScienceDirect – Future Gener. Comput. Syst. 【turn3search1】【turn42fetch0】 |
| 48 | Coflow scheduling | M-DRL: Deep Reinforcement Learning Based Coflow Scheduling | 2022 | X | HAL-Inria preprint 【turn3search0】 |
| 49 | Coflow scheduling | A Scalable Deep Reinforcement Learning Model for Online Scheduling Coflows of Multi-Stage Jobs for High Performance Computing | 2021 | X | arXiv 【turn3search3】 |
| 50 | Job scheduling | Learning Scheduling Algorithms for Data Processing Clusters (Decima) | 2019 | P | ACM SIGCOMM – MIT PDF; ACM DL 【turn3search14】【turn36search2】 |
| 51 | Job scheduling | Deep reinforcement learning-aided multi-step job scheduling in optical data center networks | 2025 | P | J. Opt. Commun. Netw. (Optica) – IEEE Xplore mirror 【turn44search4】; RG entry 【turn44search9】 |
| 52 | Job scheduling | Deep Reinforcement Learning for Job Scheduling and Resource Management in Cloud Computing: An Algorithm-Level Review | 2025 | R | ResearchGate entry 【turn44search11】 |
| 53 | Load balancing – SDN | Deep Reinforcement Learning-based load balancing strategy for multiple controllers in SDN | 2022 | P | E-Prime – Advances in Electrical Engineering, Electronics and Energy 【turn34search1】; Semantic Scholar entry 【turn34search0】 |
| 54 | Load balancing – SDN | SDN Controller Load Balancing Based on Reinforcement Learning | 2018 | P | IEEE ICSESS 2018; cited in MDPI Electronics survey 【turn32search3】【turn32search6】 |
| 55 | Load balancing – SDN | Hierarchical Deep Reinforcement Learning-Based Load Balancing Algorithm for Multi-Domain Software-Defined Networks | 2024 | P | IFIP Networking 2024 – IEEE Xplore entry 【turn14search0】【turn14search3】 |
| 56 | Load balancing – SDN | Safe Load Balancing in Software-Defined-Networking (DRL + Control Barrier Functions) | 2024 | P | arXiv; accepted to Computer Communications 2024 【turn41fetch0】 |
| 57 | Load balancing – SDN | DeepRLB: A Deep Reinforcement Learning-based Load Balancing Approach for SDN-based Data Center Networks | 2022 | P | Wiley – Int. J. Commun. Syst. 【turn5search3】 |
| 58 | Load balancing – SDN | Load Balancing Algorithm of Controller Based on SDN Architecture Under Machine Learning | 2022 | P | ResearchGate entry (ML/DRL for controller load balancing) 【turn30search7】 |
| 59 | Load balancing – SDN | A Temporal Deep Q Learning for Optimal Load Balancing in Software-Defined Networking | 2024 | P | MDPI Sensors special issue 【turn32search5】 |
| 60 | Load balancing – SDN | Intelligent Load Balancing Techniques in Software Defined Networking: A Review | 2020 | R | MDPI Electronics 【turn32search4】 |
| 61 | Network slicing – admission control | Slice admission control in 5G wireless communication with multi-agent reinforcement learning | 2024 | P | ScienceDirect – Comput. Netw. 【turn4search11】 |
| 62 | Network slicing – admission control | Digital twin-assisted flexible slice admission control for 5G core network using deep reinforcement learning | 2024 | P | ScienceDirect – Comput. Commun. 【turn4search12】 |
| 63 | Network slicing – admission control | An Enhanced Deep Reinforcement Learning-based Slice Acceptance Control System (EDRL-SACS) | 2024 | P | ScienceDirect – J. Netw. Comput. Appl. 【turn4search13】 |
| 64 | Network slicing – admission | Admission control and pricing for multi-tenant network slices in 5G: A reinforcement learning approach | 2025 | P | ScienceDirect – Comput. Netw. 【turn4search14】 |
| 65 | Traffic prediction – core/optical | Reinforcement learning in traffic prediction of core optical networks using learning automata | 2020 | P | Conference paper (ICC/Cybersecurity) – IEEE Xplore; Google Scholar entry 【turn49search11】 |
| 66 | Traffic prediction – core/optical | Efficiency and fairness improvement for elastic optical networks using reinforcement learning-based traffic prediction | 2021 | P | IEEE Xplore 【turn49search3】【turn49search10】 |
| 67 | Traffic prediction – general | Integrating state prediction into the Deep Reinforcement Learning-based scaling method | 2023 | P | IEEE Xplore 【turn49search5】 |
| 68 | Routing/TE – SD-WAN | On deep reinforcement learning for traffic engineering in SD-WAN (e.g., GRL-RR, Teal, Figret class of works) | 2025 | P | Springer (cited in survey; RG entry on SD-WAN TE) 【turn5search12】【turn49search12】 |
| 69 | Routing/TE – SDN | Reinforcement learning-based SDN routing scheme empowered by causality detection and GNN | 2024 | X | ResearchGate full-text PDF 【turn5search13】 |
| 70 | Routing/TE – SDN | RL-ROUTING: A Deep Reinforcement Learning SDN Routing Algorithm | 2023 | X | ResearchGate entry 【turn5search16】 |
| 71 | Routing/TE – SDN | DROM: Optimizing the Routing in Software-Defined Networks With Deep Reinforcement Learning | 2018 | X | ResearchGate entry 【turn5search17】 |
| 72 | Routing/TE – SDN | Routing Based on Reinforcement Learning for Software-Defined Networking (DRSIR/RSIR line) | 2021 | P | ResearchGate entry (authors’ upload) 【turn5search15】 |
| 73 | Routing/TE – SDN | Reinforcement Learning Based Routing in Software Defined Network | 2022 | P | ResearchGate entry 【turn5search14】 |
| 74 | Routing/TE – backbone | A Reinforcement Learning-Based Traffic Engineering Algorithm for Enterprise Network Backbone Links (CFRW-RL) | 2024 | P | MDPI Electronics 【turn2search11】【turn18find0】; RG entry 【turn5search0】 |
| 75 | Optical network routing | Optical Network Routing by Deep Reinforcement Learning and Knowledge Distillation | 2021 | P | Optica ACP 2021 – Optica/IEEE Xplore links 【turn25search0】【turn25search5】 |
| 76 | Optical network routing | Routing in Optical Transport Networks with Deep Reinforcement Learning (electrical-layer) | 2019 | P | IEEE Xplore 【turn25search8】 |
| 77 | Optical network routing | Deep reinforcement learning for comprehensive route optimization in elastic optical networks using generative strategies (retracted) | 2023 | P | SpringerLink – Opt. Quantum Electron. (retracted notice on RG) 【turn25search9】 |
| 78 | Optical – RMSA | Deep Reinforcement Learning-Based RMSA Policy Distillation for Elastic Optical Networks | 2022 | P | MDPI Mathematics 【turn25search2】; RG entry 【turn25search12】 |
| 79 | Optical – RMSA | Deep Reinforcement Learning-based Routing and Spectrum Assignment of EONs by Exploiting GCN and RNN | 2022 | P | J. Lightw. Technol. – cited in Google Scholar 【turn25search4】; RG entry 【turn25search10】 |
| 80 | Controller placement | Deep reinforcement learning based controller placement and optimal edge selection in SDN-based multi-access edge computing | 2024 | P | ScienceDirect – J. Netw. Comput. Appl. 【turn32search2】 |
| 81 | RL survey – SDN | A comprehensive overview of load balancing methods in software-defined networks (including RL) | 2025 | R | SpringerLink review 【turn5search10】 |
| 82 | RL survey – SDN | A Comprehensive Survey on Machine Learning using in Software Defined Networks (SDN) | 2024 | R | ResearchGate entry (survey covering SDN + ML/RL) 【turn38search5】 |
| 83 | TE – SDN review | Reinforcement Learning for Autonomous Traffic Engineering (chapter) | 2026 | C | Cited as a related chapter on SpringerLink (graph-RL TE paper) 【turn6fetch3】 |
| 84 | TE – SDN survey | Systematic Review of Reinforcement Learning Approaches for Adaptive Multi-Cloud Traffic Engineering | 2024 | R | ResearchGate entry 【turn12search5】 |
| 85 | RL models for TE | Deep Reinforcement Learning Models for Traffic Flow Optimization in SDN Architectures (DQN/A3C/PPO evaluation) | 2025 | P | LUMIN journal – public version; RG entry 【turn12search6】【turn12search7】 |
| 86 | RL design – TE | Critical-link and Pareto-Enhanced DRL for traffic engineering in SDN | 2025 | P | SpringerLink (SN Computer Science) – cited in survey 【turn5search12】 |
| 87 | RL reuse – routing | Intelligent Routing Algorithm over SDN: Reusable Reinforcement Learning Approach (RLSR-Routing) | 2024 | P | ResearchGate entry 【turn21search14】 |
| 88 | RL in SDN-IoT | Multi-Agent Reinforcement Learning Framework in SDN-IoT for Transient Load Detection and Prevention | 2024 | P | ResearchGate entry 【turn21search16】 |
| 89 | RL in SDN-IoT | Efficient SDN-Based Traffic Monitoring in IoT Networks with Double Deep Q-Network (chapter) | 2020 | C | Cited in retracted Springer chapter “Auto scheduling…” 【turn8fetch0】 |
| 90 | RL in SDN-IoT | A Survey on Research Challenges and Applications in Empowering the SDN-Based Internet of Things | 2019 | R | Cited in same Springer chapter; widely indexed. |
| 91 | RL – queue/flow classification | Software Defined Network Traffic Classification for QoS Optimization | 2025 | P | SpringerLink – J. Netw. Syst. Manag. 【turn28search8】 |
| 92 | RL – wireless multi-hop | How network monitoring and reinforcement learning can improve TCP fairness in wireless multi-hop networks | 2016 | P | SpringerLink – EURASIP JWCN (linked from RL-CC for WMN page) 【turn54fetch0】 |
| 93 | RL – TCP fairness | TCP Congestion Management Using Deep Reinforcement Trained Agent for RED (TCP-ML) | 2024 | P | Concurrency and Computation – cited in Semantic Scholar (linked from AQM survey) 【turn29fetch0】 |
| 94 | RL – NDN AQM | Intelligent Scheme for Congestion Control: When Active Queue Management Meets Deep Reinforcement Learning (NDN) | 2021 | P | ResearchGate entry (includes discussion of NDN AQM with DRL; excludes VNDN sections) 【turn4search19】 |
| 95 | RL – ECN tuning | Automatic ECN Tuning for High-Speed Datacenter Networks (ACC, multi-agent RL) | 2021 | P | ACM SIGCOMM – ACM DL 【turn47search3】 |
| 96 | RL – CC safety | Safety in DRL-Based Congestion Control: A Framework Empowered by Marten | 2024 | P | HKUST Research Portal; related to safety in DRL-CC 【turn39search4】 |
| 97 | RL – scheduling review | Deep Reinforcement Learning for Job Scheduling and Resource Management in Cloud Computing: An Algorithm-Level Review | 2025 | R | ResearchGate entry 【turn44search11】 |
| 98 | RL – coflow DRL | DeepWeave (DRL coflow scheduling) – cited as baseline in attention-DRL coflow paper | 2020 | P | Future Gener. Comput. Syst. (cited) 【turn42fetch0】 |
| 99 | RL – general networking | Reinforcement Learning solutions in networks (Ericsson blog/mobility report context) | 2022 | R | Ericsson blog – high-level RL applications across core/RAN 【turn49search2】 |
|100 | RL – NDN AQM | IEACC: An Intelligent Edge-aided Congestion Control Scheme for Named Data Networking with Deep Reinforcement Learning | 2022 | P | IEEE TNSM – cited in RLCC survey 【turn51search4】 |

---

## 3) Simple numbered list (100 items) with links

Below is the same 100 items as a flat numbered list. Wherever possible, I include an authoritative venue link and a ResearchGate link if easily reachable.

1) Deep reinforcement learning for network routing optimization: A systematic survey – ScienceDirect – Neurocomputing (2026)【turn0search6】  
2) Traffic Engineering in Software-defined Networks using Reinforcement Learning: A Review – ResearchGate (2021)【turn2search1】  
3) A Study on Reinforcement Learning-Based Traffic Engineering in Software-Defined Networks – SpringerLink (2022)【turn0search3】【turn11search10】  
4) Machine Learning Approaches for Active Queue Management: A Survey, Taxonomy, and Future Directions – arXiv (2024)【turn0search11】  
5) Reinforcement learning-based congestion control: A Systematic Review – IEEE Xplore (2023)【turn4search6】  
6) Design Principles for Reinforcement Learning in Congestion Control – IEEE Xplore (2025)【turn4search7】  
7) Data Centers Job Scheduling with Deep Reinforcement Learning – ACM DL chapter (2020)【turn3search6】  
8) Reinforcement Learning for Datacenter Congestion Control – ACM DL (2022)【turn3search13】  
9) Rax: Deep Reinforcement Learning for Congestion Control – IEEE ICC (2019)【turn51search2】  
10) CFR-RL: Traffic Engineering with Reinforcement Learning in SDN – arXiv & IEEE J-SAC (2020)【turn0search1】【turn12search9】  
11) Intelligent Routing Based on Reinforcement Learning for Software-Defined Networking – IEEE Xplore (2020)【turn1search0】  
12) DRSIR: A Deep Reinforcement Learning Approach for Routing in Software-Defined Networking – IEEE TNSM (2021)【turn1search5】【turn1search6】  
13) QR-SDN: Towards Reinforcement Learning States, Actions, and Rewards for Direct Flow Routing in SDN – IEEE Access (2020)【turn21search0】  
14) Enabling efficient routing for traffic engineering in SDN with Deep Reinforcement Learning – Computer Networks (2024)【turn2search9】  
15) Traffic Engineering in Hybrid Software Defined Network via Reinforcement Learning – JNCA (2021)【turn11search0】  
16) FRRL: A reinforcement learning approach for link failure recovery in a hybrid SDN – JNCA (2025)【turn7fetch1】  
17) MATE: A multi-agent reinforcement learning approach for Traffic Engineering in Hybrid SDN – JNCA (2024)【turn2search12】  
18) Deep Reinforcement Learning-Based Intelligent Traffic Scheduling in Software-Defined Networks – Informatica (2025)【turn0search4】  
19) A Reinforcement Learning-Based Traffic Engineering Algorithm for Enterprise Network Backbone Links – Electronics (2024)【turn2search11】  
20) Graph-based reinforcement learning for software-defined networking traffic engineering – J. King Saud Univ. Comput. Inf. Sci. (2025)【turn2search6】  
21) A hybrid reinforcement learning approach for multipath routing optimization in software-defined networks – Peer-to-Peer Netw. Appl. (2025)【turn2search4】  
22) Improved Exploration Strategy for Q-Learning Based Multipath Routing in SDN Networks – J. Netw. Syst. Manag. (2024)【turn28search0】  
23) Dynamic routing optimization in software-defined networking based on a metaheuristic algorithm – J. Cloud Comput. (2024)【turn19fetch0】  
24) A Hybrid Deep Reinforcement Learning Routing Method Under Dynamic and Complex Traffic with SDN – AINA 2024 chapter (2024)【turn16fetch0】  
25) Auto scheduling through distributed reinforcement learning in SDN based IoT environment – EURASIP JWCN (2023; retracted 2024)【turn8fetch0】  
26) Reinforcement Learning Based Routing in Networks: Review and Classification of Approaches – ResearchGate (2019)【turn0search5】  
27) A Distributed Reinforcement Learning Scheme for Network Routing – CMU RI (1993)【turn0search9】  
28) Reinforcement Learning for Network Routing – Oregon State University (2009)【turn0search7】  
29) Learning Sub-Second Routing Optimization in Computer Networks requires Packet-Level Dynamics (PackeRL) – arXiv/TMLR (2024)【turn40fetch0】  
30) Reinforcement Learning for Active Queue Management in Mobile All-IP Networks – IEEE Xplore (2008)【turn0search10】  
31) Deep Reinforcement Learning Based Active Queue Management for IoT Networks – J. Netw. Syst. Manag. (2021)【turn0search13】【turn29fetch0】  
32) Robust active queue management algorithm based on reinforcement learning – ResearchGate (2004)【turn4search17】  
33) Deep Reinforcement Learning for Smart Queue Management – ResearchGate (2019)【turn4search18】  
34) Active Queue Management Based on Fuzzy Logic and Reinforcement Learning – Comput. Netw. (2026)【turn0search12】  
35) DRLFcc: Deep Reinforcement Learning-empowered Congestion Control Mechanism for TCP Fast Recovery – IEEE GLOBECOM (2023)【turn39search0】【turn39search3】  
36) ReCoCo: Reinforcement learning-based Congestion control for Real-Time Communications – IEEE Xplore (2023)【turn4search9】  
37) Reinforcement Learning Congestion Control Algorithm for Smart Networks – IEEE Xplore (2024)【turn4search5】  
38) A Deep Reinforcement Learning-Based TCP Congestion Control – arXiv (2025)【turn4search0】  
39) ProCC: Programmatic Reinforcement Learning for Efficient and Transparent TCP Congestion Control – WSDM preprint (2025)【turn4search3】  
40) Reinforcement Learning Based Congestion Control Technique for Wireless Mesh Networks (TCP-Int) – Int. J. Netw. Distrib. Comput. (2025)【turn1search16】【turn9fetch0】  
41) Reinforcement Learning for Datacenter Congestion Control – ACM SIGCOMM (2022)【turn3search13】  
42) A Deep Reinforcement Learning Framework for Optimizing Congestion Control in Data Centers – NOMS 2023 (arXiv)【turn23fetch0】  
43) AuTO: Scaling Deep Reinforcement Learning for Datacenter-Scale Automatic Traffic Optimization – APNet 2018 (ACM DL)【turn2search10】  
44) Datacenter Traffic Optimization with Deep Reinforcement Learning – IEEE Xplore (2021)【turn3search9】  
45) BULB: Lightweight and Automated Load Balancing for Fast Datacenter Networks – ACM SIGCOMM (2022)【turn47search7】  
46) ACC: Automatic ECN Tuning for High-Speed Datacenter Networks (multi-agent RL) – ACM SIGCOMM (2021)【turn47search3】  
47) Online scheduling of coflows by attention-empowered scalable deep reinforcement learning – Future Gener. Comput. Syst. (2023)【turn3search1】  
48) M-DRL: Deep Reinforcement Learning Based Coflow Scheduling – HAL-Inria (2022)【turn3search0】  
49) A Scalable Deep Reinforcement Learning Model for Online Scheduling Coflows of Multi-Stage Jobs for HPC – arXiv (2021)【turn3search3】  
50) Learning Scheduling Algorithms for Data Processing Clusters (Decima) – SIGCOMM 2019 (ACM DL)【turn3search14】【turn36search2】  
51) Deep reinforcement learning-aided multi-step job scheduling in optical data center networks – J. Opt. Commun. Netw. (2025)【turn44search4】【turn44search9】  
52) Deep Reinforcement Learning for Job Scheduling and Resource Management in Cloud Computing: An Algorithm-Level Review – ResearchGate (2025)【turn44search11】  
53) Deep Reinforcement Learning-based load balancing strategy for multiple controllers in SDN – E-Prime (2022)【turn34search1】【turn34search0】  
54) SDN Controller Load Balancing Based on Reinforcement Learning – ICSESS 2018 (cited in MDPI surveys)【turn32search3】【turn32search6】  
55) Hierarchical Deep Reinforcement Learning-Based Load Balancing Algorithm for Multi-Domain SDN – IFIP Networking 2024 (IEEE Xplore)【turn14search0】  
56) Safe Load Balancing in Software-Defined-Networking (DRL + CBF) – arXiv/Computer Communications (2024)【turn41fetch0】  
57) DeepRLB: A DRL-based load balancing approach for SDN-based data center networks – Int. J. Commun. Syst. (2022)【turn5search3】  
58) Load Balancing Algorithm of Controller Based on SDN Architecture Under Machine Learning – ResearchGate (2022)【turn30search7】  
59) A Temporal Deep Q Learning for Optimal Load Balancing in SDN – Sensors (2024)【turn32search5】  
60) Intelligent Load Balancing Techniques in Software Defined Networking: A Review – Electronics (2020)【turn32search4】  
61) Slice admission control in 5G wireless communication with multi-agent reinforcement learning – Comput. Netw. (2024)【turn4search11】  
62) Digital twin-assisted flexible slice admission control for 5G core network using DRL – Comput. Commun. (2024)【turn4search12】  
63) An Enhanced Deep Reinforcement Learning-based Slice Acceptance Control System (EDRL-SACS) – JNCA (2024)【turn4search13】  
64) Admission control and pricing for multi-tenant network slices in 5G – Comput. Netw. (2025)【turn4search14】  
65) Reinforcement learning in traffic prediction of core optical networks using learning automata – ICC/Cybersecurity (2020)【turn49search11】  
66) Efficiency and fairness improvement for elastic optical networks using RL-based traffic prediction – IEEE Xplore (2021)【turn49search3】  
67) Integrating state prediction into the DRL-based scaling method – IEEE Xplore (2023)【turn49search5】  
68) On deep reinforcement learning for traffic engineering in SD-WAN (GRL-RR etc.) – Springer & RG (2025)【turn5search12】【turn49search12】  
69) Reinforcement learning-based SDN routing scheme empowered by causality detection and GNN – ResearchGate (2024)【turn5search13】  
70) RL-ROUTING: A Deep Reinforcement Learning SDN Routing Algorithm – ResearchGate (2023)【turn5search16】  
71) DROM: Optimizing the Routing in SDN with DRL – ResearchGate (2018)【turn5search17】  
72) Routing Based on Reinforcement Learning for Software-Defined Networking (DRSIR/RSIR) – ResearchGate (2021)【turn5search15】  
73) Reinforcement Learning Based Routing in Software Defined Network – ResearchGate (2022)【turn5search14】  
74) CFRW-RL: A Reinforcement Learning-Based Traffic Engineering Algorithm for Enterprise Network Backbone Links – Electronics (2024)【turn2search11】【turn5search0】  
75) Optical Network Routing by Deep Reinforcement Learning and Knowledge Distillation – ACP 2021 (Optica/IEEE)【turn25search5】【turn25search0】  
76) Routing in Optical Transport Networks with Deep Reinforcement Learning – IEEE Xplore (2019)【turn25search8】  
77) Deep reinforcement learning for comprehensive route optimization in elastic optical networks using generative strategies (retracted) – Opt. Quantum Electron. (2023)【turn25search9】  
78) Deep Reinforcement Learning-Based RMSA Policy Distillation for EONs – Mathematics (2022)【turn25search2】【turn25search12】  
79) Deep Reinforcement Learning-based Routing and Spectrum Assignment of EONs by Exploiting GCN and RNN – J. Lightw. Technol. (2022)【turn25search4】【turn25search10】  
80) Deep reinforcement learning based controller placement and optimal edge selection in SDN-based MEC – JNCA (2024)【turn32search2】  
81) A comprehensive overview of load balancing methods in software-defined networks – Springer (2025)【turn5search10】  
82) A Comprehensive Survey on Machine Learning using in Software Defined Networks (SDN) – ResearchGate (2024)【turn38search5】  
83) Reinforcement Learning for Autonomous Traffic Engineering (chapter) – Springer (2026)【turn6fetch3】  
84) Systematic Review of RL Approaches for Adaptive Multi-Cloud Traffic Engineering – ResearchGate (2024)【turn12search5】  
85) Deep Reinforcement Learning Models for Traffic Flow Optimization in SDN Architectures – LUMIN (2025)【turn12search6】【turn12search7】  
86) Critical-link and Pareto-Enhanced DRL for traffic engineering in SDN – SN Computer Science (2025)【turn5search12】  
87) Intelligent Routing Algorithm over SDN: Reusable Reinforcement Learning Approach (RLSR-Routing) – ResearchGate (2024)【turn21search14】  
88) Multi-Agent Reinforcement Learning Framework in SDN-IoT for Transient Load Detection and Prevention – ResearchGate (2024)【turn21search16】  
89) Efficient SDN-Based Traffic Monitoring in IoT Networks with Double Deep Q-Network (chapter) – Cited in Springer retracted chapter (2020)【turn8fetch0】  
90) A Survey on Research Challenges and Applications in Empowering the SDN-Based Internet of Things – 2019 (widely indexed)【turn8fetch0】  
91) Software Defined Network Traffic Classification for QoS Optimization – J. Netw. Syst. Manag. (2025)【turn28search8】  
92) How network monitoring and reinforcement learning can improve TCP fairness in wireless multi-hop networks – EURASIP JWCN (2016)【turn54fetch0】  
93) TCP Congestion Management Using Deep Reinforcement Trained Agent for RED (TCP-ML) – Concurrency and Computation (2024)【turn29fetch0】  
94) Intelligent Scheme for Congestion Control: When Active Queue Management Meets Deep Reinforcement Learning (NDN) – ResearchGate (2021)【turn4search19】  
95) Automatic ECN Tuning for High-Speed Datacenter Networks (ACC) – ACM SIGCOMM (2021)【turn47search3】  
96) Safety in DRL-Based Congestion Control: A Framework Empowered by Marten – HKUST Research Portal (2024)【turn39search4】  
97) Deep Reinforcement Learning for Job Scheduling and Resource Management in Cloud Computing: An Algorithm-Level Review – ResearchGate (2025)【turn44search11】  
98) DeepWeave: DRL coflow scheduling – Future Gener. Comput. Syst. (2020, cited in 2023 attention-DRL paper)【turn42fetch0】  
99) Reinforcement Learning solutions in networks (Ericsson blog context) – Ericsson (2022)【turn49search2】  
100) IEACC: An Intelligent Edge-aided Congestion Control Scheme for Named Data Networking with DRL – IEEE TNSM (2022)【turn51search4】  

---

If you want, I can next:
- Export these 100 items into BibTeX/RIS for import into Mendeley/Zotero/EndNote, or
- Add more items narrowly focused on a subdomain (e.g., “RL-based AQM only,” “DRL for datacenter coflow scheduling only,” “RL for slice admission in 5G”).