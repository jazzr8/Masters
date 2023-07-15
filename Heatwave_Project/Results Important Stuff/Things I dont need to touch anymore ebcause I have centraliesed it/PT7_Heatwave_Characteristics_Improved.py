#%% THE RELATIVE HEATWAVE DEFINITION AS A FUNCTION


'''
All I care about for this is that this actually works and not generate the list yet
'''
#%% PACKAGES
import pandas as pd, numpy as np,matplotlib.pyplot as plt, xarray as xr,PT5_Functions_For_Masters as function_M
from scipy import stats


#%% Known Information

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


CDP_Max = function_M.Calendar_Day_Percentile(MaxT_Perth,90,7,Dates,'maximum temperature (degC)',1951,2000)

#MINIMUM TEMPERATURE
# Load Data only using min Temperature for the initial start

MinT_Perth_Data = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\tmin.009021.daily.csv")
MinT_Perth = MinT_Perth_Data.copy().drop(0)
# Apply datetime
MinT_Perth['date'] = pd.to_datetime(MinT_Perth['date'],format="%d/%m/%Y")

# Apply groupby functiom
MinT_Perth['year']=MinT_Perth['date'].dt.year
MinT_Perth['month']=MinT_Perth['date'].dt.month
MinT_Perth['day']=MinT_Perth['date'].dt.day

CDP_Min = function_M.Calendar_Day_Percentile(MinT_Perth,90,7,Dates,'minimum temperature (degC)',1911,2019)

#AVERAGE TEMPERATURE
# Load Data only using max Temperature for the initial start
#CDP_Ave = function_M.Calendar_Day_Percentile(AveT_Perth,95,7,Dates,'maximum temperature (degC)',1911,1950)


#Maximum
Max_Heatwaves = function_M.Extend_Summer_Heatwaves(MaxT_Perth, True, 1951,2000,'maximum temperature (degC)',CDP_Max,'date')

#Mimimum
Min_Heatwaves = function_M.Extend_Summer_Heatwaves(MinT_Perth, False, 1951,2000,'minimum temperature (degC)',CDP_Min,'date')
#Average
#Ave_Temp_Heatwaves = function_M.Extend_Summer_Heatwaves(AveT_Perth, False, 1910,2019,'maximum temperature (degC)',CDP_Ave,'date')

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


#The final box definition is the climatological scale 
cs_start = 1981
cs_end = 2010
CDP_Max = function_M.Calendar_Day_Percentile(MaxT_Perth,90,7,Dates,'maximum temperature (degC)',cs_start,cs_end)
Clim_Scale_Charac = function_M.Extend_Summer_Heatwaves(MaxT_Perth, True, cs_start,cs_end,'maximum temperature (degC)',CDP_Max,'date')


















#%%


MaxT_Perth['year'] =MaxT_Perth['date'].dt.year
MaxT_Perth['month']=MaxT_Perth['date'].dt.month
MaxT_Perth['day']  =MaxT_Perth['date'].dt.day
#Get the data into the year range we want





#Define the excess heat factor vectors for max_min_ave
#first day in focus is index 32
EHF = np.zeros(len(MaxT_Perth))
EHIacc = np.zeros(len(MaxT_Perth))
EHIsig = np.zeros(len(MaxT_Perth))
EHIacclpositive = np.zeros(len(MaxT_Perth)) #To Sim  max[1,EHIacc]
EHFp= np.zeros(len(MaxT_Perth)) #To sim EHIsig*max[1,EHIacc]



for i in range(33,MaxT_Perth.index[len(MaxT_Perth)-1]):

    #-----3 day mean-----#
    D3mean = (MaxT_Perth['maximum temperature (degC)'][i] + MaxT_Perth['maximum temperature (degC)'][i-1]+MaxT_Perth['maximum temperature (degC)'][i-2])/3

    #-----i-32 to i - 3-----#
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

Heatwave_Characteristics_Onset = pd.concat([MaxT_Perth,EHFvect],axis=1)
#This doesn't work cause it is not positive we know it does work, but now I have relaised that a addition does not work so I stuffed up, now I need to implement the onset of the 
#heatwave as the first three days where both EHI are positve, and once this is checked, let the subsequent daysave the EHIaccl as max[1,EHIaccl[i]] so itll most likely be 
#3 or 4 if loops to extract the heatwave event.]
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
Extended_Summer_Season = pd.concat([ext_sum_heatwave,ext_sum_heatwave2]).sort_values(by=['date'], ascending=True)


Extended_Summer_Season












































