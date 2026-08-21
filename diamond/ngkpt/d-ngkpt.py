from abipy.abilab import GsrRobot
from abipy.tools.plotting import ConvergenceAnalyzer
import numpy as np
from matplotlib import pyplot as plt

robot = GsrRobot.from_dir('./abinit-out', walk=True)
df = df = robot.get_dataframe()
df['ngkpt'] = np.arange(4, 4+len(df)*2, 2)
ca = ConvergenceAnalyzer.from_dataframe(df, 'ngkpt', { 'energy': 1e-4 })

fig, (ax1, ax2) = plt.subplots(1, 2)
ca.plot(ax_mat=(ax1, ax2), show=False)
ax1.set_ylabel(r"$E_{\mathrm{tot}}$ (eV)")
ax2.set_ylabel(r"$\Delta E_{\mathrm{tot}}$ (eV)")
plt.show()