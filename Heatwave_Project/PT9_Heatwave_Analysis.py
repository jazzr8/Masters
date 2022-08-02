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
Max_Heatwaves = function_M.Extend_Summer_Heatwaves_v1(Daily_MaxMin,True, 1941, 1970,'Max',CDP_Max,'date')
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
    
                          




#%%DEBUG CODE
Is_Max = True
Dataset = Daily_MaxMin
date_title = 'date'
Start_Year =1911
End_Year = 1940
Column_Name_Max_Min_Ave = 'Max'
CDP = CDP_Max
#We alrwady have the CPD data

if (Is_Max == True):
    Q_Threshold = 3
else:
    Q_Threshold = 2
#Get
import numpy as np, warnings, pandas as pd
#Get 3 vectors of year month and day    
Dataset['year'] =Dataset[date_title].dt.year
Dataset['month']=Dataset[date_title].dt.month
Dataset['day']  =Dataset[date_title].dt.day
#Get the data into the year range we want
Data = Dataset[Dataset['year'] <= End_Year]
Data = Data[Data['year'] >= Start_Year-1]
Data = Data.reset_index()



#Define the excess heat factor vectors for max_min_ave
#first day in focus is index 32
EHF = []#np.zeros(len(Data))
EHIacc = []#np.zeros(len(Data))
EHIsig = []#np.zeros(len(Data))
EHIacclpositive = []#np.zeros(len(Data)) #To Sim  max[1,EHIacc]
EHFp= []#np.zeros(len(Data)) #To sim EHIsig*max[1,EHIacc]



for i in np.arange(Data.index[0]+33,Data.index[len(Data)-1]):
    #print(i)
    #-----3 day mean-----#
    D3mean = (Data[Column_Name_Max_Min_Ave][i] + Data[Column_Name_Max_Min_Ave][i-1]+Data[Column_Name_Max_Min_Ave][i-2])/3

    #-----i-32 to i - 3-----#
    D323SUM = 0
    for q in range(3,33):
        D323SUM = D323SUM + Data[Column_Name_Max_Min_Ave][i-q]
        
    D323mean = D323SUM/len(range(3,33))
    #-----EHI(accl)-----#
    EHIacc_single = D3mean - D323mean
    EHIacc.append(EHIacc_single*1)
    #print(EHIacc)
    EHIacc_singlePOS = np.max([1,EHIacc_single])
    
    EHIacclpositive.append(EHIacc_singlePOS*1)

    #-----Tn-----#
    CDPsortd = CDP[CDP['day'] == Data['day'][i]]    
    CDPsortm = CDPsortd[CDPsortd['month'] == Data['month'][i]]
    CDPsortm.reset_index()
    Index = CDPsortm.index[0]
    T_CDP = CDPsortm['Temp'][Index]
    #print(T_CDP)
    #-----EHI(sig) -----#
    EHIsig_single = D3mean - T_CDP
    EHIsig.append(EHIsig_single)
    
    #-----EHF -----#
    EHF.append(EHIacc_single* EHIsig_single) #degC^2
    EHFp.append(np.max([1,EHIacc_single]) * EHIsig_single)
    


EHF = pd.DataFrame(EHF,columns=['Excess Heat Factor'])
EHIacc = pd.DataFrame(EHIacc,columns=['Excess Heat Index Acclimatised'])
EHIsig = pd.DataFrame(EHIsig,columns=['Excess Heat Index Significant'])
EHIacclpositive = pd.DataFrame(EHIacclpositive,columns=['Excess Heat Index Acclimatised Maximum Will Always be Positive'])
EHFp = pd.DataFrame(EHFp,columns=["Excess Heat Factor Positive For Continuation of Long Heatwaves"])


#EHIacc = pd.Series(EHIacc,name="Excess Heat Index Acclimatised")

#EHFp = pd.concat(EHFp,axis=0)
#EHFp = EHFp.to_frame(name="Excess Heat Factor Positive For Continuation of Long Heatwaves")




ForDates = np.arange(Data.index[0]+33,Data.index[len(Data)-1])

DateData = Data['date']
DateData = DateData[DateData.index>= Data.index[0]+34]
DD = DateData.reset_index()

#Need to add dates



EHFvect = pd.concat([DD, EHIacc,EHIacclpositive,EHIsig,EHF,EHFp],axis=1)
Heatwave_Characteristics_Onset = pd.merge(Data,EHFvect,how='right',on = ['date'])

#This doesn't work cause it is not positive we know it does work, but now I have relaised that a addition does not work so I stuffed up, now I need to implement the onset of the 
#heatwave as the first three days where both EHI are positve, and once this is checked, let the subsequent daysave the EHIaccl as max[1,EHIaccl[i]] so itll most likely be 
#3 or 4 if loops to extract the heatwave event.]


list_heatwaves = []
heat_days = 0
count  = 0
for i in range(len(EHF)):
    #Define the heat_days>= 3 for long heatwave periods
    if (heat_days >= 3):
        #Define the heatwave continuation
        if(EHFvect['Excess Heat Index Significant'][i] > 0):
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
        if((EHFvect['Excess Heat Index Acclimatised'][i]> 0) and (EHFvect['Excess Heat Index Significant'][i] > 0)):
            heat_days = heat_days + 1
        else:
            heat_days  = 0
            
heatwave_df = pd.concat(list_heatwaves,axis=0)
print(heatwave_df)

ext_sum_heatwave = (heatwave_df.loc[heatwave_df['month']>=11])
ext_sum_heatwave2 =  heatwave_df.loc[heatwave_df['month']<=3]
Extended_Summer_Season = pd.concat([ext_sum_heatwave,ext_sum_heatwave2]).sort_values(by=[date_title], ascending=True)

#Now I need to find 1/11 shit
id_Max = Extended_Summer_Season['id'] 
ids = id_Max.drop_duplicates( keep='first', inplace=False)



for i in ids:
    CheckL = Extended_Summer_Season[Extended_Summer_Season['id']==i]
    LeftCheck = CheckL[CheckL['day']==1]
    LeftCheck = LeftCheck[LeftCheck['month']==11]
    #print(LeftCheck)
    CheckR = Extended_Summer_Season[Extended_Summer_Season['id']==i]
    RightCheck = CheckR[CheckR['day']==31]
    RightCheck = RightCheck[RightCheck['month']==3]
    #print(RightCheck)
    if (len(LeftCheck) == 1):
        Extended_Summer_Season = pd.concat([Extended_Summer_Season,heatwave_df[heatwave_df['id']==i]]).sort_values(by=[date_title], ascending=True)   
        #print(1)
    elif (len(RightCheck) == 1):
        Extended_Summer_Season = pd.concat([Extended_Summer_Season,heatwave_df[heatwave_df['id']==i]]).sort_values(by=[date_title], ascending=True)
Extended_Summer_Season.drop_duplicates(subset = [date_title],keep='first')


#Have fixed now need to check if it runs properly and if the values are matching up within it because I can generate hheatwaves.










