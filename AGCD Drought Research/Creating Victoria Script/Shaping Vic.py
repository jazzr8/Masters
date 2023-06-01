'''
This is to extract the shape file of victoria only
and using the code Mathilde sent me
using shape-env
''' 


import dask
import xarray as xr
import netCDF4 as nc
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import geopandas as gpd
from shapely.geometry import mapping
from pyproj import CRS
from shapely.geometry import mapping 

import rasterio as rio

from shapely.geometry import mapping
from pyproj import CRS
import rioxarray
crs = CRS("EPSG:4326")

import fiona
import rasterio
import rasterio.mask

precip_ds = xr.open_dataarray(r"E:\LIBRARY\UNIVERSITY\Completed Semesters\SUMMER 2021-22\Python\VICTORIA DATA\VICTORIA DATA FULL\PRECIP VIC DATA\VIC_1900_precip.nc")


vic_shp = gpd.read_file(r"E:\LIBRARY\UNIVERSITY\Completed Semesters\SUMMER 2021-22\Python\VICTORIA DATA\Shape File\E_VIC21_region.shp")

# Mask
precip_ds.rio.set_spatial_dims(x_dim="lon", y_dim="lat", inplace=True)
precip_ds.rio.write_crs("epsg:4326",inplace=True)

# Clip
precipc_ds = precip_ds.rio.clip(vic_shp.geometry.apply(mapping), precip_ds.rio.cf)



#Check if there is a working map
#precipc_ds.isel(time=0).plot()
#precipc_ds.encoding['grid_mapping'] = 'latitude-longitude'
#crs:grid_mapping_name = "latitude_longitude"

#cf_grid_mapping = precipc_ds.cs_to_cf()

#precipc_ds.to_netcdf(r'D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\Python\VICTORIA DATA\VICTORIA DATA FULL\PRECIP VIC DATA\SHAPING VIC DATA\VICShape_1900_precip.nc')
#precipc_ds.attrs

precip_ds.isel(time = 0).plot()


with fiona.open(r"E:\LIBRARY\UNIVERSITY\Completed Semesters\SUMMER 2021-22\Python\VICTORIA DATA\Shape File\E_VIC21_region.shp", "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]
    
    
with rasterio.open("tests/data/RGB.byte.tif") as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta
    
    
    
    
    
    
    
    
    
    
    
    
    
    
import geopandas as gpd
import xarray as xr


# Load the netCDF4 file into an xarray Dataset
nc_data = xr.open_dataset(r"E:\LIBRARY\UNIVERSITY\Completed Semesters\SUMMER 2021-22\Python\VICTORIA DATA\VICTORIA DATA FULL\PRECIP VIC DATA\VIC_1900_precip.nc")

# Extract the latitude and longitude values from the netCDF4 data
lat = nc_data['lat'].values
lon = nc_data['lon'].values

# Create a grid of lon and lat values with the same shape
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Convert the lon and lat arrays to a GeoSeries of points
points = gpd.points_from_xy(lon_grid.ravel(), lat_grid.ravel())










# Load the shapefile into a geopandas GeoDataFrame
boundary_lines = gpd.read_file(r"E:\LIBRARY\UNIVERSITY\Completed Semesters\SUMMER 2021-22\Python\VICTORIA DATA\Shape File\E_VIC21_region.shp")


# Create a new GeoDataFrame with the boundary lines
new_gdf = gpd.GeoDataFrame({'geometry': boundary_lines.geometry})
points = gpd.points_from_xy(lon, lat)
# Determine which points in the netCDF4 data fall within the boundary lines
points_within_boundary = new_gdf.contains(points)

# Create a new subset of the netCDF4 data that only includes the points within the boundary
subset_nc_data = nc_data.where(points_within_boundary, drop=True)

# Save the new subset of the netCDF4 data to a new netCDF4 file if desired
subset_nc_data.to_netcdf('subset_data.nc')


lat = nc_data['lat'].values
lon = nc_data['lon'].values
nrows = lat.shape
ncols = lon.shape

points = []
for i in range(nrows):
    for j in range(ncols):
        point = (lon[i,j], lat[i,j])
        points.append(point)
        
points_within_boundary = new_gdf.contains(gpd.points_from_xy([point[0] for point in points], [point[1] for point in points]))