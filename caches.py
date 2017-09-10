from m5.objects import Cache

# extend the BaseCache by setting parameters that do not have default values
class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    def connectCPU(self, cpu):
        raise "Error: This has not been implemented"

    def connectBus(self, bus):
        self.mem_side = bus.slave


# extend L1Cache to be i-cache and d-cache
class L1ICache(L1Cache):
    size = '16kB'


class L1DCache(L1Cache):
    size = '64kB'


# creating L2 cache
class L2Cache(Cache):
    size = '256kB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12


