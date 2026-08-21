from abipy.abilab import abiopen

with abiopen('abinit-out/_GSR.nc') as gsr:
    fig = gsr.structure.plotly_bz(show=False)
    gsr.kpoints.plotly(fig=fig, show=False)

    path = gsr.structure.hsym_kpath
    print(path.kpath['kpoints'])
    print(path.kpath['path'])

fig.show()