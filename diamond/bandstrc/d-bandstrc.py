import abipy.data as abidata
from abipy.abilab import ElectronBandsPlotter, abiopen

ebplt = ElectronBandsPlotter()

with abiopen('abinit-out/_GSR.nc') as gsr:
    bands = gsr.ebands

ebplt.add_ebands('PBE', bands)
ebplt.gridplotly(with_gaps=True)
