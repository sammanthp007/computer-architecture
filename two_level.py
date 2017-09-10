"""
Here we are modeling a system that has
- one simple CPU core
- one system-wide memory bus
- a single DDR3 memory channel
"""

import m5
from m5.objects import *

from caches import *

# instantiate the system we are simulating
system = System()

# instantiate the system clock and set the time and voltage
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# set the memory type and range
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# instantiate the cpu and a system wide memory bus
system.cpu = TimingSimpleCPU()
system.membus = SystemXBar()

# instantiate the L1 caches
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()

# connect the cache to the CPU ports
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# x86 requirement to connect PIO and interrupt ports to mem bus
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

system.system_port = system.membus.slave

# create a mem controller and connect it to membus
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# instantiate process that we will run
process = Process()
process.cmd = ['tests/test-progs/hello/bin/x86/linux/hello']

# set the system to run the process
system.cpu.workload = process
system.cpu.createThreads()

# instantiate the system and begin execution
root = Root(full_system = False, system = system)
m5.instantiate()

# simulate
print "Begin simulation"
exit_event = m5.simulate()
print "Exiting @ tick %i because %s" % (m5.curTick(), exit_event.getCause())

