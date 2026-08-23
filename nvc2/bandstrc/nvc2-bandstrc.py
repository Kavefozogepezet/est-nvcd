import abipy.data as abidata
from abipy.abilab import ElectronBandsPlotter, abiopen

ebplt = ElectronBandsPlotter()

with (
    abiopen('abinit-out/_GSR.nc') as gsr
):
    bands = gsr.ebands
    ebplt.add_ebands('Cubic cell', gsr.ebands)

ebplt.plot(
    #ylims=(-10, 5),
    #linestyle_dict={
    #    'Primitive cell': {
    #        'linewidth': 1.5,
    #        'linestyle': 'dotted',
    #        'color': 'blue',
    #        'zorder': 2,
    #    },
    #    'Cubic cell': {
    #        'linewidth': 1.5,
    #        'linestyle': 'solid',
    #        'color': 'cornflowerblue',
    #        'zorder': 1
    #    }
    #}
)

