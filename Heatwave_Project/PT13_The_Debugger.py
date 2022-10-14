# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:10:11 2022

@author: jarra
"""

import sys


sys.path.append(r"C:\Users\jarra\Desktop\Masters\Heatwave_Project")
import pandas as pd, PT5_Functions_For_Masters as function_M, matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib as mpl
from scipy.stats import pearsonr


#%% Load Data and generate the heatwave list


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
'''
PERTH REG TO PERTH ACORN SAT COMP 1967-1992
Using the 1961-1990 dataset and a percentile of 85% moderate heatwaves and 90% for extreme heatwaves.
'''
Heatwave_85, EHF_Max_85, EHF_Min_85, CDP_85  =  function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],85,7,Dates)

'''
I do not care about the other columns in this, so I can about the heatwave dates only.
'''
#%%

Dataset = Daily_MaxMin

date_name = 'date'
Time_In_Focus = [1911,2020] 
CDP_Time_In_Focus = [1961,1990]
Temperature_Record_Title = ['Max','Min']
percentile =85
window = 7
Dates = Dates


'''
Dataset:
    
date_name: 'date'
    Date Name so we can split it into day month and year

Time_In_Focus: [Start,End]
    Years to be excluded from the data-1910 and 2021 as these are incomplete
    
CDP_Time_In_Focus: [Start,End]
    
Temperature_Record_Title: ['Max','Min']
    Name of COlumn that is to be used to extract the temperatures defined by Is_Max_T
    
percentile: 
    
window: 
    
Dates:
'''

import pandas as pd
# Apply datetime to the dataset
Dataset[date_name] = pd.to_datetime(Dataset[date_name],format="%d/%m/%Y")

#2 versions of the dataset due to functions requiring different versions.
Data_not_expand = Dataset
Dataset = function_M.Date_Splitter(Dataset, date_name)

'''Max Temp or Min Temp'''
Is_Max_T = [True,False]



'''Start and end Years for the values to use
Start Year will be Nov - 1911 to Mar - 1942
I will classify a year heatwave as the 1911 season as Nov-1911 to Mar-1912

Years to be excluded from the data:
1910 and 2021 as these are incomplete

In the 1880-1900
This will be a different
'''

'''For the Excess Heat Significant Need to Use the CDP function defined beforehand'''
CDP_Max = function_M.Calendar_Day_Percentile(Dataset,percentile,window,Dates,Temperature_Record_Title[0],CDP_Time_In_Focus[0],CDP_Time_In_Focus[1],'Temp Max')
CDP_Min = function_M.Calendar_Day_Percentile(Dataset,percentile,window,Dates,Temperature_Record_Title[1],CDP_Time_In_Focus[0],CDP_Time_In_Focus[1],'Temp Min')
CDP = pd.concat([CDP_Max[date_name],CDP_Max['Temp Max'],CDP_Min['Temp Min']],axis=1) #Change the name



'''Now to put all the heatwave values together to get the 3 Max 2 Min heatwave definition'''
Heatwave_Max, EHF_Max = function_M.Perth_Heatwaves_Max_Or_Min(Is_Max_T[0],Data_not_expand,date_name,Time_In_Focus[0] ,Time_In_Focus[1] ,Temperature_Record_Title[0],CDP_Max,'Temp Max')
Heatwave_Min, EHF_Min = function_M.Perth_Heatwaves_Max_Or_Min(Is_Max_T[1],Data_not_expand,date_name,Time_In_Focus[0] ,Time_In_Focus[1] ,Temperature_Record_Title[1],CDP_Min,'Temp Min')	


Heatwave_Full_Dataset=  function_M.Proper_Heatwaves_Perth(Dataset,  Heatwave_Max,  Heatwave_Min,  date_name)



#So 2 days only are occurring and I believe it is to do with the break 
#in the heatwave function, it is only occruing to the onset so i 
#believe there is some way i need to mainuplate the break function 
#value so it pulls it out.



#%%

Heatwave_MaxT = Heatwave_Max
Heatwave_MinT = Heatwave_Min

import pandas as pd

Max = function_M.Date_Splitter(Heatwave_MaxT,date_name)
Min = function_M.Date_Splitter(Heatwave_MinT,date_name)
Data = Dataset

Heatwave_Event = []
Heatwave_Event_Min = []
Heatwave_Event_Max = []
count = 1
ids = Max['id'].drop_duplicates( keep='first', inplace=False)


for i in ids:
   #This extracts the id from the Max_Event
   Max_Event = Max[Max['id']==i]
   #Finds the days, months and years from the max event to match with the minimum event.
   Max_E = Max_Event.reset_index()
   start = Max_E['date'][0]
   end_Check = Max_E['date'][2]
   end = Max_E['date'][len(Max_E)-1]
   #Gets the Min event to see it if it within the bounds of the max event, it is actually the criteria
   #3 days and 2 nights,
   Min_Event = Min.set_index('date')
   Min_Event = Min_Event.loc[start:end_Check]

   print(i)
   

       
   #Checks the percentage and number of days within the event. The percentage is later
   
   
   Percent = 100*len(Min_Event)/len(Max_Event)
   length = len(Min_Event)
   #print((Percent,length))

          
   if(length >= 2):
       Temperature = Data.set_index('date')
       Temperature = Temperature.loc[start:end]
       Temperature['id'] = [count] * len(Temperature)
       count = count + 1
       Heatwave_Event.append(Temperature)
       
   if((i==477) or (i ==410)):
           print(Max_Event)
           print(Min_Event)
           print(length)
           print(Temperature)
           print(count)
           
   else:
           print(0)
       
Full_Heatwaves = pd.concat(Heatwave_Event,axis=0)
  

#Fixed Heatwaves alright, Now I have 15 more somehow.

#%%Altenative
Max_Event = Max[Max['id']==410]
Max_E = Max_Event.reset_index()
start = Max_E['date'][0]
end = Max_E['date'][2]

Min_E = Min.set_index('date')

Test = Min_E.loc[start:end]





