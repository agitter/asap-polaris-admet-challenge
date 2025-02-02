# asap-polaris-admet-challenge
The ADMET Challenge of the ASAP Discovery competition

## Setup
```
conda env create -f environment.yml
conda activate asap-admet
pip install git+https://github.com/PriorLabs/tabpfn-client.git
```
tabpfn-client was not available directly via `pip`, so it was installed from [GitHub](https://github.com/PriorLabs/tabpfn-client).
The command above installed tabpfn-client commit 4c591d703cd34f4c2fd8b893adfa07bf5b14b942.
The latest tabpfn-client PyPI release at the time was verison 0.1.4.
The output of `conda list` is stored is `conda-list.txt`.

## Third-party files
`Ligand-ADMET-Potency.ipynb` is derived from [`01. Ligand ADMET and Potency (Property Prediction).ipynb`](https://github.com/asapdiscovery/asap-polaris-blind-challenge-examples/blob/1952430cfed535ab13ab92eefa92487d908338ee/01.%20Ligand%20ADMET%20and%20Potency%20(Property%20Prediction).ipynb) by [Cas Wognum](https://github.com/cwognum).
