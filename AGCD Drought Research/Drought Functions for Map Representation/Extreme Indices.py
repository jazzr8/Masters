4'''PART 4'''

'''
Extreme Indices Section
Two functions that are used in here:
    1. Wet Days Function
    2. Wet Spells Function
Since the AGCD data did not have the daily precipitation we rely on the data off 
the BOM site for individual stations and combine them together to make a continuous
dataset. There is one major issue is that they cause a inhomogenous dataset which
is yet to be corrected in this section. Therefore this is a rough estimate and 
further homongenisation must be done in order for the data to be accurate which
for the project I could not do in the space of time I have.
Data loaded was from http://www.bom.gov.au/climate/data/stations/
'''

#%%
#Load Data
import pandas as pd, numpy as np,xarray as xr, matplotlib.pyplot as plt, statistics, csv
import Drought_Functions as df
import geopandas
import xclim
from sklearn.metrics import r2_score


#%%
#This was a tester to make sure my coding worked.
Caufield_Rainfall = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\EXCELL DATA FOR RAINFALL LOCATIONS\Caufield Rainfall Test Location.csv")
#Assume that any NaN value had no rainfall
Caufield_Rainfall['Rainfall amount (millimetres)']=Caufield_Rainfall['Rainfall amount (millimetres)'].fillna(0)

#Convert the data into datetime
cols=["Year","Month","Day"]
Caufield_Rainfall['date'] = Caufield_Rainfall[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")
Caufield_Rainfall['date'] = pd.to_datetime(Caufield_Rainfall['date'])#,format="%Y/%m/%d")
Caufield_Rainfall.set_index('date', inplace=True)


#%%
#Number of Wet Days/Wet Spells
import Drought_Functions as df

#Bendigo
#Load Data as a csv file
Bendigo = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\EXCELL DATA FOR RAINFALL LOCATIONS\New folder\Bendigo Precipitation.csv")
Bendigo = Bendigo.dropna(subset = ['Rainfall amount (millimetres)'])
#Convert the data into datetime
cols=["Year","Month","Day"]
Bendigo['date'] = Bendigo[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")
Bendigo['date'] = pd.to_datetime(Bendigo['date'])#,format="%Y/%m/%d")
Bendigo.set_index('date', inplace=True)
Bendigo = Bendigo.dropna(subset = ['Rainfall amount (millimetres)'])

#Generate the plots for Wet Days and Wet Spells
df.Number_Wet_Days_Precip(Bendigo,5,'Bendigo',10)
df.Wet_Spells(Bendigo,5,'Bendigo',3,1)

#Shepparton
Shepparton = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\EXCELL DATA FOR RAINFALL LOCATIONS\New folder\Shepparton.csv")
Shepparton = Shepparton.dropna(subset = ['Rainfall amount (millimetres)'])
cols=["Year","Month","Day"]
Shepparton['date'] = Shepparton[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")
Shepparton['date'] = pd.to_datetime(Shepparton['date'])#,format="%Y/%m/%d")
Shepparton.set_index('date', inplace=True)
df.Number_Wet_Days_Precip(Shepparton,5,'Shepparton',1)
df.Wet_Spells(Shepparton,5,'Shepparton',3,1)

#Albury wadonga
Albury_Wadonga = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\EXCELL DATA FOR RAINFALL LOCATIONS\New folder\Albury-Wadonga.csv")
Albury_Wadonga = Albury_Wadonga.dropna(subset = ['Rainfall amount (millimetres)'])
cols=["Year","Month","Day"]
Albury_Wadonga['date'] = Albury_Wadonga[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")
Albury_Wadonga['date'] = pd.to_datetime(Albury_Wadonga['date'])#,format="%Y/%m/%d")
Albury_Wadonga.set_index('date', inplace=True)
df.Number_Wet_Days_Precip(Albury_Wadonga,5,'Albury Wadonga',1)
df.Wet_Spells(Albury_Wadonga,5,'Albury Wadonga',3,1)

#Mildura
Mildura = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\EXCELL DATA FOR RAINFALL LOCATIONS\New folder\Mildura.csv")
Mildura = Mildura.dropna(subset = ['Rainfall amount (millimetres)'])
cols=["Year","Month","Day"]
Mildura['date'] = Mildura[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")
Mildura['date'] = pd.to_datetime(Mildura['date'])#,format="%Y/%m/%d")
Mildura.set_index('date', inplace=True)
df.Number_Wet_Days_Precip(Mildura,5,'Mildura',1)
df.Wet_Spells(Mildura,5,'Mildura',3,1)









#%%BENDIGO COMBINING
'''Due to the fact that the data in not continous we must make sure we make a continous plot 
Since However this is a nonhomogenous set where the location where the precipiation was recorded
cahnged. But using Bendigo as a guide you can do it for any town in victoria provided you have the
datasets close and available'''
import pandas as pd, numpy as np,xarray as xr, matplotlib.pyplot as plt, statistics, csv
import geopandas
import xclim
from sklearn.metrics import r2_score

#Read the different dataset in, so for Bendigo there was 2 (1863 to 1992 and 1991 to 2021)
Bendigo_1863_1992 = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\EXCELL DATA FOR RAINFALL LOCATIONS\IDCJAC0009_081003_1800_Data.csv")
Bendigo_1991_2021 = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\EXCELL DATA FOR RAINFALL LOCATIONS\IDCJAC0009_081123_1800_Data.csv")
Bendigo_1863_1992['Rainfall amount (millimetres)']=Bendigo_1863_1992['Rainfall amount (millimetres)'].fillna(0)
Bendigo_1991_2021['Rainfall amount (millimetres)']=Bendigo_1991_2021['Rainfall amount (millimetres)'].fillna(0)

#Make syre datetime is sorted for both datasets
cols=["Year","Month","Day"]
Bendigo_1863_1992['date'] = Bendigo_1863_1992[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")
Bendigo_1863_1992['date'] = pd.to_datetime(Bendigo_1863_1992['date'])#,format="%Y/%m/%d")
Bendigo_1863_1992.set_index('date', inplace=True)

cols=["Year","Month","Day"]
Bendigo_1991_2021['date'] = Bendigo_1991_2021[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")
Bendigo_1991_2021['date'] = pd.to_datetime(Bendigo_1991_2021['date'])#,format="%Y/%m/%d")
Bendigo_1991_2021.set_index('date', inplace=True)

#Group the datasets by year
Old = [g for n, g in Bendigo_1863_1992.groupby(pd.Grouper(freq='Y'))]
New = [g for n, g in Bendigo_1991_2021.groupby(pd.Grouper(freq='Y'))]


#Locate where the end of the old dataset matches with the new datasets to make it continous
Year1992O = Old[129]['1992-10']
Year1992N = New[1]['1992-10']
#Then I went into the excel and basically combined the two csv files together.


#Here you can see the correlation of the two dates.
plt.figure(1)
#plt.plot(Old[128]['Rainfall amount (millimetres)'],'g')
plt.plot(Old[129]['Rainfall amount (millimetres)'],'g')
#plt.plot(New[0]['Rainfall amount (millimetres)'],'k')
plt.plot(New[0]['Rainfall amount (millimetres)'],'y')

from scipy.stats import pearsonr
corr = pearsonr(Year1992O['Rainfall amount (millimetres)'], Year1992N['Rainfall amount (millimetres)'])
#Using this correlation we can see that it produces a high correlated value of 0.8799 where most of the 
#data in the new dataset can be seen in the old dataset in October of the last month the dataset was functioning.
#Even observing the graph, it definitely shows the correlation and cleary except throughout the year up and until the 10th month 
#when the October one stopped and the transition happened.
#So this is a useful combination but it is still nonhomogenous and needs to be corrected.







