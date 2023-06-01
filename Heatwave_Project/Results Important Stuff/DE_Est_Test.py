#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# # 0. Load Packages
# 

# In[1]:


from bisect import bisect_left
import sys
sys.path.append(r"C:\Users\jarra\Desktop\Masters\Heatwave_Project")
import pandas as pd
import PT13_Functions_For_Masters_New_Test as HW_Func
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
from scipy.stats import spearmanr
import scipy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings("ignore")
#RMSE 
from sklearn.metrics import mean_squared_error
from math import sqrt
from datetime import datetime


# # 0.1 Data Involved

# In[3]:


P_Gardens = pd.read_csv(r"E:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\perthgardens_daily_1880-1900.csv")
P_Gardens_Corr = pd.read_csv(r"E:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\perthgardens_daily_corrected_1880-1900.csv")

#Now we need to go back in time and minus 200 years off the date
#Convert To Datetime

P_Gardens['time'] = pd.to_datetime(P_Gardens['time'],format="%d/%m/%Y")
P_Gardens_Corr['time'] = pd.to_datetime(P_Gardens_Corr['time'],format="%d/%m/%Y")

#Split the Year up

P_Gardens = HW_Func.Date_Splitter(P_Gardens,'time',single= True)
P_Gardens_Corr = HW_Func.Date_Splitter(P_Gardens_Corr,'time',single= True)
P_Gardens['year'] = P_Gardens['year']-200
P_Gardens_Corr['year'] = P_Gardens_Corr['year']-200
#Combine in same format as ACORN-SAT

cols=["year","month","day"]
P_Gardens['date'] = P_Gardens[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")
P_Gardens_Corr['date'] = P_Gardens_Corr[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")

del P_Gardens['time']
del P_Gardens_Corr['time']
del P_Gardens['year']
del P_Gardens_Corr['year']
del P_Gardens['month']
del P_Gardens_Corr['month']
del P_Gardens['day']
del P_Gardens_Corr['day']

P_Gardens['date'] = pd.to_datetime(P_Gardens['date'],format="%Y/%m/%d")
P_Gardens_Corr['date'] = pd.to_datetime(P_Gardens_Corr['date'],format="%Y/%m/%d")

#Max Temp, (drop(0) has dropped the 0th index, so it starts at 1)
MaxT_Perth = pd.read_csv(r"E:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\UPDATED TMAX, TMIN ACORN-SAT\tmax.009021.daily (3).csv").drop(0)
#Min Temp
MinT_Perth = pd.read_csv(r"E:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\UPDATED TMAX, TMIN ACORN-SAT\tmin.009021.daily (2).csv").drop(0)
#Ave Temp
AvgT_Perth = (MaxT_Perth['maximum temperature (degC)']+MinT_Perth['minimum temperature (degC)'])/2

Maximum = pd.Series(MaxT_Perth['maximum temperature (degC)'], name="Max")
Minimum = pd.Series(MinT_Perth['minimum temperature (degC)'],name="Min")
Average = pd.Series(AvgT_Perth,name="Avg")

#The Daily Max Min Ave Data
ACORN_SAT = pd.concat([MaxT_Perth['date'],Maximum,Minimum,Average],axis=1)
ACORN_SAT['date'] = pd.to_datetime(ACORN_SAT['date'],format="%Y/%m/%d")



#Now load in and fix Perth Gardens 1830-1875
Per_Gard = pd.read_csv(r"E:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\swanriver_subdaily_1830-1875.csv")
Per_Gard
#Set Datetime
Per_Gard['date'] = pd.to_datetime(Per_Gard['date'],dayfirst = True)
    

#So this works, now we need to expand this into a for loop and make this a new dataframe to be added onto
#the historical time because it will make things easier



#Can't set index yet.
#Perth Regional Office 1967 to 1992 sub daily dataset
PRO_Sub = pd.read_csv(r"E:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\perthregionaloffice_subdaily_1942-1992.csv")

PRO_Sub['date'] = pd.to_datetime(PRO_Sub['date'],dayfirst = True)
PRO_Sub = PRO_Sub.set_index('date')
PRO_Sub =PRO_Sub['temp']/10 

PRO_Sub_ES  = PRO_Sub.loc['1967':'1992']
PRO_Sub_ES =PRO_Sub_ES

## Perth Regional Office Daily Extreme Dataset
#Load PRO in
#BOM PERTH REGIONAL OFFICE
MaxT_PRO = pd.read_csv(r"E:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\IDCJAC0010_009034_1800_Data.csv")
MinT_PRO = pd.read_csv(r"E:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\IDCJAC0011_009034_1800_Data.csv")

#Clean The data
MaxT_PRO['Datetime']= pd.to_datetime(MaxT_PRO[['Year', 'Month', 'Day']])
MinT_PRO['Datetime']= pd.to_datetime(MinT_PRO[['Year', 'Month', 'Day']])

#Delete irrelevent columns
del MaxT_PRO['Product code']
del MaxT_PRO['Bureau of Meteorology station number']
del MaxT_PRO['Year']
del MaxT_PRO['Month']
del MaxT_PRO['Day']
del MaxT_PRO['Days of accumulation of maximum temperature']
del MaxT_PRO['Quality']
del MinT_PRO['Product code']
del MinT_PRO['Bureau of Meteorology station number']
del MinT_PRO['Year']
del MinT_PRO['Month']
del MinT_PRO['Day']
del MinT_PRO['Days of accumulation of minimum temperature']
del MinT_PRO['Quality']

#Change the column name to date
MaxT_PRO= MaxT_PRO.rename(columns={'Datetime':'date'})
MinT_PRO= MinT_PRO.rename(columns={'Datetime':'date'})


#Change the column names
MaxT_PRO= MaxT_PRO.rename(columns={'Maximum temperature (Degree C)':'PRO Max'})
MinT_PRO= MinT_PRO.rename(columns={'Minimum temperature (Degree C)':'PRO Min'})

#Now concat it
MaxT_PRO= MaxT_PRO.set_index('date')
MinT_PRO= MinT_PRO.set_index('date')

PRO_DE = pd.merge(left = MaxT_PRO,right  =MinT_PRO,left_index=True,right_index=True  )

#Training Data
PRO_DE_Training = PRO_DE.loc['1967':'1992']
PRO_Sub_Training = PRO_Sub_ES
#Estimating Data
PRO_Sub_4_Est = PRO_Sub.reset_index()


# In[4]:


T_Ext =PRO_DE_Training.reset_index()
T_Sub =PRO_Sub_ES.reset_index()
S_Est = PRO_Sub_4_Est
S_Est


# In[26]:



Per_Gard


# # 0. Core Function
# 

# In[29]:


def Temp_Estimation(Sub_Daily, Sub_Daily_Training,Daily_Extreme_Training, Trials, Sim_Comp):
    '''
    Parameters
    --------------
    Sub_Daily : DataFrame
        This is the raw subdaily data you aim to estimate the maximum and minimum temperatures from.
    
    Sub_Daily_Training : DataFrame
        A list with the date and temp as 2 columns and index going from 0,1...X. All values are subdaily so they have hours
        associated with them also time is in 24 hour format.
        
    Daily_Extreme_Training : DataFrame
        A list with the date and temp as 3 columns and index going from 0,1...X. All values are daily with max and min
        associated with them also time is in 24 hour format.
     
    Trials : Integer
        The number of trails you want to run the estimation training over.
    
    Sim_Comp : 0,1 or 2
    0 is simple, 1 is complex v1 amd 2 is complex v2
    '''
    
    
    
    # Part 1: Split the Sub_Daily Training into individual hours ane combine
    Sub_Max, Sub_Min, Hours_Avaliable = Sub_Daily_Splitter(Sub_Daily_Training)
    
    # Part 2: Concat the Maximum and Minimum Data to the subdaily data
    Sub_Ext_Max, Sub_Ext_Min = concat_max_sub(Sub_Max, Sub_Min, Hours_Avaliable, Daily_Extreme_Training)
    
    #Now Every Single Available hour and max and min is ready to be used.
    #Part 3: Split into each respective Month and add all together so its like Month_Hour_Mx/Mn
    Monthly_Split_Dic = Month_Splitter(Hours_Avaliable,Sub_Ext_Max, Sub_Ext_Min)
    
    #Include 24 in the hours avalaible, this is to get it back to 0
    Hours_Avaliable_Inc_24 = Hours_Avaliable.copy()
    Hours_Avaliable_Inc_24.append(24)
    
    #PART 4 Is to fix up the Historical Data so it is closest to the every hour hour mark where data is avaliable
    Sub_Daily = Closest_Hour(Sub_Daily, Hours_Avaliable_Inc_24)
    
    #PART 5 Is to sample by the length of the number of datapoints for that month and max or min
    #Now I need to select 600 points and trail it 1000 times for each single thing in the dictionary and label the hour 0 as hour 0 run 1]
    #and PRO Max Run 1
    Sampled = Sampler_Trainer(Monthly_Split_Dic,Trials)
    
    #Part 6
    #Now to apply the regression anaylsis onto the data I have provide
    Linear_Analysis = Linear_Regression_Analysis(Trials, Hours_Avaliable, Sampled)
    
    #Part 7    
    #Get the data into their respective max and min with the hours matching the regression data, look at the explabations
    #above in Part 2 and Part 7 for more information
    Max_Data = Max_Sub(Sub_Daily)
    
    Min_Data= Min_Sub(Sub_Daily)
    
    #Part 8 Temperature Estimation
    Full_Temperature_Estimation= Tmax_Tmin_All_Data_Est(Trials, Max_Data, Min_Data, Linear_Analysis)
    
    #Part 9 The Best Temperature Estimation
    Temperature_Estimation = Absolute_Estimation(Full_Temperature_Estimation, Trials, Sim_Comp)
    
    return(Temperature_Estimation)


#A = Temp_Estimation(S_Est, T_Sub,T_Ext,1, 0)
#B = Temp_Estimation(S_Est, T_Sub,T_Ext,1, 1)
C= Temp_Estimation(Per_Gard, T_Sub,T_Ext,50, 2)


# In[30]:


C


# In[31]:


T1 = C.get('Trial_1')
T2 = C.get('Trial_2')
T3 = C.get('Trial_3')


# In[32]:


plt.plot(T1['Min Temp Estimation'])
plt.plot(T2['Min Temp Estimation'])
plt.plot(T3['Min Temp Estimation'])

plt.plot(PRO_DE['PRO Min'])


# In[33]:


print('All Data TMAX')

actualmx = PRO_DE['PRO Max'].loc['1942-01-01':'1992-04-29']
predmx = T2['Max Temp Estimation'].loc['1942-01-01':'1992-04-29']
Maximum = pd.concat([actualmx,predmx], axis =1).dropna()
RMSEMx = sqrt(mean_squared_error(Maximum['PRO Max'], Maximum['Max Temp Estimation']))
print('Complex 1')
print(RMSEMx)
Diff = (predmx - actualmx).mean()
print(Diff)

actualmx = PRO_DE['PRO Max'].loc['1942-01-01':'1992-04-29']
predmx = T3['Max Temp Estimation'].loc['1942-01-01':'1992-04-29']
Maximum = pd.concat([actualmx,predmx], axis =1).dropna()
RMSEMx = sqrt(mean_squared_error(Maximum['PRO Max'], Maximum['Max Temp Estimation']))
print('Complex 2')
print(RMSEMx)
Diff = (predmx - actualmx).mean()
print(Diff)

actualmx = PRO_DE['PRO Max'].loc['1942-01-01':'1992-04-29']
predmx = T1['Max Temp Estimation'].loc['1942-01-01':'1992-04-29']
Maximum = pd.concat([actualmx,predmx], axis =1).dropna()
RMSEMx = sqrt(mean_squared_error(Maximum['PRO Max'], Maximum['Max Temp Estimation']))
print('Simple')
print(RMSEMx)
Diff = (predmx - actualmx).mean()
print(Diff)
print('-------')

print('1942-1962')
actualmx = PRO_DE['PRO Max'].loc['1942-01-01':'1962-04-29']
predmx = T2['Max Temp Estimation'].loc['1942-01-01':'1962-04-29']
Maximum = pd.concat([actualmx,predmx], axis =1).dropna()
RMSEMx = sqrt(mean_squared_error(Maximum['PRO Max'], Maximum['Max Temp Estimation']))
print('Complex 1')
print(RMSEMx)
Diff = (predmx - actualmx).mean()
print(Diff)

actualmx = PRO_DE['PRO Max'].loc['1942-01-01':'1992-04-29']
predmx = T3['Max Temp Estimation'].loc['1942-01-01':'1992-04-29']
Maximum = pd.concat([actualmx,predmx], axis =1).dropna()
RMSEMx = sqrt(mean_squared_error(Maximum['PRO Max'], Maximum['Max Temp Estimation']))
print('Complex 2')
print(RMSEMx)
Diff = (predmx - actualmx).mean()
print(Diff)

actualmx = PRO_DE['PRO Max'].loc['1942-01-01':'1962-04-29']
predmx = T1['Max Temp Estimation'].loc['1942-01-01':'1962-04-29']
Maximum = pd.concat([actualmx,predmx], axis =1).dropna()
RMSEMx = sqrt(mean_squared_error(Maximum['PRO Max'], Maximum['Max Temp Estimation']))
print('Simple')
print(RMSEMx)
Diff = (predmx - actualmx).mean()
print(Diff)
print('-------')

print('1962-1992')

actualmx = PRO_DE['PRO Max'].loc['1962-01-01':'1992-04-29']
predmx = T2['Max Temp Estimation'].loc['1962-01-01':'1992-04-29']
Maximum = pd.concat([actualmx,predmx], axis =1).dropna()
RMSEMx = sqrt(mean_squared_error(Maximum['PRO Max'], Maximum['Max Temp Estimation']))
print('Complex 1')
print(RMSEMx)
Diff = (predmx - actualmx).mean()
print(Diff)

actualmx = PRO_DE['PRO Max'].loc['1942-01-01':'1992-04-29']
predmx = T3['Max Temp Estimation'].loc['1942-01-01':'1992-04-29']
Maximum = pd.concat([actualmx,predmx], axis =1).dropna()
RMSEMx = sqrt(mean_squared_error(Maximum['PRO Max'], Maximum['Max Temp Estimation']))
print('Complex 2')
print(RMSEMx)
Diff = (predmx - actualmx).mean()
print(Diff)

actualmx = PRO_DE['PRO Max'].loc['1962-01-01':'1992-04-29']
predmx = T1['Max Temp Estimation'].loc['1962-01-01':'1992-04-29']
Maximum = pd.concat([actualmx,predmx], axis =1).dropna()
RMSEMx = sqrt(mean_squared_error(Maximum['PRO Max'], Maximum['Max Temp Estimation']))
print('Simple')
print(RMSEMx)
Diff = (predmx - actualmx).mean()
print(Diff)
print('-------')


# In[53]:


print('All Data')
actualmn = PRO_DE['PRO Min'].loc['1942-01-01':'1992-04-29']
predmn = T2['Min Temp Estimation'].loc['1942-01-01':'1992-04-29']
Minimum = pd.concat([actualmn,predmn], axis =1).dropna()
RMSEMn = sqrt(mean_squared_error(Minimum['PRO Min'], Minimum['Min Temp Estimation']))
print('Complex 1')
print(RMSEMn)
Diff = (predmn - actualmn).mean()
print(Diff)

actualmn = PRO_DE['PRO Min'].loc['1942-01-01':'1992-04-29']
predmn = T3['Min Temp Estimation'].loc['1942-01-01':'1992-04-29']
Minimum = pd.concat([actualmn,predmn], axis =1).dropna()
RMSEMn = sqrt(mean_squared_error(Minimum['PRO Min'], Minimum['Min Temp Estimation']))
print('Complex 2')
print(RMSEMn)
Diff = (predmn - actualmn).mean()
print(Diff)

actualmn = PRO_DE['PRO Min'].loc['1942-01-01':'1992-04-29']
predmn = T1['Min Temp Estimation'].loc['1942-01-01':'1992-04-29']
Minimum = pd.concat([actualmn,predmn], axis =1).dropna()
RMSEMn = sqrt(mean_squared_error(Minimum['PRO Min'], Minimum['Min Temp Estimation']))
print('Simple')

print(RMSEMn)
Diff = (predmn - actualmn).mean()
print(Diff)
print('-------')

print('1942-1962')
actualmn = PRO_DE['PRO Min'].loc['1942-01-01':'1962-04-29']
predmn = T2['Min Temp Estimation'].loc['1942-01-01':'1962-04-29']
Minimum = pd.concat([actualmn,predmn], axis =1).dropna()
RMSEMn = sqrt(mean_squared_error(Minimum['PRO Min'], Minimum['Min Temp Estimation']))

print('Complex 1')
print(RMSEMn)
Diff = (predmn - actualmn).mean()
print(Diff)

actualmn = PRO_DE['PRO Min'].loc['1942-01-01':'1992-04-29']
predmn = T3['Min Temp Estimation'].loc['1942-01-01':'1992-04-29']
Minimum = pd.concat([actualmn,predmn], axis =1).dropna()
RMSEMn = sqrt(mean_squared_error(Minimum['PRO Min'], Minimum['Min Temp Estimation']))
print('Complex 2')
print(RMSEMn)
Diff = (predmn - actualmn).mean()
print(Diff)

actualmn = PRO_DE['PRO Min'].loc['1942-01-01':'1962-04-29']
predmn = T1['Min Temp Estimation'].loc['1942-01-01':'1962-04-29']
Minimum = pd.concat([actualmn,predmn], axis =1).dropna()
RMSEMn = sqrt(mean_squared_error(Minimum['PRO Min'], Minimum['Min Temp Estimation']))
print('Simple')
print(RMSEMn)
Diff = (predmn - actualmn).mean()
print(Diff)
print('-------')

print('1962-1992')
actualmn = PRO_DE['PRO Min'].loc['1962-01-01':'1992-04-29']
predmn = T2['Min Temp Estimation'].loc['1962-01-01':'1992-04-29']
Minimum = pd.concat([actualmn,predmn], axis =1).dropna()
RMSEMn = sqrt(mean_squared_error(Minimum['PRO Min'], Minimum['Min Temp Estimation']))
print('Complex 1')
print(RMSEMn)
Diff = (predmn - actualmn).mean()
print(Diff)


actualmn = PRO_DE['PRO Min'].loc['1942-01-01':'1992-04-29']
predmn = T3['Min Temp Estimation'].loc['1942-01-01':'1992-04-29']
Minimum = pd.concat([actualmn,predmn], axis =1).dropna()
RMSEMn = sqrt(mean_squared_error(Minimum['PRO Min'], Minimum['Min Temp Estimation']))
print('Complex 2')
print(RMSEMn)
Diff = (predmn - actualmn).mean()
print(Diff)

actualmn = PRO_DE['PRO Min'].loc['1962-01-01':'1992-04-29']
predmn = T1['Min Temp Estimation'].loc['1962-01-01':'1992-04-29']
Minimum = pd.concat([actualmn,predmn], axis =1).dropna()
RMSEMn = sqrt(mean_squared_error(Minimum['PRO Min'], Minimum['Min Temp Estimation']))
print('Simple')
print(RMSEMn)
Diff = (predmn - actualmn).mean()
print(Diff)
print('-------')


# ### All Data
# 
# RMSE
# 
# 2.1788581660527937
# 
# MEAN DIF OBSERVE - ESTIMATED
# 
# -0.165377988583119
# 
# -------
# 
# 2.4558149115501577
# 
# 0.24353437788586618
# 
# 
# -------
# 
# ### 1942-1962
# 
# 2.034281042565149
# 
# 0.18031951354528136
# 
# -------
# 
# 2.302497689804424
# 
# 0.5435511213715878
# 
# -------
# 
# ### 1962-1992
# 
# 2.2697273055266103
# 
# -0.39445136773750417
# 
# -------
# 
# 2.5525800283463616
# 
# 0.043628751927303325
# 
# 
# -------

# In[34]:


#Plot T
#1830-1875 resample
for 
PRO_1 = T1.resample('Y').mean().reset_index()
PRO_2 = T2.resample('Y').mean().reset_index()
PRO_3 = T3.resample('Y').mean().reset_index()


#PRO DE
PRO_DE_Y = PRO_DE.resample('Y').mean().reset_index()

#ACORN_SAT
ACORN_SAT_Y = ACORN_SAT.set_index('date').resample('Y').mean().reset_index()

#P_Gardens|
P_Gardens_Y =  P_Gardens.set_index('date').resample('Y').mean().reset_index()

P_Gardens_CORR_Y = P_Gardens_Corr.set_index('date').resample('Y').mean().reset_index()


# In[41]:


Keys = list(C)
Keys


# In[47]:


plt.figure(1,figsize= [15,10])
#Historical Estimation

for i in Keys:
    T = C.get(i)
    T1 = T.resample('Y').mean()
    
    #Current Estimation
    plt.plot(T1['Max Temp Estimation'],linewidth=0.3,label = 'Simple Code',color = 'blue')
    

T1 = C.get('Trial_1')
T2 = C.get('Trial_2')
T3 = C.get('Trial_3')

#Current Estimation
plt.plot(PRO_1['date'],PRO_1['Max Temp Estimation'],linewidth=0.3,label = 'Simple Code',color = 'blue')
plt.plot(PRO_2['date'],PRO_2['Max Temp Estimation'],linewidth=0.3,label = 'Complex 1 Code',color = 'black')

#plt.plot(PRO_3['date'],PRO_3['Max Temp Estimation'],linewidth=0.3,label = 'Complex 2 Code',color = 'green')



#PRO DE
#plt.plot(PRO_DE_Y['date'],PRO_DE_Y['PRO Max'],linewidth=1.5,label = 'Perth Reg Office Observed Max',color = 'red')

#ACORN_SAT
#plt.plot(ACORN_SAT_Y['date'],ACORN_SAT_Y['Max'],linewidth=1.5,label = 'ACORN-SAT Max',color = 'green')

#Perth Gardens
#plt.plot(P_Gardens_Y['date'],P_Gardens_Y['tmax'],linewidth=1.5,label = 'Perth Gardens Uncorrected Max',color = 'cyan')

#plt.plot(P_Gardens_CORR_Y['date'],P_Gardens_CORR_Y['tmax'],linewidth=1.5, label = 'Perth Gardens Corrected Max',color = 'orange')

plt.legend()

plt.ylabel('Temperature (degC)')
plt.xlabel('Date')
plt.title('Average Yearly Maximum Temperature')


# In[38]:


plt.figure(1,figsize= [15,10])
#Historical Estimation


#Current Estimation
plt.plot(PRO_1['date'],PRO_1['Min Temp Estimation'],linewidth=0.3,label = 'Simple',color = 'blue')
#Current Estimation
plt.plot(PRO_2['date'],PRO_2['Min Temp Estimation'],linewidth=0.3,label = 'Complex 1',color = 'black')

plt.plot(PRO_3['date'],PRO_3['Min Temp Estimation'],linewidth=0.3,label = 'Complex 2',color = 'green')


#PRO DE
plt.plot(PRO_DE_Y['date'],PRO_DE_Y['PRO Min'],linewidth=1.5,label = 'Perth Reg Office Observed Min',color = 'red')

#ACORN_SAT
plt.plot(ACORN_SAT_Y['date'],ACORN_SAT_Y['Min'],linewidth=1.5,label = 'ACORN-SAT Min',color = 'green')

#Perth Gardens
#plt.plot(P_Gardens_Y['date'],P_Gardens_Y['tmin'],linewidth=1.5,label = 'Perth Gardens Uncorrected Min',color = 'cyan')

#plt.plot(P_Gardens_CORR_Y['date'],P_Gardens_CORR_Y['tmin'],linewidth=1.5, label = 'Perth Gardens Corrected Min',color = 'orange')

plt.legend()

plt.ylabel('Temperature (degC)')
plt.xlabel('Date')
plt.title('Average Yearly Minimum Temperature')


# For max, I would choose the complex1 version as RMSE is at its lowest and its pretty much 1 for 1.
# 

# # 1. Sub_Daily Splitter

# In[7]:


def Sub_Daily_Splitter(Data):
    '''
    Parameters
    --------------
    
    Data : DataFrame
        A list with the date and temp as 2 columns and index going from 0,1...X. All values are subdaily so they have hours
        associated with them.
        
    Return
    ------------
    Sub_Max : Dictionary/DataFrames
        The respective hours and the shifts to fit the regression and tmax calculation like the BOM has done is
    Sub_Min : Dictionary/DataFrames
        The respective hours and the shifts to fit the regression and tmin calculation like the BOM has done is
    Hours_Avaliable : Array
        All the hours that have at least 10 years worth of data
        
    '''
    #Set datetime to date
    Data_Col = Data.columns
    Data = Data.set_index(Data_Col[0])
    
    #We need the hours in 24 hour format as a list.
    Every_Hour = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    
    #Now to create the dictionaries necessary for the splitting.
    Sub_Hourly_Dic = {}
    # Hours_Avaliable is different to Every_Hour as it finds hours that have data with at least 10 years worth of data.
    Hours_Avaliable = []
    
    #Begin the for loop
    for HOUR in Every_Hour:
              
        #Locate all the data for that hour
        Single_Hour_Data = pd.concat([Data[Data.index.hour==HOUR]],axis =0)
        
        #Now to check if the data has at least 10 years worth of Data
        if (len(Single_Hour_Data) >= 3600):
            #If it is then append it into the dictionary
            
            #reset the index to fix the datetime
            Single_Hour_Data = Single_Hour_Data.reset_index()
            #Make sure that datetime is still on the date we used
            Single_Hour_Data[Data_Col[0]] = pd.to_datetime(Single_Hour_Data[Data_Col[0]]).dt.date
            #Set Index back to date, but maybe not if we need to make it for Max and Min
            Single_Hour_Data = Single_Hour_Data.set_index(Data_Col[0]).dropna()
            
            #Add to Dictionaries and columns
            Sub_Hourly_Dic["Hour" +"_"+ str(HOUR)] = Single_Hour_Data
            
            #This becomes useful in the next section where we get information relative to max and min temperatures.
            Hours_Avaliable.append(HOUR)
        
        
    #Now to split the data into the respective Max and Min dictionaries.

    
    '''
    This is a bit of explanation about the choices I make with what horus I choose for this.
    So in my previous versions of creating this function I had to choose the times of when I can locate
    the Tmax and Tmin from. Now what noticed was firstly on the day (+0) the Tmax was generally found between 
    12pm+0 to 6pm+0. So this meant the likelyhood that the max was between 9am+0 to 9am+1. This actually aligns with what 
    times the Tmax is found between 9am+0 to 9am+1. This means that for this we need to shift the hour values of 0am+1 to 8am+1
    to be used on this particular day.
    
    Now there is a trickier part. It is the tmin. Like the tmax, the tmin is calulcated by the BOM from 9am-1 to 9am+0. However
    within my findings it turns out that the correlation at 9am-1 is much lower then at 9am+0, furthermore the afetrnoon of the 
    prvious day has a higher correlation to what the min will be the next day than the correlation of the day in focus.
    This has me belive that the min for the day in focus is influenced much more highly by the temperatures of the previous day
    then the temperature of the day in focus which I will go into further discussion later and read about on papers becasue this 
    is an interesting debate. But to estimate temperature more of this will be explained and explored.
    
    For now, I came to the conculsion that the tmin will be estimated by the 10am-1 to 10am+0 to account for the 9am+0 higher 
    correlation. For tmax it will be like the BOM standard 9am+0 to 9am+1
    '''
    
    #Create the dictionaries for max and min
    Sub_Max = {}
    Sub_Min = {}
    
    #Now for loop with the hours we do have
    for HOURS in Hours_Avaliable:
        #Lets shift the hours
        #Since we know the key was "Hour_HOURS"
        #Extract the DataFrame for that specific hour
        Hourly_Data =  Sub_Hourly_Dic.get('Hour_{}'.format(HOURS))
        
        #MAX
        #Remember 0+0 to 8+1
        if (HOURS in range(0,9)):
            #Shift it negative one which means everything is pushed up, so tomorrows temp is now are todays hour.
            Shift_Max = Hourly_Data.shift(-1, axis = 0).dropna()
            #Append it to max dictionary
            Sub_Max["Hour" +"_"+ str(HOURS)+"+1"] =Shift_Max
        else:
            Shift_Max = Hourly_Data
            #Append it to max dictionary
            Sub_Max["Hour" +"_"+ str(HOURS)+"+0"] = Shift_Max
            
            
        #Min
    
        #Remember 9-1 to 8+0 : IN LINE WITH BOM STANDARDS, SHOULDNT MESS WITH IT

        if (HOURS in range(10,23)):
            #Shift it positive one which means everything is pushed down, so yesterdays temp is now are todays temp.
            Shift_Min = Hourly_Data.shift(1, axis = 0).dropna()
            #Append it to min dictionary
            Sub_Min["Hour" +"_"+ str(HOURS)+"-1"] =Shift_Min
        else:
            Shift_Min = Hourly_Data
            #Append it to max dictionary
            Sub_Min["Hour" +"_"+ str(HOURS)+"+0"] = Shift_Min
    
    
    
    return(Sub_Max, Sub_Min, Hours_Avaliable)
    


# # 2. Combine the subdaily to the respective Training Max and Min

# In[8]:


def concat_max_sub(Sub_Max,Sub_Min,Hours_Avaliable, DE_values):
    '''
    Parameters
    --------------
    Sub_Max : Dictionary/DataFrames
        The respective hours and the shifts to fit the regression and tmax calculation like the BOM has done is
    Sub_Min : Dictionary/DataFrames
        The respective hours and the shifts to fit the regression and tmin calculation like the BOM has done is
    Hours_Avaliable : Array
        All the hours that have at least 10 years worth of data
    DE_values : DataFrame
        A list with the date and temp as 3 columns and index going from 0,1...X. All values are daily with max and min
        associated with them also time is in 24 hour format.
    
    Return
    ------------
    Sub_Mx : Dictionary/DataFrame
        A dictionary of many dataframes that associate the Tmax with the subdaily values of that day
    
    Sub_Mn : Dictionary/DataFrame
        A dictionary of many dataframes that associate the Tmin with the subdaily values of that day
    '''
    DE_values_col = DE_values.columns
    DE_values = DE_values.set_index(DE_values_col[0])
    
    
    #Create the and Min dictionaries
    Sub_Mx = {}
    Sub_Mn = {}
    
    #Extract the max and min keys
    Keys_Mx = list(Sub_Max)
    Keys_Mn = list(Sub_Min)

    #Go with Tmax
    for i in range(len(Keys_Mx)):
        #Extract the subdaily data for that hour
        Mx_Sub = Sub_Max.get(Keys_Mx[i])
        #Combine with Tmax where datetime si the joiner
        Combined_Train_Mx = pd.merge(left = Mx_Sub, 
                                        right  =DE_values[DE_values_col[1]],
                                        left_index=True,right_index=True  )
        #Rename to Max
        Combined_Train_Mx = Combined_Train_Mx.rename(columns={DE_values_col[1]:'Max'})
        #Append to dictioanry 
        Sub_Mx["Hour" +"_"+ str(Hours_Avaliable[i])] = Combined_Train_Mx
        
    #Min follow similar as Max
    for j in range(len(Keys_Mn)):
        #Extract the subdaily data for that hour
        Mn_Sub = Sub_Min.get(Keys_Mn[j])
        #Combine with Tmax where datetime si the joiner
        Combined_Train_Mn = pd.merge(left = Mn_Sub, 
                                        right  =DE_values[DE_values_col[2]],
                                        left_index=True,right_index=True  )
        Combined_Train_Mn = Combined_Train_Mn.rename(columns={DE_values_col[2]:'Min'})
        #Append to dictioanry 
        Sub_Mn["Hour" +"_"+ str(Hours_Avaliable[j])] = Combined_Train_Mn
        
        
    return(Sub_Mx,Sub_Mn)


# # 3. Max and Min with Sub-Daily Month Splitter

# In[9]:


# Function that splits it into each month
def Month_Splitter(Hours_Avaliable,Sub_Ext_Max, Sub_Ext_Min):
    '''
    Parameters
    --------------
    Hours_Avaliable : Array
        All the hours that have at least 10 years worth of data
    Sub_Mx : Dictionary/DataFrame
        A dictionary of many dataframes that associate the Tmax with the subdaily values of that day
    Sub_Mn : Dictionary/DataFrame
        A dictionary of many dataframes that associate the Tmin with the subdaily values of that day
        
    Return
    ------------
    Monthly_Split_Dic : Dictionary/DataFrame
        A dictionary that has the data splkit into month and hours
    
    '''
    #Lets get all the monthly arrays sorted   
    Month_Number = [1,2,3,4,5,6,7,8,9,10,11,12]
    Month_Name = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    
    #Now lets create a monthly dictionary that the subdaily and its associated tmax/tmin can go in
    Monthly_Split_Dic = {}
    
    #Lets begin the loop to extract the subdaily find the hours and append it all together
    for i in Hours_Avaliable:
        #Extract Max and Min DataFrames, as of the other function we know what the key is for the dictionary
        Max_Data = Sub_Ext_Max.get('Hour_{}'.format(i))
        Min_Data = Sub_Ext_Min.get('Hour_{}'.format(i))
        
        #Extract the Month Number and extract the data for that month
        for q in range(len(Month_Number)):
            #Get the data for the month only
            Month_Max_Data = pd.concat([Max_Data[Max_Data.index.month==Month_Number[q]],], axis = 0)
            Month_Min_Data = pd.concat([Min_Data[Min_Data.index.month==Month_Number[q]],], axis = 0)
            #Add to Dictionary
            Monthly_Split_Dic[Month_Name[q] +"_"+ str(i) + "_"+"Mx"] = Month_Max_Data
            Monthly_Split_Dic[Month_Name[q] +"_"+ str(i) +"_"+ "Mn"] = Month_Min_Data
  

    return(Monthly_Split_Dic)


# # 4. Closest Hour Function

# In[10]:


def Closest_Hour(Data, hours): 
    '''
    Parameters
    -------------
    Data: DataFrame
        The sub_daily data we are aiming to estimate the Tmax and Tmin from wtih two columns, one with datetime and the 
        other with DataFrame
    
    hours:
    The hours that are avaliable to use to get the data from this Data dataset as close as possible to the trained hours
    as some hours may not be able to be used.
    
    Returns
    -----------------
    Dataset : DataFrame
        A dataset that has the closest hour to one of the avalaible hours in the dataset.
        
    '''
    #Get a new array
    closest_hour= []
    
    #We want to match to the hour closest to the 3

    for i in range(len(Data)):
        #Extract the single day
        Individual_Day = Data.loc[i]
    
        #Extract hour
        Individual_Hour = Individual_Day['date'].hour
        
        #Take the closest hour
        Closest_Ind_Hour = take_closest(hours, Individual_Hour)
        
        #If closest hour is 24, make sure it takes the closest hour on either side with the 23 and lower being favoured
        if (Closest_Ind_Hour == 24):
            Left_Check= abs(24 - hours[len(hours)-2])
            Right_Check = abs(hours[0]-0)
            
            
            if Left_Check > Right_Check:
                Closest_Ind_Hour = hours[0]
            else:
                Closest_Ind_Hour = hours[len(hours)-2]
            
        
        #Append the closest hour 
        closest_hour.append(Closest_Ind_Hour)
    
    #Add it as a series then combine to make it a dataframe
    CL = pd.Series(closest_hour, name = 'Closest Hour')
    Dataset = pd.merge(left = Data,right  =CL,left_index=True,right_index=True  )
    return(Dataset)


# ## 4.1 The Inner Function of the Closest Hour Function

# In[11]:


def take_closest(myList, myNumber): 
    """
    Parameter
    --------------
    
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    
    myList: 
        The values that the data can be closest to
    
    myNumber:
        The raw value that will then be converted to the Closest Hour
        
    Returns
    ---------------
    after/before : Integer
        Value that the hour can be closest to
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before


# # 5. Sampling To Dictionary

# In[12]:


def Sampler_Trainer(Data,Trials):
    '''
    Parameters
    -------------
    Data : DataFrame/Dictionary
        A dictionary that has the data splkit into month and hours
        
    Trials : Integer
        The number of trails you want to run the estimation training over.

    Returns
    -----------
    Samples : DataFrame/Dictionary
        Using the observations and the training data we can have created a dictionary of DataFrames
        that have trialed that have been sampled by the lenght of the data avalaible for that month.
        
    
    '''
    
    #Now I need to select random samples from the length of the data for each month, hour and mx or mn
    #then do this 1000 times and label them in the columns Hour 0 as Hour 0 Run 1 and Max as Max Run 1.
    
    
    #Create the dictionary that all the data will be inputed to
    Samples = {}
    
    #Get the entire key column
    Keys = list(Data)
    
    #Now extract the DataFrame from the dictionary for the Key
    for keys_used in Keys:
        #Extract and drop NaNs
        Ind_DF = Data.get(keys_used).dropna()
        #Now sample by the length fo the DataFrame and this is done for the first run only 
        Run1_Data = Ind_DF.sample(n=int(len(Ind_DF)),replace=True)
        #Drop the date column with Index is 0 to Samples-1
        Run1_Data = Run1_Data.reset_index(drop = True)

        #Get the columns names
        Col = Run1_Data.columns
        
        #Now change column name to make it run 1 etc
        Run1_Data= Run1_Data.rename(columns={Col[0]:Col[0] + ' ' +  'Run 1'})
        Run_Data= Run1_Data.rename(columns={Col[1]:Col[1] + ' ' +  'Run 1'})
        
        #Now develope the for loop but the trials is based off the lenght of Data
        for rns in range(2,Trials+1):
            #This is the now the random sampling for 1000 different samples of 600 
            Individual_Run = Ind_DF.sample(n=int(len(Ind_DF)),replace=True)
            #Drop the date column
            Individual_Run = Individual_Run.reset_index(drop = True)
            
            #Get the columns names
            Col = Individual_Run.columns
        
            #Now change column name to make it run 1 etc
            Individual_Run= Individual_Run.rename(columns={Col[0]:Col[0] + ' ' +  'Run {}'.format(rns)})
            Individual_Run= Individual_Run.rename(columns={Col[1]:Col[1] + ' ' +  'Run {}'.format(rns)})
        
            #Concate with RUNS
            Run_Data = pd.concat([Run_Data, Individual_Run],axis=1)
            
        #Now add this to a new dictionary
        Samples[keys_used + "_" + "Samp"] = Run_Data
        
    return(Samples)


# # 6. Linear Regression

# In[13]:


def Linear_Regression_Analysis(Trials, hours, Data):
    '''
    Parameters
    --------------
    Trials : Integer
        The number of trails you want to run the estimation training over.
        
    hours : array
    
    Data : DataFrame/Dictionary
        Using the observations and the training data we can have created a dictionary of DataFrames
        that have trialed that have been sampled by the lenght of the data avalaible for that month.
    
    
    Data : 
    Returns
    --------------
    '''
    
    #Create dictionaries
    Regressed_Trial = {}
    
    #Define the month names
    Month_Name = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    #Being the for loop by extracting the month name
    for month_num in range(0,12):
        #Extract the month name_
        Month_Str =  Month_Name[month_num]
        #This is useful in the key as it is Aug_9_Mn_Samp where month_hour_mx/mn_samp
        
        #Now using the trials lets extract the trials within the particular dictionary
        for trial_number in range(1,Trials+1):
            #Now this is all the arrays that will be appended to at the end that include the linear
            #regression line components, A and B and the Correlation by the Pearsonr
            AMx_Total = []
            BMx_Total = []
            CORRMx_Total = []
            Time = []
            AMn_Total = []
            BMn_Total = []
            CORRMn_Total = []
            
            #Now for loop to extract the data and get the regression
            for i in hours:
                #---MAX---#
                #Extract the maximum data
                Mxt = Data.get('{}_{}_Mx_Samp'.format(Month_Str,i))
                #Get the linear formula and the correlation of the data
                AMx, BMx, corrMx = linear_regression_polyfit(Mxt['temp Run {}'.format(trial_number)],Mxt['Max Run {}'.format(trial_number)])
                #Append it all
                AMx_Total.append(AMx)
                BMx_Total.append(BMx)
                CORRMx_Total.append(corrMx)
                #Repeat for min
                #---MIN---#
                Mnt = Data.get('{}_{}_Mn_Samp'.format(Month_Str,i))
                AMn, BMn, corrMn = linear_regression_polyfit(Mnt['temp Run {}'.format(trial_number)],Mnt['Min Run {}'.format(trial_number)])
                Time.append(int(i)) 
                AMn_Total.append(AMn)
                BMn_Total.append(BMn)
                CORRMn_Total.append(corrMn)

            #Add it all into a dataframe
            Time = pd.Series(Time,name = 'Hours')
            
            AMX = pd.Series(AMx_Total,name = 'A')
            BMX = pd.Series(BMx_Total,name = 'B')
            corrMX = pd.Series(CORRMx_Total,name = 'Correlation')
            ItemsMX = pd.concat([Time,AMX,BMX,corrMX],axis = 1)
            
            AMN = pd.Series(AMn_Total,name = 'A')
            BMN = pd.Series(BMn_Total,name = 'B')
            corrMN = pd.Series(CORRMn_Total,name = 'Correlation')
            ItemsMN = pd.concat([Time,AMN,BMN,corrMN],axis = 1)
            
            Regressed_Trial["{}".format(Month_Str) + "_" + 'Trial'+ "_" + str(trial_number) + "_" + "Mx"] = ItemsMX
            Regressed_Trial["{}".format(Month_Str) + "_" + 'Trial'+ "_" + str(trial_number) + "_" + "Mn"] = ItemsMN
    return(Regressed_Trial)


# ## 6.1 The fitting function for the linear polyfit

# In[14]:


#Now develop the linear regression equation
def linear_regression_polyfit(x,y):
    #Find the linear Relationship
    A, B = np.polyfit(x, y, 1)
    #Find the correlation                  
    corr, _ = spearmanr(x, y)
    return(A,B,corr)


# '''
# Just some background on this matter. Now we have the Subdaily temperature for the estimation, we have the multilinear regression 
# for every month to be used on this temperature now to put it all togetjer and estimation the max and min for the times 
# at each day.
# 
# What we know os that the regression analysis works with the Max and Min differently. This means that the Max and Min do NOT 
# use the same times as a normal person would percieve. In my function we have worked out that the correlation of
# 12pm-1 to 6pm-1 is better for the mininum on the day in foucs then 12m+0 t 6pm+0. Therefore when estimating 
# our minimum on the day in focus we have to start from the previous day after and not including 9am and go to the day in
# focus at 9am. So to get this part of the function will require some work.
# 
# For the Max we will go with the BOM standard whihc starts at 9am of the day in focus to 9am not included the next day.
# 
# Now what has hjappend is that the regression analysis already matches these values, therefore if I was to find the minimum
# from a 12pm temperature, I would have to use the day befores 12pm temperature to estimate it.
# 
# With all this information, I hope you understand how this function will work coming up and for myslef I hope to bring this 
# RMSE down from 1.17 for max and min when comparing to the histroical of the Perth Regional Office from 1942 to 1992 lower for 
# the simple variation of the code and hopefully even lower when I apply the more complex version of the code.
# '''

# ## 7.1 Maximum Subdaily  Vector

# In[15]:


def Max_Sub(Data):
    Sub_Daily_Data = Data.copy()
    #Get the estimation sorted
    # Shift hours 0 to 8 to the previous day's hours for maximum regression of 9am+0 to 8am+1
    Sub_Daily_Data['date'] = pd.to_datetime(Sub_Daily_Data['date'])
    Sub_Daily_Data.loc[Sub_Daily_Data['date'].dt.hour < 9, 'date'] = Sub_Daily_Data['date'] - pd.offsets.Day(1)
    Sub_Daily_Data['date'] = Sub_Daily_Data['date'].dt.strftime('%Y-%m-%d %H:%M:%S')

    return(Sub_Daily_Data)


# ## 7.2 Minimum Subdaily  Vector

# In[16]:


def Min_Sub(Data):
    Sub_Daily_Data = Data.copy()
    # Shift hours 10 to 23 to the tomorrows day's hours for minimum regression of 10am-1 to 9am+0
    Sub_Daily_Data['date'] = pd.to_datetime(Sub_Daily_Data['date'])
    Sub_Daily_Data.loc[Sub_Daily_Data['date'].dt.hour > 9, 'date'] = Sub_Daily_Data['date'] + pd.offsets.Day(1)
    Sub_Daily_Data['date'] = Sub_Daily_Data['date'].dt.strftime('%Y-%m-%d %H:%M:%S')


    return(Sub_Daily_Data)


# # 8. Estimating Tmax and Tmin for all times

# In[17]:


#The first part of the estimation is to estimate for all times
#The estimation matrix should be:
#index date est_hour Tmax Tmin Corr_Max Corr_Min

#We will work on the estimations for tmax and tmin individually
def Tmax_Tmin_All_Data_Est(Trials, Historical_Max, Historical_Min, Linear):
    '''
    Parameters
    --------------
    Trials : Integer
        Number of trials that have been used in this estimation
    
    Historical : DataFrame
        The dataset we will estimate the tmax and tmin temperatures from this already should be in a good format
    
    Linear : Dictionary/DataFrame
        The dictionary with all the linear regressed data for each trial ready to be applied onto the 
    

    Returns
    --------
    
    '''
    
    #Now we begin with the final dictionary
    #Write a all data didctionary
    
    All_Data_Est = {}
    
    #Columns for data 
    Historical_Max_Col = Historical_Max.columns
    Historical_Min_Col = Historical_Min.columns
    
    #Lets begin with the for loop for the trials of the linear
    for T in range(1,Trials+1):
        #Set all the arrays for the information to be added into it
        Est_Max = []
        Est_Min = []
        Max_Corr = []
        Min_Corr = []
        
        
        #Now lets begin with Mx
        for indexed in range(len(Historical_Max)):
            #Extract the initial data
            Day_Data_Max = Historical_Max.loc[indexed]
            
            
            
            #Extract these values : closest hour, month, temp
            Month_V_Max = datetime.strptime(Day_Data_Max[Historical_Max_Col[0]], '%Y-%m-%d %H:%M:%S').month
            Hour_Max = Day_Data_Max[Historical_Max_Col[2]]
            Temperature_Max = Day_Data_Max[Historical_Max_Col[1]]
            
            #Now using another function we can sift through the trial and month to find the estimation,
            Mx_Temp, Corr_Mx = The_Estimator(Month_V_Max, Hour_Max, Temperature_Max, Linear, T, True)
        
            Est_Max.append(Mx_Temp)
            Max_Corr.append(Corr_Mx)
        
        
        #Add the data to the dates again
        Est_Max = pd.Series(Est_Max,name = 'Max Temp Estimation')
        Max_Corr = pd.Series(Max_Corr,name = 'Correlation Max T')
        
        Dataset_Max = pd.concat([Historical_Max, Est_Max, Max_Corr],axis=1)
        
        #Now lets begin with Mx
        for indexed in range(len(Historical_Min)):
            #Extract the initial data
            Day_Data_Min = Historical_Min.loc[indexed]
            
            #Extract these values : closest hour, month, temp
            Month_V_Min = datetime.strptime(Day_Data_Min[Historical_Min_Col[0]], '%Y-%m-%d %H:%M:%S').month
            Hour_Min = Day_Data_Min[Historical_Min_Col[2]]
            Temperature_Min = Day_Data_Min[Historical_Min_Col[1]]
            
            #Now using another function we can sift through the trial and month to find the estimation,
            Mn_Temp, Corr_Mn = The_Estimator(Month_V_Min, Hour_Min, Temperature_Min, Linear, T, False)
        
            Est_Min.append(Mn_Temp)
            Min_Corr.append(Corr_Mn)
        
        
        #Add the data to the dates again
        Est_Min = pd.Series(Est_Min,name = 'Min Temp Estimation')
        Min_Corr = pd.Series(Min_Corr,name = 'Correlation Min T')
        
        Dataset_Min = pd.concat([Historical_Min, Est_Min, Min_Corr],axis=1)
        
        
        #Add to a Trial Dictionary
        All_Data_Est['Trial' + '_' + str(T) + "_Mx"] = Dataset_Max
        All_Data_Est['Trial' + '_' + str(T) + "_Mn"] = Dataset_Min
            

        
    return(All_Data_Est)


# ## 8.1 The Estimator

# In[18]:


def The_Estimator(MONTH, Hour, Temp, DATA_4_EST, Trial_Number, Max):
    Month_Name = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    
    
    if (Max == True):
        #Estimate the Max Temp
        #Extract data from the linear regression dictionary
        Info = DATA_4_EST.get('{}_Trial_{}_Mx'.format(Month_Name[MONTH-1],Trial_Number))
        Info = Info.set_index('Hours')
        Info = Info.loc[int(Hour)]
        #Estimate the Max based off this information
        Est_Max = Info['A']*Temp + (Info['B'])
        #Find the Corr for this day and hour
        Corr_Max =  Info['Correlation']
        return(Est_Max,Corr_Max)
    else:
        #Estimate the Min Temp
        #Extract data from the linear regression dictionary
        Info = DATA_4_EST.get('{}_Trial_{}_Mn'.format(Month_Name[MONTH-1],Trial_Number))
        Info = Info.set_index('Hours')
        Info = Info.loc[int(Hour)]        #Estimate the Max based off this information
        Est_Min = Info['A']*Temp + (Info['B'])
        #Find the Corr for this day and hour
        Corr_Min =  Info["Correlation"]
        return(Est_Min,Corr_Min)
    
  


# # 9. The Daily Estimater

# In[19]:


#To make sure each max and min day does get chosen, we will have to estimate both indiviudally before they are combined for
#for that day
def Absolute_Estimation(Estimated_Data, Trials, simple_comp1_comp2):
    #We need a new dictionary for the finalised estimation
    Est_Daily_Extremes = {}
    

    #Lets begin by using a for loop that extracts that Trail number and the indivudal max and min estimations
    for T in range(1,Trials+1):
        #Extract the data
        Max_Data = Estimated_Data.get('Trial_{}_Mx'.format(T))
        Min_Data = Estimated_Data.get('Trial_{}_Mn'.format(T))
    
        #Lets extract the columns as well, this will be useful.
        #Get Columns
        Max_C = Max_Data.columns
        Min_C = Min_Data.columns
    
        #Make the data datetime 
        #Convert date to datetime
        Max_Data[Max_C[0]] = pd.to_datetime(Max_Data[Max_C[0]])
        Min_Data[Min_C[0]] = pd.to_datetime(Min_Data[Min_C[0]])
    
    
        #Delete the hour out of the date
        Max_Data[Max_C[0]] = Max_Data[Max_C[0]].dt.date 
        Min_Data[Min_C[0]] = Min_Data[Min_C[0]].dt.date 
        
    
    
        #Now we want to see only the individual dates only
        Unique_dates_Max = Max_Data[[Max_C[0]]].drop_duplicates()
        Unique_dates_Max =  Unique_dates_Max.reset_index(drop = True)
        Unique_dates_Min = Min_Data[[Min_C[0]]].drop_duplicates()
        Unique_dates_Min =  Unique_dates_Min.reset_index(drop = True)
        
        #Redo datetime because for some reason when removing the hour it resets the date
        Max_Data[Max_C[0]] = pd.to_datetime(Max_Data[Max_C[0]])
        Min_Data[Min_C[0]] = pd.to_datetime(Min_Data[Min_C[0]])
    
        #Now we have the necessary data for estimated for a single day.
        #Now define the vectors for the Max, Min, Max_Corr, and Min_Corr
        Tmax = []
        Corr_Max = []
        Tmin = []
        Corr_Min = []
        Dates_Mx = []
        Dates_Mn = []
        #Now go through the max and min and choose the best value either in a simple or complex case
        #Max
        for i in range(len(Unique_dates_Max)):
            #Get the individual date
            loc_date_Mx = Max_Data.loc[Max_Data[Max_C[0]] == '{}-{}-{}'.format(Unique_dates_Max[Max_C[0]][i].year,Unique_dates_Max[Max_C[0]][i].month,Unique_dates_Max[Max_C[0]][i].day)]
            #iT is in its length, the 1 length data is remaining with the index as the row
            #from here we will then select either complex or simple and then go into another function.
            if(simple_comp1_comp2 == 0):
                Max_Est,Max_Corr = Simple_Est(loc_date_Mx, True)
            elif(simple_comp1_comp2 == 1):
                Max_Est,Max_Corr = Complex_Est(loc_date_Mx, True)
            else:
                Max_Est,Max_Corr = Complex_Est2(loc_date_Mx, True)
        
            Tmax.append(Max_Est)
            Corr_Max.append(Max_Corr)
    
    
        #Min
        for i in range(len(Unique_dates_Min)):
            #Get the individual date
            loc_date_Mn = Min_Data.loc[Min_Data[Min_C[0]] == '{}-{}-{}'.format(Unique_dates_Min[Min_C[0]][i].year,Unique_dates_Min[Min_C[0]][i].month,Unique_dates_Min[Min_C[0]][i].day)]
            #iT is in its length, the 1 length data is remaining with the index as the row
            #from here we will then select either complex or simple and then go into another function.
            if(simple_comp1_comp2 == 0):
                Min_Est,Min_Corr = Simple_Est(loc_date_Mn, False)
            elif(simple_comp1_comp2 == 1):
                Min_Est,Min_Corr = Complex_Est(loc_date_Mn, False)
            else:
                Min_Est,Min_Corr = Complex_Est2(loc_date_Mn, False)
            Tmin.append(Min_Est)
            Corr_Min.append(Min_Corr)
        
        Tmax_A = pd.Series(Tmax,name = 'Max Temp Estimation')
        Tmin_A = pd.Series(Tmin,name = 'Min Temp Estimation')
        Corr_Max_A = pd.Series(Corr_Max,name = 'Correlation Max T')
        Corr_Min_A = pd.Series(Corr_Min,name = 'Correlation Min T')
        Estimated_Temp_Max = pd.concat([Unique_dates_Max, Tmax_A,Corr_Max_A],axis=1)
        Estimated_Temp_Min = pd.concat([Unique_dates_Min, Tmin_A,Corr_Min_A],axis=1)
        
        #Now add it to 1 single DataFrame
        Estimated_Merge = pd.merge(Estimated_Temp_Max, Estimated_Temp_Min, on=Max_C[0], how='outer')
        
        # Create a date range with missing dates
        start_date = str(Estimated_Merge[Max_C[0]][0])
        end_date = str(Estimated_Merge[Max_C[0]][len(Estimated_Merge)-1])
        date_range = pd.date_range(start=start_date, end=end_date)
        # Create a DataFrame with the missing dates
        missing_dates_df = pd.DataFrame({Max_C[0]: date_range})
        
        #Now add all together so its one continue daily plot
        Estimated_Merge[Max_C[0]] = pd.to_datetime(Estimated_Merge[Max_C[0]])
        
            
        # Merge the original DataFrame with the missing dates DataFrame
        Daily_Extremes_Est = pd.merge(missing_dates_df, Estimated_Merge, on=Max_C[0], how='outer')
        
        #set date as index
        Daily_Extremes_Est = Daily_Extremes_Est.set_index(Max_C[0])
        #Add to Dictionary
        Est_Daily_Extremes['Trial'+ "_" + str(T)] = Daily_Extremes_Est
    return(Est_Daily_Extremes)
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ## 9.1 The individual simple choice

# In[20]:


def Simple_Est(data, MAX):    
    #Single Case: Most simple
    if (len(data) == 1):
        #This finds the values required for a length of 1 data
        if(MAX ==True):
            data = data.reset_index(drop = True)
            Estimated_Max = data['Max Temp Estimation'].loc[0]
            Correlation_Max = data['Correlation Max T'].loc[0]
            return(Estimated_Max,Correlation_Max)
        else:
            data = data.reset_index(drop = True)
            Estimated_Min = data['Min Temp Estimation'].loc[0]
            Correlation_Min = data['Correlation Min T'].loc[0]


                
            return(Estimated_Min,Correlation_Min)


    else:
        if(MAX ==True):
            #--------- MAX ------------#
            #Doing something more complicated
            #First lets find the max of the correlation for the max and min
    
            #nOW FOR TWO INDICES
            #First we choose the highest correlation as the initial condition
            Mx_o_Mx_Corr = data.loc[data['Correlation Max T'] == data['Correlation Max T'].max()]
            Mx_o_Mx_Corr = Mx_o_Mx_Corr.reset_index(drop = True)
            Estimated_Max = Mx_o_Mx_Corr['Max Temp Estimation'].loc[0]
            Correlation_Max = Mx_o_Mx_Corr['Correlation Max T'].loc[0]
            return(Estimated_Max,Correlation_Max)
    
        else:
            #--------- MIN ------------#
            #Doing something more complicated
            #First lets find the max of the correlation for the max and min
    
            #nOW FOR TWO INDICES
            #First we choose the highest correlation as the initial condition
            Mx_o_Mn_Corr = data.loc[data['Correlation Min T'] == data['Correlation Min T'].max()]
            Mx_o_Mn_Corr = Mx_o_Mn_Corr.reset_index(drop = True)   
            Estimated_Min = Mx_o_Mn_Corr['Min Temp Estimation'].loc[0]
            Correlation_Min = Mx_o_Mn_Corr['Correlation Min T'].loc[0]

            return(Estimated_Min,Correlation_Min)
  


# ## 9.2 The individual complex choice 1

# In[ ]:





# In[ ]:




            
            
        


# In[21]:


def Complex_Est(data, Max):
    '''1.'''
    #Single Case: Most simple
    if (len(data) == 1):
        '''2.'''
        #This finds the values required for a length of 1 data
        if(Max ==True):
            data = data.reset_index(drop = True)
            Estimated_Max = data['Max Temp Estimation'].loc[0]
            Correlation_Max = data['Correlation Max T'].loc[0]
            return(Estimated_Max,Correlation_Max)
        else:
            data = data.reset_index(drop = True)
            Estimated_Min = data['Min Temp Estimation'].loc[0]
            Correlation_Min = data['Correlation Min T'].loc[0]
           
                
            return(Estimated_Min,Correlation_Min)
        '''2.'''
    
    #The only 2 datavalues choices
    elif (len(data) == 2):
        #Begin with Max
        if(Max == True):
            #Gets the value of the highest correlation first
            Highest_Correlation =  data.loc[data['Correlation Max T'] == data['Correlation Max T'].max()]
            Highest_Correlation = Highest_Correlation.reset_index(drop = True)
                
            #Now lets check if maximum estimation is the highest maximum value of the day
            Estimated_Temp = Highest_Correlation['Max Temp Estimation'].loc[0]
            #Lets see if the highest temperature is hiher then the estimated temp
            Highest_Actual_Temperature = data.loc[data['temp'] == data['temp'].max()]
            Highest_Actual_Temperature = Highest_Actual_Temperature.reset_index(drop =True)
            if(Estimated_Temp > Highest_Actual_Temperature['temp'].loc[0]):
                #Keep estimated temp
                return(Estimated_Temp, Highest_Correlation['Correlation Max T'].loc[0])
            else:
                #Choose the estimated highest actual temperature
                return(Highest_Actual_Temperature['Max Temp Estimation'].loc[0],Highest_Actual_Temperature['Correlation Max T'].loc[0])

                
        else:
            #Gets the value of the highesr correlation first
            Highest_Correlation =  data.loc[data['Correlation Min T'] == data['Correlation Min T'].max()]
            Highest_Correlation = Highest_Correlation.reset_index(drop = True)
            #Now lets check if minimum estimation is lower then the lowest minimum value of the day
            Estimated_Temp = Highest_Correlation['Min Temp Estimation'].loc[0]
            #Lets see if the highest temperature is hiher then the estimated temp
            Lowest_Actual_Temperature = data.loc[data['temp'] == data['temp'].min()]
            Lowest_Actual_Temperature = Lowest_Actual_Temperature.reset_index(drop =True)    
                
            if(Estimated_Temp < Lowest_Actual_Temperature['temp'].loc[0]):
                #Keep estimated temp
                return(Estimated_Temp, Highest_Correlation['Correlation Min T'].loc[0])
            else:
                #Choose the estimated lowest actual temperature
                return(Lowest_Actual_Temperature['Min Temp Estimation'].loc[0],Lowest_Actual_Temperature['Correlation Min T'].loc[0])
    
    else:
        #This is for 3 or more variables
        '''
        So the criteria that works for this one I believe
        1. We begin by finidng the highest correlated temperature value
        2. From this value we will then check whether at least 1 observational max is above or min is below the 
        estimated value
        3.a If None are keep the value of the highest correlated temp
        3.b If there are, extract all the temperatures that are above or below the estimated temp for max and min 
        respectively
        4. Choose the highest correlated value and repeat steps 2 and 3 until the lowesy value of the correlated value
        is chosen
        '''
        #Decide is chosing max or min
        if(Max == True):
            #Gets the value of the highest correlation first
            Highest_Correlation =  data.loc[data['Correlation Max T'] == data['Correlation Max T'].max()]
            Highest_Correlation = Highest_Correlation.reset_index(drop = True)

            #Now lets check if there are more values that are hotter observationally then this
            Estimated_Temp = Highest_Correlation['Max Temp Estimation'].loc[0]

            #Lets see if the highest temperature is hiher then the estimated temp
            Highest_Actual_Temperature = data.loc[data['temp'] == data['temp'].max()]
            Highest_Actual_Temperature = Highest_Actual_Temperature.reset_index(drop = True) ##

            #Now do the checking function or step 2
            if(Estimated_Temp < Highest_Actual_Temperature['temp'].loc[0]):
                #Extract all values that have temperatures higher then this
                Highest_Actual_Temperature = data.loc[data['temp'] >= Estimated_Temp]
                Highest_Actual_Temperature = Highest_Actual_Temperature.reset_index(drop = True) ##

                #Check if there is more then  one varibale 
                if (len(Highest_Actual_Temperature) > 1):
                    #Do the recursive for loop


                    while (len(Highest_Actual_Temperature) > 1):
                        #Now repeat steps 2 and 3
                        #Gets the value of the highest correlation first
                        Highest_Correlation =  Highest_Actual_Temperature.loc[Highest_Actual_Temperature['Correlation Max T'] == Highest_Actual_Temperature['Correlation Max T'].max()]##hIGHEST CORRE TO HIGHEST ACTU
                        Highest_Correlation = Highest_Correlation.reset_index(drop = True)


                        #Now lets check if there are more values that are hotter observationally then this
                        Estimated_Temp = Highest_Correlation['Max Temp Estimation'].loc[0]
                        #Lets see if the highest temperature is hiher then the estimated temp
                        Highest_Actual_Temperature = Highest_Actual_Temperature.loc[Highest_Actual_Temperature['temp'] == Highest_Actual_Temperature['temp'].max()] ##hIGHEST CORRE TO HIGHEST ACTU
                        Highest_Actual_Temperature = Highest_Actual_Temperature.reset_index(drop = True) ##

                        #Now do the checking function or step 2
                        if(Estimated_Temp < Highest_Actual_Temperature['temp'].loc[0]):
                            #Step Highest_Actual_Temperature to the date
                            #If not choose the other correlation and go through the loop again

                            #Extract all values that have temperatures higher then this
                            Highest_Actual_Temperature = Highest_Actual_Temperature.loc[Highest_Actual_Temperature['temp'] >= Estimated_Temp]
                            Highest_Actual_Temperature = Highest_Actual_Temperature.reset_index(drop = True) ##
                            #Remove the estimation value if theres an issue
                            Highest_Actual_Temperature = Highest_Actual_Temperature[Highest_Actual_Temperature['Max Temp Estimation'] != Estimated_Temp]
                            #Use the safety option
                            if (len(Highest_Actual_Temperature) == 0):
                                Estimated_value = Estimated_value.reset_index(drop = True)
                                return(Estimated_value['Max Temp Estimation'].loc[0], Estimated_value['Correlation Max T'].loc[0])
                        
                        else:
                            Highest_Actual_Temperature = Highest_Correlation
                    Estimated_value  = Highest_Actual_Temperature
                    return(Estimated_value['Max Temp Estimation'].loc[0], Estimated_value['Correlation Max T'].loc[0])
                else:
                    #Now choose the other variable that is onlky length 1
                    return(Highest_Actual_Temperature['Max Temp Estimation'].loc[0],Highest_Actual_Temperature['Correlation Max T'].loc[0])
            else:
                return(Estimated_Temp,Highest_Correlation['Correlation Max T'].loc[0])

        else:
            #Gets the value of the highest correlation first
            Highest_Correlation =  data.loc[data['Correlation Min T'] == data['Correlation Min T'].max()]
            Highest_Correlation = Highest_Correlation.reset_index(drop = True)

            #Now lets check if there are more values that are hotter observationally then this
            Estimated_Temp = Highest_Correlation['Min Temp Estimation'].loc[0]

            #Lets see if the highest temperature is hiher then the estimated temp
            Lowest_Actual_Temperature = data.loc[data['temp'] == data['temp'].min()]
            Lowest_Actual_Temperature = Lowest_Actual_Temperature.reset_index(drop = True) ##

            #Now do the checking function or step 2
            if(Estimated_Temp > Lowest_Actual_Temperature['temp'].loc[0]):
                #Extract all values that have temperatures higher then this
                Lowest_Actual_Temperature = data.loc[data['temp'] <= Estimated_Temp]
                Lowest_Actual_Temperature = Lowest_Actual_Temperature.reset_index(drop = True) ##
                #Check if there is more then  one varibale 
                if (len(Lowest_Actual_Temperature) > 1):
                    #Do the recursive for loop


                    while (len(Lowest_Actual_Temperature) > 1):
                        #Now repeat steps 2 and 3
                        #Gets the value of the highest correlation first
                        Highest_Correlation =  Lowest_Actual_Temperature.loc[Lowest_Actual_Temperature['Correlation Min T'] == Lowest_Actual_Temperature['Correlation Min T'].max()]##hIGHEST CORRE TO HIGHEST ACTU
                        Highest_Correlation = Highest_Correlation.reset_index(drop = True)


                        #Now lets check if there are more values that are hotter observationally then this
                        Estimated_Temp = Highest_Correlation['Min Temp Estimation'].loc[0]
                        #Lets see if the highest temperature is hiher then the estimated temp
                        Lowest_Actual_Temperature = Lowest_Actual_Temperature.loc[Lowest_Actual_Temperature['temp'] == Lowest_Actual_Temperature['temp'].min()] ##hIGHEST CORRE TO HIGHEST ACTU
                        Lowest_Actual_Temperature = Lowest_Actual_Temperature.reset_index(drop = True) ##

                        #Now do the checking function or step 2
                        if(Estimated_Temp > Lowest_Actual_Temperature['temp'].loc[0]):
                            #Step Highest_Actual_Temperature to the date
                            #If not choose the other correlation and go through the loop again

                            #Extract all values that have temperatures higher then this
                            Lowest_Actual_Temperature = Lowest_Actual_Temperature.loc[Lowest_Actual_Temperature['temp'] <= Estimated_Temp]
                            Lowest_Actual_Temperature = Lowest_Actual_Temperature.reset_index(drop = True) ##
                            #Safety check
                            Safety = Lowest_Actual_Temperature
                            #Make sure that the temp of the estimated already done is gone, 
                            Lowest_Actual_Temperature = Lowest_Actual_Temperature[Lowest_Actual_Temperature['Min Temp Estimation'] != Estimated_Temp]
                            #Use the safety option
                            if (len(Lowest_Actual_Temperature) == 0):
                                Estimated_value  = Safety
                                Estimated_value = Estimated_value.reset_index(drop = True)
                                return(Estimated_value['Min Temp Estimation'].loc[0], Estimated_value['Correlation Min T'].loc[0])
                                
                            
                        else:
                            Lowest_Actual_Temperature = Highest_Correlation

                    Estimated_value  = Lowest_Actual_Temperature
                    Estimated_value = Estimated_value.reset_index(drop = True)
                    return(Estimated_value['Min Temp Estimation'].loc[0], Estimated_value['Correlation Min T'].loc[0])
                else:
                    #Now choose the other variable that is onlky length 1
                    return(Lowest_Actual_Temperature['Min Temp Estimation'].loc[0],Lowest_Actual_Temperature['Correlation Min T'].loc[0])
            else:
                return(Estimated_Temp,Highest_Correlation['Correlation Min T'].loc[0])

                
    '''1.'''


# ## 9.3 Complex Variant 2

# In[22]:


def Complex_Est2(data, Max):
    '''
    
    
    
    '''

    '''
    Lets work on the Max only version, this should be like in temp est v4 
    
    So like complex est 2 it has 3 modes, the lenth 1, 2 or more
    
    the first two options are the same as complex v2 but if there are 3 or more then thats when we start diverging 
    from the estimation complex variant 1
    
    More weight on the initial correlation and temp estimation
    
    '''

    #Single Case: Length of 1
    if (len(data) == 1):
        '''2.'''
        #This finds the values required for a length of 1 data
        if(Max ==True):
            data = data.reset_index(drop = True)
            Estimated_Max = data['Max Temp Estimation'].loc[0]
            Correlation_Max = data['Correlation Max T'].loc[0]
            return(Estimated_Max,Correlation_Max)
        else:
            data = data.reset_index(drop = True)
            Estimated_Min = data['Min Temp Estimation'].loc[0]
            Correlation_Min = data['Correlation Min T'].loc[0]
           
                
            return(Estimated_Min,Correlation_Min)

    #The only 2 datavalues choices
    elif (len(data) == 2):
        #Begin with Max
        if(Max == True):
            #Gets the value of the highest correlation first
            Highest_Correlation =  data.loc[data['Correlation Max T'] == data['Correlation Max T'].max()]
            Highest_Correlation = Highest_Correlation.reset_index(drop = True)
                
            #Now lets check if maximum estimation is the highest maximum value of the day
            Estimated_Temp = Highest_Correlation['Max Temp Estimation'].loc[0]
            #Lets see if the highest temperature is hiher then the estimated temp
            Highest_Actual_Temperature = data.loc[data['temp'] == data['temp'].max()]
            Highest_Actual_Temperature = Highest_Actual_Temperature.reset_index(drop =True)
            if(Estimated_Temp > Highest_Actual_Temperature['temp'].loc[0]):
                #Keep estimated temp
                return(Estimated_Temp, Highest_Correlation['Correlation Max T'].loc[0])
            else:
                #Choose the estimated highest actual temperature
                return(Highest_Actual_Temperature['Max Temp Estimation'].loc[0],Highest_Actual_Temperature['Correlation Max T'].loc[0])

                
        else:
            #Gets the value of the highesr correlation first
            Highest_Correlation =  data.loc[data['Correlation Min T'] == data['Correlation Min T'].max()]
            Highest_Correlation = Highest_Correlation.reset_index(drop = True)
            #Now lets check if minimum estimation is lower then the lowest minimum value of the day
            Estimated_Temp = Highest_Correlation['Min Temp Estimation'].loc[0]
            #Lets see if the highest temperature is hiher then the estimated temp
            Lowest_Actual_Temperature = data.loc[data['temp'] == data['temp'].min()]
            Lowest_Actual_Temperature = Lowest_Actual_Temperature.reset_index(drop =True)    
                
            if(Estimated_Temp < Lowest_Actual_Temperature['temp'].loc[0]):
                #Keep estimated temp
                return(Estimated_Temp, Highest_Correlation['Correlation Min T'].loc[0])
            else:
                #Choose the estimated lowest actual temperature
                return(Lowest_Actual_Temperature['Min Temp Estimation'].loc[0],Lowest_Actual_Temperature['Correlation Min T'].loc[0])
    
    
    
    
    
    else:
        #This is for 3 or more variables
        '''
        So the criteria for this one is:
        1. We begin by choosing the temperature of highest correlation known
        2. From this value we will then check whether at least 1 observational max is above or min is below the 
        estimated value        
        3.a If None are keep the value of the highest correlated temp
        3.b If there are extract those values
        4. Using 3.b check whether the correlation of any are above 0.85 then choose the highest one and keep that
        only
        
        '''
        #Decide is chosing max or min
        if(Max == True):
            #Gets the value of the highest correlation first
            Highest_Correlation =  data.loc[data['Correlation Max T'] == data['Correlation Max T'].max()]
            Highest_Correlation = Highest_Correlation.reset_index(drop = True)

            #Now lets check if there are more values that are hotter observationally then this
            Estimated_Temp = Highest_Correlation['Max Temp Estimation'].loc[0]

            #Lets see if the highest temperature is hiher then the estimated temp
            Highest_Actual_Temperature = data.loc[data['temp'] == data['temp'].max()]
            Highest_Actual_Temperature = Highest_Actual_Temperature.reset_index(drop = True) ##

            #Now do the checking function or step 2
            if(Estimated_Temp < Highest_Actual_Temperature['temp'].loc[0]):
                #Extract all values that have temperatures higher then this
                Highest_Actual_Temperature = data.loc[data['temp'] >= Estimated_Temp]
                #Drop any with a correlation of less then 0.85
                Highest_Actual_Temperature = Highest_Actual_Temperature.loc[Highest_Actual_Temperature['Correlation Max T'] >= 0.85]
                
                Highest_Actual_Temperature = Highest_Actual_Temperature.reset_index(drop = True) ##
                
                #Check if there is more then  one varibale 
                if (len(Highest_Actual_Temperature) >= 1):
                    #Choose the highest correlated value
                    Highest_Correlation_Temp =  Highest_Actual_Temperature.loc[Highest_Actual_Temperature['Correlation Max T'] == Highest_Actual_Temperature['Correlation Max T'].max()]##hIGHEST CORRE TO HIGHEST ACTU
                    Highest_Correlation_Temp = Highest_Correlation_Temp.reset_index(drop = True)
                    return(Highest_Correlation_Temp['Max Temp Estimation'].loc[0],Highest_Correlation_Temp['Correlation Max T'].loc[0])
                else: 
                    #Return the estimated one from before
                    return(Estimated_Temp,Highest_Correlation['Correlation Max T'].loc[0])

            else:
                return(Estimated_Temp,Highest_Correlation['Correlation Max T'].loc[0])

        else:
            #Gets the value of the highest correlation first
            Highest_Correlation =  data.loc[data['Correlation Min T'] == data['Correlation Min T'].max()]
            Highest_Correlation = Highest_Correlation.reset_index(drop = True)

            #Now lets check if there are more values that are hotter observationally then this
            Estimated_Temp = Highest_Correlation['Min Temp Estimation'].loc[0]

            #Lets see if the highest temperature is hiher then the estimated temp
            Lowest_Actual_Temperature = data.loc[data['temp'] == data['temp'].min()]
            Lowest_Actual_Temperature = Lowest_Actual_Temperature.reset_index(drop = True) ##

           #Now do the checking function or step 2
            if(Estimated_Temp > Lowest_Actual_Temperature['temp'].loc[0]):
                #Extract all values that have temperatures higher then this
                Lowest_Actual_Temperature = data.loc[data['temp'] >= Estimated_Temp]
                #Drop any with a correlation of less then 0.85
                Lowest_Actual_Temperature = Lowest_Actual_Temperature.loc[Lowest_Actual_Temperature['Correlation Min T'] >= 0.85]
                
                Lowest_Actual_Temperature = Lowest_Actual_Temperature.reset_index(drop = True) ##
                
                #Check if there is more then  one varibale 
                if (len(Lowest_Actual_Temperature) >= 1):
                    #Choose the highest correlated value
                    Highest_Correlation_Temp =  Lowest_Actual_Temperature.loc[Lowest_Actual_Temperature['Correlation Min T'] == Lowest_Actual_Temperature['Correlation Min T'].max()]##hIGHEST CORRE TO HIGHEST ACTU
                    Highest_Correlation_Temp = Highest_Correlation_Temp.reset_index(drop = True)
                    return(Highest_Correlation_Temp['Min Temp Estimation'].loc[0],Highest_Correlation_Temp['Correlation Min T'].loc[0])
                else: 
                    #Return the estimated one from before
                    return(Estimated_Temp,Highest_Correlation['Correlation Min T'].loc[0])
    
            else:
                return(Estimated_Temp,Highest_Correlation['Correlation Min T'].loc[0])


# In[ ]:





# In[ ]:





# In[ ]:





# 

# In[ ]:





# In[ ]:





# In[ ]:





# 

# In[ ]:








# In[ ]:





# In[127]:





# In[ ]:





# 

# 

# In[31]:



   
        
    
    


# 

# In[ ]:





# 

# In[118]:


data = data[data['Max Temp Estimation'] != 24.4]
data


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[79]:


data = pd.read_csv(r"C:\Users\jarra\Desktop\Test.csv")
data


# In[87]:


#Gets the value of the highest correlation first
Highest_Correlation =  data.loc[data['Correlation Max T'] == data['Correlation Max T'].max()]
Highest_Correlation = Highest_Correlation.reset_index(drop = True)
       
#Now lets check if there are more values that are hotter observationally then this
Estimated_Temp = Highest_Correlation['Max Temp Estimation'].loc[0]

#Lets see if the highest temperature is hiher then the estimated temp
Highest_Actual_Temperature = data.loc[data['temp'] == data['temp'].max()]
Highest_Actual_Temperature = Highest_Actual_Temperature.reset_index(drop = True) ##

#Now do the checking function or step 2
if(Estimated_Temp < Highest_Actual_Temperature['temp'].loc[0]):
    #Extract all values that have temperatures higher then this
    Highest_Actual_Temperature = data.loc[data['temp'] >= Estimated_Temp]


    #Check if there is more then  one varibale 
    if (len(Highest_Actual_Temperature) > 1):
        #Do the recursive for loop


        while (len(Highest_Actual_Temperature) > 1):
            #Now repeat steps 2 and 3
            #Gets the value of the highest correlation first
            Highest_Correlation =  Highest_Actual_Temperature.loc[Highest_Actual_Temperature['Correlation Max T'] == Highest_Actual_Temperature['Correlation Max T'].max()]##hIGHEST CORRE TO HIGHEST ACTU
            Highest_Correlation = Highest_Correlation.reset_index(drop = True)


            #Now lets check if there are more values that are hotter observationally then this
            Estimated_Temp = Highest_Correlation['Max Temp Estimation'].loc[0]
            #Lets see if the highest temperature is hiher then the estimated temp
            Highest_Actual_Temperature = Highest_Actual_Temperature.loc[Highest_Actual_Temperature['temp'] == Highest_Actual_Temperature['temp'].max()] ##hIGHEST CORRE TO HIGHEST ACTU
            Highest_Actual_Temperature = Highest_Actual_Temperature.reset_index(drop = True) ##

            #Now do the checking function or step 2
            if(Estimated_Temp < Highest_Actual_Temperature['temp'].loc[0]):
                #Step Highest_Actual_Temperature to the date
                #If not choose the other correlation and go through the loop again

                #Extract all values that have temperatures higher then this
                Highest_Actual_Temperature = Highest_Actual_Temperature.loc[Highest_Actual_Temperature['temp'] >= Estimated_Temp]


            else:
                Highest_Actual_Temperature = Highest_Correlation

        Estimated_value  = Highest_Actual_Temperature
        return(Estimated_value['Max Temp Estimation'].loc[0], Estimated_value['Correlation Max T'].loc[0])
    else:
        #Now choose the other variable that is onlky length 1
        return(Highest_Actual_Temperature['Max Temp Estimation'].loc[0],Highest_Actual_Temperature['Correlation Max T'].loc[0])
else:
    return(Estimated_Temp,Highest_Correlation)


# In[73]:


Highest_Actual_Temperature.loc[Highest_Actual_Temperature['temp'] == Highest_Actual_Temperature['temp'].max()]


# In[85]:


Estimated_value


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[21]:


A


# In[31]:


#To make sure each max and min day does get chosen, we will have to estimate both indiviudally before they are combined for
#for that day
Est_Daily_Extremes = {}

Estimated_Data = A
T = 1

Absolute_Estimation(A, 1, 2)

#Extract the data
Max_Data = Estimated_Data.get('Trial_{}_Mx'.format(T))
Min_Data = Estimated_Data.get('Trial_{}_Mn'.format(T))

#Lets extract the columns as well, this will be useful.
#Get Columns
Max_C = Max_Data.columns
Min_C = Min_Data.columns

#Make the data datetime 
#Convert date to datetime
Max_Data[Max_C[0]] = pd.to_datetime(Max_Data[Max_C[0]])
Min_Data[Min_C[0]] = pd.to_datetime(Min_Data[Min_C[0]])


#Delete the hour out of the date
Max_Data[Max_C[0]] = Max_Data[Max_C[0]].dt.date 
Min_Data[Min_C[0]] = Min_Data[Min_C[0]].dt.date 



#Now we want to see only the individual dates only
Unique_dates_Max = Max_Data[[Max_C[0]]].drop_duplicates()
Unique_dates_Max =  Unique_dates_Max.reset_index(drop = True)
Unique_dates_Min = Min_Data[[Min_C[0]]].drop_duplicates()
Unique_dates_Min =  Unique_dates_Min.reset_index(drop = True)

#Redo datetime because for some reason when removing the hour it resets the date
Max_Data[Max_C[0]] = pd.to_datetime(Max_Data[Max_C[0]])
Min_Data[Min_C[0]] = pd.to_datetime(Min_Data[Min_C[0]])

#Now we have the necessary data for estimated for a single day.
#Now define the vectors for the Max, Min, Max_Corr, and Min_Corr
Tmax = []
Corr_Max = []
Tmin = []
Corr_Min = []
Dates_Mx = []
Dates_Mn = []
#Now go through the max and min and choose the best value either in a simple or complex case
#Max
for i in range(len(Unique_dates_Max)):
    #Get the individual date
    loc_date_Mx = Max_Data.loc[Max_Data[Max_C[0]] == '{}-{}-{}'.format(Unique_dates_Max[Max_C[0]][i].year,Unique_dates_Max[Max_C[0]][i].month,Unique_dates_Max[Max_C[0]][i].day)]
    #iT is in its length, the 1 length data is remaining with the index as the row
    #from here we will then select either complex or simple and then go into another function.
    
    Max_Est,Max_Corr = Complex_Est2(loc_date_Mx, True)

    Tmax.append(Max_Est)
    Corr_Max.append(Max_Corr)


#Min
for i in range(len(Unique_dates_Min)):
    #Get the individual date
    loc_date_Mn = Min_Data.loc[Min_Data[Min_C[0]] == '{}-{}-{}'.format(Unique_dates_Min[Min_C[0]][i].year,Unique_dates_Min[Min_C[0]][i].month,Unique_dates_Min[Min_C[0]][i].day)]
    #iT is in its length, the 1 length data is remaining with the index as the row
    #from here we will then select either complex or simple and then go into another function.
    Min_Est,Min_Corr = Complex_Est2(loc_date_Mn, False)

    
    Tmin.append(Min_Est)
    Corr_Min.append(Min_Corr)

Tmax_A = pd.Series(Tmax,name = 'Max Temp Estimation')
Tmin_A = pd.Series(Tmin,name = 'Min Temp Estimation')
Corr_Max_A = pd.Series(Corr_Max,name = 'Correlation Max T')
Corr_Min_A = pd.Series(Corr_Min,name = 'Correlation Min T')
Estimated_Temp_Max = pd.concat([Unique_dates_Max, Tmax_A,Corr_Max_A],axis=1)
Estimated_Temp_Min = pd.concat([Unique_dates_Min, Tmin_A,Corr_Min_A],axis=1)

#Now add it to 1 single DataFrame
Estimated_Merge = pd.merge(Estimated_Temp_Max, Estimated_Temp_Min, on=Max_C[0], how='outer')

# Create a date range with missing dates
start_date = str(Estimated_Merge[Max_C[0]][0])
end_date = str(Estimated_Merge[Max_C[0]][len(Estimated_Merge)-1])
date_range = pd.date_range(start=start_date, end=end_date)
# Create a DataFrame with the missing dates
missing_dates_df = pd.DataFrame({Max_C[0]: date_range})

#Now add all together so its one continue daily plot
Estimated_Merge[Max_C[0]] = pd.to_datetime(Estimated_Merge[Max_C[0]])


# Merge the original DataFrame with the missing dates DataFrame
Daily_Extremes_Est = pd.merge(missing_dates_df, Estimated_Merge, on=Max_C[0], how='outer')

#set date as index
Daily_Extremes_Est = Daily_Extremes_Est.set_index(Max_C[0])
#Add to Dictionary
Est_Daily_Extremes['Trial'+ "_" + str(T)] = Daily_Extremes_Est


# In[30]:


def Complex_Est2(data, Max):
    '''
    
    
    
    '''

    '''
    Lets work on the Max only version, this should be like in temp est v4 
    
    So like complex est 2 it has 3 modes, the lenth 1, 2 or more
    
    the first two options are the same as complex v2 but if there are 3 or more then thats when we start diverging 
    from the estimation complex variant 1
    
    More weight on the initial correlation and temp estimation
    
    '''

    #Single Case: Length of 1
    if (len(data) == 1):
        '''2.'''
        #This finds the values required for a length of 1 data
        if(Max ==True):
            data = data.reset_index(drop = True)
            Estimated_Max = data['Max Temp Estimation'].loc[0]
            Correlation_Max = data['Correlation Max T'].loc[0]
            return(Estimated_Max,Correlation_Max)
        else:
            data = data.reset_index(drop = True)
            Estimated_Min = data['Min Temp Estimation'].loc[0]
            Correlation_Min = data['Correlation Min T'].loc[0]
           
                
            return(Estimated_Min,Correlation_Min)

    #The only 2 datavalues choices
    elif (len(data) == 2):
        #Begin with Max
        if(Max == True):
            #Gets the value of the highest correlation first
            Highest_Correlation =  data.loc[data['Correlation Max T'] == data['Correlation Max T'].max()]
            Highest_Correlation = Highest_Correlation.reset_index(drop = True)
                
            #Now lets check if maximum estimation is the highest maximum value of the day
            Estimated_Temp = Highest_Correlation['Max Temp Estimation'].loc[0]
            #Lets see if the highest temperature is hiher then the estimated temp
            Highest_Actual_Temperature = data.loc[data['temp'] == data['temp'].max()]
            Highest_Actual_Temperature = Highest_Actual_Temperature.reset_index(drop =True)
            if(Estimated_Temp > Highest_Actual_Temperature['temp'].loc[0]):
                #Keep estimated temp
                return(Estimated_Temp, Highest_Correlation['Correlation Max T'].loc[0])
            else:
                #Choose the estimated highest actual temperature
                return(Highest_Actual_Temperature['Max Temp Estimation'].loc[0],Highest_Actual_Temperature['Correlation Max T'].loc[0])

                
        else:
            #Gets the value of the highesr correlation first
            Highest_Correlation =  data.loc[data['Correlation Min T'] == data['Correlation Min T'].max()]
            Highest_Correlation = Highest_Correlation.reset_index(drop = True)
            #Now lets check if minimum estimation is lower then the lowest minimum value of the day
            Estimated_Temp = Highest_Correlation['Min Temp Estimation'].loc[0]
            #Lets see if the highest temperature is hiher then the estimated temp
            Lowest_Actual_Temperature = data.loc[data['temp'] == data['temp'].min()]
            Lowest_Actual_Temperature = Lowest_Actual_Temperature.reset_index(drop =True)    
                
            if(Estimated_Temp < Lowest_Actual_Temperature['temp'].loc[0]):
                #Keep estimated temp
                return(Estimated_Temp, Highest_Correlation['Correlation Min T'].loc[0])
            else:
                #Choose the estimated lowest actual temperature
                return(Lowest_Actual_Temperature['Min Temp Estimation'].loc[0],Lowest_Actual_Temperature['Correlation Min T'].loc[0])
    
    
    
    
    
    else:
        #This is for 3 or more variables
        '''
        So the criteria for this one is:
        1. We begin by choosing the temperature of highest correlation known
        2. From this value we will then check whether at least 1 observational max is above or min is below the 
        estimated value        
        3.a If None are keep the value of the highest correlated temp
        3.b If there are extract those values
        4. Using 3.b check whether the correlation of any are above 0.85 then choose the highest one and keep that
        only
        
        '''
        #Decide is chosing max or min
        if(Max == True):
            #Gets the value of the highest correlation first
            Highest_Correlation =  data.loc[data['Correlation Max T'] == data['Correlation Max T'].max()]
            Highest_Correlation = Highest_Correlation.reset_index(drop = True)

            #Now lets check if there are more values that are hotter observationally then this
            Estimated_Temp = Highest_Correlation['Max Temp Estimation'].loc[0]

            #Lets see if the highest temperature is hiher then the estimated temp
            Highest_Actual_Temperature = data.loc[data['temp'] == data['temp'].max()]
            Highest_Actual_Temperature = Highest_Actual_Temperature.reset_index(drop = True) ##

            #Now do the checking function or step 2
            if(Estimated_Temp < Highest_Actual_Temperature['temp'].loc[0]):
                #Extract all values that have temperatures higher then this
                Highest_Actual_Temperature = data.loc[data['temp'] >= Estimated_Temp]
                #Drop any with a correlation of less then 0.85
                Highest_Actual_Temperature = data.loc[data['Correlation Max T'] >= 0.85]
                
                Highest_Actual_Temperature = Highest_Actual_Temperature.reset_index(drop = True) ##
                
                #Check if there is more then  one varibale 
                if (len(Highest_Actual_Temperature) >= 1):
                    #Choose the highest correlated value
                    Highest_Correlation_Temp =  Highest_Actual_Temperature.loc[Highest_Actual_Temperature['Correlation Max T'] == Highest_Actual_Temperature['Correlation Max T'].max()]##hIGHEST CORRE TO HIGHEST ACTU
                    Highest_Correlation_Temp = Highest_Correlation_Temp.reset_index(drop = True)
                    return(Highest_Correlation_Temp['Max Temp Estimation'].loc[0],Highest_Correlation_Temp['Correlation Max T'].loc[0])
                else: 
                    #Return the estimated one from before
                    return(Estimated_Temp,Highest_Correlation['Correlation Max T'].loc[0])

            else:
                return(Estimated_Temp,Highest_Correlation['Correlation Max T'].loc[0])

        else:
            #Gets the value of the highest correlation first
            Highest_Correlation =  data.loc[data['Correlation Min T'] == data['Correlation Min T'].max()]
            Highest_Correlation = Highest_Correlation.reset_index(drop = True)

            #Now lets check if there are more values that are hotter observationally then this
            Estimated_Temp = Highest_Correlation['Min Temp Estimation'].loc[0]

            #Lets see if the highest temperature is hiher then the estimated temp
            Lowest_Actual_Temperature = data.loc[data['temp'] == data['temp'].min()]
            Lowest_Actual_Temperature = Lowest_Actual_Temperature.reset_index(drop = True) ##

           #Now do the checking function or step 2
            if(Estimated_Temp > Lowest_Actual_Temperature['temp'].loc[0]):
                #Extract all values that have temperatures higher then this
                Lowest_Actual_Temperature = data.loc[data['temp'] >= Estimated_Temp]
                #Drop any with a correlation of less then 0.85
                Lowest_Actual_Temperature = data.loc[data['Correlation Min T'] >= 0.85]
                
                Lowest_Actual_Temperature = Lowest_Actual_Temperature.reset_index(drop = True) ##
                
                #Check if there is more then  one varibale 
                if (len(Lowest_Actual_Temperature) >= 1):
                    #Choose the highest correlated value
                    Highest_Correlation_Temp =  Lowest_Actual_Temperature.loc[Lowest_Actual_Temperature['Correlation Min T'] == Lowest_Actual_Temperature['Correlation Min T'].max()]##hIGHEST CORRE TO HIGHEST ACTU
                    Highest_Correlation_Temp = Highest_Correlation_Temp.reset_index(drop = True)
                    return(Highest_Correlation_Temp['Min Temp Estimation'].loc[0],Highest_Correlation_Temp['Correlation Min T'].loc[0])
                else: 
                    #Return the estimated one from before
                    return(Estimated_Temp,Highest_Correlation['Correlation Min T'].loc[0])
    
            else:
                return(Estimated_Temp,Highest_Correlation['Correlation Min T'].loc[0])


# In[32]:


Est_Daily_Extremes.get('Trial_1')


# In[ ]:




