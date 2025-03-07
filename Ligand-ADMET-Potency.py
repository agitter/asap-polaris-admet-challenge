#!/usr/bin/env python
# coding: utf-8

# # Ligand ADMET and Potency (Property Prediction)
# 
# The [ADMET](https://polarishub.io/competitions/asap-discovery/antiviral-admet-2025) and [Potency](https://polarishub.io/competitions/asap-discovery/antiviral-potency-2025) Challenge of the [ASAP Discovery competition](https://polarishub.io/blog/antiviral-competition) take the shape of a property prediction task. Given the SMILES (or, to be more precise, the CXSMILES) of a molecule, you are asked to predict the numerical properties of said molecule. This is a relatively straight-forward application of ML and this notebook will quickly get you up and running!
# 
# To begin with, choose one of the two challenges! The code will look the same for both. 

# In[1]:


CHALLENGE = "antiviral-admet-2025"


# ## Load the competition
# 
# Let's first load the competition from Polaris.
# 
# Make sure you are logged in! If not, simply run `polaris login` and follow the instructions. 

# In[2]:


import polaris as po

competition = po.load_competition(f"asap-discovery/{CHALLENGE}")


# As suggested in the logs, we'll cache the dataset. Note that this is not strictly necessary, but it does speed up later steps.

# In[3]:


competition.cache()


# Let's get the train and test set and take a look at the data structure.

# In[4]:


train, test = competition.get_train_test_split()


# In[5]:


train[0]


# In[6]:


test[0]


# In[7]:


len(train)


# In[8]:


len(test)


# In[9]:


import datamol as dm


# In[11]:


# From manuscript: "This new supervised tabular learning method can be applied to any small- to moderate-sized dataset and yields dominant performance for datasets with up to 10,000 samples and 500 features."
mol = dm.to_mol(train[0][0])
mol


# In[12]:


fp = dm.to_fp(mol, fpSize=500)
fp


# ### Raw data dump
# We've decided to sacrifice the completeness of the scientific data to improve its ease of use. For those that are interested, you can also access the raw data dump that this dataset has been created from.

# In[9]:


import fsspec
import zipfile

with fsspec.open("https://fs.polarishub.io/2025-01-asap-discovery/raw_data_package.zip") as fd:
    with zipfile.ZipFile(fd, 'r') as zip_ref:
        zip_ref.extractall("./raw_data_package/")


# In[8]:


import pandas as pd
from pathlib import Path

subdir = "admet" if CHALLENGE == "antiviral-admet-2025" else "potency"

path = Path("./raw_data_package")
path = path / subdir

csv_files = list(path.glob("*.csv"))
pd.read_csv(csv_files[0]).head(3)


# ## Build a model
# Next, we'll train a simple baseline model using scikit-learn. 
# 
# You'll notice that the challenge has multiple targets.

# In[13]:


train.target_cols


# An interesting idea would be to build a multi-task model to leverage shared information across tasks.
# 
# For the sake of simplicity, however, we'll simply build a model per target here. 

# In[14]:


import numpy as np

from sklearn.ensemble import GradientBoostingRegressor

# Prepare the input data. We'll use Datamol to compute the ECFP fingerprints for both the train and test columns.
# Use fingerprint size of 500 instead of default 2048
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


# In[15]:


y_pred


# ## Submit your predictions
# Submitting your predictions to the competition is simple.

# In[13]:


competition.submit_predictions(
    predictions=y_pred,
    prediction_name="tutorial-predictions",
    prediction_owner="agitter",
    report_url="https://github.com/agitter/asap-polaris-admet-challenge", 
    github_url="https://github.com/agitter/asap-polaris-admet-challenge",
    description="Submission using the tutorial Jupyter notebook",
    tags=["tutorial"],
    user_attributes={"Framework": "Scikit-learn", "Method": "Gradient Boosting"}
)


# For the ASAP competition, we will only evaluate your latest submission. 
# 
# The results will only be disclosed after the competition ends.

# The End.
