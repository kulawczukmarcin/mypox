#!/usr/bin/env python

import sys
from time import sleep

from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.log import setLogLevel
from mininet.link import TCLink


class MyTopo(Topo):
    "Simple topology example."

    def __init__(self):
        "Create custom topo."

        # Initialize topology
        Topo.__init__(self)

        # Add hosts and switches
        leftHost = self.addHost('h1', ip='10.0.0.1')
        rightHost = self.addHost('h2', ip='10.0.0.2')
        leftSwitch = self.addSwitch('s1')
        rightSwitch = self.addSwitch('s2')
        downSwitch = self.addSwitch('s3')
        upSwitch = self.addSwitch('s4')

        linkopts = dict(bw=10)
        linkoptsh = dict(bw=100)
        # Add links
        self.addLink(leftHost, leftSwitch, **linkoptsh)
        self.addLink(leftSwitch, downSwitch, **linkopts)
        self.addLink(downSwitch, rightSwitch, **linkopts)
        self.addLink(rightSwitch, rightHost, **linkoptsh)
        self.addLink(rightSwitch, upSwitch, **linkopts)
        self.addLink(leftSwitch, upSwitch, **linkopts)


topos = {'mytopo': (lambda: MyTopo())}


def run(controllers):
    topo = MyTopo()
    net = Mininet(topo=topo, controller=None, autoSetMacs=True, link=TCLink)
    ctrl_count = 0
    for controllerIP in controllers:
        net.addController('c%d' % ctrl_count, RemoteController, ip=controllerIP)
        ctrl_count += 1
    net.start()
    sleep(15)
    h1, h2 = net.getNodeByName('h1', 'h2')
    s3, s4 = net.getNodeByName('s3', 's4')
    s3.cmd("sudo wireshark &")
    s4.cmd("sudo wireshark &")
    h1.cmd("ping 10.0.0.2 -c 10 > logping.txt")
    for i in range(9):
        h2.cmd("iperf -s -u -p  500%s  -i 0.5 > logserverapp%s.txt &" % (i, i))

    for i in range(8):
        h1.cmd("iperf -c 10.0.0.2 -p 500%s -u -t 30 -b 1m -i 1 > log%s.txt &" % (i, i))
    # h1.cmd("iperf -c %s -p 5001 -t 5 > log0.txt" % h2.IP())
    #    sleep(5)
    h1.cmd("iperf -c 10.0.0.2 -p 5008 -u -t 30 -b 6m -i 1 > logele.txt &")

    sleep(30)
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    if len(sys.argv) > 1:
        controllers = sys.argv[1:]
    else:
        print 'Usage: startnet <c0 IP> <c1 IP> ...'
        exit(1)
    run(controllers)
