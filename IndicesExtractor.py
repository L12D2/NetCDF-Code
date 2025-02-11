#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 09:45:39 2025

@author: liamthompson
"""

import netCDF4
import numpy as np
from haversine import haversine, Unit
import pandas as pd

# Load netCDF file
filename = ""
wx_stations = pd.read_csv(", sep=",")
nc = netCDF4.Dataset(filename)

# Get latitude and longitude arrays
xlat = np.array(nc["XLAT"])
xlon = np.array(nc["XLONG"])

wx_stat_lat = wx_stations["Lat"]
wx_stat_lon = wx_stations["Lon"]
wx_stat_name = wx_stations["CHUWD_station_Name_final"]
urban_area = wx_stations["Within an urban area"]


def find_grid(lat, lon, xlat, xlon):
    distances = np.vectorize(lambda x, y: haversine((lat, lon), (x, y), unit=Unit.METERS))(xlat, xlon)
    indices = np.unravel_index(np.argmin(distances), distances.shape)
    return indices

# Create an empty DataFrame to store the results
result_df = pd.DataFrame(columns=["Station", "Lat", "Lon", "LatIndex", "LonIndex", "NearestLat", "NearestLon", "WithinUrbanArea", "IndicesCheck", "LatLonCheck"])

# Find closest grid points for each weather station and save in DataFrame
# Create an empty list to store dictionaries
result_data = []

# Find closest grid points for each weather station and save in list
for i in range(len(wx_stat_lat)):
    lat = wx_stat_lat.iloc[i]
    lon = wx_stat_lon.iloc[i]
    indices = find_grid(lat, lon, xlat, xlon)

    # Append the results to the list
    result_data.append({
        "Station": wx_stat_name.iloc[i],
        "Lat": lat,
        "Lon": lon,
        "LatIndex": indices[0],
        "LonIndex": indices[1],
        "NearestLat": xlat[indices],
        "NearestLon": xlon[indices],
        "WithinUrbanArea": urban_area.iloc[i],
        "IndicesCheck": f"{indices[0]}, {indices[1]}",
        "LatCheck": f"{xlat[indices]}", 
        "LonCheck": f"{xlon[indices]}"
    })

# Convert the list of dictionaries to a DataFrame
result_df = pd.DataFrame(result_data)

# Save the DataFrame to a CSV file
result_df.to_csv("station_indices.csv", index=False)

# Check and print the verification results for the first station
# Extract the indices for the first station
lat_index_check = result_df["LatIndex"].iloc[0]
lon_index_check = result_df["LonIndex"].iloc[0]

# Extract the latitude and longitude for the provided indices
lat_check = xlat[lat_index_check, lon_index_check]
lon_check = xlon[lat_index_check, lon_index_check]

# Append the verification results to the existing DataFrame
result_df.loc[0, "IndicesCheck"] = f"{lat_index_check}, {lon_index_check}"
result_df.loc[0, "LatLonCheck"] = f"{lat_check}, {lon_check}"

# Save the updated DataFrame to a CSV file
result_df.to_csv("station_indices_with_verification.csv", index=False)

