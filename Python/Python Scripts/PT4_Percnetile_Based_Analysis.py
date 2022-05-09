'''
The percentile based stuff
'''
#%% PACKAGES
import pandas as pd, numpy as np,matplotlib.pyplot as plt


#%% Load Data only using max Temperature for the initial start
MaxT_Perth_Data = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\tmax.009021.daily.csv")
MaxT_Perth = MaxT_Perth_Data.copy()
MaxT_Perth = MaxT_Perth.drop(0)

#%% Apply datetime
MaxT_Perth['date'] = pd.to_datetime(MaxT_Perth['date'],format="%d/%m/%Y")

#%% Apply groupby functiom
MaxT_Perth['year']=MaxT_Perth['date'].dt.year
MaxT_Perth['month']=MaxT_Perth['date'].dt.month
MaxT_Perth['day']=MaxT_Perth['date'].dt.day

group_days = MaxT_Perth.groupby(['month','day'])
GG = []
for groups,days in group_days:
    GGpre = group_days.get_group(groups).reset_index()
    GG.append(GGpre['maximum temperature (degC)'])

#%% Now do the concatenation

for central_day in range(366):
    #Make the forward and backward time from day
    D_F_B = 3
    #Define a changing 3D vector.
    Days_Block_{central_day}.format(central_day)= []    
    #Now we make the for loop with the central day and the days around it to append to the central day and get this tn90.
    for around_days in range(0,D_F_B+1):
        #First make the 0 if statement
        if (around_days == 0):
          days = central_day
          Days_Block.append(GG[central_day])
        else:
            #Now to create the check to add the 365 to 0 and 1 etc.
            #If hceck backwards
            back = around_days
            forward = around_days
            if ((central_day - back) < 0):
                day_large =  366 - back
                Days_Block.append(GG[day_large])
            
            if ((central_day + forward) > 365):
                #Now to create the check to minus the 365 to 0 and 1 etc.
                day_small =  -1 + around_days
                Days_Block.append(GG[day_small])
        
            Days_Block.append(GG[central_day - around_days])
            Days_Block.append(GG[central_day + around_days])
    print(Days_Block)
    

