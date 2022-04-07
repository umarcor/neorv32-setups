#!/usr/bin/env python3

from typing import Dict, List
from pathlib import Path
from os import environ
from pyEDAA.ProjectModel import Project, Design, FileSet, VHDLSourceFile, VerilogSourceFile


print(f"Current working directory: {Path.cwd()}")

project = Project("NEORV32")

Setups_Directory : Path = Path(".").resolve()
OSFlow_Directory : Path = Setups_Directory / 'osflow'
NEORV32_Directory : Path = Setups_Directory / 'neorv32'
NEORV32_RTLCoreDirectory : Path = NEORV32_Directory / 'rtl/core'


# Variants of the HDL sources for IMEM and DMEM
InstructionMemory : Dict[str, Path] = {
    "default": NEORV32_RTLCoreDirectory / "/mem/neorv32_imem.default.vhd",
    "ice40up_spram": OSFlow_Directory / "devices/ice40/neorv32_imem.ice40up_spram.vhd",
},
DataMemory : Dict[str, Path] ={
    "default": NEORV32_RTLCoreDirectory / "mem/neorv32_dmem.default.vhd",
    "ice40up_spram": OSFlow_Directory / "devices/ice40/neorv32_dmem.ice40up_spram.vhd",
}


def GetMemorySources(self, board : str, design : str) -> List[Path]:
    """
    Define which sources are used for Instruction and Data memories, depending on the target Board and/or Design
    """
    imem = "ice40up_spram"
    dmem = "ice40up_spram"

    if board == "Fomu":
        imem = "default" if design == "Minimal" else "ice40up_spram"

    elif board in ["OrangeCrab", "AlhambraII", "ULX3S"]:
        imem = "default"
        dmem = "default"

    return [InstructionMemory[imem], DataMemory[dmem]]




Fileset_Package = FileSet(
    'NEORV32:Package',
    directory=NEORV32_RTLCoreDirectory
)
Fileset_Package.AddFile(VHDLSourceFile('neorv32_package.vhd'))

Fileset_ApplicationImage = FileSet(
    'NEORV32:ApplicationImage',
    directory=NEORV32_RTLCoreDirectory
)
Fileset_ApplicationImage.AddFile(VHDLSourceFile('neorv32_application_image.vhd'))

Fileset_MemoryEntities = FileSet(
    'NEORV32:MemoryEntities',
    directory=NEORV32_RTLCoreDirectory
)
for vhdlFile in [
    'neorv32_dmem.entity.vhd',
    'neorv32_imem.entity.vhd'
]:
    Fileset_MemoryEntities.AddFile(VHDLSourceFile(vhdlFile))

Fileset_CoreSources = FileSet(
    'NEORV32:CoreSources',
    directory=NEORV32_RTLCoreDirectory
)
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
    Fileset_CoreSources.AddFile(VHDLSourceFile(vhdlFile))

Fileset_ICE40 = FileSet(
    'ICE40:Components',
    directory=OSFlow_Directory/'devices/ice40'
)
Fileset_ICE40.AddFile(VHDLSourceFile('sb_ice40_components.vhd'))

Fileset_ECP5 = FileSet(
    'ECP5:Components',
    directory=OSFlow_Directory/'devices/ecp5'
)
Fileset_ECP5.AddFile(VHDLSourceFile('ecp5_components.vhd'))


# Get the list of supported boards from the names of the '*.mk' files in 'setups/osflow/boards'
Boards = [
    str(item.stem)
    for item in (OSFlow_Directory / 'boards').glob("*")
    if item.stem != "index"
]
print(Boards)

Board_Revisions = {
    "Fomu": environ.get("FOMU_REV", "pvt"),
    "UPduino": environ.get("UPduino_REV", "v3"),
    "OrangeCrab": environ.get("OrangeCrab_REV", "r02-25F"),
}


class ProcessorDesign:
    def __init__(self, name: str, vhdl: List[Path], verilog: List[Path] = None):
        self.Name = name
        self.VHDL = vhdl
        self.Verilog = verilog


ProcessorTops = [
    ProcessorDesign(
        'Minimal',
        vhdl = [NEORV32_RTLCoreDirectory / "processor_templates/neorv32_ProcessorTop_Minimal*.vhd"]
    ),
    ProcessorDesign(
        'MinimalBoot',
        vhdl = [NEORV32_RTLCoreDirectory / "processor_templates/neorv32_ProcessorTop_MinimalBoot.vhd"]
    ),
    ProcessorDesign(
        'UP5KDemo',
        vhdl = [NEORV32_RTLCoreDirectory / "processor_templates/neorv32_ProcessorTop_UP5KDemo.vhd"]
    ),
    ProcessorDesign(
        'MixedLanguage',
        vhdl = [NEORV32_RTLCoreDirectory / "processor_templates/neorv32_ProcessorTop_Minimal*.vhd"],
        verilog = [
                OSFlow_Directory / "devices/ice40/sb_ice40_components.v",
                OSFlow_Directory / "board_tops/neorv32_Fomu_MixedLanguage_ClkGen.v",
        ]
    )
]


ExamplesList = [
        {
            "board": "UPduino",
            "design": "MinimalBoot",
            "bitstream": "neorv32_UPduino_v3_MinimalBoot.bit",
        },
        {
            "board": "UPduino",
            "design": "UP5KDemo",
            "bitstream": "neorv32_UPduino_v3_UP5KDemo.bit",
        },
        {
            "board": "Fomu",
            "design": "Minimal",
            "bitstream": "neorv32_Fomu_pvt_Minimal.bit",
        },
        {
            "board": "Fomu",
            "design": "MinimalBoot",
            "bitstream": "neorv32_Fomu_pvt_MinimalBoot.bit",
        },
        {
            "board": "Fomu",
            "design": "MixedLanguage",
            "bitstream": "neorv32_Fomu_pvt_MixedLanguage.bit",
        },
        {
            "board": "Fomu",
            "design": "UP5KDemo",
            "bitstream": "neorv32_Fomu_pvt_UP5KDemo.bit",
        },
        {
            "board": "iCESugar",
            "design": "Minimal",
            "bitstream": "neorv32_iCESugar_Minimal.bit",
        },
        {
            "board": "iCESugar",
            "design": "MinimalBoot",
            "bitstream": "neorv32_iCESugar_MinimalBoot.bit",
        },
        {
            "board": "OrangeCrab",
            "design": "MinimalBoot",
            "bitstream": "neorv32_OrangeCrab_r02-25F_MinimalBoot.bit",
        },
        {
            "board": "AlhambraII",
            "design": "MinimalBoot",
            "bitstream": "neorv32_AlhambraII_MinimalBoot.bit",
        },
        {
            "board": "ULX3S",
            "design": "MinimalBoot",
            "bitstream": "neorv32_ULX3S_MinimalBoot.bit",
        },
    ]


def GenerateExamplesJobMatrix():
    print(
        "::set-output name=matrix::"
        + str(ExamplesList)
    )




def Run(
    board: str,
    design: str,
    top: str,
    id: str,
    board_srcs: List[str],
    design_srcs: List[str],
    verilog_srcs: List[str],
    mem_srcs: List[str],
    posargs: List[str],
) -> List[str]:
    """
    Create command to call the make entrypoint 'setups/osflow/common.mk' for executing 'posargs' targets.
    """
    cmd = [
        "make",
        "-C",
        "setups/osflow",
        "-f",
        "common.mk",
        f"BOARD='{board}'",
        f"DESIGN='{design}'",
        "BOARD_SRC='{}'".format(" ".join(board_srcs)),
        f"TOP='{top}'",
        f"ID='{id}'",
        "DESIGN_SRC='{}'".format(" ".join(design_srcs)),
        "NEORV32_MEM_SRC='{}'".format(" ".join(mem_srcs)),
    ]

    if verilog_srcs is not None:
        cmd.append("NEORV32_VERILOG_SRC='{}'".format(" ".join(verilog_srcs)))

    cmd += posargs if posargs != [] else ["clean", "bit"]

    return cmd


def Example(board : str, design : str, posargs : str) -> str:
    """
    Call the 'Run' function to get the make command of a given example (Board and Design) for executing 'posargs' targets.
    """

    print(f'Gathering sources for design <{design}> on board <{board}>...')

    if board not in Boards:
        raise Exception(f"Unknown board {board}")

    DesignSources = next(
        (item for item in ProcessorTops if item.Name == design), None
    )

    if DesignSources == None:
        raise Exception(f"Unknown design {design}")

    boardtop = f"neorv32_{board}_BoardTop_{design}"

    if not (OSFlow_Directory / f"board_tops/{boardtop}.vhd").exists():
        raise Exception(f"BoardTop file {boardtop} does not exist!")

    # FIXME It should be possible to pass the command as a list, i.e., without converting it to a single string
    return Run(
        board=board,
        design=design,
        top=boardtop,
        id=design,
        board_srcs=[f"board_tops/{boardtop}.vhd"],
        design_srcs=DesignSources.VHDL,
        verilog_srcs=DesignSources.Verilog,
        mem_srcs=GetMemorySources(board, design),
        posargs=posargs,
    )





for item in ExamplesList:
    try:
        Example(item['board'], item['design'], item['bitstream'])
    except:
        pass




FileSet_Common : List[FileSet] = [
    Fileset_Package,
    Fileset_ApplicationImage,
    Fileset_MemoryEntities,
    Fileset_CoreSources,
]


#Fileset_CoreSources


Fomu_Minimal = Design("Fomu:Minimal", project=project)
Fomu_Minimal.AddFileSets([Fileset_ICE40] + FileSet_Common)

print(f"All VHDL files in {Fomu_Minimal.Name}:")
for file in Fomu_Minimal.Files(fileType=VHDLSourceFile):
	print(f"  {file.Path}")


#neorv32_Fomu_BoardTop_Minimal.vhd
#neorv32_Fomu_BoardTop_UP5KDemo.vhd
#neorv32_iCEBreaker_BoardTop_UP5KDemo.vhd
#neorv32_IceZumAlhambraII_BoardTop_MinimalBoot.vhd
#neorv32_UPDuino-v3.0_BoardTop_MinimalBoot.vhd
#neorv32_Fomu_BoardTop_MinimalBoot.vhd
#neorv32_Fomu_MixedLanguage_ClkGen.v
#neorv32_iCESugar-v1.5_BoardTop_Minimal.vhd
#neorv32_OrangeCrab_BoardTop_MinimalBoot.vhd
#neorv32_UPDuino-v3.0_BoardTop_UP5KDemo.vhd
#neorv32_Fomu_BoardTop_MixedLanguage.vhd
#neorv32_iCEBreaker_BoardTop_MinimalBoot.vhd
#neorv32_iCESugar-v1.5_BoardTop_MinimalBoot.vhd
#neorv32_ULX3S_BoardTop_MinimalBoot.vhd

