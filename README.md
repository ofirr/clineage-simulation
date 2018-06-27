# clineage-simulation

## Prerequisites

- CLineage
- Python 3+
- MATLAB 2017
- [eSTGt](https://github.com/hisplan/eSTGt) 1.1
- [TreeCmp](https://eti.pg.edu.pl/treecmp/index.html) v2.0
- TMC

## Installation

This will download and install TreeCmp and eSTGt:

```bash
$ ./install.sh
```

## Configuration

Use a proper config file for your environment:

- `config.math102-lx.env` for math102-lx
- `config.windows.env` for Windows
- `config.mac.env` for Mac OS X

or you can create a new `.env` file for your own environment.

## Run End-to-End

Using mcluster03/SGE:

```bash
$ ./run-tmc-all-sge.sh
```

## For Developers

### Updating Mutation Transition Table

- Update `om6_ms_only_ac_28x28.csv`.
- Update and run `prepare.m`.
- If the matrix size changes, there are some hardcoded number such as 28 in `run_simul.m` and `adjust_ms_mutation_transition_prob.m`.

### To Do

- maybe decouple from clineage to be runnable totally independently.
- maybe use MATLAB API for Python
