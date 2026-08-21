from abipy.abilab import SigresRobot
from abipy.tools.plotting import ConvergenceAnalyzer
from matplotlib import pyplot as plt

robot = SigresRobot.from_dir('abinit-out', walk=True)
df = robot.get_dataframe()
ca = ConvergenceAnalyzer.from_dataframe(df, 'nband', { 'qpgap': 1e-2 })

fig, (ax1, ax2) = plt.subplots(1, 2)
ca.plot(ax_mat=(ax1, ax2), show=False)
ax1.set_ylabel(r"$E_{\mathrm{gap}}$ (eV)")
ax2.set_ylabel(r"$\Delta E_{\mathrm{gap}}$ (eV)")
plt.show()