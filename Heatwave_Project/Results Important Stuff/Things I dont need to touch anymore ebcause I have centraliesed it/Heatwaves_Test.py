#!/usr/bin/env python
# coding: utf-8

# This is the heatwave function v4, it will no incorporate a 75% data avaliable for this version in order to be usable in the historical context and where data may not be fully avaliable 
# 
# 

# 

# In[ ]:





# # 0. Import Packages

# In[31]:


#Import Packages
import pandas as pd
import numpy as np, warnings


# # Test The Function

# In[32]:


#Get the Max and Min Information
MaxT_Perth = pd.read_csv(r"E:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\tmax.009021.daily.csv").drop(0).reset_index(drop=True)
MinT_Perth = pd.read_csv(r"E:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\tmin.009021.daily.csv").drop(0).reset_index(drop=True)

#Rename the columns
Maximum = pd.Series(MaxT_Perth['maximum temperature (degC)'], name="Max")
Minimum = pd.Series(MinT_Perth['minimum temperature (degC)'],name="Min")

#Concat it all together
Daily_MaxMin = pd.concat([MaxT_Perth['date'],Maximum,Minimum],axis=1)

#Apply datetime
Daily_MaxMin['date'] = pd.to_datetime(Daily_MaxMin['date'],format="%d/%m/%Y")

#Dates 
#This is used in the concatination process when the CDP is developed and other things 
#that have the data disappear. Since the full 366 days need to be accounted for, 2020 was 
#the year I chose for this
#'''
Dates = pd.read_csv(r"E:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\Dates, includes feb 29.csv")


# In[ ]:





# In[ ]:





# # 1. The Core Function

# In[ ]:





# In[33]:


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
    #if(Heatwave_Detail == True):
    #    heatwaves = Heatwave_Table_Generator(heatwaves)

    return(heatwaves,CDP)    
    


# # 2. Date Splitter Function

# In[34]:


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


# # 3. Calendar Day Percentile Function

# In[35]:


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


# # 3.1. The TnX function

# In[36]:


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


# # 4. Excess Heat Factor Function

# In[37]:


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


# ## 4.1 Heat Stress Term

# In[38]:


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





# In[ ]:





# In[ ]:





# ## 4.2 Excess Heat Term

# In[39]:


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


# ## 4.3 Excess Heat Factor 
# 

# In[40]:


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


# # 5. Finding Warm Spells

# In[41]:


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
        
        
    
    


# # 6. Heatwave Finder Nov to Mar

# In[42]:


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


# # 7. Heatwave Table Creator Function

# In[47]:


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
    return(Heatwaves)


# In[44]:



Heatwaves,CDP = Heatwave_Function_v4(Daily_MaxMin,
                         Dates,
                         CDP_Matrix = [],
                         Heatwave_Detail= True,
                         Percentile = 85,
                         window = 7,
                         CDP_start_end_years = [1961,1990])


# In[17]:


Heatwaves


# # Save it

# In[45]:


# Save the styled dataframe to an Excel file
Heatwaves.to_excel(r'C:\Users\jarra\Desktop\Masters\styled_heatwaves.xlsx', engine='openpyxl', index=False)


# In[27]:


hw = pd.read_csv(r"E:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\unstyled_heatwaves_20CR.csv")
hw = hw.set_index('Unnamed: 0')

hw = hw.reset_index(drop = True)
(hw['tmax']+hw['tmin'])/2


# In[52]:


HEATWAVES = Heatwave_Table_Generator(Heatwaves)
HEATWAVES.to_excel(r'C:\Users\jarra\Desktop\Masters\styled_heatwaves_ACORN_SAT.xlsx', engine='openpyxl', index=False)


# In[49]:


HEATWAVES


# In[ ]:





# In[ ]:





# In[155]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




