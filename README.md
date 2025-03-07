# asap-polaris-admet-challenge
The ADMET Challenge of the ASAP Discovery competition

## Setup
```
conda env create -f environment.yml
conda activate asap-admet
pip install git+https://github.com/PriorLabs/tabpfn-client.git
pip install "tabpfn-community[post_hoc_ensembles] @ git+https://github.com/PriorLabs/tabpfn-community.git"
pip install -U "tabpfn-community[post_hoc_ensembles] @ git+https://github.com/PriorLabs/tabpfn-community.git"
```
tabpfn-client was not available directly via `pip`, so it was installed from [GitHub](https://github.com/PriorLabs/tabpfn-client).
The command above installed tabpfn-client commit 4c591d703cd34f4c2fd8b893adfa07bf5b14b942.
The latest tabpfn-client PyPI release at the time was verison 0.1.4.
It installed tabpfn-community commit 366df608c79e2b8375cdd3cf5c5b3672448fcffb.
The latest tabpfn-community PyPI release at the time was verison 2.0.5.
Second time installing with -U
Resolved https://github.com/PriorLabs/tabpfn-community.git to commit 3d04dd51bbe2d3d368512c4a6f5d468d37aa9f71
The latest tabpfn-community PyPI release at the time was verison 2.0.6.
This Stack Overflow [post](https://stackoverflow.com/a/76620421) gives the pip syntax for installing optional dependencies from GitHub.

The output of `conda list` is stored is `conda-list.txt`.

Temp package notes, add to env later:  
Install missing packages:  
iprogress ipywidgets s3fs aiohttp

tabpfn-community
Successfully installed cloudpickle-3.1.1 filelock-3.17.0 future-1.0.0 hyperopt-0.2.7 kditransform-0.2.0 llvmlite-0.44.0 mpmath-1.3.0 numba-0.61.0 py4j-0.10.9.9 seaborn-0.12.2 sympy-1.13.1 tabpfn-community-0.0.4 torch-2.6.0

## Third-party files
- `Ligand-ADMET-Potency.ipynb` is derived from [`01. Ligand ADMET and Potency (Property Prediction).ipynb`](https://github.com/asapdiscovery/asap-polaris-blind-challenge-examples/blob/1952430cfed535ab13ab92eefa92487d908338ee/01.%20Ligand%20ADMET%20and%20Potency%20(Property%20Prediction).ipynb) by [Cas Wognum](https://github.com/cwognum).
- `phe_example.py` is test code from [PriorLabs/tabpfn-extensions](https://github.com/PriorLabs/tabpfn-extensions/blob/3d04dd51bbe2d3d368512c4a6f5d468d37aa9f71/examples/phe/phe_example.py).
