# clineage-simulation

## Prerequisites

- CLineage
- Python 3+
- MATLAB 2017
- [eSTGt](https://github.com/hisplan/eSTGt) 1.1
- [TreeCmp](https://eti.pg.edu.pl/treecmp/index.html) v2.0
- TMC

## Installation

### TreeCmp

This will download and install TreeCmp and eSTGt:

```bash
$ ./install.sh
```

## Configuration

Open `run.sh`, find the following lines, and make necessary changes:

```bash
path_matlab='/usr/wisdom/matlabR2017a/bin'
path_eSTGt='~/projects/eSTGt/eSTGt'
```

## Run End-to-End

Use a proper config file for your environment:

- `config.math102-lx.env` for math102-lx
- `config.windows.env` for Windows
- `config.mac.env` for Mac OS X

```bash
$ python run_end_to_end.py --env config.math102-lx.env
```

## For Developers

### Updating Mutation Transition Table

Update and run `./src/prepare.m`.

### To Do

- maybe decouple from clineage to be runnable totally independently.
