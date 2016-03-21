"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftHost = self.addHost( 'h1', ip='10.122.1.1' )
        rightHost = self.addHost( 'h2', ip='10.233.2.1'  )
        leftSwitch = self.addSwitch( 's1' )
        rightSwitch = self.addSwitch( 's2' )
	midSwitch = self.addSwitch( 's3' )
	uplSwitch = self.addSwitch( 's4' )
	uprSwitch = self.addSwitch( 's5' )
	
	

        # Add links
        self.addLink( leftHost, leftSwitch )
        self.addLink( leftSwitch, midSwitch )
        self.addLink( midSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost )
	self.addLink( rightSwitch, uprSwitch )
	self.addLink( leftSwitch, uplSwitch )
	self.addLink( uprSwitch, uplSwitch )


topos = { 'mytopo': ( lambda: MyTopo() ) }
