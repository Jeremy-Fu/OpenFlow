#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.node import CPULimitedHost
from mininet.cli import CLI


class UnblancedTree(Topo):
    
    def __init__(self, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        switch3 = self.addSwitch('s3')
        switch4 = self.addSwitch('s4')
        switch5 = self.addSwitch('s5')
        switch6 = self.addSwitch('s6')

        host1 = self.addHost('h1')
        host2 = self.addHost('h2')
        host3 = self.addHost('h3')
        host4 = self.addHost('h4')
        host5 = self.addHost('h5')
        host6 = self.addHost('h6')
        host7 = self.addHost('h7')
        host8 = self.addHost('h8')

        self.addLink(host1, switch1)
        self.addLink(switch1, switch2,
            bw = 10, delay = '1ms', loss = 3)
        self.addLink(switch1, switch3,
            bw = 15, delay = '2ms', loss = 2)


        self.addLink(switch2, host2)
        self.addLink(switch2, switch4,
            bw = 20, delay = '4ms', loss = 1)

        self.addLink(switch4, host5)
        self.addLink(switch4, host4)

        self.addLink(switch3, host3)
        self.addLink(switch3, switch5,
            bw = 20, delay = '4ms', loss = 1)

        self.addLink(switch5, switch6,
            bw = 40, delay = '10ms', loss = 2)
        self.addLink(switch5, host6)

        self.addLink(switch6, host7)
        self.addLink(switch6, host8)

def simpleTest():
    "Create and test a simple network"
    topo = UnblancedTree()
    net = Mininet(topo, host=CPULimitedHost, link=TCLink)
    net.start()
    
    for srcHostNum in range(8) :
        srcHost = net.get('h%s' % (srcHostNum + 1))

        # iperf_outfiles[ srcHostNum ] = '/tmp/iperf%s.out' % srcHostNum.name
        # iperf_errfiles[ srcHostNum ] = '/tmp/iperf%s.err' % srcHostNum.name

        for dstHostNum in range(8):
            if srcHostNum == dstHostNum:
                continue

            #tmp_out = 'h{param1}_ping_h{param2}.out'.format(param1 = srcHostNum + 1, param2 = dstHostNum + 1)
            #tmp_err = 'h{param1}_ping_h{param2}.err'.format(param1 = srcHostNum + 1, param2 = dstHostNum + 1)

            dstHost = net.get('h%s' % (dstHostNum + 1))
            print 'Now! h{param1} ping h{param2}'.format(param1 = srcHostNum + 1, param2 = dstHostNum + 1)
            
            dstHost.cmdPrint('iperf -u -s &')
            #clientcmd = "iperf -u -c " + dstHost.IP() + " -b 15"
            srcHost.cmdPrint('iperf -u -c' , dstHost.IP(), ' -b 15000000 -l 500')
            print "\n\n\n"
            
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
# Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
