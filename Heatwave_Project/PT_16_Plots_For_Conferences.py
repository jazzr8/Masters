#Plots For Conferences
#%% Load Data and generate the heatwave list

import sys


sys.path.append(r"C:\Users\jarra\Desktop\Masters\Heatwave_Project")
import pandas as pd, PT13_Functions_For_Masters_New_Test as function_M, matplotlib.pyplot as plt, PT5_Functions_For_Masters as function_M1
import pandas as pd
import numpy as np
import matplotlib as mpl
from scipy.stats import pearsonr

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
#%%
Heatwave_85, CDP  =  function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1800,2030], [1961,1990],['Max','Min'],85,7,Dates)


'''
I do not care about the other columns in this, so I can about the heatwave dates only.
'''
#%%
#Only looking at 1911-2020

#So first make the list of decadal years
#Remember heatwave summer is
#1911 Nov 1 to 1921 Mar 31

#Make the bounds wider then the Extended Summer
LowerBound = np.arange(1911,2011+1,10)
UpperBound = np.arange(1921,2021+1,10)
April = 4
October = 10
StartDay = 1
EndDay = 30

np.arange(1911,2011+1,10)
#So we can locate the decadal dates
Heatwave_For_Graph = Heatwave_85.set_index('date')


Number_Heatwaves_Table = []
Durations_Decade_Trend = []
Amplitude_Total_Decade_Trend =[]
Heatwave_Day = []
#Now the for loops for Duration, Total Temperature Max Amplitude degC, number of days under heatwave conditions
for i in range(0,len(LowerBound)):
    #Get the upper bounds for the decade
    Year_Bounds = [LowerBound[i],UpperBound[i]]
    
    #Find the decade
    Decade_Table = Heatwave_For_Graph.loc['{}-{}-{}'.format(Year_Bounds[0],October,StartDay):'{}-{}-{}'.format(Year_Bounds[1],April,EndDay)]
    
    #This is for finding the max value of each event
    find_id_range = [Decade_Table['id'].min(),Decade_Table['id'].max()]
    
    #Find Number Heatwaves Per Year
    number_heatwaves = Decade_Table['id'].max() - Decade_Table['id'].min()
    Number_Heatwaves_Table.append(number_heatwaves)
    Heatwave_Day.append(len(Decade_Table))
    
    Decade_Duration = []
    Decade_Amplitude = []
    
    
    for q in range(find_id_range[0],find_id_range[1]+1):
        
        specific_heatwave = Decade_Table[Decade_Table['id'] == q]
        
        Duration_Heatwave = specific_heatwave['Duration of Heatwaves'].values.mean()
        Decade_Duration.append(Duration_Heatwave)
        
        Amplitude_Heatwave_Total = specific_heatwave['Total Temperature Max Amplitude degC'].values.mean()
        Decade_Amplitude.append(Amplitude_Heatwave_Total)
        
        #So all events fit and we have a even spread, lets look at the top 6 extreme
    Decade_Duration = pd.Series(Decade_Duration).nlargest(5)
    Decade_Amplitude =  pd.Series(Decade_Amplitude).nlargest(5)
        
        
    Decade_Duration_Mean = Decade_Duration.mean()
    Decade_Amplitude_Mean = Decade_Amplitude.mean()
    
        
    Durations_Decade_Trend.append(Decade_Duration_Mean)
    Amplitude_Total_Decade_Trend.append(Decade_Amplitude_Mean)
    
    
    


Decade = ['1910s','1920s','1930s','1940s','1950s','1960s','1970s','1980s','1990s','2000s','2010s']
#%%
#Plots of the Top 6 events of the decade



Durations_Decade_Trend= pd.Series(Durations_Decade_Trend)
Amplitude_Total_Decade_Trend= pd.Series(Amplitude_Total_Decade_Trend)
Heatwave_Day= pd.Series(Heatwave_Day)
Number_Heatwaves_Table= pd.Series(Number_Heatwaves_Table)





plt.figure(1,figsize = (8,5))
plt.plot(Decade,Number_Heatwaves_Table.rolling(3,center=True).mean(),color ='red')
plt.scatter(Decade,Number_Heatwaves_Table,s=100,c='black', marker = 'X')

plt.title("Number of Heatwaves Each Decade",fontsize=20)
plt.ylabel("Number of Heatwaves",fontsize=12)
plt.legend(['3 Decade Moving Mean','Number of Heatwaves'])
plt.grid(axis = 'y')


plt.figure(4,figsize = (8,5))
plt.plot(Decade,Heatwave_Day.rolling(3,center=True).mean(),color ='red')
plt.scatter(Decade,Heatwave_Day,s=100,c='black', marker = 'X')

plt.title("Decadel Days Under Heatwave Conditions",fontsize=20)
plt.ylabel("Heatwave Days (days)",fontsize=12)
plt.legend(['3 Decade Moving Mean','Heatwaves Days Per Decade','3 Decade Moving Mean'])
plt.grid(axis = 'y')

plt.figure(2,figsize = (8,5))
plt.plot(Decade,Durations_Decade_Trend.rolling(3,center=True).mean(),color ='red')
plt.scatter(Decade,Durations_Decade_Trend,s=100,c='black', marker = 'X')

plt.title("Average Duration of the Top 5 Heatwaves",fontsize=20)
plt.ylabel("Duration (days)",fontsize=12)
plt.legend(['3 Decade Moving Mean', 'Duration'])
plt.grid(axis = 'y')

plt.figure(3,figsize = (8,5))
plt.plot(Decade,Amplitude_Total_Decade_Trend.rolling(3,center=True).mean(),color ='red')
plt.scatter(Decade,Amplitude_Total_Decade_Trend,s=100,c='black', marker = 'X')
plt.title("Average Day and Night Amplitude Combination of the Top 5 Heatwaves",fontsize=20)
plt.ylabel("Temperature (\N{DEGREE SIGN}C)",fontsize=12)
plt.legend(['3 Decade Moving Mean','Amplitude Temperature'])
plt.grid(axis = 'y')
#Indiviudal Amplitudes are Based of the difference between the Observed Temperature and the 85th percentile of that day.

#The 85th percentile means the temperature that the day in focus must exceed in order to be in the top 15% of all temperatures.


#plt.plot(CDP['date'],CDP['Temp Max'])


#%%

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
#Max/Min Temp, (drop(0) has dropped the 0th index, so it starts at 1)
T_Perth = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\Perth_1880_2021.csv").drop(0)

#Ave Temp
AveT_Perth = (T_Perth['Max']+T_Perth['Min'])/2

'''Temperature Dataset
This has the date, three temperature datasets altogether
'''
Maximum = pd.Series(T_Perth['Max'], name="Max")
Minimum = pd.Series(T_Perth['Min'], name="Min")
Average = pd.Series(AveT_Perth, name="Ave")

#The Daily Max Min Ave Data
Daily_MaxMin = pd.concat([T_Perth['date'],Maximum,Minimum,Average],axis=1)
'''
PERTH REG TO PERTH ACORN SAT COMP 1967-1992
Using the 1961-1990 dataset and a percentile of 85% moderate heatwaves and 90% for extreme heatwaves.
'''
Heatwave_85  =  function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1800,2030], [1961,1990],['Max','Min'],85,7,Dates)


'''
I do not care about the other columns in this, so I can about the heatwave dates only.
'''

#%%
date_sr = pd.Series(pd.date_range('2019-12-31', periods=3, freq='M', tz='Asia/Calcutta'))
 
# Creating the index
ind = ['Day 1', 'Day 2', 'Day 3']
 
# set the index
date_sr.index = ind
dates = pd.to_datetime(Daily_MaxMin['date'])

change_format = dates.dt.strftime('%d/%m/%Y')
 
# Print the formatted date
print(change_format)



Daily_MaxMin['date'] = pd.to_datetime(Daily_MaxMin['date'])
#Daily_MaxMin['date'] =  Daily_MaxMin['date'].dt.strftime('%d/%m/%Y')
print(Daily_MaxMin)
#Had to use 2 versions for the CDP and for the rest of the functions
Data_not_expand = Daily_MaxMin
Daily_MaxMin = function_M.Date_Splitter(Daily_MaxMin, 'date')





















#%%
'''
This is the bar graph where I find the number of heatwave events each period
1911-1940
1951-1980
1991-2020*

For different base periods
1911-1940,
1916-1945 etc etc
'''

#First lets do the moving base period
LowerBoundBP = np.arange(1911,1991+1,5)
UpperBoundBP = np.arange(1940,2020+1,5)

#cCapture the extended summer
April = 4
October = 10
StartDay = 1
EndDay = 30

#Now add a for loop into this

Heatwave_E = []
Heatwave_M = []
Heatwave_L = []
for i in range(0,len(UpperBoundBP)):
    #Find the heatwaves
    Heatwaves, CDP_periods  =  function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1800,2030], [LowerBoundBP[i],UpperBoundBP[i]],['Max','Min'],85,7,Dates)
    
    #Now split into 3 periods
    Heatwaves = Heatwaves.set_index('date')
    
    Heatwaves_Early = Heatwaves.loc['1911-10-1':'1940-4-30']
    Heatwaves_Mid = Heatwaves.loc['1951-10-1':'1980-4-30']
    Heatwaves_Late = Heatwaves.loc['1991-10-1':'2020-4-30']

    
    #Number of heatwaves for each period
    
    events_e = Heatwaves_Early['id'].max() - Heatwaves_Early['id'].min()
    events_m = Heatwaves_Mid['id'].max() - Heatwaves_Mid['id'].min()
    events_l = Heatwaves_Late['id'].max() - Heatwaves_Late['id'].min()
    
    #Append the number to the rest
    Heatwave_E.append(events_e)
    Heatwave_M.append(events_m)
    Heatwave_L.append(events_l)


'''
If climate change wasnt effecting heatwaves we would see no change in the number of heatwaves events in total and not change in the number of heatwave events in 
each decade

If climate change is occuring I expect to see the change in the number of heatwave events begin in the 1931-1960 periods and begun to decrease as hotter temperatures
mean that the older periods will not have as effective heatwaves as the current period. That is my hypthosesis
'''
Base_Periods = []
for i in range(0,len(UpperBoundBP)):
    xx = '{}-{}'.format(LowerBoundBP[i],UpperBoundBP[i])
    Base_Periods.append(xx)
    
plt.figure(figsize = (20,10))   
plt.bar(Base_Periods, Heatwave_E, color='r')
plt.bar(Base_Periods, Heatwave_M, bottom=Heatwave_E, color='b')
plt.bar(Base_Periods, Heatwave_L, bottom=np.add(Heatwave_M,Heatwave_E), color='g')

plt.xlabel("CDP Period")
plt.ylabel("Heatwaves")
plt.legend(["1911-1940", "1951-1980", "1991-2020*"])
plt.title("Number of Heatwaves Compared to Different 85% CDP Periods")
plt.show()


#Percentage based
Total_Heatwaves = np.add(np.add(Heatwave_M,Heatwave_E),Heatwave_L)
Percentage_E = np.multiply(np.divide(Heatwave_E,Total_Heatwaves),100)
Percentage_M = np.multiply(np.divide(Heatwave_M,Total_Heatwaves),100)
Percentage_L = np.multiply(np.divide(Heatwave_L,Total_Heatwaves),100)


Base_Periods = []
for i in range(0,len(UpperBoundBP)):
    xx = '{}-{}'.format(LowerBoundBP[i],UpperBoundBP[i])
    Base_Periods.append(xx)
    
plt.figure(figsize = (20,10))   
plt.bar(Base_Periods, Percentage_E, color='r')
plt.bar(Base_Periods, Percentage_M, bottom=Percentage_E, color='b')
plt.bar(Base_Periods, Percentage_L, bottom=np.add(Percentage_E,Percentage_M), color='g')

plt.xlabel("CDP Period")
plt.ylabel("Heatwaves/Total Heatwaves")
plt.legend(["1911-1940", "1951-1980", "1991-2020*"])
plt.title("Percentage of Heatwaves from each period Compared to Different 85% CDP Periods")
plt.ylim([0,100])
plt.show()


'''
From my hypothesis I was bang on, the number of heatwaves remained with my statement of that we will see a drop from a CDP climatoloigcal period of 1931-1960

what is interesting is that the percentage that the number of heatwave evetns as a percentage remains constant thorughout the entirety of the different refecne periods

2008 doesnt have full data therefore this may have altered the number of heatwave evvents but only by 1 or 2 in the 1991-2020 period
'''
