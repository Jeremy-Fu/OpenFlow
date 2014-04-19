#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.node import CPULimitedHost

class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def __init__(self, n=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        switch = self.addSwitch('s1')
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch,
                    bw=10, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)


def simpleTest():
    "Create and test a simple network"
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo, host=CPULimitedHost, link=TCLink)
    net.start()
    print "Starting test..."
    h1.cmd('while true; do date; sleep 1; done > /tmp/date.out &')
    sleep(10)
    print "Stopping test"
    h1.cmd('kill %while')
    print "Reading output"
    f = open('/tmp/date.out')
    lineno = 1
    for line in f.readlines():
        print "%d: %s" % ( lineno, line.strip() )
        lineno += 1
    f.close()

if __name__ == '__main__':
# Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
