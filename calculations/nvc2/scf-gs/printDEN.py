from abipy.abilab import abiopen
import os
import sys

bands = [int(i) for i in sys.argv[1:]]

with abiopen('abinit-out/_WFK.nc') as wfk:
    for band in bands:
        wfk.export_ur2(
            f'abinit-out/DEN_{band}.xsf',
            spin=0,
            kpoint=0,
            band=band,
        )
