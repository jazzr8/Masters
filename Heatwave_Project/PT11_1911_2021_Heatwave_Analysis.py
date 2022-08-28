

import pandas as pd, PT5_Functions_For_Masters as function_M, matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib as mpl


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

#%% Heatwave comparison


Heatwave_80_old = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],80,7,Dates)
Heatwave_80_new = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],80,7,Dates)
Heatwave_80_sub = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],80,7,Dates)
old_80_num =Heatwave_80_old['id'].max()
new_80_num = Heatwave_80_new['id'].max()
sub_80_num = Heatwave_80_sub['id'].max()

Heatwave_825_old = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],82.5,7,Dates)
Heatwave_825_new = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],82.5,7,Dates)
Heatwave_825_sub = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],82.5,7,Dates)
old_825_num =Heatwave_825_old['id'].max()
new_825_num =Heatwave_825_new['id'].max()
sub_825_num = Heatwave_825_sub['id'].max()

Heatwave_85_old = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],85,7,Dates)
Heatwave_85_new = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],85,7,Dates)
Heatwave_85_sub = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],85,7,Dates)
old_85_num = Heatwave_85_old['id'].max()
new_85_num =Heatwave_85_new['id'].max()
sub_85_num = Heatwave_85_sub['id'].max()


Heatwave_875_old = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],87.5,7,Dates)
Heatwave_875_new = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],87.5,7,Dates)
Heatwave_875_sub = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],87.5,7,Dates)
old_875_num =Heatwave_875_old['id'].max()
new_875_num =Heatwave_875_new['id'].max()
sub_875_num = Heatwave_875_sub['id'].max()


Heatwave_90_old = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],90,7,Dates)
Heatwave_90_new = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],90,7,Dates)
Heatwave_90_sub = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],90,7,Dates)
old_90_num =Heatwave_90_old['id'].max()
new_90_num =Heatwave_90_new['id'].max()
sub_90_num = Heatwave_90_sub['id'].max()

Heatwave_925_old = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],92.5,7,Dates)
Heatwave_925_new = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],92.5,7,Dates)
Heatwave_925_sub = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],92.5,7,Dates)
old_925_num =Heatwave_925_old['id'].max()
new_925_num =Heatwave_925_new['id'].max()
sub_925_num = Heatwave_925_sub['id'].max()


Heatwave_95_old = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],95,7,Dates)
Heatwave_95_new = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],95,7,Dates)
Heatwave_95_sub = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],95,7,Dates)
old_95_num =Heatwave_95_old['id'].max()
new_95_num =Heatwave_95_new['id'].max()
sub_95_num = Heatwave_95_sub['id'].max()


Heatwave_975_old = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],97.5,7,Dates)
Heatwave_975_new = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],97.5,7,Dates)
#Heatwave_975_sub = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],97.5,7,Dates)
old_975_num =Heatwave_975_old['id'].max()
new_975_num =Heatwave_975_new['id'].max()
#sub_975_num = Heatwave_975_sub['id'].max()

#%% These dont have heatwave events.
Heatwave_99_old = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],99,7,Dates)
Heatwave_99_new = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],99,7,Dates)
Heatwave_80_sub = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],80,7,Dates)
old_99_num =Heatwave_99_old['id'].max()
new_99_num =Heatwave_99_new['id'].max()

#%%
weather_df = pd.DataFrame([[old_80_num,old_825_num,old_85_num,old_875_num,old_90_num,old_925_num,old_95_num],
                           [new_80_num,new_825_num,new_85_num,new_875_num,new_90_num,new_925_num,new_95_num],
                           [sub_80_num,sub_825_num,sub_85_num,sub_875_num,sub_90_num,sub_925_num,new_95_num]],
                          index=pd.Index(["1961-1990", "1981-2010",'1994-2013']),
                          columns=(['80','82.5','85','87.5','90','92.5','95']))

cell_hover = {  # for row hover use <tr> instead of <td>
    'selector': 'td:hover',
    'props': [('background-color', '#ffffb3')]
}
headers = {
    'selector': 'th:not(.index_name)',
    'props': 'background-color: #000066; color: white;'
}

df_styled = weather_df.style.highlight_max()
print(weather_df.style.highlight_max())
weather_df.export(df_styled,"mytable.png")

#%% BOM and WMO CDP comparison
WMO = function_M.Calendar_Day_Percentile(Daily_MaxMin,95,15,Dates,'Min',1981,2010)
BOM = function_M.Calendar_Day_Percentile(Daily_MaxMin,95,15,Dates,'Min',1961,1991)
#%%
WMO_JM = WMO['Temp'].loc[0:90]
WMO_ND = WMO['Temp'].loc[305:365]
WMO_Ext_Sum = [WMO_ND,WMO_JM]

WMO_Ext_Sum = pd.concat(WMO_Ext_Sum,axis=0).reset_index()

BOM_JM = BOM['Temp'].loc[0:90]
BOM_ND = BOM['Temp'].loc[305:365]
BOM_Ext_Sum = [BOM_ND,BOM_JM]

BOM_Ext_Sum = pd.concat(BOM_Ext_Sum,axis=0).reset_index()

plt.plot(WMO_Ext_Sum['Temp'],'red',label ='WMO')
plt.plot(BOM_Ext_Sum['Temp'],color='black',label = 'BOM')
plt.title('Extended Summer Heatwave 95th CDP')
plt.legend()



#%%Agreed 85% percentile






#%%
'''
PERTH REG TO PERTH ACORN SAT COMP 1967-1992
Using the 1961-1990 dataset and a percentile of 85% moderate heatwaves and 90% for extreme heatwaves.
'''
Heatwave_85, EHF_Max_85, EHF_Min_85, CDP_85  =  function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],85,7,Dates)
Heatwave_90, EHF_Max_90, EHF_Min_90, CDP_90  = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],90,7,Dates)



#%% All the stuff to rearrange for heatwave individuals only::
    
'''
In order from first column to last
1. Index [1,2,3...]
2. Heatwave ID 
3. Date
4. Max
5. Min
6. Ave
7. CDPmax
8. CPDmin
9. EHF Max
10. EHF Min
11. Duration
12. Amplitude Max
13. Amplitude Min
14. Average Max
15. Average Min
16. Accumalated heat Daily
17. Accumalate heat total

'''
'''Begin by cleaning the dataset, Pt1 remove year, month day and reset index to 0'''
del Heatwave_85['year']
del Heatwave_85['month']
del Heatwave_85['day']
#Create copy
Heatwave_85_fixed = Heatwave_85.copy()

#
Heatwave_85_fixed =  Heatwave_85_fixed.set_index('id')
Heatwave_85_fixed =  Heatwave_85_fixed.reset_index()


'''Add the CDP'''

CDP_85 = CDP_85.set_index['date']
#%%
CDP_periods = []
for i in range(0,len(Heatwave_85_fixed)):
    #Extract the day
    data = Heatwave_85_fixed.loc[i]
    
    #Get Month and Day
    Day  = data['date'].day
    Month  = data['date'].month
    
    #Find the CDP heatwave day
    CDP_day = CDP_85.loc[(CDP_85['date'].dt.month==Month) &(CDP_85['date'].dt.day==Day)]
    CDP_periods.append(CDP_day)
    
CDP_periods = pd.concat(CDP_periods, axis= 0)

#Fix Index
CDP_periods =  CDP_periods.set_index('date')
CDP_periods =  CDP_periods.reset_index()

#Delete date column
del CDP_periods['date']
#Add the idnex together should be the same days 
Heatwave_85_fixed = pd.merge(left = Heatwave_85_fixed,right  =CDP_periods,left_index=True,right_index=True  )
#%% EHF stuff Max

del EHF_Max_85['year']
del EHF_Max_85['month']
del EHF_Max_85['day']
del EHF_Max_85['Excess Heat Index Acclimatised']
del EHF_Max_85['Excess Heat Index Significant']
del EHF_Max_85['Max']
del EHF_Max_85['Min']
del EHF_Max_85['Ave']
EHF_Max_85 = EHF_Max_85.set_index['date']
#%%

EHF_Useful = []
for i in range(0,len(Heatwave_85_fixed)):
    #Extract the day
    data = Heatwave_85_fixed.loc[i]
    
    #Get Month and Day
    Day  = data['date'].day
    Month  = data['date'].month
    Year  = data['date'].year
    #Find the CDP heatwave day
    EHF_Max = EHF_Max_85.loc[(EHF_Max_85['date'].dt.year==Year) & (EHF_Max_85['date'].dt.month==Month) &(EHF_Max_85['date'].dt.day==Day)]
    EHF_Useful.append(EHF_Max)
    
EHF_Useful = pd.concat(EHF_Useful, axis= 0)

#Fix Index
EHF_Useful =  EHF_Useful.set_index('date')
EHF_Useful =  EHF_Useful.reset_index()

#Delete date column
del EHF_Useful['date']
#Add the idnex together should be the same days 
Heatwave_85_fixed = pd.merge(left = Heatwave_85_fixed,right  =EHF_Useful,left_index=True,right_index=True  )



Heatwave_85_fixed= Heatwave_85_fixed.rename(columns={'Excess Heat Factor':'Excess Heat Factor Max T'})



#%% EHF stuff Min




del EHF_Min_85['year']
del EHF_Min_85['month']
del EHF_Min_85['day']
del EHF_Min_85['Excess Heat Index Acclimatised']
del EHF_Min_85['Excess Heat Index Significant']
del EHF_Min_85['Max']
del EHF_Min_85['Min']
del EHF_Min_85['Ave']
EHF_Min_85 = EHF_Min_85.set_index['date']
#%%

EHF_Useful = []
for i in range(0,len(Heatwave_85_fixed)):
    #Extract the day
    data = Heatwave_85_fixed.loc[i]
    
    #Get Month and Day
    Day  = data['date'].day
    Month  = data['date'].month
    Year  = data['date'].year
    #Find the CDP heatwave day
    EHF_Min = EHF_Min_85.loc[(EHF_Min_85['date'].dt.year==Year) & (EHF_Min_85['date'].dt.month==Month) &(EHF_Min_85['date'].dt.day==Day)]
    EHF_Useful.append(EHF_Max)
    
EHF_Useful = pd.concat(EHF_Useful, axis= 0)

#Fix Index
EHF_Useful =  EHF_Useful.set_index('date')
EHF_Useful =  EHF_Useful.reset_index()

#Delete date column
del EHF_Useful['date']
#Add the idnex together should be the same days 
Heatwave_85_fixed = pd.merge(left = Heatwave_85_fixed,right  =EHF_Useful,left_index=True,right_index=True  )


Heatwave_85_fixed= Heatwave_85_fixed.rename(columns={'Excess Heat Factor':'Excess Heat Factor Min T'})














#%%Characteristic #1
'''
Graph of Duration of heatwaves.
Graph of Number of heatwaves.
Graph of Number of Heatdays Per Year/
'''
Heatwave = Heatwave_90_sub



ids = Heatwave['id'].drop_duplicates( keep='first', inplace=False)
#I want to know the average yearly duration and the number of heatwaves.
idss = []
Duration = []
Number_Per_Season = []
Year_Heatwaves = []

for i in ids:
    '''Extract the heatwave event'''
    individal_heatwave = Heatwave[Heatwave['id']==i]
    individal_heatwave = individal_heatwave.reset_index()
    '''Find length of heatwave'''
    Length_Heatwave = len(individal_heatwave['date'])
    
    '''Lets locate the day, month and year of the first day'''
    #Already done
    
    '''Remembering that the season of the 1911 goes from ~1911-Nov to ~1912-March'''
    if (min(individal_heatwave['month']) <= 6):
        '''This means the year in focus is only Year-i'''
        Year = min(individal_heatwave['year']) - 1
    elif (min(individal_heatwave['month']) > 6):
        Year = min(individal_heatwave['year'])
    idss.append(i)
    Year_Heatwaves.append(Year)
    Duration.append(Length_Heatwave)
'''Put it all together and we get'''
Year_Heatwaves = pd.DataFrame(Year_Heatwaves,columns=['Years With Heatwaves']) 
Duration = pd.DataFrame(Duration,columns=['Duration of Heatwaves']) 
idss = pd.DataFrame(idss,columns=['Heatwave ID']) 
    

'''This is strictly be for individual heatwave analysis '''
Heatwave_Characteristics=pd.concat([idss,Year_Heatwaves,Duration],axis=1)


'''This next section is for Yearly heatwave analysis'''

'''Preliminary Scatter Plot'''
plt.scatter(Heatwave_Characteristics['Years With Heatwaves'],Heatwave_Characteristics['Duration of Heatwaves'])

year_id = Heatwave_Characteristics['Years With Heatwaves'].drop_duplicates( keep='first', inplace=False)

days_Heat =[]
Ave_Duration = []
Heatwave_events_py = []
Years =  []

for y in year_id:
    '''
    # Heatdays
    # Average Length
    # Number of heatwave events
    '''
    ''' Heatdays'''
    heatwaves = Heatwave_Characteristics[Heatwave_Characteristics['Years With Heatwaves']==y]
    Heatdays = sum(heatwaves['Duration of Heatwaves'])
    
    '''Average Length'''
    Ave_Len = heatwaves['Duration of Heatwaves'].mean()
    
    '''Number of heatwaves'''
    Num_Heat = len(heatwaves['Years With Heatwaves'])    
    Years.append(y)
    
    days_Heat.append(Heatdays)
    Heatwave_events_py.append(Num_Heat)
    Ave_Duration.append(Ave_Len)

days_Heat = pd.DataFrame(days_Heat,columns=['Heat Days Per Year (d)']) 
Heatwave_events_py = pd.DataFrame(Heatwave_events_py,columns=['Events Per Year (#)']) 
Ave_Duration = pd.DataFrame(Ave_Duration,columns=['Average_Duration (d/y)']) 
Years = pd.DataFrame(Years,columns=['Season Beginning Year']) 


Yearly_Characteristics=pd.concat([Years,days_Heat,Heatwave_events_py,Ave_Duration],axis=1)

        



def hot_period_Classification_Perth_V2(EHF,Q):
    '''
    

    Parameters
    ----------
    EHF : Dataframe
        From another function in defining heatwaves in the extended Summer period.

    Returns
    -------
    The hot periods throughout the year, these include heatwaves and warmwaves
    throughout the defined period.

    '''
    
#%% Developing the scatterplot. for Max Min correlation
def Excess_Heat_Factor_Function(Data,date_title,Column_Name,CDP,CDPColumn_Name):
    '''

    Parameters
    ----------
    Data : True or False
        It is already caterogised as False therefore to use it for Maximum Temperatures need to say True.

    Returns
    -------
    The threshold in order to be a heatwave.  Of heatwave events, that cause humans discomfort. So skips first hot day and 
    has last day as of a lag effect of heat-related health problems.

    '''
import numpy as np ,pandas as pd
from numpy import cov
from scipy.stats import pearsonr
#Our defined heatwaves
Heatwave_1967_1992 =Heatwave_85_fixed.set_index('id')
Heatwave_1967_1992 = Heatwave_1967_1992.loc[49:79]
Heatwave_Max_T = Heatwave_1967_1992['Max']
Heatwave_Min_T = Heatwave_1967_1992['Min']
Dates_for_heatwaves = Heatwave_1967_1992['date']


#define data
x = Heatwave_Max_T
y = Heatwave_Min_T

#find line of best fit
a, b = np.polyfit(x, y, 1)

#add points to plot
plt.scatter(x, y)

#add line of best fit to plot
plt.plot(x, a*x+b)   
covariance =  cov(x, y)
#BOM regional office data ehatwaves

corr, _ = pearsonr(x, y)
print('Pearsons correlation: %.3f' % corr)
#Pearsons correlation: 0.645 therefore a moderate correlation which is what we expect.


#define data
DMM = Daily_MaxMin.set_index('date')
x1 = DMM['Max'].loc['1967':'1992']
y1 = DMM['Min'].loc['1967':'1992']

#find line of best fit
a, b = np.polyfit(x1, y1, 1)

#add points to plot
plt.scatter(x1, y1)

#add line of best fit to plot
plt.plot(x1, a*x1+b,color ='black')   
covariance =  cov(x1, y1)
#BOM regional office data ehatwaves

corr, _ = pearsonr(x1, y1)
print('Pearsons correlation: %.3f' % corr)
#Pearsons correlation: 0.645 therefore a moderate correlation which is what we expect.




#%%1967 -1992