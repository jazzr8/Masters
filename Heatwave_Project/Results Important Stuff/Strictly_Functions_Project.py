#!/usr/bin/env python
# coding: utf-8

# # DAILY EXTREME ESTIMATOR FUNCTION

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
import xarray as xr
from sklearn.metrics import mean_squared_error
from math import sqrt
from datetime import datetime
import seaborn as sns
import math


# In[ ]:


def Temp_Estimation(Sub_Daily, Sub_Daily_Training,Daily_Extreme_Training, Trials):
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

    '''
    
    
    
    # Part 1: Split the Sub_Daily Training into individual hours ane combine
    Sub_Max, Sub_Min, Hours_Avaliable = Sub_Daily_Splitter(Sub_Daily_Training)
    print('DONE P1')
    # Part 2: Concat the Maximum and Minimum Data to the subdaily data
    Sub_Ext_Max, Sub_Ext_Min = concat_max_sub(Sub_Max, Sub_Min, Hours_Avaliable, Daily_Extreme_Training)
    print('DONE P2')

    #Now Every Single Available hour and max and min is ready to be used.
    #Part 3: Split into each respective Month and add all together so its like Month_Hour_Mx/Mn
    Monthly_Split_Dic = Month_Splitter(Hours_Avaliable,Sub_Ext_Max, Sub_Ext_Min)
    print('DONE P3')

    #Include 24 in the hours avalaible, this is to get it back to 0
    Hours_Avaliable_Inc_24 = Hours_Avaliable.copy()
    Hours_Avaliable_Inc_24.append(24)
    
    #PART 4 Is to fix up the Historical Data so it is closest to the every hour hour mark where data is avaliable
    Sub_Daily = Closest_Hour(Sub_Daily, Hours_Avaliable_Inc_24)
    print('DONE P4')

    #PART 5 Is to sample by the length of the number of datapoints for that month and max or min
    #Now I need to select 600 points and trail it 1000 times for each single thing in the dictionary and label the hour 0 as hour 0 run 1]
    #and PRO Max Run 1
    Sampled = Sampler_Trainer(Monthly_Split_Dic,Trials)
    print('DONE P5')

    #Part 6
    #Now to apply the regression anaylsis onto the data I have provide
    Linear_Analysis = Linear_Regression_Analysis(Trials, Hours_Avaliable, Sampled)
    print('DONE P6')

    #Part 7    
    #Get the data into their respective max and min with the hours matching the regression data, look at the explabations
    #above in Part 2 and Part 7 for more information
    Max_Data = Max_Sub(Sub_Daily)
    
    Min_Data= Min_Sub(Sub_Daily)
    print('DONE P7')

    #Part 8 Temperature Estimation
    Full_Temperature_Estimation= Tmax_Tmin_All_Data_Est(Trials, Max_Data, Min_Data, Linear_Analysis)
    print('DONE P8')

    #Part 9 The Best Temperature Estimation
    Temperature_Estimation = Absolute_Estimation(Full_Temperature_Estimation, Trials)
    print('DONE P9')

    #Part 10. Adding all into DataFrames (not dictionaries)
    Max, MaxCorr, Min, MinCorr= Cleansing_Data(Temperature_Estimation)
    print('DONE P10')

    
    
    return(Max, MaxCorr, Min, MinCorr)


# In[ ]:


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
    


# In[ ]:


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


# In[ ]:


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


# In[ ]:


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


# In[ ]:


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


# In[ ]:


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


# In[ ]:


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


# In[ ]:


#Now develop the linear regression equation
def linear_regression_polyfit(x,y):
    #Find the linear Relationship
    A, B = np.polyfit(x, y, 1)
    #Find the correlation                  
    corr, _ = spearmanr(x, y)
    return(A,B,corr)


# In[ ]:


def Max_Sub(Data):
    Sub_Daily_Data = Data.copy()
    #Get the estimation sorted
    # Shift hours 0 to 8 to the previous day's hours for maximum regression of 9am+0 to 8am+1
    Sub_Daily_Data['date'] = pd.to_datetime(Sub_Daily_Data['date'])
    Sub_Daily_Data.loc[Sub_Daily_Data['date'].dt.hour < 9, 'date'] = Sub_Daily_Data['date'] - pd.offsets.Day(1)
    Sub_Daily_Data['date'] = Sub_Daily_Data['date'].dt.strftime('%Y-%m-%d %H:%M:%S')

    return(Sub_Daily_Data)


# In[ ]:


def Min_Sub(Data):
    Sub_Daily_Data = Data.copy()
    # Shift hours 10 to 23 to the tomorrows day's hours for minimum regression of 10am-1 to 9am+0
    Sub_Daily_Data['date'] = pd.to_datetime(Sub_Daily_Data['date'])
    Sub_Daily_Data.loc[Sub_Daily_Data['date'].dt.hour > 9, 'date'] = Sub_Daily_Data['date'] + pd.offsets.Day(1)
    Sub_Daily_Data['date'] = Sub_Daily_Data['date'].dt.strftime('%Y-%m-%d %H:%M:%S')


    return(Sub_Daily_Data)


# In[ ]:


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
        print(T)
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


# In[ ]:


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


# In[ ]:


#To make sure each max and min day does get chosen, we will have to estimate both indiviudally before they are combined for
#for that day
def Absolute_Estimation(Estimated_Data, Trials):
    #We need a new dictionary for the finalised estimation
    Est_Daily_Extremes = {}
    

    #Lets begin by using a for loop that extracts that Trail number and the indivudal max and min estimations
    for T in range(1,Trials+1):
        print(T)

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
            Max_Est,Max_Corr = Choice_Model(loc_date_Mx, True)
        
            Tmax.append(Max_Est)
            Corr_Max.append(Max_Corr)
    
    
        #Min
        for i in range(len(Unique_dates_Min)):
            #Get the individual date
            loc_date_Mn = Min_Data.loc[Min_Data[Min_C[0]] == '{}-{}-{}'.format(Unique_dates_Min[Min_C[0]][i].year,Unique_dates_Min[Min_C[0]][i].month,Unique_dates_Min[Min_C[0]][i].day)]
            #iT is in its length, the 1 length data is remaining with the index as the row
            #from here we will then select either complex or simple and then go into another function.
            Min_Est,Min_Corr = Choice_Model(loc_date_Mn, False)
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


def Choice_Model(data, Max):
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


#Convert to DataFrame
def Cleansing_Data(data):
    '''
    It is the dictionaries of all the trials and this will be just cleaned up with all relevent information to covnert
    them into 4 dataframes

    
    '''
    
        #DataFrames
    Max_DF = pd.DataFrame()
    Min_DF = pd.DataFrame()
    CorrMax_DF = pd.DataFrame()
    CorrMin_DF = pd.DataFrame()

    for key, df in data.items():
        #Extract the trial number
        trial_number = key.split('_')[1]

        #Change Name of each column to Something Simple with trial Number
        df.columns = ['Max_' + trial_number, 'MaxCorr_' + trial_number,
                      'Min_' + trial_number, 'MinCorr_' + trial_number]

        #Combine the Trials
        Max_DF = pd.concat([Max_DF, df[df.columns[0]]], axis=1)
        CorrMax_DF = pd.concat([CorrMax_DF, df[df.columns[1]]], axis=1)
        Min_DF = pd.concat([Min_DF, df[df.columns[2]]], axis=1)
        CorrMin_DF = pd.concat([CorrMin_DF, df[df.columns[3]]], axis=1)



    #Add Median, Mean, Conf60, Conf90, and Range

    #----------------MAX-----------------------#
    # Calculate the median across Trials
    Data = Max_DF
    median_values = Data.median(axis=1).round(2)
    median_values.name = 'Max Median'
    # Calculate the mean across Trials
    mean_values = Data.mean(axis=1).round(2)
    mean_values.name = 'Max Mean'
    # Calculate the 60% confidence interval
    confidence_60 = Data.quantile(q=[0.2, 0.8], axis=1).T.round(2)
    confidence_60.columns = ['Max Lower CI (60%)', 'Max Upper CI (60%)']
    # Calculate the 90% confidence interval
    confidence_90 = Data.quantile(q=[0.05, 0.95], axis=1).T.round(2)
    confidence_90.columns = ['Max Lower CI (90%)', 'Max Upper CI (90%)']
    # Calculate the full range
    Range = Data.apply(lambda row: np.ptp(row), axis=1).round(2)
    Range.name = 'Max Full Range'

    Max_All = pd.concat([mean_values,median_values,confidence_60,confidence_90,Range,Data.round(2)],axis=1)

    #----------------CORRMAX-----------------------#
    # Calculate the median across Trials
    Data = CorrMax_DF
    median_values = Data.median(axis=1).round(4)
    median_values.name = 'CorrMax Median'
    # Calculate the mean across Trials
    mean_values = Data.mean(axis=1).round(4)
    mean_values.name = 'CorrMax Mean'
    # Calculate the 60% confidence interval
    confidence_60 = Data.quantile(q=[0.2, 0.8], axis=1).T.round(4)
    confidence_60.columns = ['CorrMax Lower CI (60%)', 'CorrMax Upper CI (60%)']
    # Calculate the 90% confidence interval
    confidence_90 = Data.quantile(q=[0.05, 0.95], axis=1).T.round(4)
    confidence_90.columns = ['CorrMax Lower CI (90%)', 'CorrMax Upper CI (90%)']
    # Calculate the full range
    Range = Data.apply(lambda row: np.ptp(row), axis=1).round(4)
    Range.name = 'CorrMax Full Range'

    CorrMax_All = pd.concat([mean_values,median_values,confidence_60,confidence_90,Range,Data.round(4)],axis=1)



    #----------------MIN-----------------------#
    # Calculate the median across Trials
    Data = Min_DF
    median_values = Data.median(axis=1).round(2)
    median_values.name = 'Min Median'
    # Calculate the mean across Trials
    mean_values = Data.mean(axis=1).round(2)
    mean_values.name = 'Min Mean'
    # Calculate the 60% confidence interval
    confidence_60 = Data.quantile(q=[0.2, 0.8], axis=1).T.round(2)
    confidence_60.columns = ['Min Lower CI (60%)', 'Min Upper CI (60%)']
    # Calculate the 90% confidence interval
    confidence_90 = Data.quantile(q=[0.05, 0.95], axis=1).T.round(2)
    confidence_90.columns = ['Min Lower CI (90%)', 'Min Upper CI (90%)']
    # Calculate the full range
    Range = Data.apply(lambda row: np.ptp(row), axis=1).round(2)
    Range.name = 'Min Full Range'

    Min_All = pd.concat([mean_values,median_values,confidence_60,confidence_90,Range,Data.round(2)],axis=1)

    #----------------CORRMAX-----------------------#
    # Calculate the median across Trials
    Data = CorrMin_DF
    median_values = Data.median(axis=1).round(4)
    median_values.name = 'CorrMin Median'
    # Calculate the mean across Trials
    mean_values = Data.mean(axis=1).round(4)
    mean_values.name = 'CorrMin Mean'
    # Calculate the 60% confidence interval
    confidence_60 = Data.quantile(q=[0.2, 0.8], axis=1).T.round(4)
    confidence_60.columns = ['CorrMin Lower CI (60%)', 'CorrMin Upper CI (60%)']
    # Calculate the 90% confidence interval
    confidence_90 = Data.quantile(q=[0.05, 0.95], axis=1).T.round(4)
    confidence_90.columns = ['CorrMin Lower CI (90%)', 'CorrMin Upper CI (90%)']
    # Calculate the full range
    Range = Data.apply(lambda row: np.ptp(row), axis=1).round(4)
    Range.name = 'CorrMin Full Range'

    CorrMin_All = pd.concat([mean_values,median_values,confidence_60,confidence_90,Range,Data.round(4)],axis=1)

    return(Max_All, CorrMax_All, Min_All, CorrMin_All)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # The Heatwave Function

# In[ ]:


#The Core Function
def Heatwave_Function_v4(Dataset,
                         Dates_DataFrame,
                         CDP_Matrix,
                         Heatwave_Detail= True,
                         Percentile = 85,
                         window = 7,
                         CDP_start_end_years = [1961,1990]):
    '''
    Parameters
    ----------
    Dataset : DataFrame
        A Tmax and Tmin Dataset that has index as numbers and not datetime.
        #It should be in column form date_name, Tmax, Tmin
        datetime should be in format Year-Month-Day Already
        
    Dates_DataFrame : DataFrame
        This is just a DataFrame that has the dates of 366 days ready to be used where needed. 
    
    CDP_Matrix : Array
        If set to [] then the functions and arguements relating to the CDP are irrelevant to the function by inputs should be
        for the function to work properly.
    
    Heatwave_Detail : True or False
        If True is selected the heatwaves will be expanded into more detail.
        
    Percentile : Integer/Decimal
        A number that is used for the CDP, it calculates the value where the temperature must exceed to be in 
        that x percentile
    
    
    window : Integer
        Number of days either side of the day in focus that is used to calculate the percentile value in the CDP
    
    CDP_start_end_years : array of 2
        The years when the CDP should be calculated. Forms the basis of how many heatwaves we get
    
    RETURNS
    -----------------
    
    heatwaves : DataFrame
        The heatwave with all the relevant information.
        
    CDP : DataFrame
        Calendar Day Percentile so this can be inputted in the function again and save time.
    
    
  
    
    '''
    #Extract Columns
    Column_Dataset = Dataset.columns
    
    #For the calendar day percentile (CDP) function this dataset needs to be expanded to dataset_exp
    Dataset_Exp = Date_Splitter(Dataset)
    
    #Now calculate the Calender Day Percentiles for tmax and tmin if required.
    if (len(CDP_Matrix) == 0):
        #Now to calculate the CDP for Max and Min Temperatures
        CDP_Max = Calendar_Day_Percentile(Dataset_Exp,Percentile,
                                      Column_Dataset[1],
                                      CDP_start_end_years[0],
                                      CDP_start_end_years[1],
                                      window,
                                      Dates_DataFrame)
    
        CDP_Min = Calendar_Day_Percentile(Dataset_Exp,Percentile,
                                      Column_Dataset[2],
                                      CDP_start_end_years[0],
                                      CDP_start_end_years[1],
                                      window,
                                      Dates_DataFrame)\
        #Concat the tmax and tmax CDPs together
        CDP_Max_Col = CDP_Max.columns 
        CDP_Min_Col = CDP_Min.columns 
        CDP = pd.concat([CDP_Max[CDP_Max_Col[0]],CDP_Max[CDP_Max_Col[1]],CDP_Min[CDP_Min_Col[1]]],axis=1) #Change the name
    else:
        CDP = CDP_Matrix
    
    
    # Now using all the information, generate the Excess Heat Factor Values
    #Lets make it simpler and calculate the EHF which has the components of EHI sig and EHI acc
    EHF_Max, EHF_Min = EXCESS_HEAT_FACTOR(Dataset, CDP)
    
    #Combine all the data together in 1 big dataset
    #Make all datetime set
    Dataset_Date =  Dataset.set_index(Column_Dataset[0])
    #This is finding the highest and lowest year within the dataset
    Start_end_year = [Dataset_Date['year'].min(),Dataset_Date['year'].max()]
    
    #Clean the Dataset_Date up a bit 
    del Dataset_Date['year'] 
    del Dataset_Date['month']
    del Dataset_Date['day'] 
    
    #Remane the EHF columns so its max and min categorised
    EHF_Max_Min_Col = EHF_Max.columns
    EHF_Max = EHF_Max.rename(columns={EHF_Max_Min_Col[1]:EHF_Max_Min_Col[1] + '{}'.format('Max')})
    EHF_Max = EHF_Max.rename(columns={EHF_Max_Min_Col[2]:EHF_Max_Min_Col[2] + '{}'.format('Max')})
    EHF_Max = EHF_Max.rename(columns={EHF_Max_Min_Col[3]:EHF_Max_Min_Col[3] + '{}'.format('Max')})
    EHF_Max_Date =  EHF_Max.set_index(EHF_Max_Min_Col[0])
    EHF_Min = EHF_Min.rename(columns={EHF_Max_Min_Col[1]:EHF_Max_Min_Col[1] + '{}'.format('Min')})
    EHF_Min = EHF_Min.rename(columns={EHF_Max_Min_Col[2]:EHF_Max_Min_Col[2] + '{}'.format('Min')})
    EHF_Min = EHF_Min.rename(columns={EHF_Max_Min_Col[3]:EHF_Max_Min_Col[3] + '{}'.format('Min')})
    EHF_Min_Date =  EHF_Min.set_index(EHF_Max_Min_Col[0])
    
    
    #Add all the data together and the columns should be
    '''
    index \ date \ Max \ Min \ Excess Heat Factor Max \ Heat Stress Max \ Excess Heat Max \ Excess Heat Factor Min \ Heat Stress Min \ Excess Heat Min 
    '''
    Full_Information_Vector = pd.concat([Dataset_Date, EHF_Max_Date, EHF_Min_Date],axis=1)
    Full_Information_Vector = Full_Information_Vector.reset_index()
    
    #Calculate both heatwaves and warmwaves
    Warm_Spells_Matrix, Warm_Spells_Max_Only = Warm_Spells(Full_Information_Vector)
    
    #Find the heatwaves with loose ends at the start of Nov and end of Mar
    heatwaves = Heatwave_Function(Warm_Spells_Matrix)
    
    #Generate an extended form of the heatwave table if required.
    if(Heatwave_Detail == True):
        heatwaves = Heatwave_Table_Generator(heatwaves,heatwaves_data)

    return(heatwaves,heatwaves_data,CDP,Full_Information_Vector)    


# In[ ]:


#%%
def Date_Splitter(Dataset):
    '''
    Parameters
    ----------
    Data : Dataframe 
        CSV dataframe where the data is from.
        
    date_title : String
        Datetime Column Name for the extraction

    Returns
    -------
    Dataset : DataFrame
        DataFrame that has 3 new columns for Year Month and Day

    '''
    #Exctract all the columns, but the one we need is column 0
    Column_Dataset = Dataset.columns
    #Split the data into year, month and day
    Dataset['year'] =Dataset[Column_Dataset[0]].dt.year
    Dataset['month']=Dataset[Column_Dataset[0]].dt.month
    Dataset['day']  =Dataset[Column_Dataset[0]].dt.day
    return(Dataset)


# In[ ]:


def Calendar_Day_Percentile(Data,Percentile,Column_Name,start_year,end_year, window, Dates_DataFrame):
    '''
    Parameters
    ----------
    Data : Dataframe 
        The DataFrame in the expanded date form with year, month and day done already.
        
    Percentile : Integer/Decimal
        A number that is used for the CDP, it calculates the value where the temperature must exceed to be in 
        that x percentile
        
    Column_Name : String
        Determines if we are working out max or min temperatures
        
    start_year : Integer
        Year you want to start the CDP from
        
    end_year : Integer
        Year you want to end the CDP from
        
    Dates_DataFrame : DataFrame
        These are the 366 total days that the CDP function will append to so we can extract a day and month in the future
        when caculating the Excess Heat Factor
        
    Returns
    -------
    CDP : DataFrame
        Calendar Day Percentile of the entire year from the baseline and window chsoen in DataFrame format

    '''
    
    '''
    Start and end Years for the values to use
    Start Year will be Nov - 1911 to Mar - 1942
    I will classify a year heatwave as the 1911 season as Nov-1911 to Mar-1912

    Years to be excluded from the data:
    1910 and 2021 as these are incomplete

    In the 1880-1900
    This will be a different
    '''
    #Extract Columns 
    Column_Dataset = Data.columns
    
    #Set Index to Date
    Data_Extracted = Data.set_index(Column_Dataset[0])
    
    #Extract the Start and End Year only and since we are starting from Summer and ending 
    #Lets go from 1911 - 1 December to 1940 - November as an example
    
    #Extract the Summer of first year to Last month of spring of the last year
    Data_Extracted = Data_Extracted.loc['{}-12-01'.format(start_year-1):'{}-11-30'.format(end_year)]
    
    #Group By month and day
    group_days = Data_Extracted.groupby(['month','day'])
    Daily_Data= []
    
    #Now using the month and daily data for each of the 366 days put them in their separate bins
    for groups,days in group_days:
        #Extract the specified day bin
        Dailypre = group_days.get_group(groups).reset_index()
        #Get the maximum values for the entire record for that calendar day
        Values= Dailypre[Column_Name]
        #Make it a dataframe so it is appendable
        Values = Values.to_frame()
        #Append that bin to that day so there will be 366 bins with  x years of data
        Daily_Data.append(Values[Column_Name])
            
        
    #Now The Daily_Data has been done, we can then apply the CDP onto the bins for a window and estimate the value for the 
    #percentile
    CalendarDay = TnX_Rolling(window, Daily_Data, Percentile)
    
    #Clean the data up
    CDP = pd.DataFrame(CalendarDay, columns = [Column_Name])
    CDP = pd.concat([Dates_DataFrame,CDP],axis=1)
    CDP['date'] = pd.to_datetime(CDP['date'],format="%d/%m/%Y")

        
    return(CDP)


# In[ ]:


def TnX_Rolling(Window ,Dataset, Percentile):
    '''
    Parameters
    ----------
    Window : Integer
        How many days before AND after that the CDP will use up
        
    Dataset : DataFrame
        It is the Daily_Data dataset that will be used from 3.
    
    Percentile : Integer/Decimal
        It is the percentile the temperature must reaach to be accepted

    Returns
    -------
        TnX : Series
        Array of length 366 of the CDP values.

    '''
    
    #Since we are using the quantile version we start with that, same as percentile just 100 times less.
    percent_to_quant = Percentile/100
    
    
    TnX = []
    #Ignore warnings cause we all know its a pain in the buttox
    warnings.filterwarnings('ignore')
    
    
    #Lets begin with the central day so this will then be looped around and extracts each calendar day starting with 01-01
    for central_day in range(366):
        Temp_Storage = []
        #The reason its 366 because it goes from 0 to 365 which is still length of 366
        #Now to make the loop around the day in focus and append this to the central day  
        
        for around_days in range(0,Window+1):
            #First make the if statement of central_day
            if (around_days == 0):
                #Add the data to a storage to be used
                Temp_Storage = Dataset[central_day].to_numpy()
            else:
                #This is to check the windows for the other 365 days, if <0 or >365, then it extracts it from <=365 or >=0 
                #Lets start with the addition of the window so central_day + window
                if ((central_day + around_days) > 365):
                    Window_Early_Year =  central_day + around_days - 366
                    #Append this to the Temp_Storage
                    Temp_Storage = np.concatenate((Temp_Storage, Dataset[Window_Early_Year].to_numpy()),axis =0)
                    #Append the negative version to the Temp_Storage
                    Temp_Storage = np.concatenate((Temp_Storage, Dataset[central_day - around_days].to_numpy()),axis =0)

                elif ((central_day - around_days < 0)):
                    Window_Late_Year =  central_day - around_days + 366
                    #Append this to the Temp_Storage
                    Temp_Storage = np.concatenate((Temp_Storage, Dataset[Window_Late_Year].to_numpy()),axis =0)
                    #Append the negative version to the Temp_Storage
                    Temp_Storage = np.concatenate((Temp_Storage, Dataset[central_day + around_days].to_numpy()),axis =0)
                    
                else:
                    #If within bounds append normally
                    Temp_Storage = np.concatenate((Temp_Storage, Dataset[central_day + around_days].to_numpy()),axis =0)
                    Temp_Storage = np.concatenate((Temp_Storage, Dataset[central_day - around_days].to_numpy()),axis =0)

        #Create a for loop that uses the YearTempData and find the percentile for that calendar based value.
        #Now calculate the Percentile 
        Tn = np.quantile(Temp_Storage[~np.isnan(Temp_Storage)], percent_to_quant)#Have a llok properly and code it myslef and pull out ranks and find 90th percentile
        TnX.append(Tn)
    return(TnX) 


# In[ ]:


def EXCESS_HEAT_FACTOR(Data, CDP_Data):
        '''
        Parameters
        ----------
        Dataset : DataFrame
            A Tmax and Tmin Dataset that has index as numbers and not datetime.
            It should be in column form date_name, Tmax, Tmin
            datetime should be in format Year-Month-Day Already
        
        CDP_Data : DataFrame
            The calendar day percentile based off a percetnile where the temperature needs to reach to be in that percentile.
        
        Returns 
        ----------
        Excess_Heat_Stress_Factor_Matrix_Max : DataFrame
            A DataFrame that includes the Excess Heat, Heat Stress and Excess Heat Factor variables for the tmax
        
        Excess_Heat_Stress_Factor_Matrix_Min : DataFrame
            A DataFrame that includes the Excess Heat, Heat Stress and Excess Heat Factor variables for the tmax

        
        '''
        #Extract the columsn of the Data and CDP
        Data_col = Data.columns
        CDP_col = CDP_Data.columns
        
        #Extract the date title
        Data_Date = Data_col[0]
        CDP_Date = CDP_col[0]
        
        #Set the index to dateData_Date
        Data_Date_I = Data.set_index(Data_Date)
        CDP_Date_I = CDP_Data.set_index(Data_Date)
        
        #Now we need to set the data with the start and end year to what is specified.
        #Since the extended Summer begins in November and ends in March and the EHIacc needs a 30 day average prior to the 
        #i-2 so this means from the 1-11-XXXX we need to go back 33 days prior. This sets us to 29-9-XXXX.
        #Data_Range = Data_Date_I.loc['{}-09-29'.format(start_end_years[0]):'{}-04-30'.format(start_end_years[1]+1)]
        
        #Now we have the necessary data to work out the EHIsig, EHIacc and EHF for both Max, Min and ?Average?
        #Heat_Stress
        EHIacc_Max = Heat_Stress(Data_Date_I, Data_col[1]) 
        EHIacc_Min = Heat_Stress(Data_Date_I, Data_col[2]) 

        #Excess Heat
        EHIsig_Max = Excess_Heat(CDP_Date_I,CDP_col[1], Data_Date_I, Data_col[1]) 
        EHIsig_Min = Excess_Heat(CDP_Date_I,CDP_col[2], Data_Date_I, Data_col[2]) 
        Excess_Heat_Stress_Matrix_Max = pd.merge(EHIacc_Max,EHIsig_Max,how='left',on = [Data_Date])
        Excess_Heat_Stress_Matrix_Min = pd.merge(EHIacc_Min,EHIsig_Min,how='left',on = [Data_Date])
        
        #Excess Heat Factor
        EHF_Max = Excess_Heat_Factor_Calculator(Excess_Heat_Stress_Matrix_Max)
        EHF_Min = Excess_Heat_Factor_Calculator(Excess_Heat_Stress_Matrix_Min)
        
        #Combine
        Excess_Heat_Stress_Factor_Matrix_Max = pd.merge(EHF_Max,Excess_Heat_Stress_Matrix_Max,how='left',on = [Data_Date])
        Excess_Heat_Stress_Factor_Matrix_Min = pd.merge(EHF_Min,Excess_Heat_Stress_Matrix_Min,how='left',on = [Data_Date])
    
        return(Excess_Heat_Stress_Factor_Matrix_Max,Excess_Heat_Stress_Factor_Matrix_Min)


# In[ ]:


def Heat_Stress(Data, Max_Min_Ave_Col):
    '''
    Parameters
    ----------
    Data : DataFrame
        This has the datetime as the index
    
    Max_Min_Col : Array
        The choose of choosing the max or min or average column to use from the dataset
    
    Returns
    ----------
    EHIacc_vector :  DataFrame
        The Heat Stress DataFrame
    '''
    #Extract the column
    Extracted_Data = Data[Max_Min_Ave_Col]
    
    #Reset the index to calculate the averages
    Extracted_Data = Extracted_Data.reset_index()
    Extracted_Data_col = Extracted_Data.columns
    #Necessary Columns to append
    #A date column
    date_Values = []
    #EHIacc column
    EHIacc = []
    
    #Do the for loop
    for dt in np.arange(Extracted_Data.index[0]+33,len(Data)):
        #Extract the date index
        Date = Extracted_Data[Extracted_Data_col[0]].loc[dt]
        
        #3-day mean where the day in focus is i
        #But we need a checker to make sure all values are present
        length_3day = len(Extracted_Data[Max_Min_Ave_Col].loc[dt-2:dt].dropna())
        if (length_3day < 3):
            mean_3_day = np.nan
        else:
            mean_3_day = Extracted_Data[Max_Min_Ave_Col].loc[dt-2:dt].mean()
            
        #3 to 32 day mean
        #Now a dropna of 75% of values there means we can still work out the average
        length_30day = len(Extracted_Data[Max_Min_Ave_Col].loc[dt-32:dt-3].dropna())
        
        if (length_30day < 23):
            mean_30_day = np.nan
        else:
            mean_30_day = Extracted_Data[Max_Min_Ave_Col].loc[dt-32:dt-3].dropna().mean()
        #The individual heat stress value
        Heat_Stress_Value = mean_3_day - mean_30_day
        #Append the date and Heat Stress Value
        date_Values.append(Date)
        EHIacc.append(Heat_Stress_Value)
    
    #Name the terms and combine
    EHIacc = pd.DataFrame(EHIacc,columns=['Heat Stress'])
    date_Values = pd.DataFrame(date_Values,columns=[Extracted_Data_col[0]])
    
    EHIacc_vector = pd.concat([date_Values, EHIacc],axis=1)
    
    return(EHIacc_vector)


# In[ ]:


def Excess_Heat(CDP,CDP_max_min_ave, Data, Max_Min_Ave_Col):
    '''
    Parameters
    ----------
    CDP : DataFrame
        The calendar day percentile based off a percetnile where the temperature needs to reach to be in that percentile.
    
    CDP_max_min_ave : string
        The choose of choosing the max or min or average column to use from the CDP dataset
     
    Data : DataFrame
        This has the datetime as the index
    
    Max_Min_Col : string
        The choose of choosing the max or min or average column to use from the Data dataset
    
    Return
    ---------
    EHIsig_vector :  DataFrame
        The Excess Heat DataFrame
    
    '''
    
    
    
    #Reset the index to calculate the averages of the data
    Extracted_Data = Data.reset_index()
    Extracted_Data_col = Extracted_Data.columns
    
    
    
    
    #Necessary Columns to append
    #A date column
    date_Values = []
    #EHIsig column
    EHIsig = []
    
    #Do the for loop
    for dt in np.arange(Extracted_Data.index[0]+33,len(Data)):
        
    
        #Extract the date index
        Date = Extracted_Data[Extracted_Data_col[0]].loc[dt]
        
        #Extract the date in the CDP column, we know the year is 2020
        CDP_day = CDP[CDP_max_min_ave].loc['2020-{}-{}'.format(Date.month,Date.day)]
             
        Excess_Heat_Value = Extracted_Data[Max_Min_Ave_Col].loc[dt] -  CDP_day
                                                       

        #Append the date and Heat Stress Value
        date_Values.append(Date)
        EHIsig.append(Excess_Heat_Value)
    
    #Name the terms and combine
    EHIsig = pd.DataFrame(EHIsig,columns=['Excess Heat'])
    date_Values = pd.DataFrame(date_Values,columns=[Extracted_Data_col[0]])
    
    EHIsig_vector = pd.concat([date_Values, EHIsig],axis=1)
    
    
    return(EHIsig_vector)


# In[ ]:


def Excess_Heat_Factor_Calculator(Excess_Heat_Stress_Matrix):
    '''
    Parameters
    ----------
    Excess_Heat_Stress_Matrix : DataFrame
        This is a DataFrame that combines the Excess Heat, Heat Stress together in one DataFrame
    
    Returns
    ----------
    EHF_vector : DataFrame
        This is the combination of the Excess Heat and Heat Stress as a value for each day.
    
    '''
    EH_col = Excess_Heat_Stress_Matrix.columns
    #Col 0 : Date name, Col 1: Heat Stress Col 2: Excess Heat
    
    
    
    #Necessary Columns to append
    #A date column
    date_Values = []
    #EHIsig column
    EHF = []
    
    
    
    
    #Make sure when there are 2 positive it remains positive, if there are two negatives it remains negative 
    #and if one pos and one neg it remains negative
    for dt in np.arange(Excess_Heat_Stress_Matrix.index[0],len(Excess_Heat_Stress_Matrix)):
    
        #Extract the date index
        Date = Excess_Heat_Stress_Matrix[EH_col[0]].loc[dt]
        
        #Get the Heat Stress Term
        HS = Excess_Heat_Stress_Matrix[EH_col[1]].loc[dt]
        
        #Get the Excess Heat Term 
        EH = Excess_Heat_Stress_Matrix[EH_col[2]].loc[dt]
        
        #Multiply together
        
        if ((HS <0) and (EH <0)):
            EHF_single =  -1*EH* HS #degC^2
        else:
            EHF_single =  EH* HS #degC^2

        #Append the date and Heat Stress Value
        date_Values.append(Date)
        EHF.append(EHF_single)
        
    #Name the terms and combine
    EHF = pd.DataFrame(EHF,columns=['Excess Heat Factor'])
    date_Values = pd.DataFrame(date_Values,columns=[EH_col[0]])
    
    EHF_vector = pd.concat([date_Values, EHF],axis=1)
    
    
    return(EHF_vector)


# In[ ]:


def Warm_Spells(Data):
    '''
    Parameters
    ----------
    Data : DataFrame
        Calculated from the EHF's and now used in the warm spell. The columns go like:
        index \ date \ Max \ Min \ Excess Heat Factor Max \ Heat Stress Max \ Excess Heat Max \ Excess Heat Factor Min \ Heat Stress Min \ Excess Heat Min 
                col 0  col 1 col 2  col 3                    col 4             col 5              col 6                   col 7              col 8                    
    
    Returns
    ----------
    warm_spell_df : DataFrame
        Warm and heatwaves that are calculated by using the combination of 3 days and 2 nights definition.
        
    warm_spell_M_O_df :
        Warm and heatwaves that are calculated by only the tmax component.
    '''
    
    #The way that my Warm Spell definition works is that there must be at least 3 Max positive EHFs within 3 days initially
    #with at least 2 minimums that are positive within the first 3 days. From there, the EHF can be positive in the day
    #without too much worry of the minimum. 
    
    #Side note: what about adding the EHF for the days temperatures
    #However the reason behind this is because the min temp is found from 9am to 9am of the day before to the day in focus
    #therefore some min temps might not be the day in focus 0hr-9amhr and actually be in the day before which may stuff up
    #some values. If the min and max were calcualted from 0hr to 0hr a better method that includes a more extenisve use
    #of the min temperature can be included.
    
    #Lets extract the columns first
    Data_col = Data.columns
    #Assign Appropiate lists and values
    Warm_Spell_List = []
    Warm_Spell_Max_Only_List = []
    
    break_days = 2 
    
    id_count = 0
    id_count_M_O = 0
    
    Max_Count = 0
    for dt in np.arange(Data.index[0],len(Data)):
        #We are looking for a period of at least 3 days 
        if (Max_Count >= 3):
            #So we have a Max_Count of 3 and greater
            #Lets continue to add to the max count if EHF > 0
            if (Data[Data_col[3]][dt] >= 0):
                Max_Count = Max_Count + 1
                #Since the heatwave hasnt broken continue
                break_days = 0
            else:
                break_days = break_days + 1
                #Now if two break days in a row stop the warm spell
                if (break_days > 1):
                    #This stops the heatwave creates an ID 
                    id_count_M_O = id_count_M_O + 1
                    #This is for Max only and minu to is due to the break day part
                    Warm_Spell_M_O  = Data.loc[dt-Max_Count:dt-2]
                    Warm_Spell_M_O['id'] = [id_count_M_O] * len(Warm_Spell_M_O)
                    Warm_Spell_Max_Only_List.append(Warm_Spell_M_O)
                    
                    
                    #Now to check if its an actual Warm_Spell with my definition
                    Min_Checker = Data.loc[dt-Max_Count:dt-Max_Count+2]
                    Min_Length= len(Min_Checker[Min_Checker[Data_col[6]]>=0])
                    
                    if (Min_Length >= 2):
                        #This creates an ID 
                        id_count = id_count + 1
                        #This is for the entire warm spell
                        Warm_Spell  = Data.loc[dt-Max_Count:dt-2]
                        Warm_Spell['id'] = [id_count] * len(Warm_Spell)
                        Warm_Spell_List.append(Warm_Spell)
                        Max_Count = 0
                    else:
                        Max_Count=0
                else:
                    #This will continue the hot period until break_days > 1
                    Max_Count = Max_Count + 1
            
        else:
            #This is where the Max_Count_Prior to a heatwave is and the break days goes to 0
            #No information is added into here and Min isnt checked as the main core point of the warm spell is the Max
            #being 3 days in a row.
            break_days = 0
            if (Data[Data_col[3]][dt] >= 0):
                Max_Count = Max_Count + 1
            else:
                Max_Count = 0
        #print('Max count {}'.format(Max_Count))
        #print('heatdays {}'.format(heat_days))
        #print('id {}'.format(id_count))
        #print('break {}'.format(  break_days))
        
    #Fix it up
        
    warm_spell_df = pd.concat(Warm_Spell_List,axis=0)
    warm_spell_M_O_df = pd.concat(Warm_Spell_Max_Only_List,axis=0)
    return(warm_spell_df,warm_spell_M_O_df)
        
        
    
    


# In[ ]:


def Heatwave_Function(Data):
    '''
    Parameters
    ----------
    Data : DataFrame
        The warm and heatwaves DataFrame
        date / Max / Min / Excess Heat FactorMax/Heat StressMax/Excess HeatMax/Excess Heat FactorMin/Heat StressMin/Excess HeatMin/id
        col 0 col 1 col 2  col 3                  col 4          col 5           col 6                   col 7        col 8         col 9
    
    Returns
    ----------
    Heatwaves : DataFrames
        The warm and heatwaves DataFrame is then reduced to Nov to Mar aka the Extended Summer Season for heatwave research.
    '''
    #Extract Columns
    Data_Col = Data.columns  
    
    #Get dates into days months and years
    Hot_Per = Date_Splitter(Data)
    #it will come out with, month year and day
    
    #This finds the heatwaves that reside in the extended summer period defined by Novmeber to March
    ext_sum_heatwave = Hot_Per[Hot_Per['month']>=11]
    ext_sum_heatwave2 =  Hot_Per[Hot_Per['month']<=3]
    
    Extended_Summer_Season = pd.concat([ext_sum_heatwave,ext_sum_heatwave2]).sort_values(by=[Data_Col[0]], ascending=True)
    
    
    
    
    
    #Generate a list of ids that will be used and checked to see if they are on the bounds of Nov and March
    #as these are o as the bounds cut off heatwaves that begin or end of Nov and Mar respectively
    id_Max = Extended_Summer_Season['id'] 
    ids = id_Max.drop_duplicates( keep='first', inplace=False)

    
    
    '''The checker for the left and right bounds'''
    for i in ids:
        #Checks November-1
        CheckL = Extended_Summer_Season[Extended_Summer_Season['id']==i]
        LeftCheck = CheckL[CheckL['day']==1]
        LeftCheck = LeftCheck[LeftCheck['month']==11]
        #Checks March-31
        CheckR = Extended_Summer_Season[Extended_Summer_Season['id']==i]
        RightCheck = CheckR[CheckR['day']==31]
        RightCheck = RightCheck[RightCheck['month']==3]
        
      
        #If there is a value on the ends here it add it to the heatwave list
        if (len(LeftCheck) == 1):
            
            Extended_Summer_Season = pd.concat([Extended_Summer_Season,Hot_Per[Hot_Per[Data_Col[9]]==i]]).sort_values(by=[Data_Col[0]], ascending=True)   
    
        elif (len(RightCheck) == 1):
            Extended_Summer_Season = pd.concat([Extended_Summer_Season,Hot_Per[Hot_Per[Data_Col[9]]==i]]).sort_values(by=[Data_Col[0]], ascending=True)
        
    # removes the duplicates if there were heatwaves on any of the bounds
    Extended_Summer_Season= Extended_Summer_Season.drop_duplicates(subset = [Data_Col[0]],keep='first')
    #Clean up  dataset    
    Extended_Summer_Season = Extended_Summer_Season.drop(['day','month','year'],axis=1)
    
    #fix the id's
    #New id
    Heatwaves = []
    id_n = 0
    for i in ids:
        id_n = id_n+1
        Event = Extended_Summer_Season[Extended_Summer_Season['id']==i]
        Event['id'] = [id_n] * len(Event)
        Heatwaves.append(Event)
    Heatwaves = pd.concat(Heatwaves,axis=0)
        
    return(Heatwaves)


# In[ ]:


def Heatwave_Table_Generator(data):
    '''
    Parameters
    ----------
    Data : DataFrame
        The Heatwave dataframe

    Returns
    ----------
    Heatwaves : DataFrames
        An extension and clean up of the Heatwaves dataframe that provides more insight to the heatwaves.
    
    '''
    # Add a new column called "ave" that calculates the average of the "Max" and "Min" columnsHeatwavesI
    Heatwaves =data
    #Get columns 
    
    HW_Col = Heatwaves.columns
    
    
    Heatwaves['Avg'] = (Heatwaves[HW_Col[1]] + Heatwaves[HW_Col[2]]) / 2

    # Group the DataFrame by the "id" column and calculate the difference between the first and last dates of each group
    duration = Heatwaves.groupby('id')['date'].agg([min, max]).reset_index()
    print(duration)
    duration['Duration'] = (pd.to_datetime(duration['max']) - pd.to_datetime(duration['min'])).dt.days + 1

    # Merge the "Duration" column back into the original DataFrame
    Heatwaves = pd.merge(Heatwaves, duration[['id', 'Duration']], on='id')

    # Calculate the mean "Max", "Min", and "ave" values for each event
    mean_values = Heatwaves.groupby('id')[[HW_Col[1], HW_Col[2], 'Avg']].mean().reset_index()

    # Rename the columns to include "Mean" in the column names
    mean_values = mean_values.rename(columns={HW_Col[1]: 'Max Mean', HW_Col[2]: 'Min Mean', 'Avg': 'Avg Mean'})

    # Merge the "Mean" columns back into the original DataFrame
    Heatwaves = pd.merge(Heatwaves, mean_values, on='id')

    # Add a column for the total excess heat factor
    Heatwaves['Total Excess Heat Factor'] = Heatwaves['Excess Heat FactorMax'] + Heatwaves['Excess Heat FactorMin']


    # Define a function to calculate the intensity for a given heatwave event ID
    def calculate_intensity(event_id):
        event_data = Heatwaves[Heatwaves['id'] == event_id]
        top_3_factors = event_data['Total Excess Heat Factor'].nlargest(3)
        intensity = top_3_factors.mean()
        return intensity

    # Calculate the intensity for each heatwave event and add it to the Heatwaves DataFrame
    Heatwaves['Intensity'] = Heatwaves['id'].apply(calculate_intensity)


    # Round the columns to two decimal places
    Heatwaves['Intensity'] = Heatwaves['Intensity'].round(2)
    Heatwaves['Max Mean'] = Heatwaves['Max Mean'].round(2)
    Heatwaves['Min Mean'] = Heatwaves['Min Mean'].round(2)
    Heatwaves['Avg Mean'] = Heatwaves['Avg Mean'].round(2)
    Heatwaves['Excess Heat FactorMax'] = Heatwaves['Excess Heat FactorMax'].round(2)
    Heatwaves['Excess Heat FactorMin'] = Heatwaves['Excess Heat FactorMin'].round(2)
    Heatwaves['Heat StressMax'] = Heatwaves['Heat StressMax'].round(2)
    Heatwaves['Heat StressMin'] = Heatwaves['Heat StressMin'].round(2)
    Heatwaves['Excess HeatMax'] = Heatwaves['Excess HeatMax'].round(2)
    Heatwaves['Excess HeatMin'] = Heatwaves['Excess HeatMin'].round(2)
    Heatwaves['Total Excess Heat Factor'] = Heatwaves['Total Excess Heat Factor'].round(2)
    Heatwaves['Avg'] = Heatwaves['Avg'].round(2)
    
    
    
    Heatwaves_Data = Heatwaves.copy()

    # create a function to assign the RHC category
    def assign_rhc_category(intensity, duration):
        if intensity < 10 and duration <= 4:
            return 'RHC Cat 1'
        elif intensity < 10 and duration > 4:
            return 'RHC Cat 2'
        elif intensity >= 10 and intensity < 20 and duration <= 4:
            return 'RHC Cat 2'
        elif intensity >= 10 and intensity < 20 and duration > 4:
            return 'RHC Cat 3'
        elif intensity >= 20 and intensity < 30 and duration <= 4:
            return 'RHC Cat 3'
        elif intensity >= 20 and intensity < 30 and duration > 4:
            return 'RHC Cat 4'
        elif intensity >= 30 and intensity < 40 and duration <= 4:
            return 'RHC Cat 4'
        elif intensity >= 30 and intensity < 40 and duration > 4:
            return 'RHC Cat 5'
        elif intensity >= 40 and intensity <= 50 and duration <= 4:
            return 'RHC Cat 5'
        elif intensity >= 40 and intensity <= 50 and duration > 4:
            return 'RHC Cat 6'
        elif intensity > 50 and duration <= 4:
            return 'RHC Cat 6'
        elif intensity > 40 and intensity <= 50 and duration > 4:
            return 'RHC Cat 6'
        else:
            return 'RHC Cat 7'

    # add the RHC column to the dataframe
    Heatwaves['Rowe Heatwave Categorisation'] = Heatwaves.apply(lambda x: assign_rhc_category(x['Intensity'], x['Duration']), axis=1)
    Heatwaves['Intensity'] = Heatwaves['Intensity'].astype(str) + ' \u00b0C' + '\xb2'  # Concatenate the string "degC^2"
    Heatwaves['Max Mean'] = Heatwaves['Max Mean'].astype(str) + ' \u00b0C'   # Concatenate the string "degC"
    Heatwaves['Min Mean'] = Heatwaves['Min Mean'].astype(str) + ' \u00b0C'   # Concatenate the string "degC"
    Heatwaves['Avg Mean'] = Heatwaves['Avg Mean'].astype(str) + ' \u00b0C'   # Concatenate the string "degC"
    Heatwaves['Excess Heat FactorMax'] = Heatwaves['Excess Heat FactorMax'].astype(str) + ' \u00b0C' + '\xb2'    # Concatenate the string "degC"
    Heatwaves['Excess Heat FactorMin'] = Heatwaves['Excess Heat FactorMin'].astype(str) + ' \u00b0C' + '\xb2'    # Concatenate the string "degC"
    Heatwaves['Heat StressMax'] = Heatwaves['Heat StressMax'].astype(str) + ' \u00b0C'
    Heatwaves['Heat StressMin'] = Heatwaves['Heat StressMin'].astype(str) + ' \u00b0C'
    Heatwaves['Excess HeatMax'] = Heatwaves['Excess HeatMax'].astype(str) + ' \u00b0C'
    Heatwaves['Excess HeatMin'] = Heatwaves['Excess HeatMin'].astype(str) + ' \u00b0C'
    Heatwaves['Total Excess Heat Factor'] = Heatwaves['Total Excess Heat Factor'].astype(str) + ' \u00b0C'
    Heatwaves[HW_Col[1]] = Heatwaves[HW_Col[1]].astype(str) + ' \u00b0C'   # Concatenate the string "degC"
    Heatwaves[HW_Col[2]] = Heatwaves[HW_Col[2]].astype(str) + ' \u00b0C'   # Concatenate the string "degC"
    Heatwaves['Avg'] = Heatwaves['Avg'].astype(str) + ' \u00b0C'   # Concatenate the string "degC"
    Heatwaves['Duration'] = Heatwaves['Duration'].astype(str) + ' days'# Concatenate the string "degC"

    # Rearrange columns in the Heatwaves dataframe
    Heatwaves = Heatwaves.reindex(columns=['date', 'id', 'Rowe Heatwave Categorisation',HW_Col[1], HW_Col[2], 'Avg', 'Duration', 'Intensity', 'Max Mean', 'Min Mean', 'Avg Mean', 'Excess Heat FactorMax', 'Heat StressMax', 'Excess HeatMax', 'Excess Heat FactorMin', 'Heat StressMin', 'Excess HeatMin', 'Total Excess Heat Factor'])
    # Define a list of colors to use
    colors = ['white', 'gray']

    # Create a dictionary to map each id to a color
    id_color_map = {}
    for i, id in enumerate(Heatwaves['id'].unique()):
        id_color_map[id] = colors[i % len(colors)]

    # Define a function to apply the color to each row based on the id
    def apply_color(row):
        color = id_color_map.get(row['id'])
        return ['background-color: {}'.format(color)] * len(row)

    # Apply the color to the dataframe
    Heatwaves = Heatwaves.style.apply(apply_color, axis=1, subset=Heatwaves.columns)
    return(Heatwaves,Heatwaves_Data)


# 

# ## QUANTILE QUNATILE REGRESSION

# In[ ]:


def Simple_QQ_Regression(Q_step, Historical, Present, Hist_Dates, Pres_Date):
    '''
    Q_step: Value
    Must be non negative and at least less the 0.1
    
    Historical: DataFrame
    Must have the date as the index
    
    Present: DataFrame
    Must have the date as the index
    
    Hist_Dates/Pres_Dates: Vector
    String of the dates in Y-M-D or the format that is given with the dataframes
    
    '''
    
    number = Q_step
    Historical_All = Historical
    Present = Present
    Hist_QQ_Dates_St = Hist_Dates[0]
    Hist_QQ_Dates_En = Hist_Dates[1]

    Pres_QQ_Date_St = Pres_Date[0]
    Pres_QQ_Date_En = Pres_Date[1]
    #^ call in using function





    Historical_30 = Historical_All.loc[Hist_QQ_Dates_St:Hist_QQ_Dates_En].reset_index()
    Present_30 = Present.loc[Pres_QQ_Date_St:Pres_QQ_Date_En].reset_index()



    #Select a nparange value lemgth that goes from Q0 to Q1, and produce the quantiles
    QPRE = Present_30.quantile(np.arange(0,1+number,number)).round(4)
    QPRE = QPRE.rename_axis('Quantile').reset_index()

    QHIS = Historical_30.quantile(np.arange(0,1+number,number)).round(4)
    QHIS = QHIS.rename_axis('Quantile').reset_index()


    Hist_All = Historical_All.reset_index()
    #This above is the full range of historical data

    #What we will do is append it to max and min values before combiniing with dat
    Hist_Updated_Max = []
    Hist_Updated_Min = []
    Hist_Updated_Date = []




    #For loop for all dates 
    for i in range(0,len(Hist_All)):
        Hist_Updated_Date.append(Hist_All['date'].loc[i])


        #Now get all the information from the Q-Q data for max and min for each date
        #MAX

        #If data shows a nan value set the updated value to nan
        if (math.isnan(Hist_All['tmax'].loc[i])== True):
            Hist_Updated_Max.append(np.NaN)
        else:
            #Set Temp old 
            Temp_Old = Hist_All['tmax'].loc[i]



            #So now we get the closest value for the max:
            Column = ['tmax']

            #This finds the value where the Q-Hist of the tmax is the minimum it can be for the tmax value presented
            Min_val = np.abs(QHIS[Column] - Temp_Old).min()

            #This finds the quantile*10^5 or by the decimla place you use to find the tmax
            closest_index =  QHIS[np.abs(QHIS[Column]- Temp_Old) == Min_val].stack().idxmin()

            #Now this will use the index to find the Present Vlaue to updayte the historical value to using the index/quantile*10^%
            Hist_Updated_Max.append(QPRE[Column].loc[closest_index[0]].values[0])

        #Now get all the information from the Q-Q data for max and min for each date
        #MIN

        #If data shows a nan value set the updated value to nan
        if (math.isnan(Hist_All['tmin'].loc[i])== True):
            Hist_Updated_Min.append(np.NaN)
        else:
            #Set Temp old 
            Temp_Old = Hist_All['tmin'].loc[i]


            #So now we get the closest value for the max:
            Column = ['tmin']

            #This finds the value where the Q-Hist of the tmax is the minimum it can be for the tmax value presented
            Min_val = np.abs(QHIS[Column] - Temp_Old).min()

            #This finds the quantile*10^5 or by the decimla place you use to find the tmax
            closest_index =  QHIS[np.abs(QHIS[Column]- Temp_Old) == Min_val].stack().idxmin()

            #Now this will use the index to find the Present Vlaue to updayte the historical value to using the index/quantile*10^%
            Hist_Updated_Min.append(QPRE[Column].loc[closest_index[0]].values[0])
    Hist_Updated_Date = pd.DataFrame(Hist_Updated_Date, columns=['date'])
    Hist_Updated_Max = pd.DataFrame(Hist_Updated_Max, columns=['tmax'])
    Hist_Updated_Min = pd.DataFrame(Hist_Updated_Min, columns=['tmin'])


    #Now combine altogether
    Hist_Updated = pd.concat([Hist_Updated_Date, Hist_Updated_Max, Hist_Updated_Min], axis = 1)
    return(Hist_Updated)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:



        


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




