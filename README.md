# Machine Learning - GYM Tracker  

<a target="_blank" href="https://datalumina.com/">
    <img src="https://img.shields.io/badge/Datalumina-Project%20Template-2856f7" alt="Datalumina Project" />
</a>

### Project Overview
This project aims to predict and count gym exercises based on accelerometer and gyroscope motion data collected from an Apple Watch Ultra. The project involves data preprocessing, feature engineering, model training, and evaluation to accurately identify and count repetitions of various exercises.

### Setup Instructions
To set up the project environment, ensure you have Conda installed. Create and activate the environment using the provided `environment.yml` file:
```bash
conda env create -f environment.yml
conda activate tracking-exercises
```
Duplicate the `.env.example` file to `.env` and configure your environment variables.

### Project Organization
The project is organized into the following directories:
- `data`: Contains raw, interim, and processed data.
- `reports`: Generated analysis and figures.
- `src`: Source code for data processing, feature engineering, model training, and visualization.

### Usage Instructions
To use the project, follow these steps:
1. Prepare the dataset: `python src/data/make_dataset.py`
2. Generate visualizations: `python src/visualization/visualize.py`
3. Build features: `python src/features/build_features.py`
4. Train models: `python src/models/train_model.py`
5. Run model inference: `python src/models/predict_model.py`


### Data Preparation
Load and preprocess the raw motion data from CSV files. Resample the data to a consistent frequency and save the processed data for further analysis:
```python
python src/data/make_dataset.py
```

### Visualization
Generate visualizations to explore and analyze the motion data, including plotting individual exercises, comparing sets, and visualizing feature transformations:
```python
python src/visualization/visualize.py
```

### Feature Engineering
Apply various feature engineering techniques, including low-pass filtering, PCA, temporal abstraction, and frequency transformation, to extract meaningful features from the motion data:
```python
python src/features/build_features.py
```

### Model Training and Evaluation
Train multiple machine learning models, including neural networks, SVMs, and decision trees, to classify and count exercise repetitions. Evaluate the models using accuracy and confusion matrices:
```python
python src/models/train_model.py
```


## Project Files Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── README.md          <- The top-level README for developers using this project
├── environment.yml    <- Conda Environment Setup Instructions
├── data
│   ├── interim        <- Intermediate data that has been transformed
│   └── raw            <- The original, immutable data dump
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
└── src                         <- Source code for this project
    │
    ├── __init__.py             <- Makes src a Python module
    |
    ├── data
    |   ├── __init__.py         <- 
    |   ├── make_dataset.py     <- Scripts to download or generate data
    |
    ├── features
    │   ├── __init__.py         <- 
    │   ├── build_features.py   <- Scripts to turn raw data into features for modeling
    │   ├── remove_outliers.py  <- Scripts to remove outliers from the data
    │   ├── DataTransformation.py <- Scripts for data transformation like PCA and filtering
    │   ├── FrequencyAbstraction.py <- Scripts for frequency-based feature extraction
    │   ├── TemporalAbstraction.py <- Scripts for temporal feature extraction
    │
    ├── models
    │   ├── __init__.py         <- 
    │   ├── train_model.py      <- Scripts to train models
    │   ├── predict_model.py    <- Scripts to run model inference
    │   ├── LearningAlgorithms.py <- Scripts containing various machine learning algorithms
    │
    ├── visualization
    │   ├── __init__.py         <- 
    │   ├── visualize.py        <- Scripts to create visualizations
    │   ├── plot_settings.py    <- Scripts to set plot settings
    │
    ├── count_repetitions.py    <- Scripts to count repetitions in the dataset  
```
-------

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.