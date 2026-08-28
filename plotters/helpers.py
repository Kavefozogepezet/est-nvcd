import os
from functools import wraps
import matplotlib.pyplot as plt

_CALC_DIR = os.environ['ESTNVCD_CALC_DIR']
_FIG_DIR = os.environ['ESTNVCD_FIG_DIR']

if _CALC_DIR == '': raise ValueError('Environmental variable ESTNVCD_CALC_DIR not set')
if _FIG_DIR == '': raise ValueError('Environmental variable ESTNVCD_FIG_DIR not set')

if not _CALC_DIR.endswith('/'): _CALC_DIR += '/'
if not _FIG_DIR.endswith('/'): _FIG_DIR += '/'

_CALC_PREFIX = []

_PLOTS = dict()

_EXT_PREF = '.svg'


def calcdir(address):
    prefix = ''.join(f'{it.name}/' for it in _CALC_PREFIX)
    match address.count('@'):
        case 0:
            return _CALC_DIR + prefix + address
        case 1:
            (filename, subdir) = address.split('@')
            if not subdir.endswith('/'): subdir += '/'
            return _CALC_DIR + prefix + subdir + 'abinit-out/' + filename
        case _:
            raise ValueError('Invalid address, format is: <path>[@<prefix>]')


def figdir(subpath):
    return _FIG_DIR + subpath


def calcenter(name):
    class _Prefix:
        def __init__(self, _name):
            self.name = _name

        def __enter__(self):
            _CALC_PREFIX.append(self)

        def __exit__(self, ex_type, ex_val, ex_tb):
            _CALC_PREFIX.remove(self)

    return _Prefix(name)


def plotfunc(*srcs, out='', name=None):
    srcdirs = [calcdir(src) for src in srcs]
    def _plotfunc(func):
        thename = name
        if thename == None:
            thename = func.__name__
        @wraps(func)
        def _call_func(save):
            outdir = figdir(out) if save else None
            func(outdir, *srcdirs)
        _PLOTS[thename] = _call_func
        return func
    return _plotfunc


def mplfig(fig=None, name='', outdir='./', tight_layout=True, *args, **kwargs):
    def _export_fig(_fig, _outdir, _path):
        if tight_layout:
            _fig.tight_layout()
            
        if not _outdir:
            plt.show()
        else: 
            if not _outdir.endswith('/'): _outdir += '/'
            _fig.savefig(_outdir + _path)

    def _mplfig(func):
        @wraps(func)
        def _call_func(_outdir, *_inpaths):
            _fig = plt.figure(*args, **kwargs)
            func(_fig, *_inpaths)
            _export_fig(_fig, _outdir, func.__name__ + _EXT_PREF)
        return _call_func
    
    if fig: _export_fig(fig, outdir, name + _EXT_PREF)
    else: return _mplfig


def runplot(name, save=False):
    altname = f'plot_{name}'
    if name in _PLOTS:
        _PLOTS[name](save)
    elif altname in _PLOTS:
        _PLOTS[altname](save)
    else:
        raise ValueError(f'No plot function found under names {name}, {altname}')
    

def runplots(save=False):
    for name in _PLOTS:
        print(f'========== {name} ==========')
        runplot(name, save)
