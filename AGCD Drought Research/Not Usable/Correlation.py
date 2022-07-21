'''PART 5'''
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 15:41:22 2022

@author: jarra
"""

#Import Packages
import pandas as pd, numpy as np,xarray as xr, geopandas as gpd, matplotlib.pyplot as plt, statistics, csv
import Drought_Functions as df
from pysal.lib import cg as geometry
from pysal.lib import weights
import matplotlib.gridspec as gridspec
import pandas as pd, numpy as np,xarray as xr, dask,geopandas as gpd, matplotlib.pyplot as plt, statistics, csv
from datetime import datetime
import scipy.stats as SciSt
#Read shape file in, using GIS data (from https://www.ebc.vic.gov.au/)
vic_shp = gpd.read_file(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\Python\VICTORIA DATA\Shape File\E_VIC21_region.shp")
#Read in file for AGCD data, downloaded off the NCI database
precip_ds = xr.open_dataarray(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\Python\VICTORIA DATA\VICTORIA DATA FULL\PRECIP VIC DATA\VIC_full_precip.nc")
#This function creates a shape  for Victoria however all the NaNs that surround Victoria must be changed to negative numbers in order for 
#resample and groupby to work properly
vic_precip = df.Extract_Map_Shape(precip_ds, vic_shp)
vic_precip=vic_precip.fillna(-9999)

















plt.rcParams["font.family"] = 'sans-serif'
 #--------------------------------------- SEASONAL MOVING MEAN------------------------#

#Create a new figure that creates 5 equally sized plots for the seasonal data.
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, figsize=(10,25), sharex=True,sharey=True)

#Create a list to be used for titles and to extract the seasonal data from the resampled seasonal dataset 
list = ['DJF','MAM','JJA','SON']
 #Resampling the data into seasonal data where Q-MAY starts that the quartely ends in MAY and starts in March that simulates Autumn, and this
#continues to do this for each season. Secondly it also sums the precipitation of the 3 months so it is the total seasonal precipitation.
SEASONAL_DATA_ST_MAR = vic_precip.resample(time='Q-MAY').sum()

#Grouping the datasets so I can easily extract the seasons by the list stated above.
SD=SEASONAL_DATA_ST_MAR.groupby('time.season')

#Get rid of the negative values that are on the outside of the Victoria shape
SEASONAL_DATA_ST_MAR_fixed = SEASONAL_DATA_ST_MAR.where(SEASONAL_DATA_ST_MAR>=0)
 #This is the plot that maps the entire moving mean seasonal data on the specified Period.
Annual = plt.plot(SEASONAL_DATA_ST_MAR_fixed['time'],SEASONAL_DATA_ST_MAR_fixed.sel(lat=-34.21,lon=142.12,method='nearest'), color = 'black',label = r"Seasonal Total", linestyle = 'None',marker='.',markersize = '2')



#Remove the negative areas that are on the outside of the shape.
SUMMER=SD['DJF'].where(SD['DJF']>=0).sel(lat=-34.21,lon=142.12,method='nearest')
AUTUMN=SD['MAM'].where(SD['MAM']>=0).sel(lat=-34.21,lon=142.12,method='nearest')
WINTER=SD['JJA'].where(SD['JJA']>=0).sel(lat=-34.21,lon=142.12,method='nearest')
SPRING=SD['SON'].where(SD['SON']>=0).sel(lat=-34.21,lon=142.12,method='nearest')

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
#%%
lati = -36.76
long =144.28
    
SUMMER=SD['DJF'].where(SD['DJF']>=0).sel(lat=lati,lon=long,method='nearest')
AUTUMN=SD['MAM'].where(SD['MAM']>=0).sel(lat=lati,lon=long,method='nearest')
WINTER=SD['JJA'].where(SD['JJA']>=0).sel(lat=lati,lon=long,method='nearest')
SPRING=SD['SON'].where(SD['SON']>=0).sel(lat=lati,lon=long,method='nearest')
 




#%% 1.

RanSpr = len(SPRING)
RanSum= len(SUMMER)
Summerupdated = []
SpringUpdated = []
for i in range(1,RanSum-1):
    Summerupdated.append(SUMMER[i])
for i in range(0,RanSpr-1): 
    SpringUpdated.append(SPRING[i])

plt.plot(Summerupdated,SpringUpdated,color = '{}'.format('Red'),label = r"Seasonal Total",linestyle = 'None',marker = '.',markersize = '2')
CORRP = SciSt.pearsonr(Summerupdated,SpringUpdated)
CORRS = SciSt.spearmanr(Summerupdated,SpringUpdated) #Wettest to driesta nd then rank
CORRK = SciSt.kendalltau(Summerupdated,SpringUpdated)



#%% 2.

#Plot the individual points for a reference of what happened over that period.
SummerPlot = plt.plot(SUMMER['time'],SUMMER,color = '{}'.format('Red'),label = r"Seasonal Total",linestyle = 'None',marker = '.',markersize = '2')
 
SummerVAutumn = plt.plot(SUMMER,AUTUMN,color = '{}'.format('Red'),label = r"Seasonal Total",linestyle = 'None',marker = '.',markersize = '2')
import scipy.stats as SciSt
#Peasons Correlation Coefficient 
CORR = np.corrcoef(SUMMER,AUTUMN)
CORRP = SciSt.pearsonr(SUMMER,AUTUMN)
CORRS = SciSt.spearmanr(SUMMER,AUTUMN)
CORRK = SciSt.kendalltau(SUMMER,AUTUMN)

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



#7.
#Rainfall  Precip Total: Bendigo

import pandas as pd, numpy as np,xarray as xr, dask,geopandas as gpd, matplotlib.pyplot as plt, statistics, csv
from datetime import datetime
plt.rcParams["font.family"] = 'sans-serif'
#------------------------------ YEARLY MOVING MEAN------------------------------#
#Extract the yearly precipitation totals by using groupby and removing the negative values used for the outside of the shape.
D1 = vic_precip.groupby("time.year").map(summingthing)
yearly_total= D1.where(D1>=0)

#Generate the yearly total precip 
Precip_Totals =yearly_total.sel(lat=-36.76,lon=144.28,method='nearest')


Bendigo = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\EXCELL DATA FOR RAINFALL LOCATIONS\New folder\Bendigo Precipitation.csv")
Bendigo = Bendigo.dropna(subset = ['Rainfall amount (millimetres)'])


#Count of Wet Days
cols=["Year","Month","Day"]
Bendigo['date'] = Bendigo[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")
Bendigo['date'] = pd.to_datetime(Bendigo['date'])#,format="%Y/%m/%d")
Bendigo.set_index('date', inplace=True)
  
   #% Yearly Count 
Yearly = [g for n, g in Bendigo.groupby(pd.Grouper(freq='Y'))]

Max_Y = Bendigo['Year'].max()
Min_Y = Bendigo['Year'].min()


Yearly_Count_Wet_Days = []
Yearly_Count_Wet_Days_Date = []

ranger =Max_Y - Min_Y 

for p in range(0,ranger):
    Yearly_Data = Yearly[p]
    i = 0
    ran =int(len(Yearly_Data))
    for q in range(0,ran,1):
        if Yearly_Data['Rainfall amount (millimetres)'][q]>=1:
            i = i+1
        else:
            i = i
                
    Yearly_Count_Wet_Days_Date.append(p+Min_Y)
    Yearly_Count_Wet_Days.append(i)


Yearly_Wet = pd.concat([pd.Series(Yearly_Count_Wet_Days_Date,name = 'Year'), pd.Series( Yearly_Count_Wet_Days,name='Wet Days')], axis=1)

plt.plot(Yearly_Wet['Year'],Yearly_Wet['Wet Days'])
plt.plot(Precip_Totals['year'],Precip_Totals)

fig,axes =plt.subplots(figsize=(13,9))

axes.plot(Yearly_Wet['Year'],Yearly_Wet['Wet Days'])

axes2=axes.twinx()
axes2.plot(Precip_Totals['year'],Precip_Totals,'r')
axes2.set_xlim([1880,2021])





#Shepparton
import pandas as pd, numpy as np,xarray as xr, dask,geopandas as gpd, matplotlib.pyplot as plt, statistics, csv
from datetime import datetime
plt.rcParams["font.family"] = 'sans-serif'
#------------------------------ YEARLY MOVING MEAN------------------------------#
#Extract the yearly precipitation totals by using groupby and removing the negative values used for the outside of the shape.
D1 = vic_precip.groupby("time.year").map(summingthing)
yearly_total= D1.where(D1>=0)

#Generate the yearly total precip 
Precip_Totals =yearly_total.sel(lat=-36.38,lon=145.40,method='nearest')


Shepparton = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\EXCELL DATA FOR RAINFALL LOCATIONS\New folder\Shepparton.csv")
Shepparton = Shepparton.dropna(subset = ['Rainfall amount (millimetres)'])


#Count of Wet Days
cols=["Year","Month","Day"]
Shepparton['date'] = Shepparton[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")
Shepparton['date'] = pd.to_datetime(Shepparton['date'])#,format="%Y/%m/%d")
Shepparton.set_index('date', inplace=True)
  
   #% Yearly Count 
Yearly = [g for n, g in Bendigo.groupby(pd.Grouper(freq='Y'))]

Max_Y = Shepparton['Year'].max()
Min_Y = Shepparton['Year'].min()


Yearly_Count_Wet_Days = []
Yearly_Count_Wet_Days_Date = []

ranger =Max_Y - Min_Y 

for p in range(0,ranger):
    Yearly_Data = Yearly[p]
    i = 0
    ran =int(len(Yearly_Data))
    for q in range(0,ran,1):
        if Yearly_Data['Rainfall amount (millimetres)'][q]>=1:
            i = i+1
        else:
            i = i
                
    Yearly_Count_Wet_Days_Date.append(p+Min_Y)
    Yearly_Count_Wet_Days.append(i)


Yearly_Wet = pd.concat([pd.Series(Yearly_Count_Wet_Days_Date,name = 'Year'), pd.Series( Yearly_Count_Wet_Days,name='Wet Days')], axis=1)

plt.plot(Yearly_Wet['Year'],Yearly_Wet['Wet Days'])
plt.plot(Precip_Totals['year'],Precip_Totals)

fig,axes =plt.subplots(figsize=(13,9))

axes.plot(Yearly_Wet['Year'],Yearly_Wet['Wet Days'])

axes2=axes.twinx()
axes2.plot(Precip_Totals['year'],Precip_Totals,'r')
axes2.set_xlim([1880,2021])


    
    #Extract the yearly precipitation totals by using groupby and removing the negative values used for the outside of the shape.
    D1 = data.groupby("time.year").map(summingthing)
    yearly_total= D1.where(D1>=0)
    
    #Generate the annual mean of the total yearly rainfall.
    mean_annually = yearly_total.sel(lat=Latitude,lon=Longitude, method='nearest').mean(dim='year')
    
    #Generate the yearly Moving Mean
    Move_Mean_Y = yearly_total.sel(lat=Latitude,lon=Longitude,method='nearest').rolling(year=Period,center=True).mean()
    Precip_Totals =yearly_total.sel(lat=Latitude,lon=Longitude,method='nearest')
    #Anomoly the Data by taking away the moving mean by the annual mean.
    Dif_BW_MM_Mean = (Move_Mean_Y - mean_annually)
    Dif_BW_Tot_Mean = (Precip_Totals - mean_annually)
    #Generate a Standard Deviation based off the Anomoly
    stdev = Dif_BW_MM_Mean.std()
    stdevTot = Dif_BW_Tot_Mean.std()
    #Create the Z score by having the Anomoly divided by the standard deviation
    Normalized= Dif_BW_MM_Mean/stdev
    NormalizedTot =Dif_BW_Tot_Mean /stdevTot

