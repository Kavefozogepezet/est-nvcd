from abipy.abilab import abiopen, ElectronBandsPlotter
from dataclasses import dataclass, field
import ase.io
import ase.neighborlist
import pyvista as pv
import numpy as np
from itertools import product

from helpers import *


with calcenter('nvc1'):
    @plotfunc('_GSR.nc@bands')
    def nvc1bands(outdir, gsrfile):
        ebplt = ElectronBandsPlotter()
        with abiopen(gsrfile) as gsr:
            ebplt.add_ebands('$NVC^- in 1\\times1\\times1$', gsr.ebands)

        fig = ebplt.plot(show=False)
        fig.set_size_inches(5,4)
        mplfig(
            fig=fig,
            name='nvc1bands',
            outdir=outdir
        )


class OrbitalPlotter:
    @dataclass
    class Config:
        selection_bounds: np.ndarray = field(default_factory=lambda:np.array([[0.1,0.9]]*3)*3.567*2)
        isosurfaces: list[float] = field(default_factory=lambda:[11.5])
        isosurface_color = 'cyan'
        isosurface_opacity = 0.9
        bond_thickness: float = 0.1
        bond_resolution: int = 6
        element_colors: dict[str,] = field(default_factory=lambda:{
            'C': (50, 50, 50),
            'N': 'blue',
        })
        element_radii: dict[str,] = field(default_factory=lambda:{
            'C': 0.15,
            'N': 0.2,   
        })
        bg_color = 'white'
        fading: tuple[float, float] = None
        camera_pos = None
        parallel_scale = 1

    def __init__(self, xsffile, config=Config()):
        self.conf = config
        self.atoms = ase.io.read(xsffile, format='xsf')
        self.atomsyms = np.array(self.atoms.get_chemical_symbols())
        with open(xsffile) as fileobj:
            self.data, _, _, _ = ase.io.xsf.read_xsf(fileobj, read_data=True)

        cutoffs = ase.neighborlist.natural_cutoffs(
            self.atoms,
            mult=1.10
        )
        bonds = i, j, _, shifts = ase.neighborlist.neighbor_list(
            "ijdS",
            self.atoms,
            cutoffs,
        )
        bonds = np.array([i, j]).T
        bondsel = np.logical_and(i > j, np.linalg.norm(shifts, axis=1) == 0)
        self.bonds = bonds[bondsel]

    def plot(self, plotter: pv.Plotter):
        self.plt = plotter
        self.plt.ren_win.SetAlphaBitPlanes(True)
        self.plt.ren_win.SetMultiSamples(0)
        self.plt.add_key_event('c', self._print_camera)
        self.plt.enable_depth_peeling(number_of_peels=10, occlusion_ratio=0)
        self.plt.enable_parallel_projection()
        self.plt.enable_anti_aliasing('ssaa')
        self.plt.background_color = self.conf.bg_color
        
        if self.conf.camera_pos:
            self.plt.camera_position = self.conf.camera_pos
        self.plt.camera.parallel_scale = self.conf.parallel_scale
        
        self._select()
        self._calc_grad()
        self._plot_atoms()
        self._plot_bonds()
        self._plot_isosurfaces()

    def _plot_isosurfaces(self):
        cell = self.atoms.get_cell()
        grid = pv.ImageData()
        grid.dimensions = np.array(self.data.shape)
        grid.spacing = [
            np.linalg.norm(celli) / shapei
            for celli, shapei in zip(cell, self.data.shape)
        ]
        grid.point_data['value'] = self.data.flatten('F')

        isosurface = grid.contour(self.conf.isosurfaces, 'value')
        self.plt.add_mesh(
            isosurface,
            color=self.conf.isosurface_color,
            opacity=self.conf.isosurface_opacity,
            smooth_shading=True,
            show_edges=False,
            backface_culling=True
        )

    def _select(self):
        pos = self.atoms.positions
        bounds = self.conf.selection_bounds
        sel = np.all(np.logical_and(pos <= bounds[:,1], pos >= bounds[:,0]), axis=1)
        self.bondsel = np.logical_and(sel[self.bonds[:,0]], sel[self.bonds[:,1]])
        atomidx = np.unique(self.bonds[self.bondsel].ravel())
        self.sel = np.zeros(len(self.atoms), dtype=bool)
        self.sel[atomidx] = True

    def _plot_atoms(self):
        atoms = self.atoms.positions[self.sel]
        symbols = self.atomsyms[self.sel]
        for atom, sym in zip(atoms, symbols):
            color, ambient = self._get_color(sym, atom)
            self.plt.add_mesh(
                pv.Sphere(center=atom, radius=self.conf.element_radii.get(sym, 0.1)),
                color=color,
                ambient=ambient,
                diffuse=1-ambient,
                smooth_shading=True
            )

    def _plot_bonds(self):
        for idx in self.bonds[self.bondsel]:
            p1, p2 = self.atoms.positions[idx]
            s1, s2 = self.atomsyms[idx]

            if s1 == s2:
                self._plot_bond(p1, p2, s1)
            else:
                pmid = (p1 + p2) / 2
                self._plot_bond(p1, pmid, s1)
                self._plot_bond(pmid, p2, s2)

    def _plot_bond(self, p1, p2, sym):
        color, ambient = self._get_color(sym, (p1 + p2)/2)
        self.plt.add_mesh(
            pv.Line(p1, p2).tube(
                radius=self.conf.bond_thickness/2,
                n_sides=self.conf.bond_resolution,
            ),
            color=color,
            ambient=ambient,
            diffuse=1-ambient,
            smooth_shading=True,
        )

    def _get_color(self, sym, pos):
        base = np.array(pv.Color(self.conf.element_colors.get(sym, 'pink')).float_rgb)
        if self.conf.fading:
            bg = np.array(pv.Color(self.conf.bg_color).float_rgb)
            ratio = np.clip(np.dot((pos - self.grad_start), self.grad_vec), 0, 1)
            return ratio*bg + (1-ratio)*base, ratio
        else:
            return base, 0


    def _calc_grad(self):
        if self.conf.fading:
            pmin, pmax = self.conf.fading
            vec = np.array(self.plt.camera.direction)
            adist = np.dot(self.atoms.positions[self.sel], vec)
            amin, amax = np.min(adist), np.max(adist)
            
            self.grad_start = vec * (amin*(1-pmin) + amax*(pmin))
            self.grad_vec = vec / (amax - amin) / (pmax - pmin)

    def _print_camera(self):
        print(f'camera_pos = {self.plt.camera_position}')
        print(f'parallel_scale = {self.plt.camera.parallel_scale}')


with calcenter('nvc2'):
    @plotfunc('_GSR.nc@bands')
    @mplfig(figsize=(5,4))
    def nvc2bands(fig, gsrfile):
        ax = fig.add_subplot(111)
        common = {'show': False, 'ax': ax, 'lw': 1.5}
        with abiopen(gsrfile) as gsr:
            ebands = gsr.ebands
            ebands.plot(band_range=(100,125), color='blue', **common)
            ebands.plot(band_range=(128,140), color='blue', label='diamond orbitals', **common)
            ebands.plot(band_range=(125,128), color='red', label='localized orbitals', with_band_index=True, **common)

        ax.set_ylim(-6,4)
        ax.legend()


    @plotfunc('@scf-gs')
    def nvc2orbitals(outdir, abidir):
        conf = OrbitalPlotter.Config()
        #conf.camera_pos = [
        #    (4.3295388388053775, 22.164167703283645, 7.0675032471873624),
        #    (3.572617292404175, 3.572617471218109, 3.572617471218109),
        #    (0.032340038098921095, -0.185921524288111, 0.9820322340647203)
        #]
        #conf.parallel_scale = 3.586782965321137
        conf.camera_pos = [
            (4.862082193718817, 19.829889978802544, -6.052948364035898),
            (3.9696930450237473, 3.6335409162639536, 3.709982317759845),
            (0.5680522561203183, 0.40168652731469695, 0.7183067367709116)
        ]
        conf.parallel_scale = 3.8205208422827424
        conf.isosurface_opacity = 1
        conf.fading = (0.2,2)

        for (_, _, files) in os.walk(abidir):
            for file in files:
                if file.startswith('DEN_') and file.endswith('.xsf'):
                    plotter = pv.Plotter(window_size=(500,500))
                    oplt = OrbitalPlotter(abidir + file, conf)
                    oplt.plot(plotter)
                    if not outdir:
                        plotter.show()
                    else:
                        name = file.split('.')[0]
                        plotter.save_graphic(outdir + f'nvc2orbitals_{name}.svg')
