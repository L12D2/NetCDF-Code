#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 12:48:09 2025

@author: liamthompson
@contact: liam.c.thompson-1@ou.edu


This file was originally written in a Juypter notebook. Program below processes temp, dewpoint, and wind speed for 1 year.
"""

import numpy as np
import pandas as pd
import xarray as xr
from glob import glob

# Define the path to the station indices that contains nearest lat lon of associated site
station_indices_path = "station_indices_with_verification.csv"

# Load station indices into df 
station_indices_df = pd.read_csv(station_indices_path)

# base pattern for your netCDF files
file_pattern_base = [
# file directories go here. 
]

all_loc_data = []
all_timestamp_data = []

for file_pattern in file_pattern_base:
    file_list = glob(file_pattern)

    # open and iterate 
    for filename in sorted(file_list):
        # Extract the year, month, and day from the filename
        year, month, day = map(int, filename.split("_")[-2].split("-"))

        nc = xr.open_dataset(filename)

        # Create lists to store data for each location
        temperature_data = []
        timestamps = []

        # Extract temperature data for all locations in station_indices_df
        for index, row in station_indices_df.iterrows():
            tar_lat, tar_lon = row["Lat"], row["Lon"]
            lat_index, lon_index = row["LatIndex"], row["LonIndex"]
            
            temperature_data.extend(nc["T2"].values[:, lat_index, lon_index].flatten())

            # Extract timestamps from the file path for each location
            timestamp_str = filename.split("_")[-2] + "_" + filename.split("_")[-1].split(".")[0]
            timestamp = pd.to_datetime(timestamp_str, format="%Y-%m-%d_%H:%M:%S")
            timestamps.append(timestamp)

        # Append 
        all_loc_data.append(temperature_data)
        all_timestamp_data.append(timestamps)

        # Close 
        nc.close()

# Convert lists to strings with commas
all_temperature_str = [",".join(map(str, temp_list)) for temp_list in zip(*all_loc_data)]
all_timestamps_str = [",".join(timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in timestamps) for timestamps in zip(*all_timestamp_data)]

# Add the extracted data to the main list
data_list = {
    "Lat": station_indices_df["Lat"],
    "Lon": station_indices_df["Lon"],
    "LatitudeIndex": station_indices_df["LatIndex"],
    "LongitudeIndex": station_indices_df["LonIndex"],
    "Temperature": all_temperature_str,
    "Timestamps": all_timestamps_str,
}

df = pd.DataFrame(data_list)

# Save 
csv_filename = "wy2011_temp.csv"
df.to_csv(csv_filename, index=False)

print("Script execution completed.")


#### 

import numpy as np
import pandas as pd
import xarray as xr
from glob import glob

# Define the path to the station indices that contains nearest lat lon of associated site
station_indices_path = "station_indices_with_verification.csv"

# Load station indices into df 
station_indices_df = pd.read_csv(station_indices_path)

# base pattern for your netCDF files
file_pattern_base = [
# file directories go here. 
]

all_loc_data = []
all_timestamp_data = []

for file_pattern in file_pattern_base:
    file_list = glob(file_pattern)

    # open and iterate 
    for filename in sorted(file_list):
        # Extract the year, month, and day from the filename
        year, month, day = map(int, filename.split("_")[-2].split("-"))

        nc = xr.open_dataset(filename)

        # Create lists to store data for each location
        temperature_data = []
        timestamps = []

        # Extract dew temperature data for all locations in station_indices_df
        for index, row in station_indices_df.iterrows():
            tar_lat, tar_lon = row["Lat"], row["Lon"]
            lat_index, lon_index = row["LatIndex"], row["LonIndex"]
            
            temperature_data.extend(nc["TD2"].values[:, lat_index, lon_index].flatten())

            # Extract timestamps from the file path for each location
            timestamp_str = filename.split("_")[-2] + "_" + filename.split("_")[-1].split(".")[0]
            timestamp = pd.to_datetime(timestamp_str, format="%Y-%m-%d_%H:%M:%S")
            timestamps.append(timestamp)

        # Append 
        all_loc_data.append(temperature_data)
        all_timestamp_data.append(timestamps)

        # Close 
        nc.close()

# Convert lists to strings with commas
all_temperature_str = [",".join(map(str, temp_list)) for temp_list in zip(*all_loc_data)]
all_timestamps_str = [",".join(timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in timestamps) for timestamps in zip(*all_timestamp_data)]

# Add the extracted data to the main list
data_list = {
    "Lat": station_indices_df["Lat"],
    "Lon": station_indices_df["Lon"],
    "LatitudeIndex": station_indices_df["LatIndex"],
    "LongitudeIndex": station_indices_df["LonIndex"],
    "Temperature": all_temperature_str,
    "Timestamps": all_timestamps_str,
}

df = pd.DataFrame(data_list)

# Save 
csv_filename = "wy2011_dew.csv"
df.to_csv(csv_filename, index=False)

print("Script execution completed.")


####

import numpy as np
import pandas as pd
import xarray as xr
from glob import glob

# Define the path to the station indices that contains nearest lat lon of associated site
station_indices_path = "station_indices_with_verification.csv"

# Load station indices into df 
station_indices_df = pd.read_csv(station_indices_path)

# Base pattern for your netCDF files
file_pattern_base = [
# file directories go here. 
]

all_u10_data = []
all_v10_data = []
all_timestamp_data = []

for file_pattern in file_pattern_base:
    file_list = glob(file_pattern)

     # open and iterate 
    for filename in sorted(file_list):
        # Extract the year, month, and day from the filename
        year, month, day = map(int, filename.split("_")[-2].split("-"))

        nc = xr.open_dataset(filename)

        # Create lists to store data for each location
        u10 = []
        v10 = []
        timestamps = []

        # Extract U10 and V10 data for all locations in station_indices_df
        for index, row in station_indices_df.iterrows():
            lat_index, lon_index = row["LatIndex"], row["LonIndex"]
            
            u10.extend(nc["U10"].values[:, lat_index, lon_index].flatten())
            v10.extend(nc["V10"].values[:, lat_index, lon_index].flatten())

            # Extract timestamps from the file path for each location
            timestamp_str = filename.split("_")[-2] + "_" + filename.split("_")[-1].split(".")[0]
            timestamp = pd.to_datetime(timestamp_str, format="%Y-%m-%d_%H:%M:%S")
            timestamps.append(timestamp)

        # Append 
        all_u10_data.append(u10)
        all_v10_data.append(v10)
        all_timestamp_data.append(timestamps)

        # Close 
        nc.close()

# Convert lists to strings with commas
all_u10_str = [",".join(map(str, u10_list)) for u10_list in zip(*all_u10_data)]
all_v10_str = [",".join(map(str, v10_list)) for v10_list in zip(*all_v10_data)]
all_timestamps_str = [",".join(timestamp.strftime('%Y-%m-%d %H:%M:%S') for timestamp in timestamps) for timestamps in zip(*all_timestamp_data)]

# Add the extracted data to the main list
data_list = {
    "Lat": station_indices_df["Lat"],
    "Lon": station_indices_df["Lon"],
    "LatitudeIndex": station_indices_df["LatIndex"],
    "LongitudeIndex": station_indices_df["LonIndex"],
    "U10": all_u10_str,
    "V10": all_v10_str,
    "Timestamps": all_timestamps_str,
}

df = pd.DataFrame(data_list)

# Save 
csv_filename = "wy2011_wind.csv"
df.to_csv(csv_filename, index=False)

print("Script execution completed.")


