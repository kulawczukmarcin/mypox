#!/usr/bin/python
 
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf
 
def aggNet():
 
    CONTROLLER_IP='127.0.0.1'
 
    net = Mininet( topo=None,
                build=False)
 
    net.addController( 'c0',
                    controller=RemoteController,
                    ip=CONTROLLER_IP,
                    port=6633)
 

    
    # Add hosts and switches
    leftHost = net.addHost( 'h1', ip='10.1.1.0' )
    rightHost = net.addHost( 'h2', ip='10.3.1.0' )
    leftSwitch = net.addSwitch( 's1' )
    rightSwitch = net.addSwitch( 's2' )
    midSwitch = net.addSwitch( 's3' )
    uplSwitch = net.addSwitch( 's4' )
    uprSwitch = net.addSwitch( 's5' )
	
	

    # Add links
    net.addLink( leftHost, leftSwitch )
    net.addLink( leftSwitch, midSwitch )
    net.addLink( midSwitch, rightSwitch )
    net.addLink( rightSwitch, rightHost )
    net.addLink( rightSwitch, uprSwitch )
    net.addLink( leftSwitch, uplSwitch )
    net.addLink( uprSwitch, uplSwitch )


 
 
    net.start()
    CLI( net )
    net.stop()
 
if __name__ == '__main__':
    setLogLevel( 'info' )
    aggNet()
