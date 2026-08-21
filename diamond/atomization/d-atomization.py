from abipy.abilab import GsrRobot
from abipy.tools.plotting import ConvergenceAnalyzer
from matplotlib import pyplot as plt
import numpy as np

robot = GsrRobot.from_dir('abinit-out', walk=True)
df = df = robot.get_dataframe()
df['acell'] = np.arange(14, 23, 2)
ca = ConvergenceAnalyzer.from_dataframe(df, 'acell', { 'energy': 1e-4 })

fig, (ax1, ax2) = plt.subplots(1, 2)
ca.plot(ax_mat=(ax1, ax2), show=False)
ax1.set_ylabel(r"$E_{\mathrm{tot}}$ (eV)")
ax2.set_ylabel(r"$\Delta E_{\mathrm{tot}}$ (eV)")
ax1.set_xlabel(r"cell size (Bohr)")
ax2.set_xlabel(r"cell size (Bohr)")
plt.show()