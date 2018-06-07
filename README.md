# clineage-simulation

## Prerequisites

- CLineage
- Python 3+
- MATLAB 2017
- eSTGt 1.1
- TreeCmp v2.0
- TMC

## Installation

### TreeCmp

This will download and install [TreeCmp](https://eti.pg.edu.pl/treecmp/index.html) v2.0 which is needed to obtain various metrics for tree comparison:

```bash
$ ./install.sh
```

### eSTGt

Download eSTGt:

```bash
$ git clone https://github.com/hisplan/eSTGt
```

Switch to `dev` branch:

```bash
$ git branch dev
```

## Configuration

Open `run.sh`, find the following lines, and make necessary changes:

```bash
path_matlab='/usr/wisdom/matlabR2017a/bin'
path_eSTGt='~/projects/eSTGt/eSTGt'
```

## Simulation

```bash
$ ./run.sh
```

This will generate:

- `mutation_table.txt`
- `simulation.newick`
- `simulation.png`

## Tree Reconstruction

```bash
$ python reconstruct.py
```

This will generate:

- `reconstructed.newick`
- `reconstructed.ascii_plot.txt`
- `sagis_triplets.log`
- `simulation.asicc_plot.txt`

## For Developers

### Updating Mutation Transition Table

Update and run `./src/prepare.m`.
