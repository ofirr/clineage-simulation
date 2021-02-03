# clineage-simulation

## DREAM challenge subch3 - mouse simulation
Under examples/example-dream is an eSTG script simulating the third challenge for Allen Institute Cell Lineage Reconstruction DREAM Challenge
![alt text](https://github.com/ofirr/clineage-simulation/blob/DREAM/subc3.png?raw=true)

## eSTGt - A programming and simulation environment for population dynamics
eSTGt is a MATLAB tool that enables to execute stochastic simulations that generate lineage trees. The input programs of the tool are based on a language formalism called environmental dependent Stochastic Tree Grammars (eSTG) that is described in a [published paper](https://doi.org/10.1186/1471-2105-15-249). Briefly, the formalism extends the notion of Stochastic Tree Grammars (STG)2 by incorporating both rates and probabilities to the transition rules. These can be dynamically updated by defining them as functions of the system’s state, which includes global values such as current population size or elapsed time. In addition, we extend the system by allowing each individual to hold its own internal states, which can be inherited. The species fate can also be controlled through conditional transitions on the system’s state.

## Running using eSTGt GUI
See https://github.com/ofirr/mouse-estg

![alt text](https://github.com/ofirr/mouse-estg/blob/main/GUI.png?raw=true)

Note that this is a simplified version intended to run on regular PCs, one can typically simulate a 100 cell and 1 year of mouse development within hours.

## eSTGt CLI wrapper for HPC and advance usage
### Prerequisites

- CLineage
- Python 3+
- MATLAB 2017
- [eSTGt](https://github.com/shapirolab/eSTGt) 1.1

### Installation

This will download and install TreeCmp and eSTGt:

```bash
$ ./install.sh
```

### Configuration

Use a proper config file for your environment:

- `config.math102-lx.env` for math102-lx (challenge settings)
- `config.windows.env` for Windows
- `config.mac.env` for Mac OS X

or you can create a new `.env` file for your own environment.

### Run Simulator

```bash
$ python simulator.py \
    --env config.math102-lx.env \
    --project ~/clineage-simulation/example/example-01 \
    --config config.json
```

## For Developers

### Updating Mutation Transition Table

- Update `om6_ms_only_ac_28x28.csv`.
- Update and run `prepare.m`.
- If the matrix size changes, there are some hardcoded number such as 28 in `run_simul.m` and `adjust_ms_mutation_transition_prob.m`.