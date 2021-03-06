from m5.objects import Cache

# extend the BaseCache by setting parameters that do not have default values
class L1Cache(Cache):
    assoc = 1
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    def __init__(self, options=None):
        super(L1Cache, self).__init__()
        pass

    def connectCPU(self, cpu):
        raise "Error: This has not been implemented"

    def connectBus(self, bus):
        self.mem_side = bus.slave


# extend L1Cache to be i-cache and d-cache
class L1ICache(L1Cache):
    size = '16kB'

    def __init__(self, options=None):
        super(L1ICache, self).__init__(options)
        if options:
            if options.l1i_size:
                self.size = options.l1i_size
            if options.l1i_assoc:
                self.assoc = options.l1i_assoc

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port


class L1DCache(L1Cache):
    size = '64kB'

    def __init__(self, options=None):
        super(L1DCache, self).__init__(options)
        if options:
            if options.l1i_size:
                self.size = options.l1d_size
            if options.l1i_assoc:
                self.assoc = options.l1d_assoc

    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port


# creating L2 cache
class L2Cache(Cache):
    size = '256kB'
    assoc = 1
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    def __init__(self, options=None):
        super(L2Cache, self).__init__()
        if options:
            if options.l1i_size:
                self.size = options.l2_size
            if options.l1i_assoc:
                self.assoc = options.l2_assoc

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.master

    def connectMemSideBus(self, bus):
        self.mem_side = bus.slave


