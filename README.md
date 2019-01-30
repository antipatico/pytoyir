# pytoyir
This project is an example of an Information Retrieval System, in Python3.

## Dependencies
* python3
* python3-pip
* libenchant1c2a
### Used libraries
* Whoosh
* pyenchant
* docopt

## Installation
To install the system you have to install the dependencies and the run the
setup script `./setup.sh`.

**NOTE**: this will install **virtualenv** in your pip3 environment.

`setup.sh` will run the scripts contained in the `scripts` folder, in the right
order and with the needed option for a correct installation.

In alternative, it is possible to setup the system manually:
1. Install `virtualenv` using `pip`
2. Create a virtualenv (`venv`) and activate it
3. Install the required libraries using `pip` (look at `requirements.txt`)
4. Split the datasets' documents
5. Index the documents
6. Prepare benchmark data

## ./pytoyir.py -h
```
A Python3 toy Information Retrieval system (using whoosh and pyenchant).

Usage:
  pytoyir.py -h | --help
  pytoyir.py --version
  pytoyir.py benchmark (npl|lisa) [--recall=<RECALL>|--interpolated] [--bm25f|--tf-idf|--freq]
  pytoyir.py search (npl|lisa) [-L=<max>] [-s] [-w] [-B] [--bm25f|--tf-idf|--freq] <query>
  pytoyir.py index (npl|lisa) [--delete]

Options:
  -h --help             Show this help screen.
  --version             Show version.
  -s --no-spell-check   Disable spell checking.
  -w --no-wildcard      Disable wildcard queries.
  -B --batch            Run in batch mode.
  -L --limit=<max>      Maximum number of results shown [Default: 10].
                        Use None for no limits.
  -R --recall=<RECALL>  Set a goal recall, then calculates the average
                        precision at the given recall level for all the queries.
                        If 'all', print the average precision for all the
                        standard recall levels.
  --interpolated        Calculates the interpolated average precision for each
                        query in the benchmark data.

Scoring Models:
  --bm25f               Use the BM25F probabilistic model
  --tf-idf              Use the TF-IDF model
  --freq                Use the Frequency model

Wildcard queries and spellchecking are enabled by default.
The default scoring model for the search if none is specified is BM25F.
Benchmarking is always in batch mode.
```

## Usage
Enter the venv using `source venv/bin/activate`. To exit the venv use
`deactivate`. Now you can run the program using `./pytoyir.py`

## Additional documentation
You can find a simplistic presentation of the project in `Presentazione.odp`,
note it is in **italian**.

The file `Benchmark_data.txt` contains some benchmark results.


## Used datasets
We used **LISA** and **NPL** from the **Text REtrieval Conference**.

## License
MIT License, read the file `LICENSE`.

## Authors
[Jacopo Scannella](https://github.com/antipatico)
[Alessio Lei](https://github.com/AlessioLei94)

2019

