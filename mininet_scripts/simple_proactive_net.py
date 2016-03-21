#!/usr/bin/python
 
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf

"""
THis is from https://haryachyy.wordpress.com/2014/06/14/learning-pox-openflow-controller-proactive-approach/. To save time added
    h1.cmd( 'dhclient h1-eth0 ') 
    h2.cmd( 'dhclient h2-eth0' ) 
This is staticlly setting IPs. Don't really sure if this works fine (for proactive approch).

!!!POX must started for this to work!!!

"""
def aggNet():
 
    CONTROLLER_IP='192.168.56.1'
 
    net = Mininet( topo=None,
                build=False)
 
    net.addController( 'c0',
                    controller=RemoteController,
                    ip=CONTROLLER_IP,
                    port=6633)
 
    h1 = net.addHost( 'h1', ip='0.0.0.0' )
    h2 = net.addHost( 'h2', ip='0.0.0.0' )
    s1 = net.addSwitch( 's1' )
    s2 = net.addSwitch( 's2' )
    s3 = net.addSwitch( 's3' )
 
    net.addLink( s1, s2 )
    net.addLink( s2, s3 )
 
    net.addLink( h1, s1 )
    net.addLink( h2, s1 )
 
    net.start()
    #print h1.cmd( 'ping -c1', h2.IP() ) 
    
    h1.cmd( 'dhclient h1-eth0 ') 
    h2.cmd( 'dhclient h2-eth0' ) 
    CLI( net )

    net.stop()
 
if __name__ == '__main__':
    setLogLevel( 'info' )
    aggNet()
