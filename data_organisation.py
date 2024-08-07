# -*- coding: utf-8 -*-
"""data_organisation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vtWeFXgX-fu-lcrMf2akMnNZG8RYDEh_

**Mounting the data into colab**
"""

from google.colab import files
uploaded = files.upload()

import pandas as pd
import io
# List of CSV file names
filenames = [
    "5_1_LPP_redmewnet_forecast.csv",
    "5_1_LPP_redmewnet_metrics.csv",
    "5_1_LPP_redvarnet_forecast.csv",
    "5_1_LPP_redvarnet_metrics.csv",
    "5_1_LPP_stdmewnet_forecast.csv",
    "5_1_LPP_stdmewnet_metrics.csv",
    "5_1_LPP_stdredvarnet_forecast.csv",
    "5_1_LPP_stdredvarnet_metrics.csv",
    "5_1_LPP_var_forecasts.csv",
    "5_1_LPP_var_metrics.csv",
    "5_1_LPP_varnn_forecast.csv",
    "5_1_LPP_varnn_metrics.csv",
    "5_1_LPP2005REC_varmlp_forecast.csv",
    "5_1_LPP2005REC_varmlp_metric.csv",
    "5_1_msft_redmewnet_forecast.csv",
    "5_1_msft_redmewnet_metrics.csv",
    "5_1_msft_redvarnet_forecast.csv",
    "5_1_msft_redvarnet_metrics.csv",
    "5_1_MSFT_stdmewnet_forecast.csv",
    "5_1_MSFT_stdmewnet_metrics.csv",
    "5_1_msft_stdredvarnet_forecast.csv",
    "5_1_msft_stdredvarnet_metrics.csv",
    "5_1_msft_var_forecasts.csv",
    "5_1_msft_var_Metrics.csv",
    "5_1_MSFT_varmlp_forecast.csv",
    "5_1_MSFT_varmlp_metric.csv",
    "5_1_msft_varnn_forecast.csv",
    "5_1_msft_varnn_metrics.csv",
    "10_1_LPP_redmewnet_forecast.csv",
    "10_1_LPP_redmewnet_metrics.csv",
    "10_1_LPP_redvarnet_forecast.csv",
    "10_1_LPP_redvarnet_metrics.csv",
    "10_1_LPP_stdmewnet_forecast.csv",
    "10_1_LPP_stdmewnet_metrics.csv",
    "10_1_LPP_stdredvarnet_forecast.csv",
    "10_1_LPP_stdredvarnet_metrics.csv",
    "10_1_LPP_var_forecasts.csv",
    "10_1_LPP_var_metrics.csv",
    "10_1_LPP_varnn_forecast.csv",
    "10_1_LPP_varnn_metrics.csv",
    "10_1_LPP2005REC_varmlp_forecast.csv",
    "10_1_LPP2005REC_varmlp_metric.csv",
    "10_1_msft_redmewnet_forecast.csv",
    "10_1_msft_redmewnet_metrics.csv",
    "10_1_msft_redvarnet_forecast.csv",
    "10_1_msft_redvarnet_metrics.csv",
    "10_1_MSFT_stdmewnet_forecast.csv",
    "10_1_MSFT_stdmewnet_metrics.csv",
    "10_1_msft_stdredvarnet_forecast.csv",
    "10_1_msft_stdredvarnet_metrics.csv",
    "10_1_MSFT_var_forecasts.csv",
    "10_1_MSFT_var_Metrics.csv",
    "10_1_MSFT_varmlp_forecast.csv",
    "10_1_MSFT_varmlp_metric.csv",
    "10_1_msft_varnn_forecast.csv",
    "10_1_msft_varnn_metrics.csv"
]

# Dictionary to hold DataFrames
dataframes = {}

# Read each file into a DataFrame and store it in the dictionary
for file_name in file_names:
    # Use the file name (without extension) as the key
    key = file_name.replace('.csv', '').replace(' ', '_')
    dataframes[key] = pd.read_csv(io.BytesIO(uploaded[file_name]))

# Now you can access each DataFrame using the corresponding key
# For example, to access the DataFrame for "5 _LPP2005REC_ 1 var_forecasts.csv":
print(dataframes["5__LPP2005REC__1_var_forecasts"].head())

# Lists to hold DataFrames based on their name endings
metric_list = []
forecast_list = []

# Populate the lists based on the file name endings
for key, df in dataframes.items():
    if key.lower().endswith('metrics') or key.lower().endswith('metric'):
        metric_list.append(df)
    elif key.lower().endswith('forecasts') or key.lower().endswith('forecast'):
        forecast_list.append(df)

metric_list.append()
# Example: Check the lengths of the lists to ensure they are populated
print(f"Number of metrics DataFrames: {len(metric_list)}")
print(f"Number of forecasts DataFrames: {len(forecast_list)}")

# Lists to hold DataFrames and their names based on their name starting with 5 or 10
metric_list_5 = []
metric_list_10 = []

# Lists to hold the names of the DataFrames
metric_names_5 = []
metric_names_10 = []

# Populate the lists based on the file name starting with 5 or 10
for key, df in dataframes.items():
    if key.lower().endswith('metrics') or key.lower().endswith('metric'):
        if key.startswith('5'):
            metric_list_5.append(df)
            metric_names_5.append(key)
        elif key.startswith('10'):
            metric_list_10.append(df)
            metric_names_10.append(key)

# Print the names of the DataFrames in each list
print("DataFrame names in metric_list_5:")
for name in metric_names_5:
    print(name)

print("\nDataFrame names in metric_list_10:")
for name in metric_names_10:
    print(name)

# Lists to hold DataFrames based on names containing 'LPP' or 'msft'
metric_list_5_LPP = []
metric_list_5_msft = []

# Populate the lists based on the file names containing 'LPP' or 'msft'
for key, df in dataframes.items():
    if key in metric_names_5:
        if 'lpp' in key.lower():
            metric_list_5_LPP.append(df)
        elif 'msft' in key.lower():
            metric_list_5_msft.append(df)

# Print the names of the DataFrames in each list for verification
print("DataFrame names in metric_list_5_LPP:")
for name in metric_names_5:
    if 'lpp' in name.lower():
        print(name)

print("\nDataFrame names in metric_list_5_msft:")
for name in metric_names_5:
    if 'msft' in name.lower():
        print(name)

# Lists to hold DataFrames based on names containing 'LPP' or 'msft'
metric_list_10_LPP = []
metric_list_10_msft = []

# Populate the lists based on the file names containing 'LPP' or 'msft'
for key, df in dataframes.items():
    if key in metric_names_10:
        if 'lpp' in key.lower():
            metric_list_10_LPP.append(df)
        elif 'msft' in key.lower():
            metric_list_10_msft.append(df)

# Print the names of the DataFrames in each list for verification
print("DataFrame names in metric_list_5_LPP:")
for name in metric_names_10:
    if 'lpp' in name.lower():
        print(name)

print("\nDataFrame names in metric_list_5_msft:")
for name in metric_names_10:
    if 'msft' in name.lower():
        print(name)

for df in metric_list_10_LPP:
    print(df)



