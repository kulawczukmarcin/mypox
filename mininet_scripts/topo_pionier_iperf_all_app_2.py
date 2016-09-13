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
    net = Mininet(topo=topo, controller=None,  autoSetMacs=True,  link=TCLink)
    ctrl_count = 0
    for controllerIP in controllers:
        net.addController('c%d' % ctrl_count, RemoteController, ip=controllerIP)
        ctrl_count += 1
    net.start()
    CLI(net)
    #sleep(30)
    hWarszawa = net.getNodeByName('hWarszawa')
    hPoznan = net.getNodeByName('hPoznan')
    hWroclaw = net.getNodeByName('hWroclaw')
    hKrakow = net.getNodeByName('hKrakow')
    hGdansk = net.getNodeByName('hGdansk')
    hLublin = net.getNodeByName('hLublin')
    hOlsztyn = net.getNodeByName('hOlsztyn')
    hBialy = net.getNodeByName('hBialy')

    hosts = [hWarszawa, hPoznan, hWroclaw, hKrakow, hGdansk, hLublin, hOlsztyn, hBialy]

    sleep(10)

    flows = [

            2.73,
		0.045,
		0.77,
		1.449,
		1.12,
		0.089,
		2.53,
		0.473,
		0.253,
		2.016,
            0.057,
		0.049,
		0.649,
		0.097,
		0.00038,
		0.275,
		7.13,
		0.077,
		0.396,
		0.418,
            0.858,
		0.506,
		4.65,
		0.638,
		0.197,
		1.36,
		3.72,
		0.1,
		0.028,
		0.147,
            0.25,
		1.617,
		0.1008,
		0.385,
		1.65,
		0.058,
		0.017,
		0.0777,
		0.528,
		1.21,
            0.10,
		3.038,
		1.575,
		1.023,
		1.3,
		1.12,
		0.525,
		0.627,
		1.1,
		0.67,
            0.572,
		4.65,
		5.27,
		0.748,
		0.399,
		1.302,
		0.252,
		0.059,
		1.11,
		0.649,
            2.94,
		3.99,
		0.0051,
		1.21,
		1.261,
		6.15,
		0.02,
		0.00682,
		4.1,
		0.0672,
            0.858,
		0.506,
		1.65,
		0.638,
		0.17,
		1.26,
		3.72,
		0.837,
		0.028,
		0.147,
        0.275,
        0.057,
        0.1,
        0.1134,
        0.77,
        0.081,
        0.013,
        0.01,
        1.012,
	4.65,
		5.27,
		0.748,
		0.399,
		1.302,
		0.252,
		0.059,
		1.11,
		0.649,
            2.94,
		3.99,
		0.0051,
		1.21,
		1.261,
		6.15,
		0.02,
		0.00682,
		4.1,
		0.0672,
            0.858,
		0.506,
		1.65,
		0.638,
		0.17,
		1.26,
		3.72,
		0.837,
		0.028,
		0.147,
        0.275,
        0.057,
        0.1,
        0.1134,
        0.77,
        0.081,
        0.013,
        0.01,
        1.012,
        0.11,
        0.561,
        1.65,
        0.352,
        0.77,
        0.99,
        5.88,
        3.08,
        5.518,
        0.704,
  0.013,
        0.01,
        1.012,
        0.11,
        0.561,
        1.65,
        0.352,
        0.77,
        0.99,
        5.88,
        3.08,
        5.518,
        0.704,
        1.394,
        1.394,
        2.0559,
        2.2,
        3.25,
        0.748,
        1.76,
        1.47,
        1.47,
        1.323,
        1.21,
        0.561,
        1.419,
        3.968,
        2.201,
        0.33,
        0.055,
        0.33,
        0.651,
        0,
        0.121,
        6.93,
        1.197,
        0.847,
        0.124,
        0.903,
        0.051,
        0.861,
        0.197,
        1.1041,
        1.575,
        0.13,
        0.107,
        2.856,
       2.592,
		0.66,
		1.87,
		0.16,
		0.43,
		6.51,
		0.539,
		0.609,
		0.308,
		0.319,
             2.73,
		0.045,
		0.77,
		1.449,
		0.12,
		0.089,
		2.53,
		0.473,
		0.253,
		2.016,
             0.057,
		0.049,
		0.649,
		0.097,
		0.00038,
		0.275,
		7.13,
		0.077,
		0.396,
		0.418,
             0.572,
		4.265,
		2.04,
		0.748,
		1.399,
		1.302,
		0.252,
		0.123,
		1.11,
		0.649,
             2.94,
		0.58,
		0.51,
		0.21,
		2.01,
		6.15,
		0.84,
		1.8,
		4.1,
		0.0672,
             5.27,
		0.19,
		0.18,
		1.98,
		2.418,
		0.036,
		2.046,
		0.0021,
		1.1,
		1.705,
             2.592,
		0.66,
		1.87,
		1.879,
		0.407,
		6.51,
		0.539,
		0.609,
		0.308,
		0.319,
             1.77,
		0.891,
		0.443,
		0.211,
		2.012,
		1.331,
		0.17,
		2.05,
		0.2,
		0.33,
            1.023,
		1.76,
		1.344,
0.01,
        1.012,
        0.11,
        0.561,
        1.65,
        0.352,
        0.77,
        0.99,
        5.88,
        3.08,
        5.518,
        0.704,
        1.394,
		0.00038,
		0.275,
		7.13,
		0.077,
		0.396,
		0.418,
             0.572,
		4.265,
		2.04,
		0.748,
		1.399,
		1.302
             ]

   # razy 2
    times = [19.32,
		6.38, 0.273, 25.11, 26.97, 8.4, 27.3, 8.58, 31.5, 13.2,
            0.66, 0.483, 0.5000, 11, 16.17, 23.1, 12.1, 1.54, 27.3, 27.3,
            12.39, 14.3, 0.018, 34.1, 0.28, 51, 0.93, 18.29, 0.13, 3.52,
            18.27, 15.4, 10.56, 8.19, 1.2, 27.3, 17.75, 1.7, 1.3, 17.43,
            61.5, 13.02, 20.814, 27.88, 37.2, 16.5, 6.2, 0.2, 15.4, 56.7,
            11.97, 4.2, 0.031, 4.41, 15.96, 0.19, 0.671, 16.5, 33.6, 0.52,
            5.39, 10.35, 14.57, 1.7, 5.94, 29.4, 17.98, 0.69, 0.39, 3.99,
            14.3, 4.41, 15.96, 8.67, 0.84, 1.8, 25.83, 0.29, 6.16, 17.43,
            0.23, 1.067, 16.8, 4.2, 10.5, 0.31, 1.008, 31, 0.16, 0.43,
            2.3, 13.53, 2.2,  25.2, 14.3, 8.14, 20.9, 62, 12.1, 19.8,
             0.58,
             21.39,
             4.29,
             2.09,
             39.9,
             27.3,
             0.21,
             0.76,
             6.97,
             26.04,
             1.8,
             25.83,
             6.09,
             11.76,
             25.73,
		4, 10.56, 8.19, 1.2, 27.3, 17.75, 1.7, 1.3, 17.43,
            61.5, 13.02, 20.814, 27.88, 37.2, 16.5, 6.2, 0.2, 15.4, 56.7,
            11.97, 4.2, 0.031, 4.41, 15.96, 0.19, 0.671, 16.5, 33.6, 0.52,
            5.39, 10.35, 14.57, 1.7, 5.94, 29.4, 17.98, 0.69, 0.39, 3.99,
            14.3, 4.41, 15.96, 8.67, 0.84, 1.8, 25.83, 0.29, 6.16, 17.43,
            0.23, 1.067, 16.8, 4.2, 10.5, 0.31, 1.008, 31, 0.16, 0.43,
            2.3, 13.53, 2.2,  25.2, 14.3, 8.14, 20.9, 62, 12.1, 19.8,
             0.58,
             21.39,
             4.29,
             2.09,
             39.9,
             27.3,
             0.21,
             0.76,
             6.97,
             26.04,
             1.8,
             25.83,
             6.09,
             11.76,
             25.73,
             2,
             9.43,
             1.067,
             8.8,
             8.2,
             5.5,
             6.51,
             0.048,
             31,
             1.76,
             4.7,
             19.8,
             34.1,
             7.7,
             0.46,
             8.4,
             33.18,
             3.41,
             6.71,
             25.11,
             89.9,
             0.3,
             37.5,
             54.56,
             24.57,
             3.36,
             8.8,
             4.07,
             14.9,
             17.16,
             20.13,
             3,
             8.47,
             34.007,
             19.8,
             0.8,
             46.5,
             14.49,
             19.99,
             0.6,
             26.04,
             15.73,
             0.8,
             23.1,
             6.3,
             30.6,
             24.6,
             54.18,
             27.51,
             1.61,
             1.81,
             120.9,
             7.7,
             24.3,
             113.1,
             88.97,
             24.36,
             0.2,
             15.0,
             18.81,
             104.96,
             2.83,
             84,
             19.47,
             2.09,
             30.8,
             37.8,
             102.5,
             1.69,
             40.992,
             25.83,
             6.09,
             11.76,
             25.73,
             2,
             9.43,
             1.067,
             8.8,
             8.2,
             5.5,
             6.51,
             0.048,
             31,
             1.76,
             4.7,
             19.8,
             34.1,
             7.7,
             0.46,
             8.4,
8.4,
             33.18,
             3.41,
             6.71,
             25.11,
             89.9,
             0.3,
             37.5,
             54.56,
             24.57,
             ]

    # podzielic na 30
    sleeps = [1, 19, 86, 89, 7, 29, 26, 26, 32, 22, 19, 43, 13, 1, 30, 46,
              90, 75, 16, 14, 73, 30, 44, 18, 92, 22, 73, 7, 49, 18, 57, 1,
              86, 62, 61, 85, 57, 97, 44, 44, 7, 89, 72, 6, 64, 90, 3, 66,
              30, 51, 99, 56, 48, 99, 99, 88, 8, 57, 29, 28, 22, 73, 78, 86,
              99, 91, 68, 60, 64, 87, 25, 15, 38, 82, 66, 11, 16, 29, 18, 40,
              64, 6, 26, 13, 84, 35, 34, 50, 89, 72, 6, 64, 90, 3, 66,
              30, 51, 99, 56, 48, 99, 99, 88, 8,11, 16, 51, 70, 74, 52, 41, 36,
              74, 38, 83, 28,3, 30, 44, 18, 92, 22, 73, 7, 49, 18, 57, 1,
              86, 62, 61, 85, 57, 97, 44, 44, 7,  57, 29, 28, 22, 73, 78, 86,
              99, 91, 68, 60, 64, 87, 25, 15, 38, 82, 66, 11, 16, 29, 18, 40,
              64, 6, 26, 13, 84, 35, 34, 50, 11, 16, 51,
              11, 16, 51, 70, 74, 52, 41, 36,
              74, 38, 83, 28, 3, 30, 44, 18, 92, 22, 73, 7, 49, 18, 57, 1,
              86, 62, 61, 85, 57, 97, 44, 44, 7, 87, 25, 15, 38, 82, 66, 11, 16, 29, 18, 40,
              64, 6, 26, 13, 84, 35, 34, 50, 89, 72, 6, 64, 90, 3, 66,
              30, 51, 99, 56, 48, 99, 99, 88, 8,11, 16, 51, 70, 74, 52, 41, 36,
              74, 38, 83, 28,3, 30, 44, 18, 92, 22, 73, 7, 49, 18, 57, 1,
              86, 62, 61, 85, 57, 97, 44, 44, 7,  57, 29, 28, 22, 73, 78, 86,
              99, 91, 68, 60, 64, 87, 25, 15, 38, 82, 66, 11, 16, 29, 18, 40,
              64, 6, 26, 13, 84, 35, 34, 50, 11, 16, 51,
              11, 16, 51, 70, 74, 52, 41, 36,
              74, 38, 83, 28, 3, 30, 44, 18, 92, 22, 73, 7, 49, 18, 57, 1,
             30, 44, 18, 92, 22, 73, 7, 49, 18, 57, 1,
             86, 62, 61, 85, 57, 97, 44, 44, 7, 87, 25, 15, 38, 82, 66, 11, 16, 29, 18, 40,
             64, 6, 26, 13, 84, 35, 34, 50, 89, 72, 6, 64, 90, 3, 66,
             30, 51, 99, 56, 48, 99, 99, 88, 8, 11, 16, 51, 70, 74, 52, 41, 36,
             74, 38, 83, 28, 3, 30, 44, 18, 92, 2
		, 30, 51, 99, 56, 48, 99, 99, 88, 8,11, 16, 51, 70, 74, 52, 41, 36,
              74, 38, 83, 28,3, 30, 44, 18, 92, 22, 73, 7, 49, 18, 57, 1,
              86, 62, 61, 85, 57, 97, 44, 44, 7,  57, 29, 28, 22, 73, 78, 86,
              99, 91, 68, 60, 64, 87, 25, 15, 38, 82, 66, 11, 16, 29, 18, 40,
              64, 6, 26, 13, 84, 35, 34, 50, 11, 16, 51,
              11, 16, 51, 70, 74, 52, 41, 36,
              74, 38, 83, 28, 3, 30, 44, 18, 92, 22, 73, 7, 49, 18, 57, 1,
              86, 62, 61, 85, 57, 97, 44, 44, 7, 87, 25, 15, 38, 82, 66, 11, 16, 29, 18, 40,
              64, 6, 26, 13, 84, 35, 34, 50, 89, 72, 6, 64, 90, 3, 66,
              30, 51, 99, 56, 48, 99, 99, 88, 8,11, 16, 51, 70, 74, 52, 41, 36,
              74, 38, 83, 28,3, 30, 44, 18, 92, 22, 73, 7, 49, 18, 57, 1,
              86, 62, 61, 85, 57, 97, 44, 44, 7,  57, 29, 28, 22, 73, 78, 86,
              99, 91, 68, 60, 64, 87, 25, 15, 38, 82, 66, 11, 16, 29, 18, 40,
              64, 6, 26, 13, 84, 35, 34, 50, 11, 16, 51,
              11, 16, 51, 70, 74, 52, 41, 36,
              74, 38, 83, 28, 3, 30, 44, 18, 92, 22, 73, 7, 49, 18, 57, 1,
             30, 44, 18, 92, 22, 73, 7, 49, 18, 57, 1, 6, 26, 13, 84, 35, 34, 50, 11, 16, 51,
              11, 16, 51, 70, 74, 52, 41, 36,
              74, 38, 83, 28, 3, 30, 44, 18, 92, 22, 73, 7, 49, 18, 57, 1,
              86, 62, 61, 85, 57, 97, 44, 44, 7, 87, 25, 15, 38, 82, 66, 11, 16, 29, 18, 40,
              64, 6, 26, 13, 84, 35, 34, 50, 89, 72, 6, 64, 90, 3, 66,
              30, 51, 99, 56, 48, 99, 99, 88, 8,11, 16, 51, 70, 74, 52, 41, 36,
              74, 38, 83, 28,3, 30, 44, 18, 92, 22, 73, 7, 49, 18, 57, 1,
              86, 62, 61, 85, 57, 97, 44, 44, 7,  57, 29, 28, 22, 73, 78, 86,
              99, 91, 68, 60, 64, 87, 25, 15, 38, 82, 66, 11, 16, 29, 18, 40,
              64, 6, 26, 13, 84, 35, 34, 50, 11, 16, 51,
              11, 16, 51, 70, 74, 52, 41, 36,
              74, 38, 83, 28, 3, 30, 44, 18, 92, 22, 73, 7, 49, 18, 57, 1,
             30, 44, 18, 92, 22, 73, 7, 49, 18, 57, 1,
             86, 62, 61, 85, 57, 97, 44, 44, 7, 87, 25, 15, 38, 82, 66,
              ]

    for i in range(280):
        p = 5000+i
        for host in hosts:
            host.cmd("iperf -s -u -p  %s  -y C  > alltoall/app/server/%s_%s_%s.txt &" % (p, host, i, flows[i]))

    j=-1
    for i in range(280):
        p = 5000 + i
        print "start flow ",i
        irest = i % len(hosts)
	host = hosts[irest]
        if irest  == 0:
            j=j+1
	jirest = (j+i)%len(hosts)
	print p, irest, host, jirest
        if irest != jirest:
		host.cmd("iperf -c 10.0.0.%s -p %s -u -y C -t %s -b %sm > alltoall/app/client/%s_%s_%s &" % (jirest+1, p, times[i], flows[i], host, i,j  ))
        else:
		print "matched: ",host, jirest+1
	sleep(sleeps[i]/30)


    #sleep(500)
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


