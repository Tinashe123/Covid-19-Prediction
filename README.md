Covid-19 Prediction
==============================
## Description
The scope of the project is to identify  publicly available covid-19 models in literature and identify gaps for improvement. Models that do not fit the SA scope will be modified and evaluated based on SA data. Performance evaluation prior to vaccinations and after will be conducted to determine vaccination impact and also see if the models can capture reported excess mortality deaths. The developed models will be evaluated if they are capable of predicting excess mortality rates. We should be able to evaluate the effect of vaccine rollout on the number of confirmed cases and deaths recorded.

# About the Dataset
There are 6 datasets used in this study:
1. covid19za_provincial_cumulative_timeline_confirmed
2. covid19za_provincial_cumulative_timeline_deaths
3. covid19za_provincial_cumulative_timeline_recoveries
4. covid19za_provincial_cumulative_timeline_vaccination
5. covid19za_timeline_testing
6. nicd_hospital_surveillance_data

To predict new cases, we only focus on 'cases_new' column. There are few missing data and symbol found and data cleaning process were applied. The datasets are based on cumulative data and we have preprocessed the data to reflect daily data as an additional column.

# SIR Model
SIR models provide a theoretical framework for the time rates of change of three populations in an outbreak of a contageous disease.
The populations in the model are given the shorthand 
- $S$ for the number of people in the population that are suscptable to getting infected
- $I$ for the number of people that are infected
- $R$ for the people that are recovered from the disease (an are therefore imune, possibly only temporarily).

The three populations exchange members as time goes on as shown in the diagram below. For example, suscepable people become infected. The following directed graph shows the exchanges in the model with $a,~b,~c,$ and $\alpha$ as arbitary numbers. 

- $a$ is called **transmissability**
- $b$ is called **recovery rate**
- $c$ is called **deimunization rate**
- $\alpha$ is called **vaccination rate**


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
