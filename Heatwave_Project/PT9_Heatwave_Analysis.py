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

# Apply groupby functiom
Daily_MaxMin['year']=Daily_MaxMin['date'].dt.year
Daily_MaxMin['month']=Daily_MaxMin['date'].dt.month
Daily_MaxMin['day']=Daily_MaxMin['date'].dt.day


#%% Applying Heatwave Definition
'''
Now we have that we can begin to apply the heatwave definition onto the data.
In this section, I aim to find 5 heatwave events in the last 25 years and match them
with the heatwave event described here. The key features I will look for are the 
articles descriptions, 
any deaths associated with it, 
how well the algorithm goes at capturing the heatwave with the percentile used
If these are all acceptable then I can say that my algorithm works well.
'''


'''
Heatwaves_Finder Function
'''
#Need to apply a code that checks the things max heatwave then it has 2 days of min heatwave in the first 3 days
CDP_Max = function_M.Calendar_Day_Percentile(Daily_MaxMin,90,7,Dates,'Max',1941,1970)
Max_Heatwaves = function_M.Extend_Summer_Heatwaves_v2(Daily_MaxMin,True, 1941, 1970,'Max',CDP_Max,'date')
#Min
CDP_Min = function_M.Calendar_Day_Percentile(Daily_MaxMin,90,7,Dates,'Min',1941,1970)
Min_Heatwaves = function_M.Extend_Summer_Heatwaves_v2(Daily_MaxMin,False, 1941, 1970,'Min',CDP_Min,'date')
#Ave
#CDP_Ave = function_M.Calendar_Day_Percentile(Daily_MaxMin,90,7,Dates,'Ave',1911,1940)
#Ave_Heatwaves = function_M.Extend_Summer_Heatwaves_v2(Daily_MaxMin,True, 1911, 1940,'Ave',CDP_Ave,'date')


#
max(Max_Heatwaves['id'])


id_Max = Max_Heatwaves['id'] 
ids = id_Max.drop_duplicates( keep='first', inplace=False)
   
#%%
Heatwave_Event = []
Heatwave_Event_Min = []
Heatwave_Event_Max = []
count = 1

for i in ids:
   #This extracts the id from the Max_Event
   #print(i)
   Max_Event = Max_Heatwaves[Max_Heatwaves['id']==i]
   #print(Max_Event)
   #Finds the days, months and years from the max event to match with the minimum event.
   Days = Max_Event['day'].reset_index()
   Months = Max_Event['month'].drop_duplicates( keep='first', inplace=False).reset_index()
   Years = Max_Event['year'].drop_duplicates( keep='first', inplace=False).reset_index()
   #print(Days)
   #Gets the Min event to see it if it within the bounds of the max event, it is actually the criteria
   #3 days and 2 nights,
   Min_Event = Min_Heatwaves[Min_Heatwaves['day']>=Days['day'][0]]
   #print(Min_Event)
   Min_Event = Min_Event[Min_Event['day']<=Days['day'][2]]
   #print(Min_Event)
   Min_Event = Min_Event[Min_Event['month']>=Months['month'][0]]
   #print(Min_Event)
   Min_Event = Min_Event[Min_Event['month']<=Months['month'][len(Months)-1]]
   #print(Min_Event)
   Min_Event = Min_Event[Min_Event['year']>=Years['year'][0]]
   #print(Min_Event)
   Min_Event = Min_Event[Min_Event['year']<=Years['year'][len(Years)-1]]
   #print(Min_Event)
   
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

    # Heatwave = Heatwave_Characteristics_Onset.loc[i-heat_days:i-1]
    # Heatwave['id'] = [count] * len(Heatwave)
    # list_heatwaves.append(Heatwave)
    # heat_days=0
   
   
   
   
#My Question is:
#Should I do a new approach instead of 2 days of min heat I do 60% of mins must be in heatwave conditions  means it puts more emphasis on the longer heatwave and its actual impacts
    
                          
















