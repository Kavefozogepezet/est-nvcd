from abipy.abilab import abiopen
from abipy.iotools.xsf import xsf_write_structure_and_data_to_path as xsf_write
import numpy as np
import sys

ground_state = [ # (band, spin)
    (125, 0), # a_1 up
    (125, 1), # a_1 down
    (126, 0), # e_x/y up
    (127, 0), # e_x/y up
]

with abiopen('abinit-out/_WFK.nc') as wfk:
    ks = wfk.kpoints

    example = wfk.get_wave(0, 0, 0).ur2
    den = np.zeros_like(example)

    for band, spin in ground_state:
        for k in ks:
            wave = wfk.get_wave(spin, k, band)
            den_k = wave.ur2
            den += den_k * k.weight

    xsf_write('abinit-out/DEN.xsf', wfk.structure, den)
