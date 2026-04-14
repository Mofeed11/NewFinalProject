#!/usr/bin/env python3

import os
import socket
import time
from functools import partial

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class CustomTreeTopo(Topo):
    def build(self):
        # Add 14 switches
        info("*** Adding switches\n")
        s1 = self.addSwitch("s1", dpid="0000000000000001", protocols="OpenFlow13")
        s2 = self.addSwitch("s2", dpid="0000000000000002", protocols="OpenFlow13")
        s3 = self.addSwitch("s3", dpid="0000000000000003", protocols="OpenFlow13")
        s4 = self.addSwitch("s4", dpid="0000000000000004", protocols="OpenFlow13")
        s5 = self.addSwitch("s5", dpid="0000000000000005", protocols="OpenFlow13")
        s6 = self.addSwitch("s6", dpid="0000000000000006", protocols="OpenFlow13")
        s7 = self.addSwitch("s7", dpid="0000000000000007", protocols="OpenFlow13")
        s8 = self.addSwitch("s8", dpid="0000000000000008", protocols="OpenFlow13")
        s9 = self.addSwitch("s9", dpid="0000000000000009", protocols="OpenFlow13")

        # 5 additional access switches to increase path diversity
        s10 = self.addSwitch("s10", dpid="0000000000000010", protocols="OpenFlow13")
        s11 = self.addSwitch("s11", dpid="0000000000000011", protocols="OpenFlow13")
        s12 = self.addSwitch("s12", dpid="0000000000000012", protocols="OpenFlow13")
        s13 = self.addSwitch("s13", dpid="0000000000000013", protocols="OpenFlow13")
        s14 = self.addSwitch("s14", dpid="0000000000000014", protocols="OpenFlow13")

        # Add 8 hosts
        info("*** Adding hosts\n")
        h1 = self.addHost("h1", mac="00:00:00:00:00:01")
        h2 = self.addHost("h2", mac="00:00:00:00:00:02")
        h3 = self.addHost("h3", mac="00:00:00:00:00:03")
        h4 = self.addHost("h4", mac="00:00:00:00:00:04")
        h5 = self.addHost("h5", mac="00:00:00:00:00:05")
        h6 = self.addHost("h6", mac="00:00:00:00:00:06")
        h7 = self.addHost("h7", mac="00:00:00:00:00:07")
        h8 = self.addHost("h8", mac="00:00:00:00:00:08")

        # Add links (10 Mbps, 5 ms delay)
        info("*** Adding links\n")
        linkopts = dict(bw=10, delay="5ms")

        # Connect Core and Aggregation
        self.addLink(s1, s2, **linkopts)
        self.addLink(s1, s3, **linkopts)

        self.addLink(s2, s4, **linkopts)
        self.addLink(s2, s5, **linkopts)
        self.addLink(s2, s6, **linkopts)

        self.addLink(s3, s7, **linkopts)
        self.addLink(s3, s8, **linkopts)
        self.addLink(s3, s9, **linkopts)

        # Connect Access Switches (s10-s14) to Core/Aggregation for path diversity
        self.addLink(s4, s10, **linkopts)
        self.addLink(s5, s11, **linkopts)
        self.addLink(s6, s12, **linkopts)
        self.addLink(s7, s13, **linkopts)
        self.addLink(s8, s14, **linkopts)

        # Cross links for diversity. The controller installs explicit paths,
        # so these extra links provide alternative routes without flooding.
        self.addLink(s10, s11, **linkopts)
        self.addLink(s12, s13, **linkopts)
        self.addLink(s5, s7, **linkopts)

        # Connect Hosts to Access Switches
        self.addLink(h1, s10, **linkopts)
        self.addLink(h2, s10, **linkopts)
        self.addLink(h3, s11, **linkopts)
        self.addLink(h4, s12, **linkopts)
        self.addLink(h5, s13, **linkopts)
        self.addLink(h6, s14, **linkopts)
        self.addLink(h7, s14, **linkopts)
        self.addLink(h8, s8, **linkopts)  # Connected to agg switch for variety


def configure_queues(switch):
    for intf_name in switch.intfNames():
        if intf_name == "lo":
            continue
        qos_cmd = (
            "ovs-vsctl set port {port} qos=@qos -- "
            "--id=@qos create qos type=linux-htb "
            "queues=0=@q0,1=@q1,2=@q2 -- "
            "--id=@q0 create queue other-config:min-rate=8000000 "
            "other-config:max-rate=10000000 -- "
            "--id=@q1 create queue other-config:min-rate=4000000 "
            "other-config:max-rate=7000000 -- "
            "--id=@q2 create queue other-config:min-rate=1000000 "
            "other-config:max-rate=3000000"
        ).format(port=intf_name)
        switch.cmd(qos_cmd + " 2>/dev/null")
    info("*** Configured queues on %s\n", switch.name)


def wait_for_controller(ip_addr, port, timeout=20):
    deadline = time.time() + timeout
    while time.time() < deadline:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.connect((ip_addr, port))
            sock.close()
            return True
        except OSError:
            time.sleep(1)
        finally:
            sock.close()
    return False


def run_topology():
    controller_ip = os.environ.get("SDN_CONTROLLER_IP", "127.0.0.1")
    controller_port = int(os.environ.get("SDN_CONTROLLER_PORT", "6653"))

    info("*** Waiting for controller at %s:%s\n" % (controller_ip, controller_port))
    if not wait_for_controller(controller_ip, controller_port, timeout=20):
        info("*** ERROR: Controller is not reachable. Start Ryu first.\n")
        return

    topo = CustomTreeTopo()
    switch_cls = partial(OVSSwitch, protocols="OpenFlow13")

    # We explicitly tell Mininet NOT to build a default controller here
    net = Mininet(topo=topo, controller=None, switch=switch_cls, link=TCLink)

    # Add Remote Ryu Controller
    net.addController(
        "c0",
        controller=RemoteController,
        ip=controller_ip,
        port=controller_port,
        protocol="tcp",
    )

    net.start()
    info("*** Starting network\n")

    info("*** Enabling STP on all bridges\n")
    for switch in net.switches:
        switch.cmd("ovs-vsctl set bridge %s stp_enable=true" % switch.name)

    info("*** Configuring OVS QoS Queues\n")
    for switch in net.switches:
        configure_queues(switch)

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    run_topology()
