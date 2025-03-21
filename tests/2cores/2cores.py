import m5
from m5.objects import *
from gem5.components.processors.cpu_types import CPUTypes

# 创建双核系统
system = System(
    cpu=CPUTypes.ATOMIC.create(
        num_cores=2,
        cpu_clk_domain=DerivedClockDomain(
            clk_domain=Parent.clk_domain,
            clk_divider=1
        )
    ),
    mem_mode="atomic",
    mem_ranges=[AddrRange("512MB")],
    cache_line_size=64,
)

system.workload = SEWorkload()
system.cpu_voltage_domain = VoltageDomain()
system.cpu_clk_domain = SrcClockDomain(
    clock="1GHz", voltage_domain=system.cpu_voltage_domain
)

system.membus = SystemXBar()
system.cpu.connectMemPorts(system.membus)
system.system_port = system.membus.cpu_side_ports

# 设置内存控制器
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.port = system.membus.mem_side_ports

# 设置进程和命令行参数
process = Process()
process.cmd = ["tests/2cores/2cores"]
system.cpu.workload = process
system.cpu.createThreads()

# 启动模拟
root = Root(full_system=False, system=system)
m5.instantiate()
m5.simulate()