from abipy.abilab import abiopen

with abiopen('abinit-out/_GSR.nc') as gsr:
    fermie = gsr.ebands.fermie
    energies = gsr.ebands.eigens[0,0,:]
    for ei, eval in enumerate(energies):
        print(f'E_{ei} = {eval - fermie} ({eval})')
