#!/usr/bin/env python
# coding: utf-8
# Template code by Cas Wognum, customized by Anthony Gitter

# # Ligand ADMET
# 
# The [ADMET](https://polarishub.io/competitions/asap-discovery/antiviral-admet-2025) and [Potency](
# https://polarishub.io/competitions/asap-discovery/antiviral-potency-2025) Challenge of the [ASAP Discovery
# competition](https://polarishub.io/blog/antiviral-competition) take the shape of a property prediction task. Given
# the SMILES (or, to be more precise, the CXSMILES) of a molecule, you are asked to predict the numerical properties
# of said molecule. This is a relatively straight-forward application of ML and this notebook will quickly get you up
# and running!
# 
# This code only focuses on the ADMET challenge.

import datamol as dm
import numpy as np
import pandas as pd
import polaris as po
from sklearn.ensemble import GradientBoostingRegressor

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
# Next, we'll train a simple baseline model using scikit-learn. 

# Prepare the input data. We'll use Datamol to compute the ECFP fingerprints for both the train and test columns.
# Use fingerprint size of 500 instead of default 2048
# https://github.com/datamol-io/datamol/blob/0312388b956e2b4eeb72d791167cfdb873c7beab/datamol/fp.py#L56-L65
X_train = np.array([dm.to_fp(dm.to_mol(smi), fpSize=500) for smi in train.X])
X_test = np.array([dm.to_fp(dm.to_mol(smi), fpSize=500) for smi in test.X])

y_pred = {}

# For each of the targets...
for tgt in competition.target_cols:
    # We get the training targets
    # Note that we need to mask out NaNs since the multi-task matrix is sparse.
    y_true = train.y[tgt]
    mask = ~np.isnan(y_true)

    # We'll train a simple baseline model
    model = GradientBoostingRegressor()
    model.fit(X_train[mask], y_true[mask])

    # And then use that to predict the targets for the test set
    y_pred[tgt] = model.predict(X_test)

# Inspect the predictions
print(y_pred)

# Save the predictions to disk in addition to submitting them
y_pred_df = pd.DataFrame(y_pred)
y_pred_df.to_csv(OUT_FILE, sep='\t', index=False)

# ## Submit your predictions
# Submitting your predictions to the competition is simple.

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
