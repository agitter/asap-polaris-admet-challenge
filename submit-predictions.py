#!/usr/bin/env python
# coding: utf-8

# Load the stored ADMET predictions and submit to Polaris

import pandas as pd
import polaris as po

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
