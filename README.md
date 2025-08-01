# ADMET Challenge of the ASAP Discovery competition
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14993394.svg)](https://doi.org/10.5281/zenodo.14993394)

## Setup
```
conda env create -f environment.yml
conda activate asap-admet
pip install "tabpfn-extensions[post_hoc_ensembles] @ git+https://github.com/PriorLabs/tabpfn-extensions.git"
```
The last command installed `tabpfn-extensions` commit 3d04dd51bbe2d3d368512c4a6f5d468d37aa9f71 and additional dependencies from pip:
```commandline
Successfully installed MarkupSafe-3.0.2 cloudpickle-3.1.1 filelock-3.17.0 future-1.0.0 hyperopt-0.2.7 jinja2-3.1.6 kditransform-0.2.0 llvmlite-0.44.0 mpmath-1.3.0 numba-0.61.0 numpy-2.1.3 nvidia-cublas-cu12-12.4.5.8 nvidia-cuda-cupti-cu12-12.4.127 nvidia-cuda-nvrtc-cu12-12.4.127 nvidia-cuda-runtime-cu12-12.4.127 nvidia-cudnn-cu12-9.1.0.70 nvidia-cufft-cu12-11.2.1.3 nvidia-curand-cu12-10.3.5.147 nvidia-cusolver-cu12-11.6.1.9 nvidia-cusparse-cu12-12.3.1.170 nvidia-cusparselt-cu12-0.6.2 nvidia-nccl-cu12-2.21.5 nvidia-nvjitlink-cu12-12.4.127 nvidia-nvtx-cu12-12.4.127 py4j-0.10.9.9 seaborn-0.12.2 sympy-1.13.1 tabpfn-extensions-0.0.4 torch-2.6.0 triton-3.2.0
```
This Stack Overflow [post](https://stackoverflow.com/a/76620421) gives the pip syntax for installing optional dependencies from GitHub.

The output of `conda list` is stored is `conda-list.txt`.

## Usage
```commandline
python ligand-admet-potency-single.py LogD
```
Repeat for all five ADMET properties: "LogD", "HLM", "MDR1-MDCKII", "KSOL", "MLM".
This has be spread across multiple days to stay under the TabPFN API limits.
Three properties can be run per day.

```commandline
python submit-predictions.py
```
To submit the stored predictions for all five ADMET properties.

## Source files
- `ligand-admet-potency-single.py`: Trains TabPFNRegressor on a single ADMET property specified on the command line and writes the results to disk. Does not submit.
- `ligand-admet-potency.py`: Trains TabPFNRegressor on all ADMET properties and submits. However, this hits the API limit so it cannot be run successfully. Not used for the competition.
- `submit-predictions.py`: Submits the five property predictions from the five `ligand-admet-potency-single.py` runs.

## Third-party files
- `Ligand-ADMET-Potency.ipynb`, `ligand-admet-potency.py`, and `ligand-admet-potency-single.py` are derived from [`01. Ligand ADMET and Potency (Property Prediction).ipynb`](https://github.com/asapdiscovery/asap-polaris-blind-challenge-examples/blob/1952430cfed535ab13ab92eefa92487d908338ee/01.%20Ligand%20ADMET%20and%20Potency%20(Property%20Prediction).ipynb) by [Cas Wognum](https://github.com/cwognum).
- `phe_example.py` is test code from [PriorLabs/tabpfn-extensions](https://github.com/PriorLabs/tabpfn-extensions/blob/3d04dd51bbe2d3d368512c4a6f5d468d37aa9f71/examples/phe/phe_example.py). Available under the Apache License 2.0.

```commandline
$ jupyter nbconvert --to python Ligand-ADMET-Potency.ipynb
```
was run to obtain `ligand-admet-potency.py` (the file was renamed to lowercase).

## Citation
```
@article{gitter_asap_2025,
	title = {{ASAP} {Discovery} x {OpenADMET} {Challenge} with the {Tabular} {Prior}-{Data} {Fitted} {Network}},
	url = {https://github.com/agitter/asap-polaris-admet-challenge},
	doi = {10.5281/zenodo.14993394},
	journal = {Zenodo},
	author = {Gitter, Anthony},
	month = mar,
	year = {2025},
}
```

See the challenge [preprint](https://doi.org/10.26434/chemrxiv-2025-zd9mr) for more information about the dataset and evaluation.
