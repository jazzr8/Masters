'''
This is to extract the shape file of victoria only
and using the code Mathilde sent me
using shape-env
''' 

import pandas as pd, numpy as np, xarray as xr, dask, geopandas as gpd, rasterio as rio, rioxarray, matplotlib.pyplot as plt
from shapely.geometry import mapping
from pyproj import CRS
crs = CRS("EPSG:4326")


precip_ds = xr.open_dataarray(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\Python\VICTORIA DATA\VICTORIA DATA FULL\PRECIP VIC DATA\VIC_1900_precip.nc")


vic_shp = gpd.read_file(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\Python\VICTORIA DATA\Shape File\E_VIC21_region.shp")

# Mask
precip_ds.rio.set_spatial_dims(x_dim="lon", y_dim="lat", inplace=True)
precip_ds.rio.write_crs("epsg:4326",inplace=True)

# Clip
precipc_ds = precip_ds.rio.clip(vic_shp.geometry.apply(mapping), precip_ds.rio.cf)

#Check if there is a working map
precipc_ds.isel(time=0).plot()
precipc_ds.encoding['grid_mapping'] = 'latitude-longitude'
#crs:grid_mapping_name = "latitude_longitude"

cf_grid_mapping = precipc_ds.cs_to_cf()

precipc_ds.to_netcdf(r'D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\Python\VICTORIA DATA\VICTORIA DATA FULL\PRECIP VIC DATA\SHAPING VIC DATA\VICShape_1900_precip.nc')
precipc_ds.attrs

