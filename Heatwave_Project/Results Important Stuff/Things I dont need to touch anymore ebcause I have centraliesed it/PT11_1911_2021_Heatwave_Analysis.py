import sys


sys.path.append(r"C:\Users\jarra\Desktop\Masters\Heatwave_Project")
import pandas as pd, PT13_Functions_For_Masters_New_Test as function_M, matplotlib.pyplot as plt
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


Heatwave_80_old, CDP_Max, EHF_Max, EHF_Min = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],80,7,Dates)
Heatwave_80_new, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],80,7,Dates)
Heatwave_80_sub, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],80,7,Dates)
old_80_num =Heatwave_80_old['id'].max()
new_80_num = Heatwave_80_new['id'].max()
sub_80_num = Heatwave_80_sub['id'].max()

Heatwave_825_old, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],82.5,7,Dates)
Heatwave_825_new, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],82.5,7,Dates)
Heatwave_825_sub, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],82.5,7,Dates)
old_825_num =Heatwave_825_old['id'].max()
new_825_num =Heatwave_825_new['id'].max()
sub_825_num = Heatwave_825_sub['id'].max()

Heatwave_85_old, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],85,7,Dates)
Heatwave_85_new, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],85,7,Dates)
Heatwave_85_sub, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],85,7,Dates)
old_85_num = Heatwave_85_old['id'].max()
new_85_num =Heatwave_85_new['id'].max()
sub_85_num = Heatwave_85_sub['id'].max()


Heatwave_875_old, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],87.5,7,Dates)
Heatwave_875_new, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],87.5,7,Dates)
Heatwave_875_sub, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],87.5,7,Dates)
old_875_num =Heatwave_875_old['id'].max()
new_875_num =Heatwave_875_new['id'].max()
sub_875_num = Heatwave_875_sub['id'].max()


Heatwave_90_old, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],90,7,Dates)
Heatwave_90_new, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],90,7,Dates)
Heatwave_90_sub, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],90,7,Dates)
old_90_num =Heatwave_90_old['id'].max()
new_90_num =Heatwave_90_new['id'].max()
sub_90_num = Heatwave_90_sub['id'].max()

Heatwave_925_old, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],92.5,7,Dates)
Heatwave_925_new, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],92.5,7,Dates)
Heatwave_925_sub, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],92.5,7,Dates)
old_925_num =Heatwave_925_old['id'].max()
new_925_num =Heatwave_925_new['id'].max()
sub_925_num = Heatwave_925_sub['id'].max()


Heatwave_95_old, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],95,7,Dates)
Heatwave_95_new, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],95,7,Dates)
Heatwave_95_sub, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],95,7,Dates)
old_95_num =Heatwave_95_old['id'].max()
new_95_num =Heatwave_95_new['id'].max()
sub_95_num = Heatwave_95_sub['id'].max()


Heatwave_975_old, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],97.5,7,Dates)
Heatwave_975_new, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],97.5,7,Dates)
Heatwave_975_sub, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],97.5,7,Dates)
old_975_num =Heatwave_975_old['id'].max()
new_975_num =Heatwave_975_new['id'].max()
sub_975_num = Heatwave_975_sub['id'].max()

#%% These dont have heatwave events.
Heatwave_99_old, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],99,7,Dates)
Heatwave_99_new, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1981,2010],['Max','Min'],99,7,Dates)
Heatwave_80_sub, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1994,2013],['Max','Min'],80,7,Dates)
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
WMO, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,95,15,Dates,'Min',1981,2010)
BOM, CDP_Max, EHF_Max, EHF_Min  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,95,15,Dates,'Min',1961,1991)
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
Heatwave_85, CDP_85,  EHF_Max_85, EHF_Min_85   =  function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],85,7,Dates)
Heatwave_90, CDP_90, EHF_Max_90, EHF_Min_90  = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],90,7,Dates)



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

Heatwave_85_fixed= Heatwave_85_fixed.rename(columns={'Temp Max':'85 percentile daily Max'})
Heatwave_85_fixed= Heatwave_85_fixed.rename(columns={'Temp Min':'85 percentile daily Min'})

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
    EHF_Useful.append(EHF_Min)
    
EHF_Useful = pd.concat(EHF_Useful, axis= 0)

#Fix Index
EHF_Useful =  EHF_Useful.set_index('date')
EHF_Useful =  EHF_Useful.reset_index()

#Delete date column
del EHF_Useful['date']
#Add the idnex together should be the same days 
Heatwave_85_fixed = pd.merge(left = Heatwave_85_fixed,right  =EHF_Useful,left_index=True,right_index=True  )


Heatwave_85_fixed= Heatwave_85_fixed.rename(columns={'Excess Heat Factor':'Excess Heat Factor Min T'})

##This needs to be fixed
Heatwave_85_fixed.to_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Analysis\Heatwave Events\Heatwave_Events.csv")



#%%The full table

Heatwave_85, EHF_Max_85, EHF_Min_85, CDP_85, HWMax  =  function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1911,2020], [1961,1990],['Max','Min'],85,7,Dates)


'''
In order from first column to last
1. Index [1,2,3...] - DONE
2. Heatwave ID - DONE
3. Date - DONE
4. Max - DONE
5. Min - DONE
6. Ave - DONE
7. CDPmax - DONE
8. CPDmin - DONE
9. EHF Max - DONE
10. EHF Min - DONE
11. Duration - DONE
12. Amplitude Max - DONE
13. Amplitude Min - DONE
14. Average Max - Done
15. Average Min - Done
16. Accumalated heat Daily - DONE
17. Accumalate heat total - DONE
'''

#Heatwave_Table_Generator(Heatwave_Full_Dataset,EHF_Max,EHF_Min,CDP,percentile)

Heatwave_Full_Dataset = Heatwave_85
percentile = 85
Heatwave_Table = Heatwave_Full_Dataset.reset_index()
CDP = CDP_85
EHF_Max = EHF_Max_85
EHF_Min = EHF_Min_85

'''Begin by cleaning the dataset, Pt1 remove year, month day and reset index to 0'''
del Heatwave_Table['year']
del Heatwave_Table['month']
del Heatwave_Table['day']
#Make sure it goes into order
Heatwave_Table =  Heatwave_Table.set_index('id')
Heatwave_Table =  Heatwave_Table.reset_index()



#Now lets add the max and min CDP
CDP_periods = []
for i in range(0,len(Heatwave_Table)):
    #Extract the day
    HW_DAY = Heatwave_Table.loc[i]
    
    #Get Month and Day
    Day  = HW_DAY['date'].day
    Month  = HW_DAY['date'].month
    
    #Find the CDP heatwave day
    CDP_day = CDP.loc[(CDP['date'].dt.month==Month) &(CDP['date'].dt.day==Day)]
    CDP_periods.append(CDP_day)
    
CDP_periods = pd.concat(CDP_periods, axis= 0)

#Fix Index
CDP_periods =  CDP_periods.set_index('date')
CDP_periods =  CDP_periods.reset_index()

#Delete date column
del CDP_periods['date']
#Add the idnex together should be the same days 
Heatwave_Table = pd.merge(left = Heatwave_Table,right  =CDP_periods,left_index=True,right_index=True  )

Heatwave_Table= Heatwave_Table.rename(columns={'Temp Max':'{} percentile daily Max'.format(percentile)})
Heatwave_Table= Heatwave_Table.rename(columns={'Temp Min':'{} percentile daily Min'.format(percentile)})




#NOW THE EHFs
#Delete the unwanted
del EHF_Max['year']
del EHF_Max['month']
del EHF_Max['day']
del EHF_Max['Excess Heat Index Acclimatised']
del EHF_Max['Excess Heat Index Significant']
del EHF_Max['Max']
del EHF_Max['Min']
del EHF_Max['Ave']

del EHF_Min['year']
del EHF_Min['month']
del EHF_Min['day']
del EHF_Min['Excess Heat Index Acclimatised']
del EHF_Min['Excess Heat Index Significant']
del EHF_Min['Max']
del EHF_Min['Min']
del EHF_Min['Ave']



EHF_Useful = []
for i in range(0,len(Heatwave_Table)):
    #Extract the day
    HW_D = Heatwave_Table.loc[i]
    
    #Get Month and Day
    Day  = HW_D['date'].day
    Month  = HW_D['date'].month
    Year  = HW_D['date'].year
    #Find the CDP heatwave day
    EHF_Max_iND = EHF_Max.loc[(EHF_Max_85['date'].dt.year==Year) & (EHF_Max['date'].dt.month==Month) &(EHF_Max['date'].dt.day==Day)]
    EHF_Useful.append(EHF_Max_iND)
    
EHF_Useful = pd.concat(EHF_Useful, axis= 0)

#Fix Index
EHF_Useful =  EHF_Useful.set_index('date')
EHF_Useful =  EHF_Useful.reset_index()

#Delete date column
del EHF_Useful['date']
#Add the idnex together should be the same days 
Heatwave_Table = pd.merge(left = Heatwave_Table,right  =EHF_Useful,left_index=True,right_index=True  )



Heatwave_Table= Heatwave_Table.rename(columns={'Excess Heat Factor':'Excess Heat Factor Max T'})




EHF_Useful2 = []
for i in range(0,len(Heatwave_Table)):
    #Extract the day
    HW_D = Heatwave_Table.loc[i]
        
    #Get Month and Day
    Day  = HW_D['date'].day
    Month  = HW_D['date'].month
    Year  = HW_D['date'].year
    #Find the CDP heatwave day
    EHF_Min_Ind = EHF_Min.loc[(EHF_Min['date'].dt.year==Year) & (EHF_Min['date'].dt.month==Month) &(EHF_Min['date'].dt.day==Day)]
    EHF_Useful2.append(EHF_Min_Ind)
    
EHF_Useful2 = pd.concat(EHF_Useful2, axis= 0)

#Fix Index
EHF_Useful2 =  EHF_Useful2.set_index('date')
EHF_Useful2 =  EHF_Useful2.reset_index()

#Delete date column
del EHF_Useful2['date']
#Add the idnex together should be the same days 
Heatwave_Table = pd.merge(left = Heatwave_Table,right  =EHF_Useful2,left_index=True,right_index=True  )


Heatwave_Table= Heatwave_Table.rename(columns={'Excess Heat Factor':'Excess Heat Factor Min T'})



#Duration
ids = Heatwave_Table['id'].drop_duplicates( keep='first', inplace=False)
Duration = []


for i in ids:
    '''Extract the heatwave event'''
    individal_heatwave = Heatwave_Table[Heatwave_Table['id']==i]
    individal_heatwave = individal_heatwave.reset_index()
    '''Find length of heatwave'''
    Length_Heatwave = len(individal_heatwave['date'])
    
    '''Lets locate the day, month and year of the first day'''
    #Already done
    
    for length in range(0,Length_Heatwave):
        Duration.append(Length_Heatwave)
'''Put it all together and we get'''

Duration = pd.DataFrame(Duration,columns=['Duration of Heatwaves']) 
Heatwave_Table = pd.merge(left = Heatwave_Table,right  =Duration,left_index=True,right_index=True  )


#Accumulation Daily - So amplitude of each day
'''So we do this by this definition for each day
Temperature of the day - CDP of the day
'''

#Lets define the data templates for the accumulation
Heat_Accumulation_Max = []
Heat_Accumulation_Min = []
Heat_Accumulation_Tot = []

#For loop to go through each day
for i in range(0,len(Heatwave_Table)):
    #Max Accumulation
    Ind_Max_Acc = Heatwave_Table['Max'][i] - Heatwave_Table['{} percentile daily Max'.format(percentile)][i] 
    #Min Accumulation
    Ind_Min_Acc = Heatwave_Table['Min'][i] - Heatwave_Table['{} percentile daily Min'.format(percentile)][i]
    #Min Accumulation
    Ind_Tot_Acc = Ind_Max_Acc +  Ind_Min_Acc
    
    
    #Append
    Heat_Accumulation_Max.append(Ind_Max_Acc)
    Heat_Accumulation_Min.append(Ind_Min_Acc)
    Heat_Accumulation_Tot.append(Ind_Tot_Acc)
    
#Clean and Fix     #Not the best wording for the title ever
Heat_Accumulation_Max = pd.DataFrame(Heat_Accumulation_Max,columns = ['Maximum Heat Accumulation degC'])
Heat_Accumulation_Min = pd.DataFrame(Heat_Accumulation_Min,columns = ['Minimum Heat Accumulation degC'])
Heat_Accumulation_Tot = pd.DataFrame(Heat_Accumulation_Tot,columns = ['Total Heat Accumulation degC'])

Heatwave_Table = pd.merge(left = Heatwave_Table,right  =Heat_Accumulation_Max,left_index=True,right_index=True  )
Heatwave_Table = pd.merge(left = Heatwave_Table,right  =Heat_Accumulation_Min,left_index=True,right_index=True  )
Heatwave_Table = pd.merge(left = Heatwave_Table,right  =Heat_Accumulation_Tot,left_index=True,right_index=True  )


# Maximum Amplitude of the Max and Min
#Similar template to the duration but we are going to use a max on the greatest amplitude, of the max, min and total from the accumulation




Max_Amp = []
Min_Amp = []
Total_Amp = []
Accumulation_Max_Sum = []
Accumulation_Min_Sum = []
Accumulation_Total_Sum = []
Max_Mean = []
Min_Mean = []
Mean_Average= []

for i in ids:
    '''Extract the heatwave event'''
    individal_heatwave = Heatwave_Table[Heatwave_Table['id']==i]
    '''Find length of heatwave'''
    Length_Heatwave = len(individal_heatwave['date'])
    
    '''For each pf the Max Min and Total accumulation do a .max'''
    Max = individal_heatwave['Maximum Heat Accumulation degC'].max()
    Min = individal_heatwave['Minimum Heat Accumulation degC'].max() 
    Total = individal_heatwave['Total Heat Accumulation degC'].max() 
    
    '''Accumulation Total'''
    Max_Sum = individal_heatwave['Maximum Heat Accumulation degC'].sum()
    Min_Sum = individal_heatwave['Minimum Heat Accumulation degC'].sum() 
    Total_Sum = individal_heatwave['Total Heat Accumulation degC'].sum() 
    
    '''Means of the Temperature'''
    Mean_Max = individal_heatwave['Max'].mean()
    Mean_Min = individal_heatwave['Min'].mean() 
    Average_Mean = individal_heatwave['Ave'].mean() 
    
    
    
    
    
    '''Append these'''
      
    for length in range(0,Length_Heatwave):
        Max_Amp.append(Max)
        Min_Amp.append(Min)
        Total_Amp.append(Total)
        Accumulation_Max_Sum.append(Max_Sum)
        Accumulation_Min_Sum.append(Min_Sum)
        Accumulation_Total_Sum.append(Total_Sum)
        Max_Mean.append(Mean_Max)
        Min_Mean.append(Mean_Min)
        Mean_Average.append(Average_Mean)
'''Put it all together and we get'''

Max_Amp = pd.DataFrame(Max_Amp,columns=['Maximum Temperature Max Amplitude degC']) 
Min_Amp = pd.DataFrame(Min_Amp,columns=['Minimum Temperature Max Amplitude degC']) 
Total_Amp = pd.DataFrame(Total_Amp,columns=['Total Temperature Max Amplitude degC'])
Accumulation_Max_Sum = pd.DataFrame(Accumulation_Max_Sum,columns=['Maximum Temperature Total Accumulation degC']) 
Accumulation_Min_Sum = pd.DataFrame(Accumulation_Min_Sum,columns=['Minimum Temperature Total Accumulation degC']) 
Accumulation_Total_Sum = pd.DataFrame(Accumulation_Total_Sum,columns=['Total Temperature Total Accumulation degC']) 
Max_Mean = pd.DataFrame(Max_Mean,columns=['Heatwave Maximum Mean degC']) 
Min_Mean = pd.DataFrame(Min_Mean,columns=['Heatwave Minimum Mean degC']) 
Mean_Average = pd.DataFrame(Mean_Average,columns=['Heatwave Average Mean degC'])


Heatwave_Table = pd.merge(left = Heatwave_Table,right  =Max_Amp,left_index=True,right_index=True  )
Heatwave_Table = pd.merge(left = Heatwave_Table,right  =Min_Amp,left_index=True,right_index=True  )
Heatwave_Table = pd.merge(left = Heatwave_Table,right  =Total_Amp,left_index=True,right_index=True  )
Heatwave_Table = pd.merge(left = Heatwave_Table,right  =Accumulation_Max_Sum,left_index=True,right_index=True  )
Heatwave_Table = pd.merge(left = Heatwave_Table,right  =Accumulation_Min_Sum,left_index=True,right_index=True  )
Heatwave_Table = pd.merge(left = Heatwave_Table,right  =Accumulation_Total_Sum,left_index=True,right_index=True  )
Heatwave_Table = pd.merge(left = Heatwave_Table,right  =Max_Mean,left_index=True,right_index=True  )
Heatwave_Table = pd.merge(left = Heatwave_Table,right  =Min_Mean,left_index=True,right_index=True  )
Heatwave_Table = pd.merge(left = Heatwave_Table,right  =Mean_Average,left_index=True,right_index=True  )


#%%
#Max and Min Heatwave Average


#Accumulation Total
































    
#%% Developing the scatterplot. for Max Min correlation for overall temperautre to Heatwave

'''
These are the scatterplots/distrbiutions for heatwave days in orange compared to days that are not heatwave days blue in 
the extended SUMMER PERIOD NOV TO MARCH
'''
Heatwave_85_fixed,D,E,F = function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1800,2030], 
                                                                [1961,1990],['Max','Min'],85,7,Dates)






import numpy as np ,pandas as pd
from numpy import cov
from scipy.stats import pearsonr
#Our defined heatwaves
Heatwave_1967_1992 =Heatwave_85_fixed.set_index('id')
Heatwave_1967_1992 = Heatwave_1967_1992.loc[49:79]
Heatwave_Max_T = Heatwave_1967_1992['Max']
Heatwave_Min_T = Heatwave_1967_1992['Min']
Dates_for_heatwaves = Heatwave_1967_1992['date']

'''
The scatter plot of Max on Y axis compared to min on x axis
'''

#define data for Max and Min For the period of 1967 to 1992
plt.figure(1)
DMM = Daily_MaxMin.set_index('date')



DMM = pd.concat([  DMM[DMM.index.month==11], DMM[DMM.index.month==12], DMM[DMM.index.month==1], DMM[DMM.index.month==2], DMM[DMM.index.month==3],], axis = 0)

DMMMAX_67_92  = DMM['Max'].loc['1967':'1992']
DMMMIN_67_92 = DMM['Min'].loc['1967':'1992']

#find line of best fit
a_daily, b_daily = np.polyfit(DMMMIN_67_92, DMMMAX_67_92, 1)

#add points to plot
plt.scatter(DMMMIN_67_92, DMMMAX_67_92,color = 'green')
corr_daily, _ = pearsonr(DMMMIN_67_92, DMMMAX_67_92)
#add line of best fit to plot
plt.plot(DMMMIN_67_92, a_daily*DMMMIN_67_92+b_daily,color ='black',label = 'Max_T = {}*Min_T+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a_daily, 2),round(b_daily, 2),round(np.power(corr_daily,2), 3)))   


plt.legend()
plt.title('Maximum Vs Minimum Temperature for Non Heatwave Days')
plt.xlabel('Minimum Temperature')
plt.ylabel('Maximum Temperature')



plt.figure(2)
'''
This one is looking at heatwave days in 1967-1992 only.
'''


#find line of best fit
a_heat, b_heat = np.polyfit(Heatwave_Min_T, Heatwave_Max_T, 1)

#add points to plot
plt.scatter(Heatwave_Min_T, Heatwave_Max_T,color = 'green')
corr_heat, _ = pearsonr(Heatwave_Min_T, Heatwave_Max_T)

#add line of best fit to plot
plt.plot(Heatwave_Min_T, a_heat*Heatwave_Min_T+b_heat,color ='black',label = 'Max_T = {}*Min_T+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a_heat, 2),round(b_heat, 2),round(np.power(corr_heat,2), 3)))   
plt.legend()
plt.title('Maximum Vs Minimum Temperature for Heatwave Days')
plt.xlabel('Minimum Temperature')
plt.ylabel('Maximum Temperature')


plt.figure(3,figsize = (12,8))
plt.scatter(DMMMIN_67_92, DMMMAX_67_92,color = 'green',label = 'Max Min Points Daily')
plt.scatter(Heatwave_Min_T, Heatwave_Max_T,color = 'blue', label = 'Max Min Points Heatwave Days')
plt.plot(Heatwave_Min_T, a_heat*Heatwave_Min_T+b_heat,color ='aqua',label = 'Heatwave: Max_T = {}*Min_T+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a_heat, 2),round(b_heat, 2),round(np.power(corr_heat,2), 3)))
plt.plot(DMMMIN_67_92, a_daily*DMMMIN_67_92+b_daily,color ='orange',label = 'Daily: Max_T = {}*Min_T+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a_daily, 2),round(b_daily, 2),round(np.power(corr_daily,2), 3)))   
plt.xlim([-7,33])
plt.ylim([0,53])
plt.legend(fontsize = 10,loc = 0 )
plt.title('Maximum Vs Minimum Temperature for Heatwave and Non Heatwave Days')
plt.xlabel('Minimum Temperature')
plt.ylabel('Maximum Temperature')
'''Now we are going to plot a) histogram of max T
b) historgram of min T'''

    
#%%    
plt.figure(4)
plt.hist(DMMMIN_67_92,bins = 40,label = 'Daily',color = 'green')
plt.hist(Heatwave_Min_T,bins = 40, label = 'Heatwave Days',color = 'blue')
plt.title('Comparison of frequencies of minimum temperatures')
plt.xlabel('Temperature')
plt.ylabel('Number of Occurances')

plt.figure(5)
plt.hist(DMMMAX_67_92,bins = 40,label = 'Daily',color = 'green')
plt.hist(Heatwave_Max_T,bins = 40, label = 'Heatwave Days',color = 'blue')
plt.title('Comparison of frequencies of maximum temperatures')
plt.xlabel('Temperature')
plt.ylabel('Number of Occurances')

'''
At a closer look
'''
plt.figure(6)
plt.hist(DMMMIN_67_92,bins = 40,label = 'Daily',color = 'green')
plt.hist(Heatwave_Min_T,bins = 40, label = 'Heatwave Days',color = 'blue')
plt.title('Comparison of frequencies of minimum temperatures')
plt.xlabel('Temperature')
plt.ylabel('Number of Occurances')
plt.xlim([12,28])
plt.ylim([0,300])

plt.figure(7)
plt.hist(DMMMAX_67_92,bins = 40,label = 'Daily',color = 'green')
plt.hist(Heatwave_Max_T,bins = 40, label = 'Heatwave Days',color = 'blue')
plt.title('Comparison of frequencies of maximum temperatures')
plt.xlabel('Temperature')
plt.ylabel('Number of Occurances')
plt.xlim([30,50])
plt.ylim([0,250])

'''
Next one I want to do is find the percentage of each bin and plot the percetnage of known days to heatwave events
'''




#Try corrolation of pure heatwave days.



#%%1967 -1992 Regional Data Correlation During Heatwave Events, Extended Summer and Year Round
#So we need to load the data from above on the Daily_Max_Min, and Heatwave Max_Min

'''
Below is the data cleanup for the ACORN-SAT and Regional Office from 1967-1992
'''

#ACORN_SAT 
AC_SAT_Max = Daily_MaxMin['Max']
AC_SAT_Min = Daily_MaxMin['Min']


#BOM PERTH REGIONAL OFFICE
MaxT_Perth_Reg_Office = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\IDCJAC0010_009034_1800_Data.csv")
MinT_Perth_Reg_Office = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\IDCJAC0011_009034_1800_Data.csv")

#Clean Data
MaxT_Perth_Reg_Office['Datetime']= pd.to_datetime(MaxT_Perth_Reg_Office[['Year', 'Month', 'Day']])
MinT_Perth_Reg_Office['Datetime']= pd.to_datetime(MinT_Perth_Reg_Office[['Year', 'Month', 'Day']])


#Delete irrelevent columns
del MaxT_Perth_Reg_Office['Product code']
del MaxT_Perth_Reg_Office['Bureau of Meteorology station number']
del MaxT_Perth_Reg_Office['Year']
del MaxT_Perth_Reg_Office['Month']
del MaxT_Perth_Reg_Office['Day']
del MaxT_Perth_Reg_Office['Days of accumulation of maximum temperature']
del MaxT_Perth_Reg_Office['Quality']
del MinT_Perth_Reg_Office['Product code']
del MinT_Perth_Reg_Office['Bureau of Meteorology station number']
del MinT_Perth_Reg_Office['Year']
del MinT_Perth_Reg_Office['Month']
del MinT_Perth_Reg_Office['Day']
del MinT_Perth_Reg_Office['Days of accumulation of minimum temperature']
del MinT_Perth_Reg_Office['Quality']

#Change the column name to date
MaxT_Perth_Reg_Office= MaxT_Perth_Reg_Office.rename(columns={'Datetime':'date'})
MinT_Perth_Reg_Office= MinT_Perth_Reg_Office.rename(columns={'Datetime':'date'})

#Delete irrelevent columns
AC_SAT = Daily_MaxMin
del AC_SAT['Ave']
del AC_SAT['year']
del AC_SAT['month']
del AC_SAT['day']
AC_SAT= AC_SAT.set_index('date')

#Change the column n,aes
MaxT_Perth_Reg_Office= MaxT_Perth_Reg_Office.rename(columns={'Maximum temperature (Degree C)':'PRO Max'})
MinT_Perth_Reg_Office= MinT_Perth_Reg_Office.rename(columns={'Minimum temperature (Degree C)':'PRO Min'})

MinT_Perth_Reg_Office= MinT_Perth_Reg_Office.set_index('date')
MaxT_Perth_Reg_Office= MaxT_Perth_Reg_Office.set_index('date')

AC_SAT= AC_SAT.rename(columns={'Max':'AC-SAT Max'})
AC_SAT= AC_SAT.rename(columns={'Min':'AC-SAT Min'})

Perth_Regional_Office = pd.merge(left = MaxT_Perth_Reg_Office,right  =MinT_Perth_Reg_Office,left_index=True,right_index=True  )
#Put all together
Temperature_Comp_AC_SAT_PRO = pd.merge(left = AC_SAT,right  =Perth_Regional_Office,left_index=True,right_index=True  ).dropna()
Temperature_Comp_AC_SAT_PRO = Temperature_Comp_AC_SAT_PRO.loc["1967-01-01":"1992-3-31"]

#%% The comparisons
#The first one is looking at the entire record in focus from 1967-1992

plt.figure(8)
ACORN_SAT_Mx =Temperature_Comp_AC_SAT_PRO['AC-SAT Max']
REG_OFFICE_Mx =Temperature_Comp_AC_SAT_PRO['PRO Max']

#find line of best fit
a1, b1 = np.polyfit(REG_OFFICE_Mx, ACORN_SAT_Mx, 1)
#add points to plot
plt.scatter(REG_OFFICE_Mx, ACORN_SAT_Mx,color = 'green')
corr, _ = pearsonr(REG_OFFICE_Mx, ACORN_SAT_Mx)
#add line of best fit to plot
plt.plot(REG_OFFICE_Mx, a1*REG_OFFICE_Mx+b1,color ='black',label = 'ACOMax = {}*PROMax+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a1, 2),round(b1, 2),round(np.power(corr,2), 3)))   
plt.legend()
plt.title('ACORN SAT AGAINST PERTH REGIONAL OFFICE 1967-1992 RECORD')
plt.xlabel('PERTH REGIONAL OFFICE MAX TEMP')
plt.ylabel('ACORN SAT MAX TEMP')







plt.figure(9)
ACORN_SAT_Mn =Temperature_Comp_AC_SAT_PRO['AC-SAT Min']
REG_OFFICE_Mn =Temperature_Comp_AC_SAT_PRO['PRO Min']

#find line of best fit
a2, b2 = np.polyfit(REG_OFFICE_Mn, ACORN_SAT_Mn, 1)
#add points to plot
plt.scatter(REG_OFFICE_Mn, ACORN_SAT_Mn,color = 'green')
corr, _ = pearsonr(REG_OFFICE_Mn, ACORN_SAT_Mn)
#add line of best fit to plot
plt.plot(REG_OFFICE_Mn, a2*REG_OFFICE_Mn+b2,color ='black',label = 'ACOMin = {}*PROMin+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a2, 2),round(b2, 2),round(np.power(corr,2), 3)))   
plt.legend()
plt.title('ACORN SAT AGAINST PERTH REGIONAL OFFICE ENTIRE RECORD')
plt.xlabel('PERTH REGIONAL OFFICE MIN TEMP')
plt.ylabel('ACORN SAT MIN TEMP')




plt.figure(10)
Ext_Sum_Temps_ACSAT_PRO = pd.concat([  Temperature_Comp_AC_SAT_PRO[Temperature_Comp_AC_SAT_PRO.index.month==11], Temperature_Comp_AC_SAT_PRO[Temperature_Comp_AC_SAT_PRO.index.month==12], Temperature_Comp_AC_SAT_PRO[Temperature_Comp_AC_SAT_PRO.index.month==1], Temperature_Comp_AC_SAT_PRO[Temperature_Comp_AC_SAT_PRO.index.month==2], Temperature_Comp_AC_SAT_PRO[Temperature_Comp_AC_SAT_PRO.index.month==3],], axis = 0)


ACORN_SAT_Mx =Ext_Sum_Temps_ACSAT_PRO['AC-SAT Max']
REG_OFFICE_Mx =Ext_Sum_Temps_ACSAT_PRO['PRO Max']

#find line of best fit
a3, b3 = np.polyfit(REG_OFFICE_Mx, ACORN_SAT_Mx, 1)
#add points to plot
plt.scatter(REG_OFFICE_Mx, ACORN_SAT_Mx,color = 'green')
corr, _ = pearsonr(REG_OFFICE_Mx, ACORN_SAT_Mx)
#add line of best fit to plot
plt.plot(REG_OFFICE_Mx, a3*REG_OFFICE_Mx+b3,color ='black',label = 'ACOMax = {}*PROMax+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a3, 2),round(b3, 2),round(np.power(corr,2), 3)))   
plt.legend()
plt.title('ACORN SAT AGAINST PERTH REGIONAL OFFICE EXTENDED SUMMER RECORD')
plt.xlabel('PERTH REGIONAL OFFICE MAX TEMP')
plt.ylabel('ACORN SAT MAX TEMP')

plt.figure(11)
ACORN_SAT_Mn =Ext_Sum_Temps_ACSAT_PRO['AC-SAT Min']
REG_OFFICE_Mn =Ext_Sum_Temps_ACSAT_PRO['PRO Min']

#find line of best fit
a4, b4 = np.polyfit(REG_OFFICE_Mn, ACORN_SAT_Mn, 1)
#add points to plot
plt.scatter(REG_OFFICE_Mn, ACORN_SAT_Mn,color = 'green')
corr, _ = pearsonr(REG_OFFICE_Mn, ACORN_SAT_Mn)
#add line of best fit to plot
plt.plot(REG_OFFICE_Mn, a4*REG_OFFICE_Mn+b4,color ='black',label = 'ACOMin = {}*PROMin+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a4, 2),round(b4, 2),round(np.power(corr,2), 3)))   
plt.legend()
plt.title('ACORN SAT AGAINST PERTH REGIONAL OFFICE EXTENDED SUMMER RECORD')
plt.xlabel('PERTH REGIONAL OFFICE MIN TEMP')
plt.ylabel('ACORN SAT MIN TEMP')







#The third is heatwave events only
Heatwaves = Heatwave_85_fixed.set_index('date')

del Heatwaves['id']
del Heatwaves['Excess Heat Factor Max T']
del Heatwaves['Excess Heat Factor Min T']
del Heatwaves['Ave']
del Heatwaves['Max']
del Heatwaves['Min']
del Heatwaves['85 percentile daily Max']
del Heatwaves['85 percentile daily Min']

Temperature_Heatwave_AC_SAT_PRO = pd.merge(left = Temperature_Comp_AC_SAT_PRO,right  =Heatwaves,left_index=True,right_index=True  )




plt.figure(12)


ACORN_SAT_Mx =Temperature_Heatwave_AC_SAT_PRO['AC-SAT Max']
REG_OFFICE_Mx =Temperature_Heatwave_AC_SAT_PRO['PRO Max']

#find line of best fit
a5, b5 = np.polyfit(REG_OFFICE_Mx, ACORN_SAT_Mx, 1)
#add points to plot
plt.scatter(REG_OFFICE_Mx, ACORN_SAT_Mx,color = 'green')
corr, _ = pearsonr(REG_OFFICE_Mx, ACORN_SAT_Mx)
#add line of best fit to plot
plt.plot(REG_OFFICE_Mx, a5*REG_OFFICE_Mx+b5,color ='black',label = 'ACOMax = {}*PROMax+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a5, 2),round(b5, 2),round(np.power(corr,2), 3)))   
plt.legend()
plt.title('ACORN SAT AGAINST PERTH REGIONAL OFFICE HEATWAVE ONLY RECORD')
plt.xlabel('PERTH REGIONAL OFFICE MAX TEMP')
plt.ylabel('ACORN SAT MAX TEMP')


plt.figure(13)
ACORN_SAT_Mn =Temperature_Heatwave_AC_SAT_PRO['AC-SAT Min']
REG_OFFICE_Mn =Temperature_Heatwave_AC_SAT_PRO['PRO Min']

#find line of best fit
a6, b6 = np.polyfit(REG_OFFICE_Mn, ACORN_SAT_Mn, 1)
#add points to plot
plt.scatter(REG_OFFICE_Mn, ACORN_SAT_Mn,color = 'green')
corr, _ = pearsonr(REG_OFFICE_Mn, ACORN_SAT_Mn)
#add line of best fit to plot
plt.plot(REG_OFFICE_Mn, a6*REG_OFFICE_Mn+b6,color ='black',label = 'ACOMin = {}*PROMin+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a6, 2),round(b6, 2),round(np.power(corr,2), 3)))   
plt.legend()
plt.title('ACORN SAT AGAINST PERTH REGIONAL OFFICE EXTENDED SUMMER RECORD')
plt.xlabel('PERTH REGIONAL OFFICE MIN TEMP')
plt.ylabel('ACORN SAT MIN TEMP')

#%% All together

fig,ax = plt.subplots(nrows = 3, ncols = 2, sharex = True, sharey = True,figsize = (20,20))


ACORN_SAT_Mx =Temperature_Comp_AC_SAT_PRO['AC-SAT Max']
REG_OFFICE_Mx =Temperature_Comp_AC_SAT_PRO['PRO Max']

#find line of best fit
a1, b1 = np.polyfit(REG_OFFICE_Mx, ACORN_SAT_Mx, 1)
#add points to plot
ax[0,0].scatter(REG_OFFICE_Mx, ACORN_SAT_Mx,color = 'green')
corr, _ = pearsonr(REG_OFFICE_Mx, ACORN_SAT_Mx)
#add line of best fit to plot
ax[0,0].plot(REG_OFFICE_Mx, a1*REG_OFFICE_Mx+b1,color ='black',label = 'ACOMax = {}*PROMax+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a1, 2),round(b1, 2),round(np.power(corr,2), 3)))   
ax[0,0].legend()
ax[0,0].set_title('ACORN SAT AGAINST PERTH REGIONAL OFFICE 1967-1992 RECORD MAX')
ax[0,0].set_ylabel('ACORN SAT MAX TEMP')







ACORN_SAT_Mn =Temperature_Comp_AC_SAT_PRO['AC-SAT Min']
REG_OFFICE_Mn =Temperature_Comp_AC_SAT_PRO['PRO Min']

#find line of best fit
a2, b2 = np.polyfit(REG_OFFICE_Mn, ACORN_SAT_Mn, 1)
#add points to plot
ax[0,1].scatter(REG_OFFICE_Mn, ACORN_SAT_Mn,color = 'green')
corr, _ = pearsonr(REG_OFFICE_Mn, ACORN_SAT_Mn)
#add line of best fit to plot
ax[0,1].plot(REG_OFFICE_Mn, a2*REG_OFFICE_Mn+b2,color ='black',label = 'ACOMin = {}*PROMin+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a2, 2),round(b2, 2),round(np.power(corr,2), 3)))   
ax[0,1].legend()
ax[0,1].set_title('ACORN SAT AGAINST PERTH REGIONAL OFFICE ENTIRE RECORD MIN')
ax[0,1].set_ylabel('ACORN SAT MIN TEMP')




Ext_Sum_Temps_ACSAT_PRO = pd.concat([  Temperature_Comp_AC_SAT_PRO[Temperature_Comp_AC_SAT_PRO.index.month==11], Temperature_Comp_AC_SAT_PRO[Temperature_Comp_AC_SAT_PRO.index.month==12], Temperature_Comp_AC_SAT_PRO[Temperature_Comp_AC_SAT_PRO.index.month==1], Temperature_Comp_AC_SAT_PRO[Temperature_Comp_AC_SAT_PRO.index.month==2], Temperature_Comp_AC_SAT_PRO[Temperature_Comp_AC_SAT_PRO.index.month==3],], axis = 0)


ACORN_SAT_Mx =Ext_Sum_Temps_ACSAT_PRO['AC-SAT Max']
REG_OFFICE_Mx =Ext_Sum_Temps_ACSAT_PRO['PRO Max']

#find line of best fit
a3, b3 = np.polyfit(REG_OFFICE_Mx, ACORN_SAT_Mx, 1)
#add points to plot
ax[1,0].scatter(REG_OFFICE_Mx, ACORN_SAT_Mx,color = 'green')
corr, _ = pearsonr(REG_OFFICE_Mx, ACORN_SAT_Mx)
#add line of best fit to plot
ax[1,0].plot(REG_OFFICE_Mx, a3*REG_OFFICE_Mx+b3,color ='black',label = 'ACOMax = {}*PROMax+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a3, 2),round(b3, 2),round(np.power(corr,2), 3)))   
ax[1,0].legend()
ax[1,0].set_title('ACORN SAT AGAINST PERTH REGIONAL OFFICE EXTENDED SUMMER RECORD MAX')
ax[1,0].set_ylabel('ACORN SAT MAX TEMP')


ACORN_SAT_Mn =Ext_Sum_Temps_ACSAT_PRO['AC-SAT Min']
REG_OFFICE_Mn =Ext_Sum_Temps_ACSAT_PRO['PRO Min']

#find line of best fit
a4, b4 = np.polyfit(REG_OFFICE_Mn, ACORN_SAT_Mn, 1)
#add points to plot
ax[1,1].scatter(REG_OFFICE_Mn, ACORN_SAT_Mn,color = 'green')
corr, _ = pearsonr(REG_OFFICE_Mn, ACORN_SAT_Mn)
#add line of best fit to plot
ax[1,1].plot(REG_OFFICE_Mn, a4*REG_OFFICE_Mn+b4,color ='black',label = 'ACOMin = {}*PROMin+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a4, 2),round(b4, 2),round(np.power(corr,2), 3)))   
ax[1,1].legend()
ax[1,1].set_title('ACORN SAT AGAINST PERTH REGIONAL OFFICE EXTENDED SUMMER RECORD MIN')
ax[1,1].set_ylabel('ACORN SAT MIN TEMP')







#The third is heatwave events only


ACORN_SAT_Mx =Temperature_Heatwave_AC_SAT_PRO['AC-SAT Max']
REG_OFFICE_Mx =Temperature_Heatwave_AC_SAT_PRO['PRO Max']

#find line of best fit
a5, b5 = np.polyfit(REG_OFFICE_Mx, ACORN_SAT_Mx, 1)
#add points to plot
ax[2,0].scatter(REG_OFFICE_Mx, ACORN_SAT_Mx,color = 'green')
corr, _ = pearsonr(REG_OFFICE_Mx, ACORN_SAT_Mx)
#add line of best fit to plot
ax[2,0].plot(REG_OFFICE_Mx, a5*REG_OFFICE_Mx+b5,color ='black',label = 'ACOMax = {}*PROMax+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a5, 2),round(b5, 2),round(np.power(corr,2), 3)))   
ax[2,0].legend()
ax[2,0].set_title('ACORN SAT AGAINST PERTH REGIONAL OFFICE HEATWAVE ONLY RECORD MAX')
ax[2,0].set_xlabel('PERTH REGIONAL OFFICE MAX TEMP')
ax[2,0].set_ylabel('ACORN SAT MAX TEMP')



ACORN_SAT_Mn =Temperature_Heatwave_AC_SAT_PRO['AC-SAT Min']
REG_OFFICE_Mn =Temperature_Heatwave_AC_SAT_PRO['PRO Min']

#find line of best fit
a6, b6 = np.polyfit(REG_OFFICE_Mn, ACORN_SAT_Mn, 1)
#add points to plot
ax[2,1].scatter(REG_OFFICE_Mn, ACORN_SAT_Mn,color = 'green')
corr, _ = pearsonr(REG_OFFICE_Mn, ACORN_SAT_Mn)
#add line of best fit to plot
ax[2,1].plot(REG_OFFICE_Mn, a6*REG_OFFICE_Mn+b6,color ='black',label = 'ACOMin = {}*PROMin+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a6, 2),round(b6, 2),round(np.power(corr,2), 3)))   
ax[2,1].legend()
ax[2,1].set_title('ACORN SAT AGAINST PERTH REGIONAL OFFICE EXTENDED SUMMER RECORD MIN')
ax[2,1].set_xlabel('PERTH REGIONAL OFFICE MIN TEMP')
ax[2,1].set_ylabel('ACORN SAT MIN TEMP')

#Now we can decide whether it is useful using this as a 1:1 type of graph.









Heatwave_Table.to_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Analysis\Heatwave Events\Heatwave_Table.csv")











