#%% This is the coding that will be used for the presentation in my masters coursework.
'''
This section will have a few graphs in place:
    Figure 1
    This is the comparision of 15 day PB to 0 day PB with max and min
    
    Figure 2
    1.1 90th percentile Max/Min
    2.1 90th percentile deviation
    1.2 95th percentile Max/Min
    2.2 95th Percentile deviadeviation

From here I will also generate statistics that provide means for these 90th percentile stuff
and also the days that the modern time is about the old time.
'''

#%% PACKAGES
import pandas as pd, numpy as np,matplotlib.pyplot as plt
from scipy import stats

#%% MAXIMUM and Minimum Data
#Maximum

#Load the data in and groupby for the boxes in order for the percentile base funciton to work

# Load Data only using max Temperature for the initial start
MaxT_Perth_Data = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\tmax.009021.daily.csv")
MaxT_Perth = MaxT_Perth_Data.copy()
MaxT_Perth = MaxT_Perth.drop(0)

# Apply datetime
MaxT_Perth['date'] = pd.to_datetime(MaxT_Perth['date'],format="%d/%m/%Y")

# Apply groupby functiom
MaxT_Perth['year']=MaxT_Perth['date'].dt.year
MaxT_Perth['month']=MaxT_Perth['date'].dt.month
MaxT_Perth['day']=MaxT_Perth['date'].dt.day

#Separate into monthly and daily bins
group_days_Max = MaxT_Perth.groupby(['month','day'])
Daily_Data_Max = []
for groups,days in group_days_Max:
    #Extract the specified day bin
    Dailypre_Max = group_days_Max.get_group(groups).reset_index()
    #Get the maximum values for the entire record for that calendar day
    Values_Max= Dailypre_Max['maximum temperature (degC)']
    #Make it a dataframe so it is appendable
    Values_Max = Values_Max.to_frame()
    #Append that bin to that day so there will be 366 bins with  x years data for that day
    Daily_Data_Max.append(Values_Max['maximum temperature (degC)'])

#Minimum
#Everything described above in the maximum section is similar for this minimum section.

#Load Data only using min Temperature for the initial start
MinT_Perth_Data = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\tmin.009021.daily.csv")
MinT_Perth = MinT_Perth_Data.copy()
MinT_Perth = MinT_Perth.drop(0)

# Apply datetime
MinT_Perth['date'] = pd.to_datetime(MinT_Perth['date'],format="%d/%m/%Y")

#Apply groupby functiom
MinT_Perth['year']=MinT_Perth['date'].dt.year
MinT_Perth['month']=MinT_Perth['date'].dt.month
MinT_Perth['day']=MinT_Perth['date'].dt.day


group_days_Min = MinT_Perth.groupby(['month','day'])
Daily_Data_Min = []
for groups,days in group_days_Min:
    Dailypre_Min = group_days_Min.get_group(groups).reset_index()
    Values_Min= Dailypre_Min['minimum temperature (degC)']
    Values_Min = Values_Min.to_frame()
    Daily_Data_Min.append(Values_Min['minimum temperature (degC)'])

#%%
#Import the functions created in a separate file.
import PT5_Functions_For_Masters as function_M


#%% Lets Generate Figure 1
#We will compare the 90th percentile graphs here
CalendarDayMax_0 = function_M.TnX_Rolling(0, Daily_Data_Max, 90)
CalendarDayMin_0 = function_M.TnX_Rolling(0, Daily_Data_Min, 90)

#Now the 15 day percentile for the calendar day.
CalendarDayMax_15 = function_M.TnX_Rolling(7, Daily_Data_Max, 90)
CalendarDayMin_15 = function_M.TnX_Rolling(7, Daily_Data_Min, 90)
#%%
#Lets graph the comparisons
plt.figure(1)
fig, ax = plt.subplots(figsize = (12,8))
ax.plot(CalendarDayMax_0,color = 'orange')
ax.plot(CalendarDayMin_0,color = 'green')
ax.plot(CalendarDayMax_15, color = 'red')
ax.plot(CalendarDayMin_15, color = 'blue')
ax.legend(['1-Day Window CDP Maximum','1-Day Window CDP Minimum','15-Day Window CDP Maximum','15-Day Window CDP Minimum'],loc=9,prop={'size': 14})

ax.set_title('Calendar Day 90$^{th}$ Percentile (CDP) Temperature',size=26)  
ax.set_xlim([0,365])
ax.set_ylim([10,45])

months_start = [0,31,60,91,121,152,182,213,244,274,305,335]
month_names =['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
ax.set_xticks(months_start)
ax.set_xticklabels(month_names)

ax.set_xlabel('Calendar Day',size=16)
ax.set_ylabel('Temperature (\N{DEGREE SIGN}C)',size=16)
ax.tick_params(labelsize=16)
'''
15 Days is chosen as it still captures slight variations hwoever it continues to caputre a smoother seaosnal signal.
'''

#%% Lets Generate Figure 2

#This requires more coding and spliting into 2 time periods, Federation and Millenial 
'''1910/1/1-1940/31/12'''
#Maximumn/Minimum For the Period Millenial Period
MaxT_1910_1940 = MaxT_Perth[1:11323]
MinT_1910_1940 = MinT_Perth[1:11323]


#Separate into monthly and daily bins
group_days_Max_O = MaxT_1910_1940.groupby(['month','day'])
Daily_Data_Max_O = []
for groups,days in group_days_Max_O:
    #Extract the specified day bin
    Dailypre_Max_O = group_days_Max_O.get_group(groups).reset_index()
    #Get the maximum values for the entire record for that calendar day
    Values_Max_O= Dailypre_Max_O['maximum temperature (degC)']
    #Make it a dataframe so it is appendable
    Values_Max_O = Values_Max_O.to_frame()
    #Append that bin to that day so there will be 366 bins with  x years data for that day
    Daily_Data_Max_O.append(Values_Max_O['maximum temperature (degC)'])
#Minimum
#Everything described above in the maximum section is similar for this minimum section


group_days_Min_O = MinT_1910_1940.groupby(['month','day'])
Daily_Data_Min_O = []
for groups,days in group_days_Min_O:
    Dailypre_Min_O = group_days_Min_O.get_group(groups).reset_index()
    Values_Min_O= Dailypre_Min_O['minimum temperature (degC)']
    Values_Min_O = Values_Min_O.to_frame()
    Daily_Data_Min_O.append(Values_Min_O['minimum temperature (degC)'])
    

#Maximumn/Minimum For the Period Millenial Period
#Minimum
MaxT_1990_2020 =MaxT_Perth[29221:40543]
MinT_1990_2020 = MinT_Perth[29221:40543]




#Separate into monthly and daily bins
group_days_Max_N = MaxT_1990_2020.groupby(['month','day'])
Daily_Data_Max_N = []
for groups,days in group_days_Max_N:
    #Extract the specified day bin
    Dailypre_Max_N = group_days_Max_N.get_group(groups).reset_index()
    #Get the maximum values for the entire record for that calendar day
    Values_Max_N= Dailypre_Max_N['maximum temperature (degC)']
    #Make it a dataframe so it is appendable
    Values_Max_N = Values_Max_N.to_frame()
    #Append that bin to that day so there will be 366 bins with  x years data for that day
    Daily_Data_Max_N.append(Values_Max_N['maximum temperature (degC)'])

#Minimum
#Everything described above in the maximum section is similar for this minimum section.



group_days_Min_N= MinT_1990_2020.groupby(['month','day'])
Daily_Data_Min_N = []
for groups,days in group_days_Min_N:
    Dailypre_Min_N = group_days_Min_N.get_group(groups).reset_index()
    Values_Min_N= Dailypre_Min_N['minimum temperature (degC)']
    Values_Min_N = Values_Min_N.to_frame()
    Daily_Data_Min_N.append(Values_Min_N['minimum temperature (degC)'])
    

#Now generate the 90% and 95th percetile graphs 


CalendarDayMax_Old90 = function_M.TnX_Rolling(7, Daily_Data_Max_O, 90)
CalendarDayMin_Old90 = function_M.TnX_Rolling(7, Daily_Data_Min_O, 90)
CalendarDayMax_New90 = function_M.TnX_Rolling(7, Daily_Data_Max_N, 90)
CalendarDayMin_New90 = function_M.TnX_Rolling(7, Daily_Data_Min_N, 90)
#Now the 15 day percentile for the calendar day.

CalendarDayMax_Old95 = function_M.TnX_Rolling(7, Daily_Data_Max_O, 95)
CalendarDayMin_Old95 = function_M.TnX_Rolling(7, Daily_Data_Min_O, 95)
CalendarDayMax_New95 = function_M.TnX_Rolling(7, Daily_Data_Max_N, 95)
CalendarDayMin_New95 = function_M.TnX_Rolling(7, Daily_Data_Min_N, 95)



#Generate the deviations and statistics for the old and new
#Deviation Graph
Max_Dev90 =  CalendarDayMax_New90 - CalendarDayMax_Old90
Min_Dev90 =  CalendarDayMin_New90 - CalendarDayMin_Old90
Max_Dev95 =  CalendarDayMax_New95 - CalendarDayMax_Old95
Min_Dev95 =  CalendarDayMin_New95 - CalendarDayMin_Old95

#%%



plt.figure(2)
fig, axs = plt.subplots(2, 2, sharex=True,figsize = (27,12))
fig.suptitle('15-Day Window Calendar Day 90$^{th}$ and 95$^{th}$ Percentile (CDP) Temperatures ',fontname="Sans-serif", size=32)

 
axs[0, 0].grid(True, which='both')
axs[1, 0].grid(True, which='both')
axs[1, 1].grid(True, which='both')
axs[0, 1].grid(True, which='both')

axs[0, 0].plot(CalendarDayMax_Old90,color = 'pink')
axs[0, 0].plot(CalendarDayMin_Old90, color = 'cyan')
axs[0, 0].plot(CalendarDayMax_New90, color ='red')
axs[0, 0].plot(CalendarDayMin_New90, color ='blue')
axs[0, 0].set_title('a) 90$^{th}$ CDP',size=26)
axs[0, 0].legend(['1910-1940 CDP Maximum','1910-1940 CDP Maximum','1990-2020 CDP Minimum','1990-2020 CDP Minimum'],loc=9,prop={'size': 14})  
axs[0, 0].set_xlim([0,365])
axs[0, 0].set_ylim([10,45])
axs[0, 0].set_ylabel('Temperature (\N{DEGREE SIGN}C)',size=20)
axs[0, 0].tick_params(labelsize=16)


axs[1, 0].plot(Max_Dev90,color ='red')
axs[1, 0].plot(Min_Dev90, color ='blue')
axs[1, 0].set_title('c) 90$^{th}$ CDP Difference ([1990-2020]-[1910-1940])',size=26)
axs[1, 0].legend(['Maximum Difference','Minimum Difference'],loc=9,prop={'size': 14})
axs[1, 0].axhline(y=0, color='k')
axs[1, 0].set_xlim([0,365])
axs[1, 0].set_ylim([-1,6])
axs[1, 0].set_xlabel('Calendar Day',size=20)
axs[1, 0].set_ylabel('Temperature (\N{DEGREE SIGN}C)',size=20)
axs[1, 0].tick_params(labelsize=16)

axs[0, 1].plot(CalendarDayMax_Old95,color = 'pink')
axs[0, 1].plot(CalendarDayMin_Old95, color = 'cyan')
axs[0, 1].plot(CalendarDayMax_New95, color = 'red')
axs[0, 1].plot(CalendarDayMin_New95, color = 'blue')
axs[0, 1].set_title('b) 95$^{th}$ CDP',size=26)
axs[0, 1].legend(['1910-1940 CDP Maximum','1910-1940 CDP Maximum','1990-2020 CDP Minimum','1990-2020 CDP Minimum'],loc=9,prop={'size': 14})  
axs[0, 1].set_xlim([0,365])
axs[0, 1].set_ylim([10,45])
axs[0, 1].set_ylabel('Temperature (\N{DEGREE SIGN}C)',size=20)
axs[0, 1].tick_params(labelsize=16)

axs[1, 1].plot(Max_Dev95,color ='red')
axs[1, 1].plot(Min_Dev95, color = 'blue')
axs[1, 1].set_title('d) 95$^{th}$ CDP Difference ([1990-2020]-[1910-1940])',size=26)
axs[1, 1].legend(['Maximum Difference','Minimum Difference'],loc=9,prop={'size': 14})
axs[1, 1].axhline(y=0, color='k')
axs[1, 1].set_xlim([0,365])
axs[1, 1].set_ylim([-1,6])
axs[1, 1].set_xlabel('Calendar Day',size=20)
axs[1, 1].set_ylabel('Temperature (\N{DEGREE SIGN}C)',size=20)
axs[1, 1].tick_params(labelsize=16)

months_start = [0,31,60,91,121,152,182,213,244,274,305,335]
month_names =['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
axs[0,0].set_xticks(months_start)
axs[0,0].set_xticklabels(month_names)
axs[0,1].set_xticks(months_start)
axs[0,1].set_xticklabels(month_names)
axs[1,0].set_xticks(months_start)
axs[1,0].set_xticklabels(month_names,size=16)
axs[1,1].set_xticks(months_start)
axs[1,1].set_xticklabels(month_names,size=16)


#%%
#Max90
#Generate the average
Stats_DiffMax90 = stats.describe(Max_Dev90)

#Generate number of days above the non climatic change
count = 0
for i in range(366):
    if (Max_Dev90[i] > 0):
        count = count + 1
Percent_days_above_non_CC_Max90 = 100*count/len(range(366))
print()
print()
print('Percent Days Above')
print(Percent_days_above_non_CC_Max90)
print(Stats_DiffMax90)

#Min90
#Generate the average
Stats_DiffMin90 = stats.describe(Min_Dev90)

#Generate number of days above the non climatic change
count = 0
for i in range(366):
    if (Min_Dev90[i] > 0):
        count = count + 1
Percent_days_above_non_CC_Min90 = 100*count/len(range(366))
print()
print()
print('Percent Days Above')
print(Percent_days_above_non_CC_Min90)
print(Stats_DiffMin90)

#Max95
#Generate the average
Stats_DiffMax95 = stats.describe(Max_Dev95)

#Generate number of days above the non climatic change
count = 0
for i in range(366):
    if (Max_Dev95[i] > 0):
        count = count + 1
Percent_days_above_non_CC_Max95 = 100*count/len(range(366))
print()
print()
print('Percent Days Above')
print(Percent_days_above_non_CC_Max95)
print(Stats_DiffMax95)

#Max95
#Generate the average
Stats_DiffMin95 = stats.describe(Min_Dev95)

#Generate number of days above the non climatic change
count = 0
for i in range(366):
    if (Min_Dev95[i] > 0):
        count = count + 1
Percent_days_above_non_CC_Min95 = 100*count/len(range(366))
print()
print()
print('Percent Days Above')
print(Percent_days_above_non_CC_Min95)
print(Stats_DiffMin95)

#%%
CalendarDayMax_Old50 = function_M.TnX_Rolling(7, Daily_Data_Max_O, 50)
CalendarDayMin_Old50 = function_M.TnX_Rolling(7, Daily_Data_Min_O, 50)
CalendarDayMax_New50 = function_M.TnX_Rolling(7, Daily_Data_Max_N, 50)
CalendarDayMin_New50 = function_M.TnX_Rolling(7, Daily_Data_Min_N, 50)

Max_Dev50 =  CalendarDayMax_New50 - CalendarDayMax_Old50
Min_Dev50 =  CalendarDayMin_New50 - CalendarDayMin_Old50

Stats_DiffMax50 = stats.describe(Max_Dev50)
#Generate number of days above the non climatic change
count = 0
for i in range(366):
    if (Max_Dev50[i] > 0):
        count = count + 1
Percent_days_above_non_CC_Max50 = 100*count/len(range(366))
print()
print()
print('Percent Days Above')
print(Percent_days_above_non_CC_Max50)
print(Stats_DiffMax50)

#Min90
#Generate the average
Stats_DiffMin50 = stats.describe(Min_Dev50)

#Generate number of days above the non climatic change
count = 0
for i in range(366):
    if (Min_Dev50[i] > 0):
        count = count + 1
Percent_days_above_non_CC_Min50 = 100*count/len(range(366))
print()
print()
print('Percent Days Above')
print(Percent_days_above_non_CC_Min50)
print(Stats_DiffMin50)

#%%
