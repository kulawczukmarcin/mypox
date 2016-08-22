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
    CLI( net )
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    if len(sys.argv) > 1:
        controllers = sys.argv[1:]
    else:
        print 'Usage: startnet <c0 IP> <c1 IP> ...'
        exit(1)
    run(controllers)
