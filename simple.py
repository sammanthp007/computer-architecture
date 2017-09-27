"""
Here we are modeling a system that has
- one simple CPU core
- one system-wide memory bus
- a single DDR3 memory channel
"""

import m5
from m5.objects import *

from caches import *
from optparse import OptionParser

parser = OptionParser()
parser.add_option('--cpu_model', help="CPU Model. \n1 - TimingSimpleCPU \n2 - MinorCPU")

parser.add_option('--use_cache', help="Bool to use cache or not. \n1 for yes. \nDefault is 0")
parser.add_option('--l1i_size', help="L1 instruction cache size. e.g 16kB")
parser.add_option('--l1i_assoc', help="L1 instruction cache associativity. Default is 1")
parser.add_option('--l1d_size', help="L1 data cache size")
parser.add_option('--l1d_assoc', help="L1 data cache associativity. Default is 1")
parser.add_option('--l2_size', help="Unified L2 cache size")
parser.add_option('--l2_assoc', help="Unified L2 cache associativity. Default is 1")

parser.add_option('--mem_config', help="The memory. Default is DDR3_1600_8x8. \n You can find other options using build/X86/gem5.opt configs/example/fs.py --list-mem-types")

parser.add_option('--clk_freq', help="CPU Clock Frequency. e.g 2GHz. Default is 1GHz")

(options, args) = parser.parse_args()

# instantiate the system we are simulating
system = System()

# instantiate the system clock and set the time and voltage
system.clk_domain = SrcClockDomain()
if options and options.clk_freq:
    system.clk_domain.clock = options.clk_freq
else:
    system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# set the memory type and range
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# instantiate the cpu
if options and options.cpu_model == '1':
    system.cpu = TimingSimpleCPU()
elif options and options.cpu_model == '2':
    system.cpu = MinorCPU()

# instantiate a system wide memory bus
system.membus = SystemXBar()

# add cache if needed
if options and options.use_cache:
    # instantiate the L1 caches
    system.cpu.icache = L1ICache(options)
    system.cpu.dcache = L1DCache(options)

    # connect the cache to the CPU ports
    system.cpu.icache.connectCPU(system.cpu)
    system.cpu.dcache.connectCPU(system.cpu)

    # create the L2 bus
    system.l2bus = L2XBar()

    # connect the l2 bus with the l1 caches
    system.cpu.icache.connectBus(system.l2bus)
    system.cpu.dcache.connectBus(system.l2bus)

    # create the unified l2 cache
    system.l2cache = L2Cache(options)

    # connect the l2 cache with membus and l2bus
    system.l2cache.connectCPUSideBus(system.l2bus)
    system.l2cache.connectMemSideBus(system.membus)
else:
    # connect the i-cache and d-cache port to membus directly
    system.cpu.icache_port = system.membus.slave
    system.cpu.dcache_port = system.membus.slave

# x86 requirement to connect PIO and interrupt ports to mem bus
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

system.system_port = system.membus.slave

# create a mem controller and connect it to membus
if options and options.mem_config:
    system.mem_ctrl = options.mem_config
else:
    system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# instantiate process that we will run
process = Process()
process.cmd = ['configs/tutorial/test/sieve']

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

