from pathlib import Path
from pyEDAA.ProjectModel import Project, Design, FileSet, VHDLSourceFile

print(f"Current working directory: {Path.cwd()}")
project = Project("NEORV32")

Setups_Directory = Path(".").resolve().parent
OSFlow_Directory = Setups_Directory / 'osflow'
NEORV32_Directory = Setups_Directory / 'neorv32'
NEORV32_RTLCoreDirectory = NEORV32_Directory / 'rtl/core'

Fileset_NEORV32_Package = FileSet('NEORV32:Package')
Fileset_NEORV32_Package.AddFile(VHDLSourceFile(NEORV32_RTLCoreDirectory/'neorv32_package.vhd'))

Fileset_NEORV32_ApplicationImage = FileSet('NEORV32:ApplicationImage')
Fileset_NEORV32_ApplicationImage.AddFile(VHDLSourceFile(NEORV32_RTLCoreDirectory/'neorv32_application_image.vhd'))

Fileset_NEORV32_MemoryEntities = FileSet('NEORV32:MemoryEntities')
for vhdlFile in [
    'neorv32_dmem.entity.vhd',
    'neorv32_imem.entity.vhd'
]:
    Fileset_NEORV32_ApplicationImage.AddFile(VHDLSourceFile(NEORV32_RTLCoreDirectory/vhdlFile))

Fileset_NEORV32_CoreSources = FileSet('NEORV32:CoreSources')
for vhdlFile in [
    'neorv32_bootloader_image.vhd',
    'neorv32_boot_rom.vhd',
    'neorv32_bus_keeper.vhd',
    'neorv32_busswitch.vhd',
    'neorv32_cfs.vhd',
    'neorv32_cpu.vhd',
    'neorv32_cpu_alu.vhd',
    'neorv32_cpu_bus.vhd',
    'neorv32_cpu_control.vhd',
    'neorv32_cpu_cp_bitmanip.vhd',
    'neorv32_cpu_cp_fpu.vhd',
    'neorv32_cpu_cp_muldiv.vhd',
    'neorv32_cpu_cp_shifter.vhd',
    'neorv32_cpu_decompressor.vhd',
    'neorv32_cpu_regfile.vhd',
    'neorv32_debug_dm.vhd',
    'neorv32_debug_dtm.vhd',
    'neorv32_fifo.vhd',
    'neorv32_gpio.vhd',
    'neorv32_gptmr.vhd',
    'neorv32_icache.vhd',
    'neorv32_mtime.vhd',
    'neorv32_neoled.vhd',
    'neorv32_pwm.vhd',
    'neorv32_slink.vhd',
    'neorv32_spi.vhd',
    'neorv32_sysinfo.vhd',
    'neorv32_top.vhd',
    'neorv32_trng.vhd',
    'neorv32_twi.vhd',
    'neorv32_uart.vhd',
    'neorv32_wdt.vhd',
    'neorv32_wishbone.vhd',
    'neorv32_xirq.vhd',
]:
    Fileset_NEORV32_CoreSources.AddFile(VHDLSourceFile(NEORV32_RTLCoreDirectory/vhdlFile))

Fileset_NEORV32_ICE40 = FileSet('ICE40:Components')
Fileset_NEORV32_ICE40.AddFile(VHDLSourceFile(OSFlow_Directory/'devices/ice40/sb_ice40_components.vhd'))

Fileset_NEORV32_ECP5 = FileSet('ECP5:Components')
Fileset_NEORV32_ECP5.AddFile(VHDLSourceFile(OSFlow_Directory/'devices/ecp5/ecp5_components.vhd'))
