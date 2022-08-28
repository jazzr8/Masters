#%%
'''
PART 10 FINALISING THE HEATWAVE CODE
'''

#%%Heatwave Analysis

'''
This is the file that will combine all the parts together into one, all the test functions that work
all the data to make the heatwave analysis come together on 1 file. PT 5 will still be used as the 
functions list but this is the skeleton that will ultimately produce everything like graphs, data, changes and everything
else
'''

#%% Import Packages
import pandas as pd, numpy as np,matplotlib.pyplot as plt, xarray as xr,PT5_Functions_For_Masters as function_M
from scipy import stats
#Max_Heatwaves = function_M.Extend_Summer_Heatwaves_v2(Daily_MaxMin,True, 1911, 1940,'Max',CDP_Max,'date')
#%% Load Data

'''Dates 
This is used in the concatination process when the CDP is developed and other things 
that have the data disappear. Since the full 366 days need to be accounted for, 2020 was 
the year I chose for this
'''
Dates = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\Dates, includes feb 29.csv")

'''MaxT, MinT and finding AveT
The max and min temperatures are found in the files but the ave needs to be the combination of the two for that day.
To make it easier we will combine all three into one file.

'''
#Max Temp, (drop(0) has dropped the 0th index, so it starts at 1)
MaxT_Perth = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\tmax.009021.daily.csv").drop(0)
#Min Temp
MinT_Perth = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\tmin.009021.daily.csv").drop(0)
#Ave Temp
AveT_Perth = (MaxT_Perth['maximum temperature (degC)']+MinT_Perth['minimum temperature (degC)'])/2

'''Temperature Dataset
This has the date, three temperature datasets altogether
'''
Maximum = pd.Series(MaxT_Perth['maximum temperature (degC)'], name="Max")
Minimum = pd.Series(MinT_Perth['minimum temperature (degC)'],name="Min")
Average = pd.Series(AveT_Perth,name="Ave")

#The Daily Max Min Ave Data
Daily_MaxMin = pd.concat([MaxT_Perth['date'],Maximum,Minimum,Average],axis=1)




Heatwave = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1911,1940],['Max','Min'],90,7,Dates)



#%%
# Apply datetime
Daily_MaxMin['date'] = pd.to_datetime(Daily_MaxMin['date'],format="%d/%m/%Y")
DMN = Daily_MaxMin
# Apply groupby functiom
Daily_MaxMin['year']=Daily_MaxMin['date'].dt.year
Daily_MaxMin['month']=Daily_MaxMin['date'].dt.month
Daily_MaxMin['day']=Daily_MaxMin['date'].dt.day


#%%
'''
Heatwaves Version 3

'''

#%%Functions Extra



#What we need
'''Max Temp or Min Temp'''
Is_Max_T = True
'''Dataset To be Used adn the date column'''
Dataset = DMN
date_title = 'date'
#For the test 
Data = Dataset
'''Start and end Years for the values to use
Start Year will be Nov - 1911 to Mar - 1942
I will classify a year heatwave as the 1911 season as Nov-1911 to Mar-1912

Years to be excluded from the data:
1910 and 2021 as these are incomplete

In the 1880-1900
This will be a different
'''
Start_Year = 1911
End_Year = 1940

'''Name of COlumn that is to be used to extract the temperatures defined by Is_Max_T'''
Column_Name = 'Max'

'''Date Name so we can split it into day month and year'''

'''For the Excess Heat Significant Need to Use the CDP function defined beforehand'''
CDP_Max = function_M.Calendar_Day_Percentile(Daily_MaxMin,90,7,Dates,'Max',1911,1940)
CDP_Min = function_M.Calendar_Day_Percentile(Daily_MaxMin,90,7,Dates,'Min',1911,1940)
CDP = pd.concat([CDP_Max['date'],CDP_Max['Temp'],CDP_Min['Temp']],axis=1)

CDPColumn_Name = 'Temp'
#%%

'''Now to put all the heatwave values together to get the 3 Max 2 Min heatwave definition'''
Heatwaves_Max = function_M.Perth_Heatwaves_Max_Or_Min(True,DMN,'date',1911 ,2020 ,'Max',CDP_Max,'Temp')
Heatwaves_Min = function_M.Perth_Heatwaves_Max_Or_Min(False,DMN,'date',1911 ,2020 ,'Min',CDP_Min,'Temp')

A =  function_M.Proper_Heatwaves_Perth(Daily_MaxMin,  function_M.Perth_Heatwaves_Max_Or_Min(True,DMN,'date',1911 ,2020 ,'Max',CDP_Max,'Temp'),  function_M.Perth_Heatwaves_Max_Or_Min(False,DMN,'date',1911 ,2020 ,'Min',CDP_Min,'Temp'),  'date')


#So 2 days only are occurring and I believe it is to do with the break 
#in the heatwave function, it is only occruing to the onset so i 
#believe there is some way i need to mainuplate the break function 
#value so it pulls it out.



#%% Add CDP

CDP_IND_0 = function_M.Date_Splitter(CDP, 'date')
CDP_HW = []
ids = A['id'].drop_duplicates( keep='first', inplace=False)

for i in ids:
    Event = A[A['id']==i]
    Days = Event['day'].reset_index()
    Months = Event['month'].drop_duplicates( keep='first', inplace=False).reset_index()
    Years = Event['year'].drop_duplicates( keep='first', inplace=False).reset_index()
    
    CDP_IND = CDP_IND_0[CDP_IND_0['day']>=Days['day'][0]]
    CDP_IND = CDP_IND[CDP_IND['day']<=Days['day'][len(Days)-1]]
    CDP_IND = CDP_IND[CDP_IND['month']>=Months['month'][0]]
    CDP_IND = CDP_IND[CDP_IND['month']<=Months['month'][len(Months)-1]]
    
    CDP_HW.append(CDP_IND)

CDP_FOR_HW = pd.concat(CDP_HW,axis=0)

Heatwave_event = pd.concat([A,CDP_FOR_HW['Temp']],axis=0)





