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

        def int2dpid(dpid):
            try:
                dpid = hex(dpid)[2:]
                dpid = '0' * (16 - len(dpid)) + dpid
                return dpid
            except IndexError:
                raise Exception('Unable to derive default datapath ID - '
                                'please either specify a dpid or use a '
                                'canonical switch name such as s23.')

        # Initialize topology
        Topo.__init__(self)

        # Add hosts and switches
        hWarszawa = self.addHost('hWarszawa', ip='10.0.0.1')
        hPoznan = self.addHost('hPoznan', ip='10.0.0.2')
        hWroclaw= self.addHost('hWroclaw', ip='10.0.0.3')
        hKrakow = self.addHost('hKrakow', ip='10.0.0.4')
        hGdansk = self.addHost('hGdansk', ip='10.0.0.5')
        hLublin = self.addHost('hLublin', ip='10.0.0.6')
        hOlsztyn = self.addHost('hOlsztyn', ip='10.0.0.7')
        hBialy = self.addHost('hBialy', ip='10.0.0.8')

        swWarszawa = self.addSwitch('swWarszawa', dpid=int2dpid(1))
        swBialy = self.addSwitch('swBialy', dpid=int2dpid(2))
        swGdansk = self.addSwitch('swGdansk', dpid=int2dpid(3))
        swKoszalin = self.addSwitch('swKoszalin', dpid=int2dpid(5))
        swSzczecin = self.addSwitch('swSzczecin', dpid=int2dpid(6))
        swOlsztyn = self.addSwitch('swOlsztyn', dpid=int2dpid(7))
        swGorzow = self.addSwitch('swGorzow', dpid=int2dpid(8))
        swBydgosz = self.addSwitch('swBydgosz', dpid=int2dpid(9))
        swTorun = self.addSwitch('swTorun', dpid=int2dpid(10))
        swPoznan = self.addSwitch('swPoznan', dpid=int2dpid(11))
        swZielona = self.addSwitch('swZielona', dpid=int2dpid(12))
        swWroclaw = self.addSwitch('swWroclaw', dpid=int2dpid(13))
        swLodz = self.addSwitch('swLodz', dpid=int2dpid(14))
        swOpole = self.addSwitch('swOpole', dpid=int2dpid(15))
        swCzesto = self.addSwitch('swCzesto', dpid=int2dpid(16))
        swGliwice = self.addSwitch('swGliwice', dpid=int2dpid(17))
        swRadom = self.addSwitch('swRadom', dpid=int2dpid(18))
        swKielce = self.addSwitch('swKielce', dpid=int2dpid(19))
        swPulawy = self.addSwitch('swPulawy', dpid=int2dpid(20))
        swLublin = self.addSwitch('swLublin', dpid=int2dpid(21))
        swRzeszow = self.addSwitch('swRzeszow', dpid=int2dpid(22))
        swBielsko = self.addSwitch('swBielsko', dpid=int2dpid(23))
        swKrakow = self.addSwitch('swKrakow', dpid=int2dpid(24))


        linkopts = dict(bw=10)
        linkoptsh = dict(bw=1000)
        # Add links
        self.addLink(hWarszawa, swWarszawa, **linkoptsh)
        self.addLink(hPoznan, swPoznan, **linkoptsh)
        self.addLink(hWroclaw, swWroclaw, **linkoptsh)
        self.addLink(hKrakow, swKrakow, **linkoptsh)
        self.addLink(hGdansk, swGdansk, **linkoptsh)
        self.addLink(hLublin, swLublin, **linkoptsh)
        self.addLink(hOlsztyn, swOlsztyn, **linkoptsh)
        self.addLink(hBialy, swBialy, **linkoptsh)


        self.addLink(swOlsztyn, swGdansk, **linkopts)
        self.addLink(swOlsztyn, swBialy, **linkopts)
        self.addLink(swGdansk, swTorun, **linkopts)
        self.addLink(swKoszalin, swGdansk, **linkopts)
        self.addLink(swKoszalin, swSzczecin, **linkopts)
        self.addLink(swSzczecin, swGorzow, **linkopts)
        self.addLink(swGorzow, swPoznan, **linkopts)
        self.addLink(swPoznan, swZielona, **linkopts)
        self.addLink(swZielona, swWroclaw, **linkopts)
        self.addLink(swWroclaw, swOpole, **linkopts)
        self.addLink(swOpole, swGliwice, **linkopts)
        self.addLink(swGliwice, swBielsko, **linkopts)
        self.addLink(swBielsko, swKrakow, **linkopts)
        self.addLink(swKrakow, swRzeszow, **linkopts)
        self.addLink(swRzeszow, swLublin, **linkopts)
        self.addLink(swLublin, swPulawy, **linkopts)
        self.addLink(swPulawy, swRadom, **linkopts)
        self.addLink(swRadom, swWarszawa, **linkopts)
        self.addLink(swWarszawa, swBialy, **linkopts)
        self.addLink(swWarszawa, swPoznan, **linkopts)
        self.addLink(swWarszawa, swLodz, **linkopts)
        self.addLink(swRadom, swKielce, **linkopts)
        self.addLink(swKielce, swKrakow, **linkopts)
        self.addLink(swLodz, swPoznan, **linkopts)
        self.addLink(swCzesto, swLodz, **linkopts)
        self.addLink(swTorun, swBydgosz, **linkopts)
        self.addLink(swBydgosz, swPoznan, **linkopts)
        self.addLink(swCzesto, swGliwice, **linkopts)



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
