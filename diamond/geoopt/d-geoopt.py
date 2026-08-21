import abipy.data as abidata
from abipy.abilab import abiopen
from matplotlib import pyplot as plt


wfk = abiopen('./abinit-out/_WFK.nc')
structure = wfk.structure
fig, (axpc, axbz) = plt.subplots(1, 2, subplot_kw={'projection': '3d'})
axbz.autoscale()
structure.plot(ax=axpc, show=False)
structure.plot_bz(axbz, show=False)
wfk.close()


plt.show()