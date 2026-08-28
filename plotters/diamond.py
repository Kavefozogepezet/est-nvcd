from abipy.abilab import GsrRobot, SigresRobot, abiopen, ElectronBandsPlotter
from abipy.tools.plotting import ConvergenceAnalyzer
from matplotlib import pyplot as plt
import numpy as np

from helpers import *


E_CONV_CRIT = { 'energy': 1e-4 }
SELFE_CONV_CRIT = { 'qpgap': 1e-2 }

E_TOT = r'E_\mathrm{tot}'
E_QP_GAP = r'E^\mathrm{(qp)}_\mathrm{gap}'


def plot_conv(fig, df, param, tols, param_name, param_unit='eV'):
    print(df[[param, *tols.keys()]])
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    
    ca = ConvergenceAnalyzer.from_dataframe(df, param, tols)
    ca.plot(ax_mat=(ax1, ax2), show=False)

    ax1.set_ylabel(f"${param_name}$ ({param_unit})")
    ax2.set_ylabel(f"$\\Delta {param_name}$ ({param_unit})")

    return ax1, ax2


with calcenter('diamond'):
    @plotfunc('@ecut')
    @mplfig(figsize=(8,4))
    def ecut(fig, indir):
        df = GsrRobot.from_dir(indir, walk=True).get_dataframe()
        plot_conv(fig, df, 'ecut', E_CONV_CRIT, E_TOT)


    @plotfunc('@ngkpt')
    @mplfig(figsize=(8,4))
    def ngkpt(fig, indir):
        df = GsrRobot.from_dir(indir, walk=True).get_dataframe()
        df['ngkpt'] = np.arange(6, 6+len(df)*2, 2)
        plot_conv(fig, df, 'ngkpt', E_CONV_CRIT, E_TOT)


    @plotfunc('@scr-ecut')
    @mplfig(figsize=(8,4))
    def screcut(fig, indir):
        df = SigresRobot.from_dir(indir, walk=True).get_dataframe()
        df['ecuteps'] = np.arange(4, 21, 4)
        plot_conv(fig, df, 'ecuteps', SELFE_CONV_CRIT, E_QP_GAP)


    @plotfunc('@scr-nbands')
    @mplfig(figsize=(8,4))
    def scrnbands(fig, indir):
        df = SigresRobot.from_dir(indir, walk=True).get_dataframe()
        plot_conv(fig, df, 'scr_nband', SELFE_CONV_CRIT, E_QP_GAP)


    @plotfunc('@gw-ecut')
    @mplfig(figsize=(8,4))
    def gwecut(fig, indir):
        df = SigresRobot.from_dir(indir, walk=True).get_dataframe()
        plot_conv(fig, df, 'ecutsigx', SELFE_CONV_CRIT, E_QP_GAP)


    @plotfunc('@gw-nbands')
    @mplfig(figsize=(8,4))
    def gwnbands(fig, indir):
        df = SigresRobot.from_dir(indir, walk=True).get_dataframe()
        plot_conv(fig, df, 'nband', SELFE_CONV_CRIT, E_QP_GAP)


    @plotfunc('@atomization')
    @mplfig(figsize=(8,4))
    def atomization(fig, indir):
        df = GsrRobot.from_dir(indir, walk=True).get_dataframe()
        df['acell'] = np.arange(14, 23, 2)
        ax1, ax2 = plot_conv(fig, df, 'acell', E_CONV_CRIT, E_TOT)
        ax1.set_xlabel('cell size (Bohr)')
        ax2.set_xlabel('cell size (Bohr)')


    @plotfunc('_GSR.nc@scf-gs')
    @mplfig(figsize=(4,4), layout='constrained')
    def dbz(fig, gsrfile):
        ax = fig.add_subplot(111, projection="3d")

        with abiopen(gsrfile) as gsr:
            gsr.structure.plot_bz(ax=ax, show=False)

            rkpt = gsr.kpoints.frac_coords
            xkpt = gsr.structure.lattice.get_cartesian_coords(rkpt)

            ax.scatter(*(xkpt.T), color='orange')

        ax.set_proj_type('ortho')
        ax.view_init(elev=35, azim=95, roll=145)
        ax.set_box_aspect((1,1,1), zoom=0.8)

    @plotfunc('_SIGRES.nc@gw', '_GSR.nc@bands', '_GSR.nc@nscf-bands')
    def dbands(outdir, sigfile, gsrpfile, gsrmfile):
        ebplt = ElectronBandsPlotter()

        with (
            abiopen(sigfile)  as sig,
            abiopen(gsrpfile) as gsrp,
            abiopen(gsrmfile) as gsrm
        ):
            ebandsp = gsrp.ebands
            ebandsm = gsrm.ebands
            r = sig.interpolate(lpratio=5, ks_ebands_kpath=ebandsp, ks_ebands_kmesh=ebandsm)

            ebplt.add_ebands('PBE', ebandsp)
            ebplt.add_ebands('GW', r.qp_ebands_kpath)

        fig = ebplt.plot(show=False)
        fig.set_size_inches(5,4)
        mplfig(
            fig=fig,
            name='dbands-combined',
            outdir=outdir
        )
        fig = ebplt.gridplot(with_gaps=True, show=False)
        fig.set_size_inches(10,4)
        mplfig(
            fig=fig,
            name='dbands-separate',
            outdir=outdir
        )


@plotfunc('_GSR.nc@diamond/bands', '_GSR.nc@diamond1/bands')
def d1bands(outdir, gsrpfile, gsrfile):
    ebplt = ElectronBandsPlotter()

    with(
        abiopen(gsrpfile) as gsrp,
        abiopen(gsrfile) as gsr
    ):
        ebplt.add_ebands('Primitive cell', gsrp.ebands)
        ebplt.add_ebands('Cubic cell', gsr.ebands)

    fig = ebplt.plot(
        show=False,
        ylims=(-22, 3),
        linestyle_dict={
            'Primitive cell': {
                'linewidth': 2,
                'linestyle': 'dotted',
                'color': 'blue',
                'zorder': 2,
            },
            'Cubic cell': {
                'linewidth': 1.5,
                'linestyle': 'solid',
                'color': 'cornflowerblue',
                'zorder': 1
            }
        }
    )
    fig.set_size_inches(5,4)
    mplfig(
        fig=fig,
        name='d1bands',
        outdir=outdir
    )
