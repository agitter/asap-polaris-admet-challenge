#!/usr/bin/env python
# coding: utf-8

# Load the stored ADMET predictions and submit to Polaris

import pandas as pd
import polaris as po

CHALLENGE = "antiviral-admet-2025"

# Hard code the properties to ensure all five are present
PROPERTIES = ["LogD", "HLM", "MDR1-MDCKII", "KSOL", "MLM"]
IN_PREFIX = "antiviral-admet-2025-"
IN_SUFFIX = "-pred.tsv"

y_pred = {}

# Iterate over all targets (ADMET properties)
for tgt in PROPERTIES:
    # Load the stored predictions for that target
    filename = IN_PREFIX + tgt + IN_SUFFIX
    df = pd.read_csv(filename, header=0)

    # Recreate the expected dict data structure mapping target to predictions
    y_pred[tgt] = df[tgt].to_numpy()

print(y_pred)

# Submit the aggregated predictions
# Load the competition from Polaris.
# Make sure you are logged in! If not, simply run `polaris login` and follow the instructions.
competition = po.load_competition(f"asap-discovery/{CHALLENGE}")
competition.submit_predictions(
    predictions=y_pred,
    prediction_name="TabPFNRegressor",
    prediction_owner="agitter",
    report_url="https://doi.org/10.5281/zenodo.14993394",
    github_url="https://github.com/agitter/asap-polaris-admet-challenge",
    description="The approach featurizes molecules using ECFP6 fingerprints of size 500, which is the maximum number"
                "of features tested by TabPFN. The training data is fit with a TabPFNRegressor, which is a pretrained"
                "tabular foundation model. It uses in-context learning to adapt to the ADMET dataset and make"
                "predictions on the test set. This is an entirely black box approach that treats the ADMET data as"
                "an arbitrary tabular dataset. Further details are in writeup.md in the GitHub repository, which is"
                "archived on Zenodo.",
    tags=["tabular foundation model", "single-task", "in-context-learning", "black box"],
    user_attributes={"Framework": "Tabular Prior-data Fitted Network (TabPFN)",
                     "Method": "TabPFNRegressor",
                     "Citation": "https://doi.org/10.1038/s41586-024-08328-6",
                     "Features": "ECFP6 fingerprints of size 500"}
)
