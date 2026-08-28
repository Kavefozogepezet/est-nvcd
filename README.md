# A DFT simulation of Nitrogen-vacancy centers in diamond

## Final project for Electronic Structure Theory

Bálint Apostagi, SoSe 2026

---------------------------------------------------------

### Repository structure

- **calculations**: all abinit stuff here
  - **diamond**: primitive cell of diamond
    - **ecut**, **ngkpt**: convergence for the respective variables
    - **geoopt**: geometry optimization
    - **scf-gs**: scf ground state calculation with all converged parameters 
    - **atomization**: reference energy for a carbon atom, atomization energy
    - **nscf-bands**: nscf calculation with many empty bands for screening
    - **bandstrc**: nscf calculation along a high-symmetry k-path
    - **scr\***: convergence for screening parameters, and the screening calculation itself
    - **gw\***: convergence for self-energy, and the self-energy calculation itself, application to the band structure
  - **diamond1**: cubic cell of diamond
  - **nvc\<i\>**: NV-center in an i^3 supercell
- **plotters**: scripts which plot the results from the calculations
- **docs**
  - **figures**: exported plots

---------------------------------------------------------

### ROADMAP

- simulation of a primitive cell of diamond
  - basic convergence tests: ✅
    - energy cutoff ✅
    - k point grid ✅
  - geometry optimization ✅
  - convergence tests for GW:
    - epsilon^-1
      - number of bands
      - energy cutoff
    - self-energy
      - number of bands
      - energy cutoff
  - band structure:
    - KS band structure
    - GW correction
- cubic cell of diamond
  - ground state
  - KS band structure 
- NV-center in a cubic cell of diamond
- NV center in 2x2x2 supercell

---------------------------------------------------------

### conventions used

- output files:
  - output data is saved to "./abinit-out/"
  - temporary data is saved to "./abinit-tmp/"
  - these files are ignored by git to ensure a lightweight repository
- pseudo potentials: 
  - the directory of pseudopotentials is given by the ABI_PPDIR environmental variable
  - the pseudopotentials are named "\<element\>.psp8" (for the example of carbon "C.psp8")
  - the atoms appearing in the simulation are listed in the .abi file

Simulations were carried out with Abinit 10.6.7
