# User Interface

## Installation

Follow the official Streamlit [documentation](https://docs.streamlit.io/library/get-started/installation) to install Streamlit onto your system.

## Usage

1. Ensure that `defaults.joblib` (default values for features) and `elastic-net-model.joblib` (linear regression model with Elastic Net regularization) are in the same directory as `ui.py`.
2. Open a new terminal in your Streamlit environment (follow the installation guide above if you are missing this) using Anaconda Navigator.
3. Run the application using `streamlit run ui.py`.

# Model

## Usage

1. Upload `model.ipynb` and `train.csv` into the same Google Drive folder.
2. Open `model.ipynb` with Google Colab.
3. Change the path of `train.csv` to match your directory layout in the second code block (marked with the comment "REPLACE AS NECESSARY").
