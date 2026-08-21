import abipy.data as abidata
from abipy.abilab import ElectronBandsPlotter, abiopen


ebplt = ElectronBandsPlotter()

with (
    abiopen('abinit-out/_SIGRES.nc')        as sig,
    abiopen('../bandstrc/abinit-out/_GSR.nc')   as gsrp,
    abiopen('../nscf-bands/abinit-out/_GSR.nc') as gsrm
):
    ebandsp = gsrp.ebands
    ebandsm = gsrm.ebands
    r = sig.interpolate(lpratio=5, ks_ebands_kpath=ebandsp, ks_ebands_kmesh=ebandsm)

    ebplt.add_ebands('PBE', ebandsp)
    ebplt.add_ebands('GW', r.qp_ebands_kpath)

ebplt.plotly()
ebplt.gridplotly(with_gaps=True)