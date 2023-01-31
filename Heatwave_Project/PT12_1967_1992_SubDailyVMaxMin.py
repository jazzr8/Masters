import sys


sys.path.append(r"C:\Users\jarra\Desktop\Masters\Heatwave_Project")
import pandas as pd, PT13_Functions_For_Masters_New_Test as function_M, matplotlib.pyplot as plt, PT5_Functions_For_Masters as function_M1
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
Heatwave_85  =  function_M.Heatwave_Function_Perth_Specific(Daily_MaxMin,'date',[1800,2030], [1961,1990],['Max','Min'],85,7,Dates)


'''
I do not care about the other columns in this, so I can about the heatwave dates only.
'''






#%% Load the max and min PRO
'''
Since we already have our data lets load the PRO and its subdaily data
'''



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

MaxT_Perth_Reg_Office= MaxT_Perth_Reg_Office.rename(columns={'Maximum temperature (Degree C)':'PRO Max'})
MinT_Perth_Reg_Office= MinT_Perth_Reg_Office.rename(columns={'Minimum temperature (Degree C)':'PRO Min'})
MaxT_Perth_Reg_Office= MaxT_Perth_Reg_Office.set_index('date')
MinT_Perth_Reg_Office= MinT_Perth_Reg_Office.set_index('date')
Perth_Regional_Office = pd.merge(left = MaxT_Perth_Reg_Office,right  =MinT_Perth_Reg_Office,left_index=True,right_index=True  )

#Get the extended summer only
PRO_Extremes  = Perth_Regional_Office.loc['1967':'1992']
PRO_Extremes = pd.concat([  PRO_Extremes[PRO_Extremes.index.month==11], PRO_Extremes[PRO_Extremes.index.month==12], PRO_Extremes[PRO_Extremes.index.month==1], PRO_Extremes[PRO_Extremes.index.month==2], PRO_Extremes[PRO_Extremes.index.month==3],], axis = 0)


#%% Sub-Daily PRO
#Load PRO data in

PRO_SD = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\perthregionaloffice_subdaily_1942-1992.csv")

PRO_SD['date'] = pd.to_datetime(PRO_SD['date'],dayfirst = True)



PRO_SD_T = PRO_SD.set_index('date')
PRO_SD_T =PRO_SD_T['temp']/10 


# Lets get this into extended summer
PRO_SD_ES  = PRO_SD_T.loc['1967':'1992']
PRO_SD_ES = pd.concat([  PRO_SD_ES[PRO_SD_ES.index.month==11], PRO_SD_ES[PRO_SD_ES.index.month==12], PRO_SD_ES[PRO_SD_ES.index.month==1], PRO_SD_ES[PRO_SD_ES.index.month==2], PRO_SD_ES[PRO_SD_ES.index.month==3],], axis = 0)
PRO_SD_0 = pd.concat([PRO_SD_ES[PRO_SD_ES.index.hour==0]],axis =0)
PRO_SD_3= pd.concat([PRO_SD_ES[PRO_SD_ES.index.hour==3]],axis =0)
PRO_SD_6= pd.concat([PRO_SD_ES[PRO_SD_ES.index.hour==6]],axis =0)
PRO_SD_9= pd.concat([PRO_SD_ES[PRO_SD_ES.index.hour==9]],axis =0)
PRO_SD_12= pd.concat([PRO_SD_ES[PRO_SD_ES.index.hour==12]],axis =0)
PRO_SD_15= pd.concat([PRO_SD_ES[PRO_SD_ES.index.hour==15]],axis =0)
PRO_SD_18= pd.concat([PRO_SD_ES[PRO_SD_ES.index.hour==18]],axis =0)
PRO_SD_21= pd.concat([PRO_SD_ES[PRO_SD_ES.index.hour==21]],axis =0)



#Reomve hours out of it for concatiation

PRO_SD_0 = PRO_SD_0.reset_index()
PRO_SD_0['date'] = pd.to_datetime(PRO_SD_0['date']).dt.date
PRO_SD_0 = PRO_SD_0.set_index('date')

PRO_SD_3 = PRO_SD_3.reset_index()
PRO_SD_3['date'] = pd.to_datetime(PRO_SD_3['date']).dt.date
PRO_SD_3 = PRO_SD_3.set_index('date')


PRO_SD_6 = PRO_SD_6.reset_index()
PRO_SD_6['date'] = pd.to_datetime(PRO_SD_6['date']).dt.date
PRO_SD_6 = PRO_SD_6.set_index('date')

PRO_SD_9 = PRO_SD_9.reset_index()
PRO_SD_9['date'] = pd.to_datetime(PRO_SD_9['date']).dt.date
PRO_SD_9 = PRO_SD_9.set_index('date')

PRO_SD_12 = PRO_SD_12.reset_index()
PRO_SD_12['date'] = pd.to_datetime(PRO_SD_12['date']).dt.date
PRO_SD_12 = PRO_SD_12.set_index('date')

PRO_SD_15 = PRO_SD_15.reset_index()
PRO_SD_15['date'] = pd.to_datetime(PRO_SD_15['date']).dt.date
PRO_SD_15 = PRO_SD_15.set_index('date')

PRO_SD_18 = PRO_SD_18.reset_index()
PRO_SD_18['date'] = pd.to_datetime(PRO_SD_18['date']).dt.date
PRO_SD_18 = PRO_SD_18.set_index('date')

PRO_SD_21 = PRO_SD_21.reset_index()
PRO_SD_21['date'] = pd.to_datetime(PRO_SD_21['date']).dt.date
PRO_SD_21 = PRO_SD_21.set_index('date')










#%%

Plotters = [PRO_Extremes['PRO Max'],PRO_Extremes['PRO Min'],PRO_SD_0,PRO_SD_3,PRO_SD_6,PRO_SD_9,PRO_SD_12,PRO_SD_15,PRO_SD_18,PRO_SD_21]
for Plot in Plotters:
    plt.figure()
    Plot.plot()
    plt.ylim([5,50])

#%% Concate all this together




PRO_SD_0 = PRO_SD_0.rename(columns={'temp':'12am Temperature'})
PRO_SD_3 = PRO_SD_3.rename(columns={'temp':'3am Temperature'})
PRO_SD_6 = PRO_SD_6.rename(columns={'temp':'6am Temperature'})
PRO_SD_9 = PRO_SD_9.rename(columns={'temp':'9am Temperature'})
PRO_SD_12 = PRO_SD_12.rename(columns={'temp':'12pm Temperature'})
PRO_SD_15 = PRO_SD_15.rename(columns={'temp':'3pm Temperature'})
PRO_SD_18= PRO_SD_18.rename(columns={'temp':'6pm Temperature'})
PRO_SD_21 = PRO_SD_21.rename(columns={'temp':'9pm Temperature'})




PRO_SD_TIMES = [PRO_SD_0,PRO_SD_3,PRO_SD_6,PRO_SD_9,PRO_SD_12,PRO_SD_15,PRO_SD_18,PRO_SD_21]

#%%
#Merge the sub-daily with max and min
PRO_SD_0 = pd.merge(left = PRO_Extremes,right  =PRO_SD_0 ,left_index=True,right_index=True  ).dropna()
PRO_SD_3 = pd.merge(left = PRO_Extremes,right  =PRO_SD_3 ,left_index=True,right_index=True  ).dropna()
PRO_SD_6 = pd.merge(left = PRO_Extremes,right  =PRO_SD_6 ,left_index=True,right_index=True  ).dropna()
PRO_SD_9 = pd.merge(left = PRO_Extremes,right  =PRO_SD_9 ,left_index=True,right_index=True  ).dropna()
PRO_SD_12 = pd.merge(left = PRO_Extremes,right  =PRO_SD_12 ,left_index=True,right_index=True  ).dropna()
PRO_SD_15= pd.merge(left = PRO_Extremes,right  =PRO_SD_15 ,left_index=True,right_index=True  ).dropna()
PRO_SD_18 = pd.merge(left = PRO_Extremes,right  =PRO_SD_18 ,left_index=True,right_index=True  ).dropna()
PRO_SD_21 = pd.merge(left = PRO_Extremes,right  =PRO_SD_21 ,left_index=True,right_index=True  ).dropna()    
#%%Plots

PROSD = [PRO_SD_0,PRO_SD_3,PRO_SD_6,PRO_SD_9,PRO_SD_12,PRO_SD_15,PRO_SD_18,PRO_SD_21]
Titles_X =  ['12am Temperature','3am Temperature','6am Temperature','9am Temperature','12pm Temperature','3pm Temperature','6pm Temperature','9pm Temperature']


fig,ax = plt.subplots(nrows = 8, ncols = 2, sharex = True, sharey = True,figsize = (40,40))

for i in np.array([0,1,2,3,4,5,6,7]):
    #Plot the scatter
    #Max v Sub
    #find line of best fit
    a, b = np.polyfit(PROSD[i][Titles_X[i]],PROSD[i]['PRO Max'], 1)
    #add points to plot
    corr, _ = pearsonr(PROSD[i][Titles_X[i]],PROSD[i]['PRO Max'])
    ax[i,0].scatter(PROSD[i][Titles_X[i]],PROSD[i]['PRO Max'],color = 'orange')
    ax[i,0].set_ylabel('PRO Max')
    ax[i,0].set_title('{} v Max'.format(Titles_X[i]))
    ax[i,0].set_xlabel('{}'.format(Titles_X[i]))
    ax[i,0].plot(PROSD[i][Titles_X[i]], a*PROSD[i][Titles_X[i]]+b,color ='black',label = 'PROMax = {}*({})+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a, 2),Titles_X[i],round(b, 2),round(np.power(corr,2), 3)))   
    ax[i,0].legend()
    
    
    #Max v Sub
    a1, b1 = np.polyfit(PROSD[i][Titles_X[i]],PROSD[i]['PRO Min'], 1)
    #add points to plot
    corr, _ = pearsonr(PROSD[i][Titles_X[i]],PROSD[i]['PRO Min'])
    ax[i,1].scatter(PROSD[i][Titles_X[i]],PROSD[i]['PRO Min'])
    ax[i,1].set_ylabel('PRO Min')
    ax[i,1].set_title('{} v Min'.format(Titles_X[i]))
    ax[i,1].set_xlabel('{}'.format(Titles_X[i]))
    ax[i,1].plot(PROSD[i][Titles_X[i]], a1*PROSD[i][Titles_X[i]]+b1,color ='black',label = 'PROMin = {}*({})+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a1, 2),Titles_X[i],round(b1, 2),round(np.power(corr,2), 3)))   
    ax[i,1].legend()


#%% Now means, 85th and 90th of the subo-daily.

Titles_shortened =  ['12am','3am','6am','9am','12pm','3pm','6pm','9pm']
means = []
p_85 = []
p_90 = []
for i in range(0,len(PROSD)):
    #Calc the mean
    mean_ind = PROSD[i][Titles_X[i]].mean()
    
    #Calc the percenitle
    p_85_ind = PROSD[i][Titles_X[i]].quantile(q=0.85)
    p_90_ind = PROSD[i][Titles_X[i]].quantile(q=0.90) 
    
    #Append
    means.append(mean_ind)
    p_85.append(p_85_ind)
    p_90.append(p_90_ind)

#Combine lists
means = pd.Series(means,name = 'mean sub-daily')
p_85 = pd.Series(p_85,name = '85 percentile sub-daily')
p_90 = pd.Series(p_90,name = '90 percentile sub-daily')
Titles_shortened = pd.Series(Titles_shortened,name = 'Subdaily Time')

PRO_subdaily = pd.concat([Titles_shortened,means,p_85,p_90],axis=1)

plt.figure(1,figsize = (15,10))
#Plot these
plt.plot(PRO_subdaily['Subdaily Time'], PRO_subdaily['mean sub-daily'],label = 'mean',color = 'black')
plt.plot(PRO_subdaily['Subdaily Time'], PRO_subdaily['85 percentile sub-daily'], label = '85th',color = 'gray')
plt.plot(PRO_subdaily['Subdaily Time'], PRO_subdaily['90 percentile sub-daily'], label = '90th',color = 'silver')
plt.xlabel('Time')
plt.ylabel('Temperature (degC)')
plt.title('Temperature Cycle During Day 1967-1992')
plt.grid()

#Now to add max and min temperatures on this
Max_mean =  pd.Series(PRO_Extremes['PRO Max'].mean(),name = 'Max Mean')
Min_mean =  pd.Series(PRO_Extremes['PRO Min'].mean(),name = 'Min Mean')

Max_85 =  pd.Series(PRO_Extremes['PRO Max'].quantile(q=0.85),name = 'Max 85')
Min_85  = pd.Series(PRO_Extremes['PRO Min'].quantile(q=0.85),name = 'Min 85')

Max_90 = pd.Series(PRO_Extremes['PRO Max'].quantile(q=0.90),name = 'Max 90')
Min_90 = pd.Series(PRO_Extremes['PRO Min'].quantile(q=0.90),name = 'Min 90')


Extremes = pd.concat([Max_mean,Min_mean,Max_85,Min_85,Max_90,Min_90],axis =1)



plt.axhspan(Extremes['Max Mean'][0],Extremes['Max Mean'][0], color = 'coral',label = 'Min Mean')
plt.axhspan(Extremes['Min Mean'][0],Extremes['Min Mean'][0], color = 'magenta',label = 'Min Mean')
plt.axhspan(Extremes['Max 85'][0],Extremes['Max 85'][0], color = 'red',label = 'Max 85th')
plt.axhspan(Extremes['Min 85'][0],Extremes['Min 85'][0], color = 'blue',label = 'Min 85th')
plt.axhspan(Extremes['Max 90'][0],Extremes['Max 90'][0], color = 'maroon',label = 'Max 90th')
plt.axhspan(Extremes['Min 90'][0],Extremes['Min 90'][0], color = 'midnightblue',label = 'Min 90th')

plt.legend()


#%% NOVEMBER

def months_ind_for_plotter(month_number,PRO,month_name):
    PRO = pd.concat([PRO[PRO.index.month==month_number],], axis = 0)
    PRO_SD_0 = pd.concat([PRO[PRO.index.hour==0]],axis =0)
    PRO_SD_3= pd.concat([PRO[PRO.index.hour==3]],axis =0)
    PRO_SD_6= pd.concat([PRO[PRO.index.hour==6]],axis =0)
    PRO_SD_9= pd.concat([PRO[PRO.index.hour==9]],axis =0)
    PRO_SD_12= pd.concat([PRO[PRO.index.hour==12]],axis =0)
    PRO_SD_15= pd.concat([PRO[PRO.index.hour==15]],axis =0)
    PRO_SD_18= pd.concat([PRO[PRO.index.hour==18]],axis =0)
    PRO_SD_21= pd.concat([PRO[PRO.index.hour==21]],axis =0)

    

    #Reomve hours out of it for concatiation

    PRO_SD_0 = PRO_SD_0.reset_index()
    PRO_SD_0['date'] = pd.to_datetime(PRO_SD_0['date']).dt.date
    PRO_SD_0 = PRO_SD_0.set_index('date')

    PRO_SD_3 = PRO_SD_3.reset_index()
    PRO_SD_3['date'] = pd.to_datetime(PRO_SD_3['date']).dt.date
    PRO_SD_3 = PRO_SD_3.set_index('date')

    
    PRO_SD_6 = PRO_SD_6.reset_index()
    PRO_SD_6['date'] = pd.to_datetime(PRO_SD_6['date']).dt.date
    PRO_SD_6 = PRO_SD_6.set_index('date')

    PRO_SD_9 = PRO_SD_9.reset_index()
    PRO_SD_9['date'] = pd.to_datetime(PRO_SD_9['date']).dt.date
    PRO_SD_9 = PRO_SD_9.set_index('date')

    PRO_SD_12 = PRO_SD_12.reset_index()
    PRO_SD_12['date'] = pd.to_datetime(PRO_SD_12['date']).dt.date
    PRO_SD_12 = PRO_SD_12.set_index('date')

    PRO_SD_15 = PRO_SD_15.reset_index()
    PRO_SD_15['date'] = pd.to_datetime(PRO_SD_15['date']).dt.date
    PRO_SD_15 = PRO_SD_15.set_index('date')

    PRO_SD_18 = PRO_SD_18.reset_index()
    PRO_SD_18['date'] = pd.to_datetime(PRO_SD_18['date']).dt.date
    PRO_SD_18 = PRO_SD_18.set_index('date')

    PRO_SD_21 = PRO_SD_21.reset_index()
    PRO_SD_21['date'] = pd.to_datetime(PRO_SD_21['date']).dt.date
    PRO_SD_21 = PRO_SD_21.set_index('date')
    


    PRO_SD_0 = PRO_SD_0.rename(columns={'temp':'12am Temperature'})
    PRO_SD_3 = PRO_SD_3.rename(columns={'temp':'3am Temperature'})
    PRO_SD_6 = PRO_SD_6.rename(columns={'temp':'6am Temperature'})
    PRO_SD_9 = PRO_SD_9.rename(columns={'temp':'9am Temperature'})
    PRO_SD_12 = PRO_SD_12.rename(columns={'temp':'12pm Temperature'})
    PRO_SD_15 = PRO_SD_15.rename(columns={'temp':'3pm Temperature'})
    PRO_SD_18= PRO_SD_18.rename(columns={'temp':'6pm Temperature'})
    PRO_SD_21 = PRO_SD_21.rename(columns={'temp':'9pm Temperature'})




    #Merge the sub-daily with max and min
    PRO_SD_0 = pd.merge(left = PRO_Extremes,right  =PRO_SD_0 ,left_index=True,right_index=True  ).dropna()
    PRO_SD_3 = pd.merge(left = PRO_Extremes,right  =PRO_SD_3 ,left_index=True,right_index=True  ).dropna()
    PRO_SD_6 = pd.merge(left = PRO_Extremes,right  =PRO_SD_6 ,left_index=True,right_index=True  ).dropna()
    PRO_SD_9 = pd.merge(left = PRO_Extremes,right  =PRO_SD_9 ,left_index=True,right_index=True  ).dropna()
    PRO_SD_12 = pd.merge(left = PRO_Extremes,right  =PRO_SD_12 ,left_index=True,right_index=True  ).dropna()
    PRO_SD_15= pd.merge(left = PRO_Extremes,right  =PRO_SD_15 ,left_index=True,right_index=True  ).dropna()
    PRO_SD_18 = pd.merge(left = PRO_Extremes,right  =PRO_SD_18 ,left_index=True,right_index=True  ).dropna()
    PRO_SD_21 = pd.merge(left = PRO_Extremes,right  =PRO_SD_21 ,left_index=True,right_index=True  ).dropna()    

    PROSD = [PRO_SD_0,PRO_SD_3,PRO_SD_6,PRO_SD_9,PRO_SD_12,PRO_SD_15,PRO_SD_18,PRO_SD_21]
    Titles_X =  ['12am Temperature','3am Temperature','6am Temperature','9am Temperature','12pm Temperature','3pm Temperature','6pm Temperature','9pm Temperature']


    Titles_shortened =  ['12am','3am','6am','9am','12pm','3pm','6pm','9pm']
    means = []
    p_85 = []
    p_90 = []
    for i in range(0,len(PROSD)):
        #Calc the mean
        mean_ind = PROSD[i][Titles_X[i]].mean()
        
        #Calc the percenitle
        p_85_ind = PROSD[i][Titles_X[i]].quantile(q=0.85)
        p_90_ind = PROSD[i][Titles_X[i]].quantile(q=0.90) 
        
        #Append
        means.append(mean_ind)
        p_85.append(p_85_ind)
        p_90.append(p_90_ind)

    #Combine lists
    means = pd.Series(means,name = 'mean sub-daily')
    p_85 = pd.Series(p_85,name = '85 percentile sub-daily')
    p_90 = pd.Series(p_90,name = '90 percentile sub-daily')
    Titles_shortened = pd.Series(Titles_shortened,name = 'Subdaily Time')

    PRO_subdaily = pd.concat([Titles_shortened,means,p_85,p_90],axis=1)

    plt.figure(month_number,figsize = (15,10))
    #Plot these
    plt.plot(PRO_subdaily['Subdaily Time'], PRO_subdaily['mean sub-daily'],label = 'mean',color = 'black')
    plt.plot(PRO_subdaily['Subdaily Time'], PRO_subdaily['85 percentile sub-daily'], label = '85th',color = 'gray')
    plt.plot(PRO_subdaily['Subdaily Time'], PRO_subdaily['90 percentile sub-daily'], label = '90th',color = 'silver')
    plt.xlabel('Time')
    plt.ylabel('Temperature (degC)')
    plt.title('Temperature Cycle During Day 1967-1992 {}'.format(month_name))
    plt.grid()
    PRO_Extremes_Month = pd.concat([PRO_Extremes[PRO_Extremes.index.month==month_number],], axis = 0)
    #Now to add max and min temperatures on this
    Max_mean =  pd.Series(PRO_Extremes_Month['PRO Max'].mean(),name = 'Max Mean')
    Min_mean =  pd.Series(PRO_Extremes_Month['PRO Min'].mean(),name = 'Min Mean')

    Max_85 =  pd.Series(PRO_Extremes_Month['PRO Max'].quantile(q=0.85),name = 'Max 85')
    Min_85  = pd.Series(PRO_Extremes_Month['PRO Min'].quantile(q=0.85),name = 'Min 85')

    Max_90 = pd.Series(PRO_Extremes_Month['PRO Max'].quantile(q=0.90),name = 'Max 90')
    Min_90 = pd.Series(PRO_Extremes_Month['PRO Min'].quantile(q=0.90),name = 'Min 90')


    Extremes = pd.concat([Max_mean,Min_mean,Max_85,Min_85,Max_90,Min_90],axis =1)



    plt.axhspan(Extremes['Max Mean'][0],Extremes['Max Mean'][0], color = 'coral',label = 'Min Mean')
    plt.axhspan(Extremes['Min Mean'][0],Extremes['Min Mean'][0], color = 'magenta',label = 'Min Mean')
    plt.axhspan(Extremes['Max 85'][0],Extremes['Max 85'][0], color = 'red',label = 'Max 85th')
    plt.axhspan(Extremes['Min 85'][0],Extremes['Min 85'][0], color = 'blue',label = 'Min 85th')
    plt.axhspan(Extremes['Max 90'][0],Extremes['Max 90'][0], color = 'maroon',label = 'Max 90th')
    plt.axhspan(Extremes['Min 90'][0],Extremes['Min 90'][0], color = 'midnightblue',label = 'Min 90th')

    plt.legend()

    return(plt.figure(month_number), PRO_subdaily)




#%% Plot the months
months_ind_for_plotter(11,PRO_SD_ES,'Nov')
months_ind_for_plotter(12,PRO_SD_ES,'Dec')
months_ind_for_plotter(1,PRO_SD_ES,'Jan')
months_ind_for_plotter(2,PRO_SD_ES,'Feb')
months_ind_for_plotter(3,PRO_SD_ES,'Mar')





|#%% Time to apply the extended summer to heatwaves

#Heatwave_85 = Heatwave_85.set_index('date')
#Delete the unwanted columns

#Merge the sub-daily with max and min
HW_0 = pd.merge(left = Heatwave_85,right  =PRO_SD_0 ,left_index=True,right_index=True  ).dropna()
HW_3 = pd.merge(left = Heatwave_85,right  =PRO_SD_3 ,left_index=True,right_index=True  ).dropna()
HW_6 = pd.merge(left = Heatwave_85,right  =PRO_SD_6 ,left_index=True,right_index=True  ).dropna()
HW_9 = pd.merge(left = Heatwave_85,right  =PRO_SD_9 ,left_index=True,right_index=True  ).dropna()
HW_12 = pd.merge(left = Heatwave_85,right  =PRO_SD_12 ,left_index=True,right_index=True  ).dropna()
HW_15 = pd.merge(left = Heatwave_85,right  =PRO_SD_15 ,left_index=True,right_index=True  ).dropna()
HW_18 = pd.merge(left = Heatwave_85,right  =PRO_SD_18 ,left_index=True,right_index=True  ).dropna()
HW_21 = pd.merge(left = Heatwave_85,right  =PRO_SD_21 ,left_index=True,right_index=True  ).dropna()    



#%%Plot



HW_Sub = [HW_0,HW_3,HW_6,HW_9,HW_12,HW_15,HW_18,HW_21]
Titles_X =  ['12am Temperature','3am Temperature','6am Temperature','9am Temperature','12pm Temperature','3pm Temperature','6pm Temperature','9pm Temperature']


fig,ax = plt.subplots(nrows = 8, ncols = 2, sharex = True, sharey = True,figsize = (40,40))

for i in np.array([0,1,2,3,4,5,6,7]):
    #Plot the scatter
    #Max v Sub OF EXT
    #find line of best fit
    a, b = np.polyfit(PROSD[i][Titles_X[i]],PROSD[i]['PRO Max'], 1)
    #add points to plot
    corr, _ = pearsonr(PROSD[i][Titles_X[i]],PROSD[i]['PRO Max'])
    ax[i,0].scatter(PROSD[i][Titles_X[i]],PROSD[i]['PRO Max'],color = 'orange',label ='Ext Sum')
    ax[i,0].set_ylabel('PRO Max')
    ax[i,0].set_title('{} v Max'.format(Titles_X[i]))
    ax[i,0].set_xlabel('{}'.format(Titles_X[i]))
    ax[i,0].plot(PROSD[i][Titles_X[i]], a*PROSD[i][Titles_X[i]]+b,color ='black',label = 'PROMax = {}*({})+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a, 2),Titles_X[i],round(b, 2),round(np.power(corr,2), 3)))   
    
    #Max v Heatwave
    #find line of best fit
    a2, b2 = np.polyfit(HW_Sub[i][Titles_X[i]],HW_Sub[i]['PRO Max'], 1)
    #add points to plot
    corr2, _ = pearsonr(HW_Sub[i][Titles_X[i]],HW_Sub[i]['PRO Max'])
    ax[i,0].scatter(HW_Sub[i][Titles_X[i]],HW_Sub[i]['PRO Max'],color = 'red',label ='Heatwave Days')
    ax[i,0].plot(HW_Sub[i][Titles_X[i]], a2*HW_Sub[i][Titles_X[i]]+b2,color ='grey',label = 'PROMax = {}*({})+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a2, 2),Titles_X[i],round(b2, 2),round(np.power(corr2,2), 3)))   
    
    ax[i,0].legend()
    #Max v Sub
    a1, b1 = np.polyfit(PROSD[i][Titles_X[i]],PROSD[i]['PRO Min'], 1)
    #add points to plot
    corr1, _ = pearsonr(PROSD[i][Titles_X[i]],PROSD[i]['PRO Min'])
    ax[i,1].scatter(PROSD[i][Titles_X[i]],PROSD[i]['PRO Min'],color = 'blue',label ='Ext Sum')
    ax[i,1].set_ylabel('PRO Min')
    ax[i,1].set_title('{} v Min'.format(Titles_X[i]))
    ax[i,1].set_xlabel('{}'.format(Titles_X[i]))
    ax[i,1].plot(PROSD[i][Titles_X[i]], a1*PROSD[i][Titles_X[i]]+b1,color ='black',label = 'PROMin = {}*({})+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a1, 2),Titles_X[i],round(b1, 2),round(np.power(corr1,2), 3)))   


    ax[i,1].scatter(HW_Sub[i][Titles_X[i]],HW_Sub[i]['PRO Min'],color = 'navy',label ='Heatwave Days')

    #Max v Heatwave
    #find line of best fit
    a3, b3 = np.polyfit(HW_Sub[i][Titles_X[i]],HW_Sub[i]['PRO Min'], 1)
    #add points to plot
    corr3, _ = pearsonr(HW_Sub[i][Titles_X[i]],HW_Sub[i]['PRO Min'])
    ax[i,1].scatter(HW_Sub[i][Titles_X[i]],HW_Sub[i]['PRO Min'],color = 'navy',label ='Heatwave Days')
    ax[i,1].plot(HW_Sub[i][Titles_X[i]], a3*HW_Sub[i][Titles_X[i]]+b3,color ='grey',label = 'PROMin = {}*({})+({}), r\N{SUPERSCRIPT TWO}: {}'.format(round(a3, 2),Titles_X[i],round(b3, 2),round(np.power(corr3,2), 3)))   
    
    ax[i,1].legend()

    
    

#%%






Titles_shortened =  ['12am','3am','6am','9am','12pm','3pm','6pm','9pm']
means = []
for i in range(0,len(PROSD)):
    #Calc the mean
    mean_ind = HW_Sub[i][Titles_X[i]].mean()
    

    #Append
    means.append(mean_ind)


#Combine lists
means_HW = pd.Series(means,name = 'mean Heatwave sub-daily')

Titles_shortened = pd.Series(Titles_shortened,name = 'Subdaily Time')

PRO_subdaily = pd.concat([Titles_shortened,means_HW],axis=1)

plt.figure(1,figsize = (15,10))
#Plot these
plt.plot(PRO_subdaily['Subdaily Time'], PRO_subdaily['mean Heatwave sub-daily'],label = 'mean',color = 'black')
plt.xlabel('Time')
plt.ylabel('Temperature (degC)')
plt.title('Temperature Cycle During Day 1967-1992')
plt.grid()




plt.legend()






#%% NOVEMBER

def months_ind_for_plotter_Heatwave(month_number,PRO,hw, month_name):
    PRO = pd.concat([PRO[PRO.index.month==month_number],], axis = 0)
    PRO_SD_0 = pd.concat([PRO[PRO.index.hour==0]],axis =0)
    PRO_SD_3= pd.concat([PRO[PRO.index.hour==3]],axis =0)
    PRO_SD_6= pd.concat([PRO[PRO.index.hour==6]],axis =0)
    PRO_SD_9= pd.concat([PRO[PRO.index.hour==9]],axis =0)
    PRO_SD_12= pd.concat([PRO[PRO.index.hour==12]],axis =0)
    PRO_SD_15= pd.concat([PRO[PRO.index.hour==15]],axis =0)
    PRO_SD_18= pd.concat([PRO[PRO.index.hour==18]],axis =0)
    PRO_SD_21= pd.concat([PRO[PRO.index.hour==21]],axis =0)

    

    #Reomve hours out of it for concatiation

    PRO_SD_0 = PRO_SD_0.reset_index()
    PRO_SD_0['date'] = pd.to_datetime(PRO_SD_0['date']).dt.date
    PRO_SD_0 = PRO_SD_0.set_index('date')

    PRO_SD_3 = PRO_SD_3.reset_index()
    PRO_SD_3['date'] = pd.to_datetime(PRO_SD_3['date']).dt.date
    PRO_SD_3 = PRO_SD_3.set_index('date')

    
    PRO_SD_6 = PRO_SD_6.reset_index()
    PRO_SD_6['date'] = pd.to_datetime(PRO_SD_6['date']).dt.date
    PRO_SD_6 = PRO_SD_6.set_index('date')

    PRO_SD_9 = PRO_SD_9.reset_index()
    PRO_SD_9['date'] = pd.to_datetime(PRO_SD_9['date']).dt.date
    PRO_SD_9 = PRO_SD_9.set_index('date')

    PRO_SD_12 = PRO_SD_12.reset_index()
    PRO_SD_12['date'] = pd.to_datetime(PRO_SD_12['date']).dt.date
    PRO_SD_12 = PRO_SD_12.set_index('date')

    PRO_SD_15 = PRO_SD_15.reset_index()
    PRO_SD_15['date'] = pd.to_datetime(PRO_SD_15['date']).dt.date
    PRO_SD_15 = PRO_SD_15.set_index('date')

    PRO_SD_18 = PRO_SD_18.reset_index()
    PRO_SD_18['date'] = pd.to_datetime(PRO_SD_18['date']).dt.date
    PRO_SD_18 = PRO_SD_18.set_index('date')

    PRO_SD_21 = PRO_SD_21.reset_index()
    PRO_SD_21['date'] = pd.to_datetime(PRO_SD_21['date']).dt.date
    PRO_SD_21 = PRO_SD_21.set_index('date')
    


    PRO_SD_0 = PRO_SD_0.rename(columns={'temp':'12am Temperature'})
    PRO_SD_3 = PRO_SD_3.rename(columns={'temp':'3am Temperature'})
    PRO_SD_6 = PRO_SD_6.rename(columns={'temp':'6am Temperature'})
    PRO_SD_9 = PRO_SD_9.rename(columns={'temp':'9am Temperature'})
    PRO_SD_12 = PRO_SD_12.rename(columns={'temp':'12pm Temperature'})
    PRO_SD_15 = PRO_SD_15.rename(columns={'temp':'3pm Temperature'})
    PRO_SD_18= PRO_SD_18.rename(columns={'temp':'6pm Temperature'})
    PRO_SD_21 = PRO_SD_21.rename(columns={'temp':'9pm Temperature'})



    
    #Merge the sub-daily with max and min
    HW_0 = pd.merge(left = hw,right  =PRO_SD_0 ,left_index=True,right_index=True  ).dropna()
    HW_3 = pd.merge(left = hw,right  =PRO_SD_3 ,left_index=True,right_index=True  ).dropna()
    HW_6 = pd.merge(left = hw,right  =PRO_SD_6 ,left_index=True,right_index=True  ).dropna()
    HW_9 = pd.merge(left = hw,right  =PRO_SD_9 ,left_index=True,right_index=True  ).dropna()
    HW_12 = pd.merge(left = hw,right  =PRO_SD_12 ,left_index=True,right_index=True  ).dropna()
    HW_15 = pd.merge(left = hw,right  =PRO_SD_15 ,left_index=True,right_index=True  ).dropna()
    HW_18 = pd.merge(left = hw,right  =PRO_SD_18 ,left_index=True,right_index=True  ).dropna()
    HW_21 = pd.merge(left = hw,right  =PRO_SD_21 ,left_index=True,right_index=True  ).dropna()    

    HW = [HW_0,HW_3,HW_6,HW_9,HW_12,HW_15,HW_18,HW_21]
    Titles_X =  ['12am Temperature','3am Temperature','6am Temperature','9am Temperature','12pm Temperature','3pm Temperature','6pm Temperature','9pm Temperature']
    

    Titles_shortened =  ['12am','3am','6am','9am','12pm','3pm','6pm','9pm']
    means = []

    for i in range(0,len(HW)):
        #Calc the mean
        mean_ind = HW[i][Titles_X[i]].mean()
        #Append
        means.append(mean_ind)

    #Combine lists
    means = pd.Series(means,name = 'mean sub-daily')
    Titles_shortened = pd.Series(Titles_shortened,name = 'Subdaily Time')

    PRO_subdaily = pd.concat([Titles_shortened,means],axis=1)

    plt.figure(month_number,figsize = (15,10))
    #Plot these
    plt.plot(PRO_subdaily['Subdaily Time'], PRO_subdaily['mean sub-daily'],label = 'mean',color = 'black')
    plt.xlabel('Time')
    plt.ylabel('Temperature (degC)')
    plt.title('Temperature Cycle During Day 1967-1992 {}'.format(month_name))
    plt.grid()
 

    plt.legend()

    return(plt.figure(month_number),PRO_subdaily)



Plot_11_HW, HW_SUB_11= months_ind_for_plotter_Heatwave(11,PRO_SD_ES, Heatwave_85,'Nov')
Plot_12_HW, HW_SUB_12 =months_ind_for_plotter_Heatwave(12,PRO_SD_ES,Heatwave_85,'Dec')
Plot_1_HW, HW_SUB_1 = months_ind_for_plotter_Heatwave(1,PRO_SD_ES,Heatwave_85,'Jan')
Plot_2_HW, HW_SUB_2 = months_ind_for_plotter_Heatwave(2,PRO_SD_ES,Heatwave_85,'Feb')
Plot_3_HW, HW_SUB_3 = months_ind_for_plotter_Heatwave(3,PRO_SD_ES,Heatwave_85,'Mar')

#%% Combine the two


Plot_11, SUB_11 = months_ind_for_plotter(11,PRO_SD_ES,'Nov')
Plot_12, SUB_12 = months_ind_for_plotter(12,PRO_SD_ES,'Dec')
Plot_1, SUB_1 = months_ind_for_plotter(1,PRO_SD_ES,'Jan')
Plot_2, SUB_2 = months_ind_for_plotter(2,PRO_SD_ES,'Feb')
Plot_3, SUB_3 = months_ind_for_plotter(3,PRO_SD_ES,'Mar')




plt.figure(15)
plt.plot(SUB_11['Subdaily Time'], SUB_11['mean sub-daily'],color = 'blue',label = 'Average Extended Summer Day')
plt.plot(HW_SUB_11['Subdaily Time'], HW_SUB_11['mean sub-daily'],color = 'red',label = 'Average Heatwave Day')
plt.xlabel('Time')
plt.ylabel('Temperature (degC)')
plt.title('Temperature Cycle During Day 1967-1992 Nov')
plt.grid()    

plt.legend()
plt.figure(16)
plt.plot(SUB_12['Subdaily Time'], SUB_12['mean sub-daily'],color = 'blue',label = 'Average Extended Summer Day')
plt.plot(HW_SUB_12['Subdaily Time'], HW_SUB_12['mean sub-daily'],color = 'red',label = 'Average Heatwave Day')
plt.xlabel('Time')
plt.ylabel('Temperature (degC)')
plt.title('Temperature Cycle During Day 1967-1992 Dec')
plt.grid()
plt.legend()
plt.figure(17)
plt.plot(SUB_1['Subdaily Time'], SUB_1['mean sub-daily'],color = 'blue',label = 'Average Extended Summer Day')
plt.plot(HW_SUB_1['Subdaily Time'], HW_SUB_1['mean sub-daily'],color = 'red',label = 'Average Heatwave Day')
plt.xlabel('Time')
plt.ylabel('Temperature (degC)')
plt.title('Temperature Cycle During Day 1967-1992 Jan')
plt.grid()
plt.legend()
plt.figure(18)
plt.plot(SUB_2['Subdaily Time'], SUB_2['mean sub-daily'],color = 'blue',label = 'Average Extended Summer Day')
plt.plot(HW_SUB_2['Subdaily Time'], HW_SUB_2['mean sub-daily'],color = 'red',label = 'Average Heatwave Day')
plt.xlabel('Time')
plt.ylabel('Temperature (degC)')
plt.title('Temperature Cycle During Day 1967-1992 Feb')
plt.grid()
plt.legend()
plt.figure(19)
plt.plot(SUB_3['Subdaily Time'], SUB_3['mean sub-daily'],color = 'blue',label = 'Average Extended Summer Day')
plt.plot(HW_SUB_3['Subdaily Time'], HW_SUB_3['mean sub-daily'],color = 'red',label = 'Average Heatwave Day')
plt.xlabel('Time')
plt.ylabel('Temperature (degC)')
plt.title('Temperature Cycle During Day 1967-1992 Mar')
plt.legend()
plt.grid()


#%% Difference B/W Heatwaves and EXT SUMMER 

TIMES = pd.Series([0, 3, 6, 9, 12, 15, 18, 21],name = 'Time 24HR')

'''NOVEMBER'''
NOV = HW_SUB_11['mean sub-daily'] - SUB_11['mean sub-daily']
NOV = pd.merge(left = NOV,right  =TIMES ,left_index=True,right_index=True  )
'''DECEMBER'''
DEC = HW_SUB_12['mean sub-daily'] - SUB_12['mean sub-daily']
DEC = pd.merge(left = DEC,right  =TIMES ,left_index=True,right_index=True  )
'''JANUARY'''
JAN = HW_SUB_1['mean sub-daily'] - SUB_1['mean sub-daily']
JAN = pd.merge(left = JAN,right  =TIMES ,left_index=True,right_index=True  )
'''FEBRUARY'''
FEB = HW_SUB_2['mean sub-daily'] - SUB_2['mean sub-daily']
FEB = pd.merge(left = FEB,right  =TIMES ,left_index=True,right_index=True  )
'''MARCH'''
MAR = HW_SUB_3['mean sub-daily'] - SUB_3['mean sub-daily']
MAR = pd.merge(left = MAR,right  =TIMES ,left_index=True,right_index=True  )


plt.plot(NOV['Time 24HR'],NOV['mean sub-daily'],label = 'November')
plt.plot(DEC['Time 24HR'],DEC['mean sub-daily'],label = 'December')
plt.plot(JAN['Time 24HR'],JAN['mean sub-daily'],label = 'January')
plt.plot(FEB['Time 24HR'],FEB['mean sub-daily'],label = 'Februay')
plt.plot(MAR['Time 24HR'],MAR['mean sub-daily'],label = 'March')
plt.legend()
plt.xlim([0,21])
plt.grid()
plt.title('Difference Between Sub-Daily Averages of Heatwave Days and Extended Summer Days')
plt.xlabel('24HR Time')
plt.ylabel('Temperature (C)')


#%% Example lets choose the 16th of December 1990

#Max and Min
PRO_Extremes  = Perth_Regional_Office.loc['1967':'1992']
PRO_Extremes = pd.concat([  PRO_Extremes[PRO_Extremes.index.month==11], PRO_Extremes[PRO_Extremes.index.month==12], PRO_Extremes[PRO_Extremes.index.month==1], PRO_Extremes[PRO_Extremes.index.month==2], PRO_Extremes[PRO_Extremes.index.month==3],], axis = 0)
Max = PRO_Extremes['PRO Max'].loc['1990-12-12']
Min = PRO_Extremes['PRO Min'].loc['1990-12-12']



PRO_9 = PRO_SD_9['9am Temperature'].loc['1990-12-12']

PRO_12 = PRO_SD_12['12pm Temperature'].loc['1990-12-12'] 

PRO_15 = PRO_SD_15['3pm Temperature'].loc['1990-12-12'] 

PRO_18 = PRO_SD_18['6pm Temperature'].loc['1990-12-12'] 


PRO_21 = PRO_SD_21['9pm Temperature'].loc['1990-12-12'] 



PRO_0 = PRO_SD_0['12am Temperature'].loc['1990-12-12']

PRO_3  = PRO_SD_3['3am Temperature'].loc['1990-12-12'] 


PRO_6  = PRO_SD_6['6am Temperature'].loc['1990-12-12']

TIMES = ['9am', '12pm', '3pm', '6pm', '9pm','12am','3am','6am']
Titles_shortened = pd.Series(TIMES,name = 'Subdaily Time')

Sub_Temp = [PRO_9,PRO_12,PRO_15,PRO_18,PRO_21,PRO_0,PRO_3,PRO_6]

plt.scatter(Titles_shortened,Sub_Temp)
plt.scatter()

#%%

PRO_Extremes  = Perth_Regional_Office.loc['1967':'1992']
PRO_Extremes = pd.concat([  PRO_Extremes[PRO_Extremes.index.month==11], PRO_Extremes[PRO_Extremes.index.month==12], PRO_Extremes[PRO_Extremes.index.month==1], PRO_Extremes[PRO_Extremes.index.month==2], PRO_Extremes[PRO_Extremes.index.month==3],], axis = 0)
Max = PRO_Extremes['PRO Max'].loc['1990-12-12']
Min = PRO_Extremes['PRO Min'].loc['1990-12-13']
print(Max,Min)


PRO_9 = PRO_SD_9['9am Temperature'].loc['1990-12-12']

PRO_12 = PRO_SD_12['12pm Temperature'].loc['1990-12-12'] 

PRO_15 = PRO_SD_15['3pm Temperature'].loc['1990-12-12'] 

PRO_18 = PRO_SD_18['6pm Temperature'].loc['1990-12-12'] 


PRO_21 = PRO_SD_21['9pm Temperature'].loc['1990-12-12'] 



PRO_0 = PRO_SD_0['12am Temperature'].loc['1990-12-13']

PRO_3  = PRO_SD_3['3am Temperature'].loc['1990-12-13'] 


PRO_6  = PRO_SD_6['6am Temperature'].loc['1990-12-13']

PRO_92 = PRO_SD_9['9am Temperature'].loc['1990-12-13']

Titles_shortened = ['9am', '12pm', '3pm', '6pm', '9pm','12am' ,'3am','6am', '9am ']

Sub_Temp = [PRO_9,PRO_12,PRO_15,PRO_18,PRO_21,PRO_0,PRO_3,PRO_6, PRO_92]
Max_Temp = [Max,Max,Max,Max,Max,Max,Max,Max,Max]
Min_Temp = [Min,Min,Min,Min,Min,Min,Min,Min,Min]
plt.scatter(Titles_shortened,Sub_Temp,label = 'Sub-daily',color = 'black')
plt.plot(Titles_shortened,Max_Temp,label = 'Maximum',color ='red')

plt.title('Temperatures from 9am 12/12/1990 to 9am 13/12/1990',fontsize = 14)
plt.ylabel('Temperature (\N{DEGREE SIGN}C)',fontsize = 12)
plt.plot(Titles_shortened,Min_Temp, label = 'Minimum',color = 'blue')
plt.legend(loc=1)
plt.ylim([25,41])

#%%
TIMES = ['9am', '12pm', '3pm', '6pm', '9pm','12am','3am','6am']
Sub_Temp = [PRO_9,PRO_12,PRO_15,PRO_18,PRO_21,PRO_0,PRO_3,PRO_6]
Max_Temp = [Max,Max,Max,Max,Max,Max,Max,Max]
Min_Temp = [Min,Min,Min,Min,Min,Min,Min,Min]
plt.scatter(Titles_shortened,Sub_Temp)

plt.ylim([25,41])
