Plotlines
=========

Create and display Story structure.

Use Case
--------

![Story board](./plotlines/test/data/spiki-demo_n51.svg)

Features
--------

Mode of use                             | CLI options               |   Progress        |   Status
----------------------------------------|---------------------------|-------------------|-------
Auto-generation of plot structures      | Omit `--i` option         |   Ongoing         | :x:
Convert Dunnart files to TOML format    | `--i design.svg -o .toml` |   Complete        | :ok:
Convert Inkscape files to TOML format   | `--i design.svg -o .toml` |   Complete        | :ok:
Load and plot a file in TOML format     | `--i design.toml`         |   Complete        | :ok:
Load and generate a Spiki template tree | `--i design.svg -o <dir>` |   Complete        | :ok:


Usage
-----

```
python3 -m plotlines.main --help
usage: python -m plotlines.main [-h] [--debug] [-i INPUT] [-o OUTPUT] [--ending ENDING] [--limit LIMIT] [--exits EXITS]

options:
  -h, --help            show this help message and exit
  --debug               Display debug information
  -i, --input INPUT     Specify an input file
  -o, --output OUTPUT   Specify an output file or directory
  --ending ENDING       Set the number of endings [4].
  --limit LIMIT         Limit the number of Nodes and Edges in the graph [100]
  --exits EXITS         Fix the number of exiting Edges from each Node [4]
```
