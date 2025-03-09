# ADMET prediction with TabPFN
Anthony Gitter  
Archived at https://doi.org/10.5281/zenodo.14993394

## Introduction
This submission is based on the intuition (speculation) that the ligand poses and potency subchallenges of the [antiviral competition](https://polarishub.io/blog/antiviral-competition) would benefit from chemical-specific modeling, and likely 3D structure modeling of the targets, but the ADMET subchallenge would not.
The [ADMET properties](https://polarishub.io/competitions/asap-discovery/antiviral-admet-2025) --- Mouse Liver Microsomal stability, Human Liver Microsomal stability, Solubility, LogD, Cell permeation --- are difficult to predict, and there is not a large quantity of high-quality public training data available for some of these properties.
Therefore, my strategy abandons domain-specific knowledge.
There will be no consideration of stereochemistry, pretrained multimodal models with [3D molecule representations](https://doi.org/10.1093/bioinformatics/btae260), or big ol' [graph neural networks](https://arxiv.org/abs/2404.11568).
I am closing my eyes and treating the problem as a black box tabular dataset.
A January 2025 paper presenting the [Tabular Prior-data Fitted Network (TabPFN)](https://doi.org/10.1038/s41586-024-08328-6) claims to have excellent performance on diverse tabular datasets, so this provides an opportunity to test the claim.
TabPFN is a pretrained tabular foundation model.
It uses in-context learning to adapt to a new dataset and make predictions on the test set.
It states:
> This new supervised tabular learning method can be applied to any small- to moderate-sized dataset and yields dominant performance for datasets with up to 10,000 samples and 500 features.

which is a perfect fit for the ADMET challenge.

## Methods
My approach featurizes molecules using ECFP6 fingerprints of size 500, which is the maximum number of features tested by TabPFN.
This is an atypical fingerprint length compared to the more common 2048 or 1024 but is better suited to the scope of TabPFN.
The training data is fit with a TabPFNRegressor using all default settings.
The model is run using the TabPFN API instead of the local model.
Each ADMET property is fit independently in a single-task manner.

## Results
To be determined after the competition closes.

## Discussion
Was ignoring the biochemical domain a good idea?
Maybe.
Maybe not.
That is the joy of open competitions.
We as a community can try things and see what works and what fails.
I like to use these competitions to explore ideas I would not use in my day-to-day research.
In the Adaptyv EGFR protein design competition [round 1](https://github.com/agitter/adaptyvbio-egfr?tab=readme-ov-file#round-1-submission) I used Llama 3.1 and [ProTrek](https://doi.org/10.1101/2024.05.30.596740) for some of my designs.
They failed.

TabPFN was easy to implement because it follows the scikit-learn API.
Installing the Python packages in a conda environment took much more time than actually updating the tutorial Jupyter notebook code to use the TabPFNRegressor instead of a GradientBoostingRegressor.
I was unable to get the TabPFN model ensembles to work property, however, which will likely hurt performance.

From a usability and commercialization perspective, TabPFN makes some interesting choices.
The code is Apache License 2.0 licensed, which is great.
The API is free to use up to a point.
There is a limit of 5000000 (table) cells per day, which is consumed quickly.
I was unable to train models for all the ADMET properties within the daily limit, which was a practical challenge that made the code more complicated than it needed to be.
I have not yet tried running the models locally or contacting the team to discuss increasing the default daily limit.

Polaris was excellent as a competition platform.
The tutorial Jupyter notebook was easy to adapt, and making submissions was seamless.
The organizers were responsive to my questions.
