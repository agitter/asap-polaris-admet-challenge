#!/usr/bin/env python
# coding: utf-8
# Template code by Cas Wognum, customized by Anthony Gitter

# # Ligand ADMET
# 
# The [ADMET](https://polarishub.io/competitions/asap-discovery/antiviral-admet-2025) and [Potency](
# https://polarishub.io/competitions/asap-discovery/antiviral-potency-2025) Challenge of the [ASAP Discovery
# competition](https://polarishub.io/blog/antiviral-competition) take the shape of a property prediction task. Given
# the SMILES (or, to be more precise, the CXSMILES) of a molecule, you are asked to predict the numerical properties
# of said molecule.
# 
# This code only focuses on the ADMET challenge.

import datamol as dm
import numpy as np
import pandas as pd
import polaris as po
from tabpfn_client import TabPFNRegressor
from tabpfn_extensions.post_hoc_ensembles.sklearn_interface import AutoTabPFNRegressor

CHALLENGE = "antiviral-admet-2025"
OUT_FILE = CHALLENGE + '-pred.tsv'

# ## Load the competition data
# Let's first load the competition from Polaris.
# Make sure you are logged in! If not, simply run `polaris login` and follow the instructions. 
competition = po.load_competition(f"asap-discovery/{CHALLENGE}")

# As suggested in the logs, we'll cache the dataset. Note that this is not strictly necessary, but it does speed up
# later steps.
competition.cache()
train, test = competition.get_train_test_split()

# ## Build a model

# Prepare the input data. We'll use Datamol to compute the ECFP fingerprints for both the train and test columns. Use
# fingerprint size of 500 instead of default 2048
# https://github.com/datamol-io/datamol/blob/0312388b956e2b4eeb72d791167cfdb873c7beab/datamol/fp.py#L56-L65
# 500 is selected based on the TabPFN manuscript (https://doi.org/10.1038/s41586-024-08328-6):
# "This new supervised tabular learning method can be applied to any small- to moderate-sized dataset and yields
# dominant performance for datasets with up to 10,000 samples and 500 features."
X_train = np.array([dm.to_fp(dm.to_mol(smi), fpSize=500) for smi in train.X])
X_test = np.array([dm.to_fp(dm.to_mol(smi), fpSize=500) for smi in test.X])

y_pred = {}

# For each of the targets... (TabPFN supports single-task modeling)
for tgt in competition.target_cols:
    # We get the training targets
    # Note that we need to mask out NaNs since the multi-task matrix is sparse.
    y_true = train.y[tgt]
    mask = ~np.isnan(y_true)

    # Train the TabPFN regression model
    # AutoTabPFNRegressor fails in the demo code phe_example.py
    # https://github.com/PriorLabs/tabpfn-extensions/issues/38
    # Train a single TabPFNRegressor until this is resolved
    # model = AutoTabPFNRegressor(max_time=60 * 3)
    # Use default args (see
    # https://github.com/PriorLabs/TabPFN/blob/05ab7da2df93104e071e62cea0d1fffd78883716/src/tabpfn/regressor.py#L173)
    model = TabPFNRegressor()
    model.fit(X_train[mask], y_true[mask])

    # And then use that to predict the targets for the test set
    y_pred[tgt] = model.predict(X_test)

# Inspect the predictions
print(y_pred)

# Save the predictions to disk in addition to submitting them
y_pred_df = pd.DataFrame(y_pred)
y_pred_df.to_csv(OUT_FILE, sep='\t', index=False)

# Submit the predictions
# competition.submit_predictions(
#     predictions=y_pred,
#     prediction_name="tutorial-predictions",
#     prediction_owner="agitter",
#     report_url="https://github.com/agitter/asap-polaris-admet-challenge",
#     github_url="https://github.com/agitter/asap-polaris-admet-challenge",
#     description="Submission using the tutorial Jupyter notebook",
#     tags=["tutorial"],
#     user_attributes={"Framework": "Scikit-learn", "Method": "Gradient Boosting"}
# )
