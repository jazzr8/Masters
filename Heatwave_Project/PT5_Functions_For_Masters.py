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
    Extended_Summer_Season = pd.concat([ext_sum_heatwave,ext_sum_heatwave2]).sort_values(by=['date'], ascending=True)
    
    #Now I need to find 1/11 shit
    id_Max = Extended_Summer_Season['id'] 
    print(id_Max)
    ids = id_Max.drop_duplicates( keep='first', inplace=False)
    print(ids)
    for i in ids:
        
        Check = Extended_Summer_Season[Extended_Summer_Season['id']==i]
        LeftCheck = Check[Check['day']==1]
        LeftCheck = LeftCheck[LeftCheck['month']==11]
        print(LeftCheck)
        RightCheck = Check[Check['day']==31]
        RightCheck = RightCheck[LeftCheck['month']==3]
        print(RightCheck)
        if (len(LeftCheck == 1)):
            Extended_Summer_Season = pd.concat([Extended_Summer_Season,heatwave_df[heatwave_df['id']==i]],replace = 'True').sort_values(by=['date'], ascending=True)   
        elif (len(RightCheck == 1)):
            Extended_Summer_Season = pd.concat([Extended_Summer_Season,heatwave_df[heatwave_df['id']==i]],replace = 'True').sort_values(by=['date'], ascending=True)
        
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