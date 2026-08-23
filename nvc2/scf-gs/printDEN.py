from abipy.abilab import abiopen

with abiopen('abinit-out/_WFK.nc') as wfk:
    wfk.visualize_ur2(
        spin=0,
        kpoint=0,
        band=125,
        appname="vesta",
    )