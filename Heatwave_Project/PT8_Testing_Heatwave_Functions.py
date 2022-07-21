# -*- coding: utf-8 -*-
"""
Testing the Heatwave Generating Function
"""
#%% PACKAGES
import pandas as pd, numpy as np,matplotlib.pyplot as plt, xarray as xr,PT5_Functions_For_Masters as function_M
from scipy import stats

#MAXIMUM TEMPERATURE
# Load Data only using max Temperature for the initial start
Dates = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\Dates, includes feb 29.csv")
MaxT_Perth_Data = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\tmax.009021.daily.csv")
MaxT_Perth = MaxT_Perth_Data.copy().drop(0)
# Apply datetime
MaxT_Perth['date'] = pd.to_datetime(MaxT_Perth['date'],format="%d/%m/%Y")

# Apply groupby functiom
MaxT_Perth['year']=MaxT_Perth['date'].dt.year
MaxT_Perth['month']=MaxT_Perth['date'].dt.month
MaxT_Perth['day']=MaxT_Perth['date'].dt.day



MaxT_Perth = MaxT_Perth[MaxT_Perth['year'] <= 2021]
MaxT_Perth = MaxT_Perth[MaxT_Perth['year'] >= 1911]



#Define the excess heat factor vectors for max_min_ave
#first day in focus is index 32
EHF = np.zeros(len(MaxT_Perth))
EHIacc = np.zeros(len(MaxT_Perth))
EHIsig = np.zeros(len(MaxT_Perth))
EHIacclpositive = np.zeros(len(MaxT_Perth)) #To Sim  max[1,EHIacc]
EHFp= np.zeros(len(MaxT_Perth)) #To sim EHIsig*max[1,EHIacc]



#Expect 50% all ALL days to be record or roughly 50%
CDP_Max = function_M.Calendar_Day_Percentile(MaxT_Perth,90,7,Dates,'maximum temperature (degC)',1911,1940)
Clim_Scale_Charac = function_M.Extend_Summer_Heatwavesv1(MaxT_Perth, True, 1911,1940,'maximum temperature (degC)',CDP_Max,'date')
Clim_Scale_Charac2 = function_M.Extend_Summer_Heatwavesv2(MaxT_Perth, True, 1911,1940,'maximum temperature (degC)',CDP_Max,'date')
#%%

EHF = np.zeros(len(MaxT_Perth))
EHIacc = np.zeros(len(MaxT_Perth))
EHIsig = np.zeros(len(MaxT_Perth))
EHIacclpositive = np.zeros(len(MaxT_Perth)) #To Sim  max[1,EHIacc]
EHFp= np.zeros(len(MaxT_Perth)) #To sim EHIsig*max[1,EHIacc]

MaxT_Perth =  MaxT_Perth.reset_index()
IndexT = MaxT_Perth.index[0]
IndexTT=MaxT_Perth.index[len(MaxT_Perth)-1]

print((IndexT,IndexTT))

    
    
    
    

for i in range(IndexT+33,IndexTT):
    
    #-----3 day mean-----#
    D3mean = (MaxT_Perth['maximum temperature (degC)'][i] + MaxT_Perth['maximum temperature (degC)'][i-1]+MaxT_Perth['maximum temperature (degC)'][i-2])/3
    
    #-----i-33 to i - 3-----#
    D323SUM = 0
    for q in range(3,33):
        D323SUM = D323SUM + MaxT_Perth['maximum temperature (degC)'][i-q]
        
    D323mean = D323SUM/len(range(3,33))
    
    #-----EHI(accl)-----#
    EHIacc_single = D3mean - D323mean
   
    EHIacc[i] = EHIacc_single
    EHIacclpositive[i] = np.max([1,EHIacc_single])
    
    
    #-----Tn-----#
    CDPsortd = CDP_Max[CDP_Max['day'] == MaxT_Perth['day'][i]]    
    CDPsortm = CDPsortd[CDPsortd['month'] == MaxT_Perth['month'][i]]
    T_CDP = CDPsortm['Temp']

    #-----EHI(sig) -----#
    EHIsig_single = D3mean - T_CDP
    EHIsig[i] = EHIsig_single
    
    #-----EHF -----#
    EHF[i] = EHIacc[i] * EHIsig[i] #degC^2
    EHFp[i] = EHIacclpositive[i] * EHIsig[i]
    
    
EHF = pd.Series(EHF, name="Excess Heat Factor")
EHIacc = pd.Series(EHIacc,name="Excess Heat Index Acclimatised")
EHIsig = pd.Series(EHIsig,name="Excess Heat Index Significant")
EHIacclpositive = pd.Series(EHIacclpositive,name="Excess Heat Index Acclimatised Maximum Will Always be Positive")
EHFp = pd.Series(EHFp,name="Excess Heat Factor Positive For Continuation of Long Heatwaves")


EHFvect = pd.concat([EHIacc,EHIacclpositive,EHIsig,EHF,EHFp],axis=1)

#Concat not working
Heatwave_Characteristics_Onset = pd.concat([MaxT_Perth,EHFvect],axis=1)
#This doesn't work cause it is not positive we know it does work, but now I have relaised that a addition does not work so I stuffed up, now I need to implement the onset of the 
#heatwave as the first three days where both EHI are positve, and once this is checked, let the subsequent daysave the EHIaccl as max[1,EHIaccl[i]] so itll most likely be 
#3 or 4 if loops to extract the heatwave event.]
#%%
import time
start_time = time.perf_counter()
list_heatwaves = []
count = 0
Q = 0
for i in range(len(EHF)):
    # print(i, Q, sep=' , ')
    if (EHF[i] > 0) and (EHIacc[i]> 0) and (EHIsig[i] > 0):
        Q = Q+1

    elif(EHFp[i] > 0) and (EHIsig[i]> 0) and (Q >= 3):
        Q = Q+1
    else:
        if (Q >= 3):
            count = count+1
            Heatwave = Heatwave_Characteristics_Onset.loc[i-Q:i-1]
            Heatwave['id'] = [count] * len(Heatwave)
            list_heatwaves.append(Heatwave)
            Q=0
        else:
            Q=0
    
heatwave_df = pd.concat(list_heatwaves,axis=0)


ext_sum_heatwave = (heatwave_df.loc[heatwave_df['month']>=11])
ext_sum_heatwave2 =  heatwave_df.loc[heatwave_df['month']<=3]
Extended_Summer_Season1 = pd.concat([ext_sum_heatwave,ext_sum_heatwave2]).sort_values(by=['date'], ascending=True)


Extended_Summer_Season1

end_time = time.perf_counter()
print(f"Execution Time : {end_time - start_time:0.6f}" )
#Something is off bascially



#%% RESTART DIFFERENT WAY
start_time = time.perf_counter()
list_heatwaves = []
heat_days = 0
count  = 0
for i in range(len(EHF)):
    #Define the heat_days>= 3 for long heatwave periods
    if (heat_days >= 3):
        #Define the heatwave continuation
        if(EHIsig[i] > 0):
            heat_days = heat_days + 1
        #Define the ending of the heatwave, without the break at the moment
        else:
            count = count+1
            Heatwave = Heatwave_Characteristics_Onset.loc[i-heat_days:i-1]
            Heatwave['id'] = [count] * len(Heatwave)
            list_heatwaves.append(Heatwave)
            heat_days=0
        
    #Define everything for the initiation of the heatwave
    else:
        if((EHIacc[i]> 0) and (EHIsig[i] > 0)):
            heat_days = heat_days + 1
        else:
            heat_days  = 0
            
heatwave_df = pd.concat(list_heatwaves,axis=0)


ext_sum_heatwave = (heatwave_df.loc[heatwave_df['month']>=11])
ext_sum_heatwave2 =  heatwave_df.loc[heatwave_df['month']<=3]
Extended_Summer_Season2 = pd.concat([ext_sum_heatwave,ext_sum_heatwave2]).sort_values(by=['date'], ascending=True)


Extended_Summer_Season2

end_time = time.perf_counter()
print(f"Execution Time : {end_time - start_time:0.6f}" )

#Second variation is faster by 0.5s for 50 years.


#

'''
How to calculate the min max checking for the heatwave.
step 1, get the ID for max
Step 2 extract information of max heattwave and find the 1st, 2nd and 3rd date it starts
Step 3, cross check the 3 dates to see if a heatwave event is captured by minimum
Step 4, if so this is used as a heatwave event and keep it, if not resort to average 
Step 5, if the minimum wasnt working, check the average and see if this has an associated 3 day heatwave event recorded for the same period
Step 6, if it is keep this heatwave event

'''






#%% Moving Boxes
start = list(range(1911,1992,5))
end = list(range(1940,2021,5))

for i in range(len(start)):
    
    #Define the bounds of start and end year
    datstart = start[i]
    datend = end[i]
    
    #Define the CDP pperiod from the bounds
    CDP_Max = function_M.Calendar_Day_Percentile(MaxT_Perth,90,7,Dates,'maximum temperature (degC)',datstart,datend)
    
    #This for loop will now do two things, a changing CDP with a changing 30 year block matching the dates and a stable block 
    
    #Part 1, constant 1911-2021 using the changing CDP
    function_M.Extend_Summer_Heatwaves(MaxT_Perth, True, 1911,2021,'maximum temperature (degC)',CDP_Max,'date')
    #Add in the characteristic functions here 
    
    
    #Part 2, using the moving changes
    function_M.Extend_Summer_Heatwaves(MaxT_Perth, True, datstart,datend,'maximum temperature (degC)',CDP_Max,'date')
    #Add in the characteristic functions here 
    
    
    #Part 3 using a moving CDP and the lasy 30 years to show how the ages would view the heatwaves at the extreme ends choose which one is better to be explained
    function_M.Extend_Summer_Heatwaves(MaxT_Perth, True, 1992,2021,'maximum temperature (degC)',CDP_Max,'date')
    function_M.Extend_Summer_Heatwaves(MaxT_Perth, True, 1911,1940,'maximum temperature (degC)',CDP_Max,'date')



#The final box definition is the climatological scale 
cs_start = 1981
cs_end = 2010
CDP_Max = function_M.Calendar_Day_Percentile(MaxT_Perth,90,7,Dates,'maximum temperature (degC)',cs_start,cs_end)
Clim_Scale_Charac = function_M.Extend_Summer_Heatwaves(MaxT_Perth, True, 1910,2021,'maximum temperature (degC)',CDP_Max,'date')

#To compare the difference of what happens when you choose the recent average compared ot the old
cs_start = 1961
cs_end = 1990
CDP_Max = function_M.Calendar_Day_Percentile(MaxT_Perth,90,7,Dates,'maximum temperature (degC)',cs_start,cs_end)
Clim_Scale_Charac = function_M.Extend_Summer_Heatwaves(MaxT_Perth, True, 1910,2021,'maximum temperature (degC)',CDP_Max,'date')

#Different Timescales ~~ 37 Years
cs_start = 1911
cs_end = 1947
CDP_Max = function_M.Calendar_Day_Percentile(MaxT_Perth,90,7,Dates,'maximum temperature (degC)',cs_start,cs_end)
Clim_Scale_Charac = function_M.Extend_Summer_Heatwaves(MaxT_Perth, True, cs_start,cs_end,'maximum temperature (degC)',CDP_Max,'date')


cs_start = 1948
cs_end = 1984
CDP_Max = function_M.Calendar_Day_Percentile(MaxT_Perth,90,7,Dates,'maximum temperature (degC)',cs_start,cs_end)
Clim_Scale_Charac = function_M.Extend_Summer_Heatwaves(MaxT_Perth, True, cs_start,cs_end,'maximum temperature (degC)',CDP_Max,'date')


cs_start = 1985
cs_end = 2021
CDP_Max = function_M.Calendar_Day_Percentile(MaxT_Perth,90,7,Dates,'maximum temperature (degC)',cs_start,cs_end)
Clim_Scale_Charac = function_M.Extend_Summer_Heatwaves(MaxT_Perth, True, cs_start,cs_end,'maximum temperature (degC)',CDP_Max,'date')

#Different Timesalces ~~ 55 years
cs_start = 1911
cs_end = 1965
CDP_Max = function_M.Calendar_Day_Percentile(MaxT_Perth,90,7,Dates,'maximum temperature (degC)',cs_start,cs_end)
Clim_Scale_Charac = function_M.Extend_Summer_Heatwaves(MaxT_Perth, True, cs_start,cs_end,'maximum temperature (degC)',CDP_Max,'date')


cs_start = 1966
cs_end = 2020
CDP_Max = function_M.Calendar_Day_Percentile(MaxT_Perth,90,7,Dates,'maximum temperature (degC)',cs_start,cs_end)
Clim_Scale_Charac = function_M.Extend_Summer_Heatwaves(MaxT_Perth, True, cs_start,cs_end,'maximum temperature (degC)',CDP_Max,'date')


#%% To separate into individual summers
ESS2 = Extended_Summer_Season2.resample()
Extended_Summer_Season2['date'] = pd.to_datetime(Extended_Summer_Season2['date'],format="%d/%m/%Y")
Yearly_Vic = Extended_Summer_Season2.resample(time='AS-DEC')


#%% To complete the alogirthm
'''
How to calculate the min max checking for the heatwave.
step 1, get the ID for max
Step 2 extract information of max heattwave and find the 1st, 2nd and 3rd date it starts
Step 3, cross check the 3 dates to see if a heatwave event is captured by minimum
Step 4, if so this is used as a heatwave event and keep it, if not resort to average 
Step 5, if the minimum wasnt working, check the average and see if this has an associated 3 day heatwave event recorded for the same period
Step 6, if it is keep this heatwave event

'''
#Expect 50% all ALL days to be record or roughly 50%
CDP_Max = function_M.Calendar_Day_Percentile(MaxT_Perth,90,7,Dates,'maximum temperature (degC)',1911,1940)
Clim_Scale_Charac2 = function_M.Extend_Summer_Heatwavesv2(MaxT_Perth, True, 1911,1940,'maximum temperature (degC)',CDP_Max,'date')



