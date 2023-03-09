#%%
def Date_Splitter(Data,date_title,single=True):
    '''
    

    Parameters
    ----------
    Data : Dataframe
        Where the temperature comes from
    date_title : String
        Within the dataset what did you use at the column name for the date (needs to be in datetime.)

    Returns
    -------
    dataframe that has 3 new columns for Year Month and Day

    '''
    Data['year'] =Data[date_title].dt.year
    Data['month']=Data[date_title].dt.month
    Data['day']  =Data[date_title].dt.day
    return(Data)





#%% THE HEATWAVE FUNCTION
def Heatwave_Function_Perth_Specific(Dataset,
                            date_name,
                            Time_In_Focus, 
                            CDP_Time_In_Focus,
                            Temperature_Record_Title,
                            percentile,
                            window,
                            Dates):
    '''
    This is the heatwave function that is specific to Perth, it will find the 3 days and 2 nights that is required for a
    heatwave to begin in Australia and in this research for Perth, and like Nairn et al. has done, made a requirement, that 
    creates a heatwave that are long periods of abnormally hot temperatures.
    
    Dataset: 'csv file'
        Make sure the index starts off with dates on the right and index going from [0:x]
        Max, Min must be part of the record
        
        
    date_name: 'date' csv file.
        Date Name so we can split it into day month and year, important for the CDP function to work.
    
    Time_In_Focus: [Start,End]
        Years to be excluded from the data-1910 and 2021 as these are incomplete, but you can add any period you want
        as long as you have filled that gaps with NaNs
        
    CDP_Time_In_Focus: [Start,End]
        The reference period for how heatwaves are observed. For example a Heatwave in the futur
        
    Temperature_Record_Title: ['Max','Min'] or any variation of your maximum or minimum column titles
        Name of COlumn that is to be used to extract the temperatures defined by Is_Max_T, this will be required
        
    percentile: 0 -> 100
        The higher the value, the less likely it is for a value that may occur today to be above that percentile value.
        90% percentile is the lower value of the values that are within the highest 10% of all values.
        
    window: 0 -> x days 
        Used for the CDP, which is the window that is incorporated each day that will be used with the percentile, the longer
        the window is the less likely the seasonal variations will affect the temperature changes therefore finidng
        the right window is ideal. Best one we have would be between 5-9 days. So 5 to 9 days either side of the day in
        focus when using a percentile over the stated time in focus reference period.
        
    Dates: csv file
        Used in the CDP file
    '''
    #Import Packages
    import pandas as pd
    
    #Clean up data and make sure the format is correct
    # Apply datetime to the dataset    
    Dataset[date_name] = pd.to_datetime(Dataset[date_name],format="%Y/%m/%d")
    #Had to use 2 versions for the CDP and for the rest of the functions
    Data_not_expand = Dataset
    Dataset = Date_Splitter(Dataset, date_name)
    
 
   

    '''Start and end Years for the values to use
    Start Year will be Nov - 1911 to Mar - 1942
    I will classify a year heatwave as the 1911 season as Nov-1911 to Mar-1912

    Years to be excluded from the data:
    1910 and 2021 as these are incomplete

    In the 1880-1900
    This will be a different
    '''

    '''For the Excess Heat Significant Need to Use the CDP function defined beforehand'''
    CDP_Max = Calendar_Day_Percentile(Dataset,
                                      percentile,
                                      window,Dates,
                                      Temperature_Record_Title[0],
                                      CDP_Time_In_Focus[0],
                                      CDP_Time_In_Focus[1],
                                      'Temp Max')
    CDP_Min = Calendar_Day_Percentile(Dataset,
                                      percentile,
                                      window,Dates,
                                      Temperature_Record_Title[1],
                                      CDP_Time_In_Focus[0],
                                      CDP_Time_In_Focus[1],
                                      'Temp Min')
                                                                 
    CDP = pd.concat([CDP_Max[date_name],CDP_Max['Temp Max'],CDP_Min['Temp Min']],axis=1) #Change the name



    '''Now to put all the heatwave values together to get the 3 Max 2 Min heatwave definition'''
    Heatwave_Max, EHF_Max = Perth_Heatwaves_Max(       Data_not_expand,
                                                       date_name,Time_In_Focus[0] ,
                                                       Time_In_Focus[1] ,
                                                       Temperature_Record_Title[0],
                                                       CDP_Max,
                                                       'Temp Max')
   
    #Dont think we need this minimum, you will see why all we need is the EHF_Min
    EHF_Min = Perth_Min_EHF(Data_not_expand,
                            date_name,
                            Time_In_Focus[0] ,
                            Time_In_Focus[1] ,
                            Temperature_Record_Title[1],
                            CDP_Min,
                            'Temp Min')
    
    #Now apply the 3 day 2 night definition and there is a break already indrudcied
    
    '''Currenlty Fixing'''
    Heatwave_Full_Dataset= Proper_Heatwaves_Perth_v2(Dataset,  Heatwave_Max,  EHF_Min,  date_name)
    
    #Now get all the charasteristics of all the heatwaves
    Perths_Heatwaves  = Heatwave_Table_Generator(Heatwave_Full_Dataset,EHF_Max,EHF_Min,CDP,percentile)
    
    
    return(Perths_Heatwaves, CDP_Max, EHF_Max, EHF_Min )

    #So 2 days only are occurring and I believe it is to do with the break 
    #in the heatwave function, it is only occruing to the onset so i 
    #believe there is some way i need to mainuplate the break function 
    #value so it pulls it out.
    
#%%
def TnX_Rolling(Before_After_Calendar_Day,Dataset,Percentile_Value):
    '''
    Before_After_Calendar_Day:
    
    Dataset:
    
    Percentile_Value:

    Returns
    -------
    None.

    '''
    
    
    percent_to_quant = Percentile_Value/100
    import numpy as np, warnings
    

    #Generate empty vector to place the final data in
    YearTempData = []
    warnings.filterwarnings('ignore')
    #Number of days that will contribute to the PARTICULAR calendar day in mind.
    D_F_B = Before_After_Calendar_Day
    
    #for loop for the year long record extracting each calendar day and its surroundings
    for central_day in range(366):
        
        #Now we make the for loop with the central day and the days around it to append to the central da
        for around_days in range(0,D_F_B+1):
            #First make the 0 if statement
            if (around_days == 0):
              Temp = Dataset[central_day];
              Temp_Storage =  Dataset[central_day]
            else:
                #Now to create the check so if its at day 366 and the next day should be day 1 and vice versa when going backwards.
                
                #if statement for if the around_days goes below the lower bound.
                if ((central_day - around_days) < 0):
                    day_large =  366 - around_days;
                    TempU= Dataset[day_large];
                    Temp_Storage = Temp_Storage.append(TempU)
                    TempL=Dataset[central_day + around_days];
                    Temp_Storage = Temp_Storage.append(TempL)
                    
                #if statement for if the around_days goes above the upper bound.
                elif (central_day + around_days) > 365:
                    day_small = -1 + around_days;
                    TempL=Dataset[day_small];
                    Temp_Storage = Temp_Storage.append(TempL)
                    TempU=Dataset[central_day - around_days];
                    Temp_Storage = Temp_Storage.append(TempU)
                #if statement for if the around_days is between the bounds. 
                else:
                    Temp=Dataset[central_day - around_days];
                    Temp_Storage = Temp_Storage.append(Temp)
                    Temp=Dataset[central_day + around_days];
                    Temp_Storage = Temp_Storage.append(Temp)
        #Append the data for that calendar and move to the next calendar day.  
        YearTempData.append(Temp_Storage)
        
        
        #Percentile based information
    
    TnX = []
    #Create a for loop that uses the YearTempData and find the percentile for that calendar based value.
    for i in range(366):
        Tn = YearTempData[i].quantile(q=percent_to_quant) #Have a llok properly and code it myslef and pull out ranks and find 90th percetile
        TnX = np.append(TnX,Tn)
    
    return(TnX) 

#%%
def Calendar_Day_Percentile(Data,percentile,window,Dates,Column_Name,start_year,end_year,temp):
    import pandas as pd
    Data = Data[Data['year'] <= end_year]
    Data = Data[Data['year'] >= start_year-1]
    group_days = Data.groupby(['month','day'])
    Daily_Data= []
    for groups,days in group_days:
        #Extract the specified day bin
        Dailypre = group_days.get_group(groups).reset_index()
        #Get the maximum values for the entire record for that calendar day
        Values= Dailypre[Column_Name]
        #Make it a dataframe so it is appendable
        Values = Values.to_frame()
        #Append that bin to that day so there will be 366 bins with  x years data for that day
        Daily_Data.append(Values[Column_Name])
            
    #Now use CDP 15 day  for the max
    CalendarDay = TnX_Rolling(window, Daily_Data, percentile)
    CDP = pd.DataFrame(CalendarDay, columns = [temp])
    CDP = pd.concat([Dates,CDP],axis=1)
    CDP['date'] = pd.to_datetime(CDP['date'],format="%d/%m/%Y")
    CDP['year']=CDP['date'].dt.year
    CDP['month']=CDP['date'].dt.month
    CDP['day']=CDP['date'].dt.day
    del CDP['year']
    del CDP['day']
    del CDP['month']
    
    
    return(CDP)

#%%
def Perth_Heatwaves_Max(Data,date_title,Start_Year ,End_Year ,Column_Name,CDP,CDPColumn_Name):
    '''    
    Data: Dataframe
    Dataset we will be using.
    
    date_title: string
    the title of the date column.
    
    Start_Year: integer
    
    End_Year: integer
    
    Both start and end_Year will be within the bounds of the first full year and last full year.
    
    Example will be Start Year will be Nov - 1911 to Mar - 1942
    I will classify a year heatwave as the 1911 season as Nov-1911 to Mar-1912

    

    
    Column_Name = string
    Name of COlumn that is to be used to extract the temperatures defined by Is_Max_T

    
    CDP: dataframe
    For the Excess Heat Significant Need to Use the CDP function defined beforehand
    CDPColumn_Name = string
    Column of the CDP temperature used 
    '''
    
    
    
    
    '''
    This is to determine the initiation of the heatwave for the Max and Min temperatures.

    The basic theory is that the beginning of a heatwave for Australia and Perth should be:
        3 days Max Temp of above average temps
        2 days Min Temp of above average temps
    '''
    Q_Threshold = 3


    '''
    Now with the Dataset we can define the 33 days. To make it easier get the previous 33 days before Nov for the start period.
    '''
    Data = Data.set_index([date_title])
    CDP =  CDP.set_index([date_title])
    Day_S = 29
    Month_S = 9
    Year_S = Start_Year

    Day_E = 30
    Month_E = 4
    Year_E = End_Year+1

    Data_Range = Data.loc['{}-{}-{}'.format(Year_S,Month_S,Day_S):'{}-{}-{}'.format(Year_E,Month_E,Day_E)]




    '''
    Now developing the first part of the function which will be its own function, the Excess Heat Factor.

    Ive realeased that I can save tiem and remove the EHI positive and EHFp as the EHIacc, EHIsig are only needed in the rest of the function.
    I will have EHF avalaible to be used though.

    In order for this to work properly we will have to reset index.
    '''
    Data_Range = Data_Range.reset_index()
    '''This is an index range of 0 to length-1'''

    ''' This is the Excess Heat Factor Function, developed by Nairn 2009'''
    #Heatwaves events using a lag for heat-related health issues.
    #EHF = Excess_Heat_Factor_Function(Data_Range,date_title,Column_Name,CDP,CDPColumn_Name)
    #Heatwave events full
    EHF = Excess_Heat_Factor_Function_v3(Data_Range,date_title,Column_Name,CDP,CDPColumn_Name)

    '''These are the hot periods which is not heatwaves but these are the hotter then average periods developed
    by the EHF.
    '''
    Hot_Periods = hot_period_Classification(EHF,Q_Threshold)

    '''To concude my wonderful function for heatwaves in perth this is the final output'''
    Heatwaves_Max= Heatwaves_Defined(Hot_Periods,date_title)


    return(Heatwaves_Max, EHF)
#%%
def Excess_Heat_Factor_Function_v3(Data,date_title,Column_Name,CDP,CDPColumn_Name):
    '''

    Parameters
    ----------
    Data : True or False
        It is already caterogised as False therefore to use it for Maximum Temperatures need to say True.

    Returns
    -------
    The threshold in order to be a heatwave. Of heatwave events, not heatwaves that cause humans discomfort

    '''
    import numpy as np ,pandas as pd
    #I want to see whether this has better accuracy for heatwaves???
    
    
    Date_Value = [] #To match the EHF values to the date.
    EHF = [] #Excess Heat Factor
    EHIacc = [] #Excess Heat Index Acclimatised (Previous 32 days)
    EHIsig = [] #Excess Heat Index Singificant (CDP value)

    for dt in np.arange(Data.index[0]+33,len(Data)):
        #----- Date Index -----#
        Dates = Data[date_title].loc[dt]
        #print(Dates)
        #----- 3 day Mean -----#
        mean_3_day = Data[Column_Name].loc[dt-2:dt].mean()
        #print(mean_3_day)
        # ----- 3 to 32 day mean ----#
        mean_1_tp_30_day = Data[Column_Name].loc[dt-32:dt-3].mean()
        #print(mean_3_tp_32_day)
        #----EHI(accl.)----#
        EHIacclim_single =  mean_3_day - mean_1_tp_30_day
        #print(EHIacclim_single)
        #----Tn CDP function----#
        '''For that indivudal date we use the Date_Splitter to get the day and month out so we can find the CDP value'''
        CDP_day = CDP[CDPColumn_Name].loc['2020-{}-{}'.format(Data['month'].loc[dt],Data['day'].loc[dt])]
        
        #------ EHI(sig.) ------#
        EHIsig_single =  Data[Column_Name].loc[dt] -  CDP_day
        
        #----- EHF-----#
        '''Now using the combination of the two EHI sig and acc we can now produce the EHF, sp this means if negative, it
        is alwasy negative when multiplying them together'''
        if ((EHIacclim_single <0) and (EHIsig_single <0)):
            EHF_single =  -1*EHIacclim_single* EHIsig_single #degC^2
        else:
            EHF_single =  EHIacclim_single* EHIsig_single #degC^2
        
        
        '''Now with all the necassary information needed we can append it all together'''
        Date_Value.append(Dates)
        EHIacc.append(EHIacclim_single)
        EHIsig.append(EHIsig_single)
        EHF.append(EHF_single)
        #print(EHIacc)
    '''Putting all the vectors together'''
    EHF = pd.DataFrame(EHF,columns=['Excess Heat Factor'])
    EHIacc = pd.DataFrame(EHIacc,columns=['Excess Heat Index Acclimatised'])
    EHIsig = pd.DataFrame(EHIsig,columns=['Excess Heat Index Significant'])
    Date_Value = pd.DataFrame(Date_Value,columns=[date_title])
   

    EHFvect = pd.concat([Date_Value, EHIacc, EHIsig, EHF],axis=1)
    Excess_Heat_Factor_Matrix = pd.merge(Data,EHFvect,how='right',on = [date_title])
    
    return(Excess_Heat_Factor_Matrix)

#%%
#%%
def hot_period_Classification(EHF,Q):
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
    
    
    import numpy as np ,pandas as pd
    '''Lets create a few lists essential for the hot periods and count functions'''
    list_hot_period = []
    heat_days = 0
    count  = 0
    break_days = 2 #Since the first day cannot be a heatwave if it was 0 it would automatically create a heatwave
    
    '''The first for loop is essentially checking to see if the day in focus is classified as a hot period day, and the 
    onset is for 3 or more days. I am not sure if I can cut this down'''
    #This is the full period with the assciated EHI and EHF values
    for dt in np.arange(EHF.index[0],len(EHF)):
        '''
        Now define the algorithm which for anything greater then 2 or 3 days is classified as a hot period.
        See thesis into how it works.
        '''
        '''Check If heat_days count is already => 3'''
        if (heat_days >= Q):
            '''Since this if statement is true then we develop the contiuation of the hot period event'''
            if(EHF['Excess Heat Index Significant'][dt] > 0):
                #As long as EHIsig > 0 then there is a prolonged heatwave
                heat_days = heat_days + 1
                break_days = 0 
            #Define the ending of the hot period, without the break at the moment
            else:
                break_days = break_days + 1
                #Now this is the interesting point, we can implement a break in the system
                if(break_days > 1):
                        #This will stop the hot period event and add an id on the event with a count function.
                        count = count+1
                        hot_period = EHF.loc[dt-heat_days:dt-2]
                        hot_period['id'] = [count] * len(hot_period)
                        list_hot_period.append(hot_period)
                        heat_days=0
                else:
                        #This will continue the hot period until break_days > 1
                        heat_days = heat_days + 1
                        
                
            
        #Define everything for the initiation of the hot period
        
        else:
            '''
            Now this is the criteria for the start of a hot period event, 3 max or 2 min.
            '''
            break_days = 0
            #Define everything for the initiation of the hot period
            if((EHF['Excess Heat Index Acclimatised'][dt]> 0) and (EHF['Excess Heat Index Significant'][dt] > 0)):
                heat_days = heat_days + 1
            else:
                heat_days  = 0

    hot_period_df = pd.concat(list_hot_period,axis=0)
    return(hot_period_df)

#%%
def Heatwaves_Defined(Hot_Periods,date_title):
    import pandas as pd
    
    #Get dates into days months and years
    Hot_Per = Date_Splitter(Hot_Periods, date_title)

    '''This finds the heatwaves that reside in the extended summer period defined by Novmeber to March'''
    ext_sum_heatwave = (Hot_Periods.loc[Hot_Periods['month']>=11])
    ext_sum_heatwave2 =  Hot_Periods.loc[Hot_Periods['month']<=3]
    Extended_Summer_Season = pd.concat([ext_sum_heatwave,ext_sum_heatwave2]).sort_values(by=[date_title], ascending=True)

    '''Generate a list of ids that will be used and checked to see if they are on the bounds of Nov and March
    as these are o as the bounds cut off heatwaves that begin or end of Nov and Mar respectively'''
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
            Extended_Summer_Season = pd.concat([Extended_Summer_Season,Hot_Per[Hot_Per['id']==i]]).sort_values(by=[date_title], ascending=True)   
            #print(1)
        elif (len(RightCheck) == 1):
            Extended_Summer_Season = pd.concat([Extended_Summer_Season,Hot_Per[Hot_Per['id']==i]]).sort_values(by=[date_title], ascending=True)
    # removes the duplicates if there were heatwaves on any of the bounds
    Extended_Summer_Season= Extended_Summer_Season.drop_duplicates(subset = [date_title],keep='first')
    Heatwaves = Extended_Summer_Season.drop(['day','month','year'],axis=1)
    return(Heatwaves)

#%%
def Perth_Min_EHF(Data,date_title,Start_Year ,End_Year ,Column_Name,CDP,CDPColumn_Name):
    '''    
    Data: Dataframe
    Dataset we will be using.
    
    date_title: string
    the title of the date column.
    
    Start_Year: integer
    
    End_Year: integer
    
    Both start and end_Year will be within the bounds of the first full year and last full year.
    
    Example will be Start Year will be Nov - 1911 to Mar - 1942
    I will classify a year heatwave as the 1911 season as Nov-1911 to Mar-1912

    

    
    Column_Name = string
    Name of COlumn that is to be used to extract the temperatures defined by Is_Max_T

    
    CDP: dataframe
    For the Excess Heat Significant Need to Use the CDP function defined beforehand
    CDPColumn_Name = string
    Column of the CDP temperature used 
    '''
    
    
    
    


    '''
    Now with the Dataset we can define the 33 days. To make it easier get the previous 33 days before Nov for the start period.
    '''
    Data = Data.set_index([date_title])
    CDP =  CDP.set_index([date_title])
    Day_S = 29
    Month_S = 9
    Year_S = Start_Year

    Day_E = 30
    Month_E = 4
    Year_E = End_Year+1

    Data_Range = Data.loc['{}-{}-{}'.format(Year_S,Month_S,Day_S):'{}-{}-{}'.format(Year_E,Month_E,Day_E)]




    '''
    Now developing the first part of the function which will be its own function, the Excess Heat Factor.

    Ive realeased that I can save tiem and remove the EHI positive and EHFp as the EHIacc, EHIsig are only needed in the rest of the function.
    I will have EHF avalaible to be used though.

    In order for this to work properly we will have to reset index.
    '''
    Data_Range = Data_Range.reset_index()
    '''This is an index range of 0 to length-1'''

    ''' This is the Excess Heat Factor Function, developed by Nairn 2009'''
    #Heatwaves events using a lag for heat-related health issues.
    #EHF = Excess_Heat_Factor_Function(Data_Range,date_title,Column_Name,CDP,CDPColumn_Name)
    #Heatwave events full
    EHF = Excess_Heat_Factor_Function_v3(Data_Range,date_title,Column_Name,CDP,CDPColumn_Name)



    return(EHF)

#%%The Heatwaves Perth
def Proper_Heatwaves_Perth_v2(Data,Heatwave_MaxT,EHF_Min,date_name):
    '''
    Data: Dataframe
        This is the daily maximum and minimum temperatures.
    
    Max_Heatwave: Dataframe
        List of all heatwaves within the maxmimum temperature.
    
    Min_EHF: Dataframe
        List of all heatwaves within the minimum temperature and its EHF value, which is vital to be checked for the 
        2 night criteria
        
    date_name: string
        Name of column that you have for heatwave
        
    Output: Full_Heatwaves
        This is the full heatwave list using the 3 max and 2 min definition of heatwaves. This only has the maximum and minimum, CDP,
        and ... may have to add more.
    '''
    #Here we import the necessary packages
    import pandas as pd
    
    #Now we import our maximum temperature only here, because the min for the 
    #two days must be YYN, YNY, NYY, therefore the min heatwace variant is actually irrelevent.
    Max = Heatwave_MaxT
    Data = Data.set_index('date')
    EHF_Min = EHF_Min.set_index('date')
    #print(EHF_Min)
    #Storing the heatwaves
    Heatwave_Event = []
    count = 1
    ids = Max['id'].drop_duplicates( keep='first', inplace=False)

    for i in ids:
       #This extracts the id from the Max_Event
       Max_Event = Max[Max['id']==i]
       #Reset Index to extract the dates for the loc function in Data 
       Max_Event = Max_Event.reset_index() 
       #Find the 1st date and the 3rd date of the heatwave event in the max
       start = Max_Event['date'][0]
       end_Check = Max_Event['date'][2]
       end = Max_Event['date'][len(Max_Event)-1]
       #Gets the Min event to see it if it within the bounds of the max event, it is actually the criteria
       #3 days and 2 nights,
       #print(start)
       #print(end_Check)
       
       Min_Check = EHF_Min.loc[start:end_Check]
       #Here should have the minimum temperature EHF which should be positive for at least 2 days.
       Min_Check = Min_Check[Min_Check['Excess Heat Factor'] >= 0 ]
       
       length = len(Min_Check)
       #print((Percent,length))
       
       #Now extract the information for the period.
       if(length >= 2):
           Temperature = Data.loc[start:end]
           Temperature['id'] = [count] * len(Temperature)
           count = count + 1
           Heatwave_Event.append(Temperature)
           
    Full_Heatwaves = pd.concat(Heatwave_Event,axis=0)
      
    return(Full_Heatwaves)

#%% Heatwave Table
'''
In order from first column to last
1. Index [1,2,3...]
2. Heatwave ID 
3. Date
4. Max
5. Min
6. Avg
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



def Heatwave_Table_Generator(Heatwave_Full_Dataset,EHF_Max,EHF_Min,CDP,percentile):
    import pandas as pd
    Heatwave_Table = Heatwave_Full_Dataset.reset_index()
    '''Begin by cleaning the dataset, Pt1 remove year, month day and reset index to 0'''
    del Heatwave_Table['year']
    del Heatwave_Table['month']
    del Heatwave_Table['day']
    
    '''Begin by cleaning the dataset, Pt1 remove year, month day and reset index to 0'''
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
        EHF_Max_iND = EHF_Max.loc[(EHF_Max['date'].dt.year==Year) & (EHF_Max['date'].dt.month==Month) &(EHF_Max['date'].dt.day==Day)]
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
    

    return(Heatwave_Table)