'''
FUNCTIONS
'''
def TnX_Rolling(Before_After_Calendar_Day,Dataset,Percentile_Value):
    '''
    

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



#%%:
def Extend_Summer_Heatwaves_v1(Dataset,Is_Max, Start_Year, End_Year,Column_Name_Max_Min_Ave,CDP,date_title):
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
    
    

    
    #Define the excess heat factor vectors for max_min_ave
    #first day in focus is index 32
    EHF = np.zeros(len(Data))
    EHIacc = np.zeros(len(Data))
    EHIsig = np.zeros(len(Data))
    EHIacclpositive = np.zeros(len(Data)) #To Sim  max[1,EHIacc]
    EHFp= np.zeros(len(Data)) #To sim EHIsig*max[1,EHIacc]
    
    
    
    for i in range(Data.index[0]+33,Data.index[len(Data)-1]):
    
        #-----3 day mean-----#
        D3mean = (Data[Column_Name_Max_Min_Ave][i] + Data[Column_Name_Max_Min_Ave][i-1]+Data[Column_Name_Max_Min_Ave][i-2])/3
    
        #-----i-32 to i - 3-----#
        D323SUM = 0
        for q in range(3,33):
            D323SUM = D323SUM + Data[Column_Name_Max_Min_Ave][i-q]
            
        D323mean = D323SUM/len(range(3,33))
        #-----EHI(accl)-----#
        EHIacc_single = D3mean - D323mean
        EHIacc[i] = EHIacc_single
        EHIacclpositive[i] = np.max([1,EHIacc_single])

        #-----Tn-----#
        CDPsortd = CDP[CDP['day'] == Data['day'][i]]    
        CDPsortm = CDPsortd[CDPsortd['month'] == Data['month'][i]]
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

    Heatwave_Characteristics_Onset = pd.concat([Data,EHFvect],axis=1)
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
            if (Q >= Q_Threshold):
                count = count+1
                Heatwave = Heatwave_Characteristics_Onset.loc[i-Q:i-1]
                Heatwave['id'] = [count] * len(Heatwave)
                list_heatwaves.append(Heatwave)
                Q=0
            else:
                Q=0
        
    heatwave_df = pd.concat(list_heatwaves,axis=0)
    print(heatwave_df)
    
    ext_sum_heatwave = (heatwave_df.loc[heatwave_df['month']>=11])
    ext_sum_heatwave2 =  heatwave_df.loc[heatwave_df['month']<=3]
    Extended_Summer_Season = pd.concat([ext_sum_heatwave,ext_sum_heatwave2]).sort_values(by=['date'], ascending=True)
    return(Extended_Summer_Season)

#%% Improved
def Extend_Summer_Heatwaves_v2(Dataset,Is_Max, Start_Year, End_Year,Column_Name_Max_Min_Ave,CDP,date_title):
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
    
    

    
    #Define the excess heat factor vectors for max_min_ave
    #first day in focus is index 32
    EHF = np.zeros(len(Data))
    EHIacc = np.zeros(len(Data))
    EHIsig = np.zeros(len(Data))
    EHIacclpositive = np.zeros(len(Data)) #To Sim  max[1,EHIacc]
    EHFp= np.zeros(len(Data)) #To sim EHIsig*max[1,EHIacc]
    
    
    
    for i in range(Data.index[0]+33,Data.index[len(Data)-1]):
    
        #-----3 day mean-----#
        D3mean = (Data[Column_Name_Max_Min_Ave][i] + Data[Column_Name_Max_Min_Ave][i-1]+Data[Column_Name_Max_Min_Ave][i-2])/3
    
        #-----i-32 to i - 3-----#
        D323SUM = 0
        for q in range(3,33):
            D323SUM = D323SUM + Data[Column_Name_Max_Min_Ave][i-q]
            
        D323mean = D323SUM/len(range(3,33))
        #-----EHI(accl)-----#
        EHIacc_single = D3mean - D323mean
        EHIacc[i] = EHIacc_single
        EHIacclpositive[i] = np.max([1,EHIacc_single])

        #-----Tn-----#
        CDPsortd = CDP[CDP['day'] == Data['day'][i]]    
        CDPsortm = CDPsortd[CDPsortd['month'] == Data['month'][i]]
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

    Heatwave_Characteristics_Onset = pd.concat([Data,EHFvect],axis=1)
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
    Extended_Summer_Season = pd.concat([ext_sum_heatwave,ext_sum_heatwave2]).sort_values(by=[date_title], ascending=True)
    
    #Now I need to find 1/11 shit
    id_Max = Extended_Summer_Season['id'] 
    ids = id_Max.drop_duplicates( keep='first', inplace=False)
    
    
    
    for i in ids:
        CheckL = Extended_Summer_Season[Extended_Summer_Season['id']==i]
        LeftCheck = CheckL[CheckL['day']==1]
        LeftCheck = LeftCheck[LeftCheck['month']==11]
        print(LeftCheck)
        CheckR = Extended_Summer_Season[Extended_Summer_Season['id']==i]
        RightCheck = CheckR[CheckR['day']==31]
        RightCheck = RightCheck[RightCheck['month']==3]
        print(RightCheck)
        if (len(LeftCheck) == 1):
            Extended_Summer_Season = pd.concat([Extended_Summer_Season,heatwave_df[heatwave_df['id']==i]]).sort_values(by=[date_title], ascending=True)   
            print(1)
        elif (len(RightCheck) == 1):
            Extended_Summer_Season = pd.concat([Extended_Summer_Season,heatwave_df[heatwave_df['id']==i]]).sort_values(by=[date_title], ascending=True)
    Extended_Summer_Season.drop_duplicates(subset = [date_title],keep='first')
    return(Extended_Summer_Season)



#%%
def Calendar_Day_Percentile(Data,percentile,window,Dates,Column_Name,start_year,end_year):
    import numpy as np, warnings, pandas as pd
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
    CDP = pd.DataFrame(CalendarDay, columns = ['Temp'])
    CDP = pd.concat([Dates,CDP],axis=1)
    CDP['date'] = pd.to_datetime(CDP['date'],format="%d/%m/%Y")
    CDP['year']=CDP['date'].dt.year
    CDP['month']=CDP['date'].dt.month
    CDP['day']=CDP['date'].dt.day
        
    return(CDP)



#%%
def Is_Max_Temp(Is_Max_T = False):
    '''

    Parameters
    ----------
    Is_Max_T : True or False
        It is already caterogised as False therefore to use it for Maximum Temperatures need to say True.

    Returns
    -------
    The threshold in order to be a heatwave.

    '''
    if (Is_Max_T == True):
        Q_Threshold = 3
    else:
        Q_Threshold = 2
    return(Q_Threshold)

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
    import numpy as np ,pandas as pd
    Data['year'] =Data[date_title].dt.year
    Data['month']=Data[date_title].dt.month
    Data['day']  =Data[date_title].dt.day
    return(Data)




#%%
def Excess_Heat_Factor_Function(Data,date_title,Column_Name,CDP,CDPColumn_Name):
    '''

    Parameters
    ----------
    Data : True or False
        It is already caterogised as False therefore to use it for Maximum Temperatures need to say True.

    Returns
    -------
    The threshold in order to be a heatwave.

    '''
    import numpy as np ,pandas as pd
    
    
    
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
        mean_3_tp_32_day = Data[Column_Name].loc[dt-32:dt-3].mean()
        #print(mean_3_tp_32_day)
        #----EHI(accl.)----#
        EHIacclim_single =  mean_3_day - mean_3_tp_32_day
        #print(EHIacclim_single)
        #----Tn CDP function----#
        '''For that indivudal date we use the Date_Splitter to get the day and month out so we can find the CDP value'''
        CDP_day = CDP[CDPColumn_Name].loc['2020-{}-{}'.format(Data['month'].loc[dt],Data['day'].loc[dt])]
        
        #------ EHI(sig.) ------#
        EHIsig_single =  mean_3_day -  CDP_day
        
        #----- EHF-----#
        '''Now using the combination of the two EHI sig and acc we can now produce the EHF'''
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
    print(EHF)
    print(EHIacc)
    print(EHIsig)
    print(Date_Value)
    EHFvect = pd.concat([Date_Value, EHIacc, EHIsig, EHF],axis=1)
    Excess_Heat_Factor_Matrix = pd.merge(Data,EHFvect,how='right',on = [date_title])
    
    return(Excess_Heat_Factor_Matrix)


#%%
def Heatwaves_Defined(Hot_Periods,date_title):
    import numpy as np ,pandas as pd
    
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
def hot_period_Classification_Perth(EHF,Q):
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
            #Define everything for the initiation of the hot period
            if((EHF['Excess Heat Index Acclimatised'][dt]> 0) and (EHF['Excess Heat Index Significant'][dt] > 0)):
                heat_days = heat_days + 1
            else:
                heat_days  = 0

    hot_period_df = pd.concat(list_hot_period,axis=0)
    return(hot_period_df)




#%%
def Perth_Heatwaves_Max_Or_Min(Is_Max_T,Data,date_title,Start_Year ,End_Year ,Column_Name,CDP,CDPColumn_Name):
    '''
    Is_Max_T = True or False
    this determines whether it will be 2 or 3 day for the initation of a heatwave event.
    
    
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
    Q_Threshold = Is_Max_Temp(Is_Max_T)

    '''
    Now to split the date up into sections day, month and year.
    Using loc[] so I don't think this matters anymore'
    '''
    #Data = function_M.Date_Splitter(Dataset,'date')

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

    #Data = subset(Data, date > as.Date("29-09-1911") )




    '''
    Now developing the first part of the function which will be its own function, the Excess Heat Factor.

    Ive realeased that I can save tiem and remove the EHI positive and EHFp as the EHIacc, EHIsig are only needed in the rest of the function.
    I will have EHF avalaible to be used though.

    In order for this to work properly we will have to reset index.
    '''
    Data_Range = Data_Range.reset_index()
    '''This is an index range of 0 to length-1'''

    ''' This is the Excess Heat Factor Function, developed by Nairn 2009'''
    EHF = Excess_Heat_Factor_Function(Data_Range,date_title,Column_Name,CDP,CDPColumn_Name)

    '''These are the hot periods which is not heatwaves but these are the hotter then average periods developed
    by the EHF.
    '''
    Hot_Periods = hot_period_Classification_Perth(EHF,Q_Threshold)

    '''To concude my wonderful function for heatwaves in perth this is the final output'''
    Heatwaves_Max_Or_Min = Heatwaves_Defined(Hot_Periods,date_title)


    return(Heatwaves_Max_Or_Min)





