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

'''Expand date
Since we want to use the day, month and year individually we need to expand these
'''

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
CDP = CDP_Max
CDPColumn_Name = 'Temp'
#%%

'''Now to put all the heatwave values together to get the 3 Max 2 Min heatwave definition'''
Heatwaves_Max = function_M.Perth_Heatwaves_Max_Or_Min(True,DMN,'date',1911 ,2020 ,'Max',CDP,'Temp')
Heatwaves_Min = function_M.Perth_Heatwaves_Max_Or_Min(False,DMN,'date',1911 ,2020 ,'Max',CDP,'Temp')



#%%To get the proper definition of a heatwave.

Max = function_M.Date_Splitter(Heatwaves_Max,'date')
Min = function_M.Date_Splitter(Heatwaves_Min,'date')

Heatwave_Event = []
Heatwave_Event_Min = []
Heatwave_Event_Max = []
count = 1
ids = Max['id'].drop_duplicates( keep='first', inplace=False)

for i in ids:
   #This extracts the id from the Max_Event
   Max_Event = Max[Max['id']==i]
   #Finds the days, months and years from the max event to match with the minimum event.
   Days = Max_Event['day'].reset_index()
   Months = Max_Event['month'].drop_duplicates( keep='first', inplace=False).reset_index()
   Years = Max_Event['year'].drop_duplicates( keep='first', inplace=False).reset_index()
   #Gets the Min event to see it if it within the bounds of the max event, it is actually the criteria
   #3 days and 2 nights,
   Min_Event = Min[Min['day']>=Days['day'][0]]
   Min_Event = Min_Event[Min_Event['day']<=Days['day'][2]]
   Min_Event = Min_Event[Min_Event['month']>=Months['month'][0]]
   Min_Event = Min_Event[Min_Event['month']<=Months['month'][len(Months)-1]]
   Min_Event = Min_Event[Min_Event['year']>=Years['year'][0]]
   Min_Event = Min_Event[Min_Event['year']<=Years['year'][len(Years)-1]]
   
   
   #Checks the percentage and number of days within the event. The percentage is later
   
   
   Percent = 100*len(Min_Event)/len(Max_Event)
   length = len(Min_Event)
   #print((Percent,length))
   
   #Now extract the information for the period.
   if(length >= 2):
       Temperature = Daily_MaxMin[Daily_MaxMin['day']>=Days['day'][0]]
       #print(Min_Event)
       Temperature = Temperature[Temperature['day']<=Days['day'][len(Days)-1]]
       #print(Min_Event)
       Temperature = Temperature[Temperature['month']>=Months['month'][0]]
       #print(Min_Event)
       Temperature = Temperature[Temperature['month']<=Months['month'][len(Months)-1]]
       #print(Min_Event)
       Temperature = Temperature[Temperature['year']>=Years['year'][0]]
       #print(Min_Event)
       Temperature = Temperature[Temperature['year']<=Years['year'][len(Years)-1]]
       #print(Min_Event)

       Temperature['id'] = [count] * len(Temperature)
       count = count + 1
       Heatwave_Event.append(Temperature)
   Full_Heatwaves = pd.concat(Heatwave_Event,axis=0)



#So 2 days only are occurring and I believe it is to do with the break 
#in the heatwave function, it is only occruing to the onset so i 
#believe there is some way i need to mainuplate the break function 
#value so it pulls it out.







