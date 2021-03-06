from functools import partial
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.node import CPULimitedHost
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.node import RemoteController


class MactableAttack(Topo):
    
    def __init__(self, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)     
        h1 = self.addHost( 'h1' )                                                                                              
        h2 = self.addHost( 'h2' )                                                                                              
        s1 = self.addSwitch( 's1' )                                                                                         
        self.addLink( h1, s1 )                                                                                                 
        self.addLink( h2, s1 )                                                                                                 



def simpleTest():
    topo=MactableAttack()
    net = Mininet( topo=topo, controller=partial( RemoteController, ip='10.0.2.2', port=6633 ) )
    net.start()
    h1=net.get('h1')
    h2=net.get('h2')
    print h1.cmd( 'ping -c1', h2.IP() )                                                                                   
    CLI( net )                                                                                                            
    net.stop()  

if __name__ == '__main__':
# Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()