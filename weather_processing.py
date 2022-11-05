"""
Created on Mon Feb  7 14:10:42 2022

@author: Okhrimchuk Roman
for Sierentz Global Merchants

Test task
"""


# TODO Import the necessary libraries
import pandas as pd
import numpy as np


# TODO Import the dataset 
path = r'./data/weather_dataset.data'
data_orig = pd.read_csv(path, sep='\s+', encoding='utf8')


# TODO  Assign it to a variable called data and replace the first 3 columns by a proper datetime index
# TODO Write a function in order to fix date (this relate only to the year info) and apply it
# TODO Set the right dates as the index. Pay attention at the data type, it should be datetime64[ns]

data = data_orig

def fix_date(df, column_names, century = '19'):
    date = df[column_names].astype('string')
    date = century + date.apply(lambda x: '/'.join(x.values), axis=1)
    date = pd.to_datetime(date, format='%Y/%m/%d')
    return date

date_columns = ['Yr', 'Mo', 'Dy']
date_column = fix_date(data, date_columns)

data = data.set_index(pd.DatetimeIndex(date_column))
data = data.drop(date_columns, axis=1)

# TODO Check if everything is okay with the data. Create functions to delete/fix rows with strange cases and apply them

# get all badly converted rows
def get_corrupted_numeric_columns(df):
    corrupted_data_mask = df.apply(pd.to_numeric, errors='coerce').apply(np.isnan).any(axis=1)
    return df[corrupted_data_mask]

# fix numbers with comma separated digits
def fix_comma_numeric_columns(df):
    df = df.replace(',', '.', regex=True)
    return df

# fix na cells by replacing it by row average
def fix_na_numeric_columns(df):
    df = df.apply(lambda row: row.fillna(row.mean()), axis=1)
    return df

# check for outliers (like -123 for loc11)
IQR_RATE = 12
def fix_outlier_numeric_values(df):
    q1 = df.quantile(.25, axis=1)
    q3 = df.quantile(.75, axis=1)
    iqr = q3 - q1
    mask = df.apply(lambda row: row.between(q1 - IQR_RATE * iqr, q3 + IQR_RATE * iqr))
    df = df[mask]
    return df

data_to_fix = get_corrupted_numeric_columns(data)
data_to_fix = fix_comma_numeric_columns(data_to_fix)
data.loc[data_to_fix.index] = data_to_fix

data = data.apply(pd.to_numeric, errors='coerce')
data = fix_outlier_numeric_values(data)
data = fix_na_numeric_columns(data)

# TODO Compute how many values are missing for each location over the entire record
missing_per_location = data.isna().sum()

# TODO Compute how many non-missing values there are in total
non_missing_total = (~data.isna().all(axis=1)).sum()

# TODO Calculate the mean windspeeds of the windspeeds over all the locations and all the times
general_mean = data.mean(axis=1).mean()

# TODO Create a DataFrame called loc_stats and calculate the min, max and mean windspeeds and standard deviations of the windspeeds at each location over all the days
loc_stats = data.describe().loc[['min','max', 'mean', 'std']].T

# TODO Find the average windspeed in January for each location
month_filter = data.index.month_name() == 'January'
january_mean = data.loc[month_filter].mean()

# TODO Downsample the record to a yearly frequency for each location
yearly = data.resample('Y').mean()

# TODO Downsample the record to a monthly frequency for each location
monthly = data.resample('M').mean()

# TODO Downsample the record to a weekly frequency for each location
weekly = data.resample('W').mean()

# TODO Calculate the min, max and mean windspeeds and standard deviations of the windspeeds across all locations for each week (assume that the first week starts on January 2 1961) for the first 21 weeks
def calc_stat(resample, func_name, n=21):
    resampling_res = getattr(resample, func_name)().head(n)
    return getattr(resampling_res, func_name)(axis=1)

resample = data.resample('W-MON')
first_weeks_stats = pd.DataFrame({'min': calc_stat(resample, 'min'), 'max': calc_stat(resample, 'max'), 'mean': calc_stat(resample, 'mean'), 'std': calc_stat(resample, 'std')})

# make prints of results (if required, can be forwarded to some file later)
print('\n\nCompute how many values are missing for each location over the entire record\n', missing_per_location)
print('\n\nCompute how many non-missing values there are in total: ', non_missing_total)
print('\n\nCalculate the mean windspeeds of the windspeeds over all the locations and all the times:', general_mean)
print('\n\nCreate a DataFrame called loc_stats and calculate the min, max and mean windspeeds and standard deviations of the windspeeds at each location over all the days\n', loc_stats)
print('\n\nFind the average windspeed in January for each location\n', january_mean)
print('\n\nDownsample the record to a yearly frequency for each location\n', yearly)
print('\n\nDownsample the record to a monthly frequency for each location\n', monthly)
print('\n\nDownsample the record to a weekly frequency for each location\n', weekly)
print('\n\nCalculate the min, max and mean windspeeds and standard deviations of the windspeeds across all locations for each week (assume that the first week starts on January 2 1961) for the first 21 weeks\n', first_weeks_stats)