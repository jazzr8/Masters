'''PART 3'''
'''
Moving Means and Normalized Plots
'''

#Import Packages
import pandas as pd, numpy as np,xarray as xr, geopandas as gpd, matplotlib.pyplot as plt, statistics, csv
import Drought_Functions as df
from pysal.lib import cg as geometry
from pysal.lib import weights
import matplotlib.gridspec as gridspec
'''
Extract the data and shape file from the place you have stored it. All these packages must be downloaded.
import pandas, numpy, xarray, rasterio, geopandas, matplotlib, statistics, csv, dask, rioxarray, from shapely.geometry import mapping
HOW TO DO:
    1. Open anaconda3 prompt screen
    2. Create a new environment (create env)
    3. conda -n {name of env} spyder
    4. conda install python=3.7
    5. conda install/pip install the pandas numpy...
    6. 2 more packages to install for the data are netcdf4 and h5netcdf
    7. just type spyder
'''
#%% Import Data and clean the NaNs, regions: Victoria, Mallee, Nicholls, Indi, Bendigo.

#Read shape file in, using GIS data (from https://www.ebc.vic.gov.au/)
vic_shp = gpd.read_file(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\Python\VICTORIA DATA\Shape File\E_VIC21_region.shp")
#Read in file for AGCD data, downloaded off the NCI database
precip_ds = xr.open_dataarray(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\Python\VICTORIA DATA\VICTORIA DATA FULL\PRECIP VIC DATA\VIC_full_precip.nc")
#This function creates a shape  for Victoria however all the NaNs that surround Victoria must be changed to negative numbers in order for 
#resample and groupby to work properly
vic_precip = df.Extract_Map_Shape(precip_ds, vic_shp)
vic_precip=vic_precip.fillna(-9999)

#%% Extract the shapes of the regions

#This locates the region based off its Index ID in the shape file for Victoria
Mallee_shp = vic_shp.loc[29]
#These two functions (to_frame and .transpose) make sure that the Extract_Map_Shape function will read the shape file for the region correctly.
Mallee_shp = Mallee_shp.to_frame()
Mallee_shp = Mallee_shp.transpose()
Mallee_precip = df.Extract_Map_Shape(precip_ds, Mallee_shp)
Mallee_precip=Mallee_precip.fillna(-9999)


Nicholls_shp = vic_shp.iloc[35]
Nicholls_shp = Nicholls_shp.to_frame()
Nicholls_shp = Nicholls_shp.transpose()
Nicholls_precip = df.Extract_Map_Shape(precip_ds, Nicholls_shp)
Nicholls_precip=Nicholls_precip.fillna(-9999)


Indi_shp = vic_shp.iloc[22]
Indi_shp = Indi_shp.to_frame()
Indi_shp = Indi_shp.transpose()
Indi_precip = df.Extract_Map_Shape(precip_ds, Indi_shp)
Indi_precip=Indi_precip.fillna(-9999)

Bendigo_shp= vic_shp.iloc[2]
Bendigo_shp = Bendigo_shp.to_frame()
Bendigo_shp = Bendigo_shp.transpose()
Bendigo_precip = df.Extract_Map_Shape(precip_ds, Bendigo_shp)
Bendigo_precip=Bendigo_precip.fillna(-9999)

#%%
'''
1. Run the Drought Function file
2. Import the Drought Functions
'''

#This is the drought function that uses everything that I have completed for the Moving Mean and Z score indicator for drought periods.
import Drought_Functions as df


#%%
'''
This is the functions from the drought function that will:
    a) extract the specific location precipitation data
    b) extract the region precipitation data
    c) extract the regions drought periods
    d) Use a moving mean of 5 years, but can extract up to a moving mean of 100 years.
'''

#Specific Location Data using the Month_Year_MovingAve_Location_Spec function.
#REQUIREMENTS IN ORDER: Rainfall Data, latitude, longitude, Moving Mean Period (Years), Name for Location

'''Mildura'''
df.Month_Year_MovingAve_Location_Spec(vic_precip,-34.21,142.12,5,'Mildura') 

'''Shepparton'''
df.Month_Year_MovingAve_Location_Spec(vic_precip,-36.38,145.40,5,'Shepparton') 

'''Wadonga'''
df.Month_Year_MovingAve_Location_Spec(vic_precip,-36.12,146.88,5,'Wadonga') 

'''Wangarrata'''
df.Month_Year_MovingAve_Location_Spec(vic_precip,-36.37,146.32,5,'Wangarrata') 

'''Bendigo'''
df.Month_Year_MovingAve_Location_Spec(vic_precip,-36.76,144.28,5,'Bendigo') 


#------------------------------------------------------------------------#

## Regional Specific Data using the Month_Year_MovingAve_Region_Spec and Drought_Period function

#Month_Year_MovingAve_Region_Spec: This is exactly the same as te speicifc location hwovwer it incorporates another mean for the latitude and longitude
#that generates a regional specific moving mean.
#REQUIREMENTS IN ORDER: Name for region, Rainfall Data,  Moving Mean Period (Years)


#Month_Year_MovingAve_Region_Spec: This is a snapshot of a specified period that represents the 4 drought periods that we are observing.
#This is a map of the region that shows whether it is drier or wetter then the average 1880-2021 data period.
#REQUIREMENTS IN ORDER: Name for Region, Rainfall Data, Shape of Region, Start Year, End Year, Z Score Lower Bound, Z Score Upper Bound.
'''This is the year prior and after the designated drought period'''

'''Victoria'''
import Drought_Functions as df
df.Month_Year_MovingAve_Region_Spec('Victoria', vic_precip, 5)

df.Drought_Period('Victoria', vic_precip, vic_shp, 1880, 2020,-5,5)
df.Drought_Period('Victoria', vic_precip, vic_shp, 1936, 1946,-5,5)
df.Drought_Period('Victoria', vic_precip, vic_shp, 1996, 2010,-5,5)
df.Drought_Period('Victoria', vic_precip, vic_shp, 2012, 2019,-5,5)

'''Mallee'''
df.Month_Year_MovingAve_Region_Spec('Mallee', Mallee_precip, 5)

df.Drought_Period('Mallee', Mallee_precip, Mallee_shp, 1894, 1903,-3,3)
df.Drought_Period('Mallee', Mallee_precip, Mallee_shp, 1936, 1946,-3,3)
df.Drought_Period('Mallee', Mallee_precip, Mallee_shp, 1996, 2010,-3,3)
df.Drought_Period('Mallee', Mallee_precip, Mallee_shp, 2012, 2019,-3,3)

'''Nicholls'''
df.Month_Year_MovingAve_Region_Spec('Nicholls', Nicholls_precip, 5)
df.Drought_Period('Nicholls', Nicholls_precip, Nicholls_shp, 1894, 1903,-3,3)
df.Drought_Period('Nicholls', Nicholls_precip, Nicholls_shp, 1936, 1946,-3,3)
df.Drought_Period('Nicholls', Nicholls_precip, Nicholls_shp, 1996, 2010,-3,3)
df.Drought_Period('Nicholls', Nicholls_precip, Nicholls_shp, 2012, 2019,-3,3)

'''Indi'''
df.Month_Year_MovingAve_Region_Spec('Indi', Indi_precip, 5)
df.Drought_Period('Indi', Indi_precip, Indi_shp, 1894, 1903,-3,3)
df.Drought_Period('Indi', Indi_precip, Indi_shp, 1936, 1946,-3,3)
df.Drought_Period('Indi', Indi_precip, Indi_shp, 1996, 2010,-3,3)
df.Drought_Period('Indi', Indi_precip, Indi_shp, 2012, 2019,-3,3)

'''Bendigo'''
df.Month_Year_MovingAve_Region_Spec('Bendigo', Bendigo_precip, 5)
df.Drought_Period('Bendigo', Bendigo_precip, Bendigo_shp, 1894, 1903,-3,3)
df.Drought_Period('Bendigo', Bendigo_precip, Bendigo_shp, 1936, 1946,-3,3)
df.Drought_Period('Bendigo', Bendigo_precip, Bendigo_shp, 1996, 2010,-3,3)
df.Drought_Period('Bendigo', Bendigo_precip, Bendigo_shp, 2012, 2019,-3,3)

#%%9.
SEASONAL_DATA_ST_MAR = vic_precip.resample(time='Q-MAY').sum()
 
 #Grouping so I can easily extract the seasons by 'DJF','MAM' in a for loop
SD=SEASONAL_DATA_ST_MAR.groupby('time.season')
 #Remove the negative values so the are NaNs
SEASONAL_DATA_ST_MAR_fixed = SEASONAL_DATA_ST_MAR.where(SEASONAL_DATA_ST_MAR>=0)

#Make the Z Score
SummerFixed = SD['DJF']
SummerFixed = SummerFixed.where(SEASONAL_DATA_ST_MAR>=0)
AutumnFixed= SD['MAM']
AutumnFixed = AutumnFixed.where(SEASONAL_DATA_ST_MAR>=0)
WinterFixed= SD['JJA']
WinterFixed = WinterFixed.where(SEASONAL_DATA_ST_MAR>=0)
SpringFixed= SD['SON']
SpringFixed = SpringFixed.where(SEASONAL_DATA_ST_MAR>=0)

#Means
Precip_Mean_Sum= SummerFixed.mean(dim =('lon','lat')).mean(dim='time')
Precip_Mean_Aut= AutumnFixed.mean(dim =('lon','lat')).mean(dim='time')
Precip_Mean_Wint= WinterFixed.mean(dim =('lon','lat')).mean(dim='time')
Precip_Mean_Spr= SpringFixed.mean(dim =('lon','lat')).mean(dim='time')

#Get Standardized Score
 #Mean the shape in terms of latitude and longitude
Dif_BW_MM_MeanSum = (SummerFixed.mean(dim =('lon','lat')) - Precip_Mean_Sum)
Dif_BW_MM_MeanAut = (AutumnFixed.mean(dim =('lon','lat')) - Precip_Mean_Aut)  
Dif_BW_MM_MeanWint = (WinterFixed.mean(dim =('lon','lat')) - Precip_Mean_Wint)
Dif_BW_MM_MeanSpr = (SpringFixed.mean(dim =('lon','lat')) - Precip_Mean_Spr)

 #Create a standard deviation of the Anomoly
stdevSum = Dif_BW_MM_MeanSum.std()
stdevWin = Dif_BW_MM_MeanAut.std()
stdevSpr = Dif_BW_MM_MeanWint.std()
stdevAut = Dif_BW_MM_MeanSpr.std()
 #Create the normalised data by dividing the anomoly by the standard deviation.
NormalizedSum= Dif_BW_MM_MeanSum/stdevSum
NormalizedAut=  Dif_BW_MM_MeanAut/stdevAut
NormalizedWint= Dif_BW_MM_MeanWint/stdevWin
NormalizedSpr= Dif_BW_MM_MeanSpr/stdevSpr

plt.plot(NormalizedSum)
plt.plot(NormalizedAut)
plt.plot(NormalizedWint)
plt.plot(NormalizedSpr)
SuW_AuD_WiSpD = 0
SuD_AuW_WiSpD = 0
Neither = 0

RanWint = len(NormalizedWint)
RanSum= len(NormalizedSum)
RanAut = len(NormalizedAut)
RanSpr = len(NormalizedSpr)
SummerUpdated = []
SpringUpdated = []
WinterUpdated = []
AutumnUpdated = []
for i in range(0,RanSum-1):
    SummerUpdated.append(NormalizedSum[i])
for i in range(0,RanSpr): 
    SpringUpdated.append(NormalizedSpr[i])
for i in range(0,RanAut-1):
    AutumnUpdated.append(NormalizedAut[i])
for i in range(0,RanWint): 
    WinterUpdated.append(NormalizedWint[i])

SuW_AuW_WiW_SpW = 0
SuW_AuW_WiW_SpD = 0
SuW_AuW_WiD_SpW =0 
SuW_AuW_WiD_SpD=0
SuW_AuD_WiW_SpW=0
SuW_AuD_WiW_SpD=0
SuW_AuD_WiD_SpW=0
SuW_AuD_WiD_SpD=0
SuD_AuW_WiW_SpW=0
SuD_AuW_WiW_SpD=0
SuD_AuW_WiD_SpW=0
SuD_AuW_WiD_SpD=0
SuD_AuD_WiW_SpW=0
SuD_AuD_WiW_SpD=0
SuD_AuD_WiD_SpW=0
SuD_AuD_WiD_SpD=0


for i in range(0,139):
    if SummerUpdated[i]>=0 and AutumnUpdated[i] >=0 and SpringUpdated[i] >=0 and WinterUpdated[i] >=0:
        SuW_AuW_WiW_SpW = SuW_AuW_WiW_SpW +1
    elif SummerUpdated[i]>=0 and AutumnUpdated[i] >=0 and SpringUpdated[i] >=0 and WinterUpdated[i] <0:
        SuW_AuW_WiW_SpD = SuW_AuW_WiW_SpD +1  
    elif SummerUpdated[i]>=0 and AutumnUpdated[i] >=0 and SpringUpdated[i] <0 and WinterUpdated[i] >=0:
        SuW_AuW_WiD_SpW = SuW_AuW_WiD_SpW +1  
    elif SummerUpdated[i]>=0 and AutumnUpdated[i] >=0 and SpringUpdated[i] <0 and WinterUpdated[i] <0:
        SuW_AuW_WiD_SpD = SuW_AuW_WiD_SpD +1  
    elif SummerUpdated[i]>=0 and AutumnUpdated[i] <0 and SpringUpdated[i] >=0 and WinterUpdated[i] >=0:
        SuW_AuD_WiW_SpW = SuW_AuD_WiW_SpW +1  
    elif SummerUpdated[i]>=0 and AutumnUpdated[i] <0 and SpringUpdated[i] >=0 and WinterUpdated[i] <0:    
        SuW_AuD_WiW_SpD = SuW_AuD_WiW_SpD +1  
    elif SummerUpdated[i]>=0 and AutumnUpdated[i] <0 and SpringUpdated[i] <0 and WinterUpdated[i] >=0:    
        SuW_AuD_WiD_SpW = SuW_AuD_WiD_SpW +1  
    elif SummerUpdated[i]>=0 and AutumnUpdated[i] <0 and SpringUpdated[i] <0 and WinterUpdated[i] <0:
        SuW_AuD_WiD_SpD = SuW_AuD_WiD_SpD +1  
    elif SummerUpdated[i]<0 and AutumnUpdated[i] >=0 and SpringUpdated[i] >=0 and WinterUpdated[i] >=0:
        SuD_AuW_WiW_SpW = SuD_AuW_WiW_SpW +1  
    elif SummerUpdated[i]<0 and AutumnUpdated[i] >=0 and SpringUpdated[i] >=0 and WinterUpdated[i] <0:
        SuD_AuW_WiW_SpD = SuD_AuW_WiW_SpD +1  
    elif SummerUpdated[i]<0 and AutumnUpdated[i] >=0 and SpringUpdated[i] <0 and WinterUpdated[i] >=0:
        SuD_AuW_WiD_SpW = SuD_AuW_WiD_SpW +1  
    elif SummerUpdated[i]<0 and AutumnUpdated[i] >=0 and SpringUpdated[i] <0 and WinterUpdated[i] <0:
        SuD_AuW_WiD_SpD = SuD_AuW_WiD_SpD +1  
    elif SummerUpdated[i]<0 and AutumnUpdated[i] <0 and SpringUpdated[i] >=0 and WinterUpdated[i] >=0:
        SuD_AuD_WiW_SpW = SuD_AuD_WiW_SpW +1      
    elif SummerUpdated[i]<0 and AutumnUpdated[i] <0 and SpringUpdated[i] >=0 and WinterUpdated[i] <0:    
        SuD_AuD_WiW_SpD = SuD_AuD_WiW_SpD +1      
    elif SummerUpdated[i]<0 and AutumnUpdated[i] <0 and SpringUpdated[i] <0 and WinterUpdated[i] >=0:    
        SuD_AuD_WiD_SpW = SuD_AuD_WiD_SpW +1      
    elif SummerUpdated[i]<0 and AutumnUpdated[i] <0 and SpringUpdated[i] <0 and WinterUpdated[i] <0:  
        SuD_AuD_WiD_SpD = SuD_AuD_WiD_SpD +1      
print(SuW_AuW_WiW_SpW,SuW_AuW_WiW_SpD,SuW_AuW_WiD_SpW,SuW_AuW_WiD_SpD,SuW_AuD_WiW_SpW,SuW_AuD_WiW_SpD,SuW_AuD_WiD_SpW,SuW_AuD_WiD_SpD,SuD_AuW_WiW_SpW,SuD_AuW_WiW_SpD,SuD_AuW_WiD_SpW,SuD_AuW_WiD_SpD,SuD_AuD_WiW_SpW,SuD_AuD_WiW_SpD,SuD_AuD_WiD_SpW,SuD_AuD_WiD_SpD)


RAW_Annual_Precip = vic_precip.resample(time='AS-JAN').sum(dim='time')
RAW_Annual_Precip.drop(time=1880)
