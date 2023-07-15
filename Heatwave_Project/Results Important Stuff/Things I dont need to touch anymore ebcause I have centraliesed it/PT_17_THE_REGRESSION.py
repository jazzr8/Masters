# Creating the sub-daily and Max Relationship
import sys
sys.path.append(r"C:\Users\jarra\Desktop\Masters\Heatwave_Project")
import pandas as pd
import PT13_Functions_For_Masters_New_Test as HW_Func
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
import scipy

#Load the Sub_Daily Data In
PRO_Sub = pd.read_csv(r"E:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\perthregionaloffice_subdaily_1942-1992.csv")

PRO_Sub['date'] = pd.to_datetime(PRO_Sub['date'],dayfirst = True)

#What we notice is that the temp has the decimal in the wrong place

PRO_Sub = PRO_Sub.set_index('date')
PRO_Sub =PRO_Sub['temp']/10 
PRO_Sub
PRO_Sub_ES  = PRO_Sub.loc['1967':'1992']
PRO_Sub_ES =PRO_Sub_ES
PRO_Sub_0 = pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==0]],axis =0)
PRO_Sub_3= pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==3]],axis =0)
PRO_Sub_6= pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==6]],axis =0)
PRO_Sub_9= pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==9]],axis =0)
PRO_Sub_12= pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==12]],axis =0)
PRO_Sub_15= pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==15]],axis =0)
PRO_Sub_18= pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==18]],axis =0)
PRO_Sub_21= pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==21]],axis =0)


PRO_Sub_1 = pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==1]],axis =0)
PRO_Sub_2 = pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==2]],axis =0)
PRO_Sub_4 = pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==4]],axis =0)


PRO_Sub_5 = pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==5]],axis =0)
PRO_Sub_7 = pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==7]],axis =0)
PRO_Sub_8 = pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==8]],axis =0)


PRO_Sub_10 = pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==10]],axis =0)
PRO_Sub_11 = pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==11]],axis =0)
PRO_Sub_13 = pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==13]],axis =0)


PRO_Sub_14 = pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==14]],axis =0)
PRO_Sub_16 = pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==16]],axis =0)
PRO_Sub_17 = pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==17]],axis =0)




PRO_Sub_19 = pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==19]],axis =0)
PRO_Sub_20 = pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==20]],axis =0)
PRO_Sub_22 = pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==22]],axis =0)
PRO_Sub_23 = pd.concat([PRO_Sub_ES[PRO_Sub_ES.index.hour==23]],axis =0)


#Now lets get it into the extended Summer Record with the extra months of the 10th and 4th in because we want the prior stuff
#for early Nov and Late March

# Lets get this into extended summer and break it up into individual hours

#%%



#Reomve hours out of it for concatiation

PRO_Sub_0 = PRO_Sub_0.reset_index()

PRO_Sub_0['date'] = pd.to_datetime(PRO_Sub_0['date']).dt.date
PRO_Sub_0 = PRO_Sub_0.set_index('date')

PRO_Sub_3 = PRO_Sub_3.reset_index()
PRO_Sub_3['date'] = pd.to_datetime(PRO_Sub_3['date']).dt.date
PRO_Sub_3 = PRO_Sub_3.set_index('date')


PRO_Sub_6 = PRO_Sub_6.reset_index()
PRO_Sub_6['date'] = pd.to_datetime(PRO_Sub_6['date']).dt.date
PRO_Sub_6 = PRO_Sub_6.set_index('date')

PRO_Sub_9 = PRO_Sub_9.reset_index()
PRO_Sub_9['date'] = pd.to_datetime(PRO_Sub_9['date']).dt.date
PRO_Sub_9 = PRO_Sub_9.set_index('date')

PRO_Sub_12 = PRO_Sub_12.reset_index()
PRO_Sub_12['date'] = pd.to_datetime(PRO_Sub_12['date']).dt.date
PRO_Sub_12 = PRO_Sub_12.set_index('date')

PRO_Sub_15 = PRO_Sub_15.reset_index()
PRO_Sub_15['date'] = pd.to_datetime(PRO_Sub_15['date']).dt.date
PRO_Sub_15 = PRO_Sub_15.set_index('date')

PRO_Sub_18 = PRO_Sub_18.reset_index()
PRO_Sub_18['date'] = pd.to_datetime(PRO_Sub_18['date']).dt.date
PRO_Sub_18 = PRO_Sub_18.set_index('date')

PRO_Sub_21 = PRO_Sub_21.reset_index()
PRO_Sub_21['date'] = pd.to_datetime(PRO_Sub_21['date']).dt.date
PRO_Sub_21 = PRO_Sub_21.set_index('date')



PRO_Sub_1 = PRO_Sub_1.reset_index()
PRO_Sub_1['date'] = pd.to_datetime(PRO_Sub_1['date']).dt.date
PRO_Sub_1 = PRO_Sub_1.set_index('date')

PRO_Sub_2 = PRO_Sub_2.reset_index()
PRO_Sub_2['date'] = pd.to_datetime(PRO_Sub_2['date']).dt.date
PRO_Sub_2 = PRO_Sub_2.set_index('date')


PRO_Sub_4 = PRO_Sub_4.reset_index()
PRO_Sub_4['date'] = pd.to_datetime(PRO_Sub_4['date']).dt.date
PRO_Sub_4 = PRO_Sub_4.set_index('date')

PRO_Sub_5 = PRO_Sub_5.reset_index()
PRO_Sub_5['date'] = pd.to_datetime(PRO_Sub_5['date']).dt.date
PRO_Sub_5 = PRO_Sub_5.set_index('date')

PRO_Sub_7 = PRO_Sub_7.reset_index()
PRO_Sub_7['date'] = pd.to_datetime(PRO_Sub_7['date']).dt.date
PRO_Sub_7 = PRO_Sub_7.set_index('date')

PRO_Sub_8 = PRO_Sub_8.reset_index()
PRO_Sub_8['date'] = pd.to_datetime(PRO_Sub_8['date']).dt.date
PRO_Sub_8 = PRO_Sub_8.set_index('date')

PRO_Sub_10 = PRO_Sub_10.reset_index()
PRO_Sub_10['date'] = pd.to_datetime(PRO_Sub_10['date']).dt.date
PRO_Sub_10 = PRO_Sub_10.set_index('date')

PRO_Sub_11 = PRO_Sub_11.reset_index()
PRO_Sub_11['date'] = pd.to_datetime(PRO_Sub_11['date']).dt.date
PRO_Sub_11 = PRO_Sub_11.set_index('date')



PRO_Sub_13 = PRO_Sub_13.reset_index()
PRO_Sub_13['date'] = pd.to_datetime(PRO_Sub_13['date']).dt.date
PRO_Sub_13 = PRO_Sub_13.set_index('date')

PRO_Sub_14 = PRO_Sub_14.reset_index()
PRO_Sub_14['date'] = pd.to_datetime(PRO_Sub_14['date']).dt.date
PRO_Sub_14 = PRO_Sub_14.set_index('date')


PRO_Sub_16 = PRO_Sub_16.reset_index()
PRO_Sub_16['date'] = pd.to_datetime(PRO_Sub_16['date']).dt.date
PRO_Sub_16 = PRO_Sub_16.set_index('date')

PRO_Sub_17 = PRO_Sub_17.reset_index()
PRO_Sub_17['date'] = pd.to_datetime(PRO_Sub_17['date']).dt.date
PRO_Sub_17 = PRO_Sub_17.set_index('date')

PRO_Sub_19 = PRO_Sub_19.reset_index()
PRO_Sub_19['date'] = pd.to_datetime(PRO_Sub_19['date']).dt.date
PRO_Sub_19 = PRO_Sub_19.set_index('date')

PRO_Sub_20 = PRO_Sub_20.reset_index()
PRO_Sub_20['date'] = pd.to_datetime(PRO_Sub_20['date']).dt.date
PRO_Sub_20 = PRO_Sub_20.set_index('date')

PRO_Sub_22 = PRO_Sub_22.reset_index()
PRO_Sub_22['date'] = pd.to_datetime(PRO_Sub_22['date']).dt.date
PRO_Sub_22 = PRO_Sub_22.set_index('date')

PRO_Sub_23 = PRO_Sub_23.reset_index()
PRO_Sub_23['date'] = pd.to_datetime(PRO_Sub_23['date']).dt.date
PRO_Sub_23 = PRO_Sub_23.set_index('date')


PRO_Sub_0 = PRO_Sub_0.rename(columns={'temp':'12am Temperature'})
PRO_Sub_3 = PRO_Sub_3.rename(columns={'temp':'3am Temperature'})
PRO_Sub_6 = PRO_Sub_6.rename(columns={'temp':'6am Temperature'})
PRO_Sub_9 = PRO_Sub_9.rename(columns={'temp':'9am Temperature'})
PRO_Sub_12 = PRO_Sub_12.rename(columns={'temp':'12pm Temperature'})
PRO_Sub_15 = PRO_Sub_15.rename(columns={'temp':'3pm Temperature'})
PRO_Sub_18= PRO_Sub_18.rename(columns={'temp':'6pm Temperature'})
PRO_Sub_21 = PRO_Sub_21.rename(columns={'temp':'9pm Temperature'})


PRO_Sub_1 = PRO_Sub_1.rename(columns={'temp':'1am Temperature'})
PRO_Sub_2 = PRO_Sub_2.rename(columns={'temp':'2am Temperature'})
PRO_Sub_4 = PRO_Sub_4.rename(columns={'temp':'4am Temperature'})
PRO_Sub_5 = PRO_Sub_5.rename(columns={'temp':'5am Temperature'})
PRO_Sub_7 = PRO_Sub_7.rename(columns={'temp':'7am Temperature'})
PRO_Sub_8 = PRO_Sub_8.rename(columns={'temp':'8am Temperature'})
PRO_Sub_10= PRO_Sub_10.rename(columns={'temp':'10am Temperature'})
PRO_Sub_11 = PRO_Sub_11.rename(columns={'temp':'11am Temperature'})



PRO_Sub_13 = PRO_Sub_13.rename(columns={'temp':'1pm Temperature'})
PRO_Sub_14 = PRO_Sub_14.rename(columns={'temp':'2pm Temperature'})
PRO_Sub_16 = PRO_Sub_16.rename(columns={'temp':'4pm Temperature'})
PRO_Sub_17 = PRO_Sub_17.rename(columns={'temp':'5pm Temperature'})
PRO_Sub_19 = PRO_Sub_19.rename(columns={'temp':'7pm Temperature'})
PRO_Sub_20 = PRO_Sub_20.rename(columns={'temp':'8pm Temperature'})
PRO_Sub_22= PRO_Sub_22.rename(columns={'temp':'10pm Temperature'})
PRO_Sub_23 = PRO_Sub_23.rename(columns={'temp':'11pm Temperature'})

PRO_Sub_Dummy = PRO_Sub_1.rename(columns={'temp':'Dummy'})



#%%
#Put it all into one big vector
#So now we have it split we need to put it into a Mx24 matrix with the date on the left





PR01 = pd.merge(PRO_Sub_0,PRO_Sub_1, on = ['date'], how  = 'left')

PR23 = pd.merge(PRO_Sub_2,PRO_Sub_3, on = ['date'], how  = 'right')

PR45 = pd.merge(PRO_Sub_4,PRO_Sub_5, on = ['date'], how  = 'right')

PR67 = pd.merge(PRO_Sub_6,PRO_Sub_7, on = ['date'], how  = 'left')

PR89 = pd.merge(PRO_Sub_8,PRO_Sub_9, on = ['date'], how  = 'right')

PR1011 =pd.merge(PRO_Sub_10,PRO_Sub_11, on = ['date'], how  = 'right')

PR1213 =pd.merge(PRO_Sub_12,PRO_Sub_13, on = ['date'], how  = 'left')

PR1415 = pd.merge(PRO_Sub_14,PRO_Sub_15, on = ['date'], how  = 'right')

PR1617 = pd.merge(PRO_Sub_16,PRO_Sub_17, on = ['date'], how  = 'right')

PR1819 =pd.merge(PRO_Sub_18,PRO_Sub_19, on = ['date'], how  = 'left')

PR2021 =pd.merge(PRO_Sub_20,PRO_Sub_21, on = ['date'], how  = 'right')

PR2223 =pd.merge(PRO_Sub_22,PRO_Sub_23, on = ['date'], how  = 'right')

PR0123 = pd.merge(PR01,PR23, on = ['date'], how  = 'left')
PR4567 = pd.merge(PR45,PR67, on = ['date'], how  = 'right')
PR891011 = pd.merge(PR89,PR1011, on = ['date'], how  = 'left')
PR12131415 = pd.merge(PR1213,PR1415, on = ['date'], how  = 'left')
PR16171819 = pd.merge(PR1617,PR1819, on = ['date'], how  = 'right')
PR20212223 = pd.merge(PR2021,PR2223, on = ['date'], how  = 'left')


print(PR0123)
print(PR4567)
print(PR891011)
print(PR12131415)
print(PR16171819)
print(PR20212223)

PR_1 = pd.merge(PR0123,PR4567, on = ['date'], how  = 'left')
PR_2 = pd.merge(PR891011,PR12131415, on = ['date'], how  = 'left')
PR_3 = pd.merge(PR16171819,PR20212223, on = ['date'], how  = 'left')

PR_L =  pd.merge(PR_1,PR_2, on = ['date'], how  = 'left')
PR_FULL_MATRIX =  pd.merge(PR_L,PR_3, on = ['date'], how  = 'left')
PR_FULL_MATRIX = PR_FULL_MATRIX.reset_index()
PR_FULL_MATRIX['date'] = pd.to_datetime(PR_FULL_MATRIX['date'])
PR_FULL_MATRIX = PR_FULL_MATRIX.set_index('date')


#%% Now split it up into different months
#Calculate the Average of each column which excludes NaNs
#Find Anomolies
#Set NaNs to 0
#September


PR_SEPT = pd.concat([PR_FULL_MATRIX[PR_FULL_MATRIX.index.month==9],], axis = 0)
PR_SEPT_Mean = PR_SEPT.mean(axis=0,skipna = True)
PR_SEPT_ANOM =  PR_SEPT- PR_SEPT_Mean
PR_SEPT_ANOM=PR_SEPT_ANOM.fillna(0)


#October
PR_OCT = pd.concat([PR_FULL_MATRIX[PR_FULL_MATRIX.index.month==10],], axis = 0)
PR_OCT_Mean = PR_OCT.mean(axis=0,skipna = True)
PR_OCT_ANOM =  PR_OCT- PR_OCT_Mean
PR_OCT_ANOM=PR_OCT_ANOM.fillna(0)

#November
PR_NOV = pd.concat([PR_FULL_MATRIX[PR_FULL_MATRIX.index.month==11],], axis = 0)
PR_NOV_Mean = PR_NOV.mean(axis=0,skipna = True)
PR_NOV_ANOM =  PR_NOV - PR_NOV_Mean
PR_NOV_ANOM=PR_NOV_ANOM.fillna(0)
#Decemver
PR_DEC = pd.concat([PR_FULL_MATRIX[PR_FULL_MATRIX.index.month==12],], axis = 0)
PR_DEC_Mean = PR_DEC.mean(axis=0,skipna = True)
PR_DEC_ANOM =  PR_DEC- PR_DEC_Mean
PR_DEC_ANOM=PR_DEC_ANOM.fillna(0)

#January
PR_JAN = pd.concat([PR_FULL_MATRIX[PR_FULL_MATRIX.index.month==1],], axis = 0)
PR_JAN_Mean = PR_JAN.mean(axis=0,skipna = True)
PR_JAN_ANOM =  PR_JAN -  PR_JAN_Mean
PR_JAN_ANOM=PR_JAN_ANOM.fillna(0)
#February
PR_FEB = pd.concat([PR_FULL_MATRIX[PR_FULL_MATRIX.index.month==2],], axis = 0)
PR_FEB_Mean = PR_FEB.mean(axis=0,skipna = True)
PR_FEB_ANOM =  PR_FEB- PR_FEB_Mean
PR_FEB_ANOM=PR_FEB_ANOM.fillna(0)
#March
PR_MAR= pd.concat([PR_FULL_MATRIX[PR_FULL_MATRIX.index.month==3],], axis = 0)
PR_MAR_Mean = PR_MAR.mean(axis=0,skipna = True)
PR_MAR_ANOM =  PR_MAR- PR_MAR_Mean
PR_MAR_ANOM= PR_MAR_ANOM.fillna(0)
#April
PR_APR = pd.concat([PR_FULL_MATRIX[PR_FULL_MATRIX.index.month==4],], axis = 0)
PR_APR_Mean = PR_APR.mean(axis=0,skipna = True)
PR_APR_ANOM =  PR_APR- PR_APR_Mean
PR_APR_ANOM = PR_APR_ANOM.fillna(0)

#Any NaNs is skipped in here. So great

#%% Now th model we know that the Coefficents must add up to 1 

Coef = np.ones(24)/24
Coef = pd.Series(Coef,name = 'Coefficents')
Coef = pd.DataFrame(Coef)
def LinearModelForTAnon(c,x,t):
    #Extract a date
    PR_SEPT_Day = PR_SEPT.loc[t]
    PR_SEPT_Day = PR_SEPT_Day.reset_index()
    PR_SEPT_Day = pd.concat([PR_SEPT_Day,Coef],axis=1)
    
    #Coeff matching up with the Sub-daily
    #Now lets remove 0s
    All_No_0_PR = PR_SEPT_Day[(PR_SEPT_Day[t]>0) | (PR_SEPT_Day[t]<0)]
    
    #Now caculate the new delta for each of the coefficents
    for i in range(len(All_No_0_PR)):
        All_No_0_PR['Coefficents'][i] = All_No_0_PR['Coefficents'][i]/sum(All_No_0_PR['Coefficents'])
    
    #Now all the coeffs are updated we can then find the total maximum
    deltaMax = All_No_0_PR['Coefficents'] * All_No_0_PR[t]
    for 
    Max_DeltaX = 



#So Now delaTmax is the
C0*deltaT1 + C1*DeltaT2

So now I have to make a function that














#%%
#Lets go with the way I originally planned it
#Firstly lets reset index
PR_SEPT = PR_SEPT.loc['1967-09-01'].reset_index()
del PR_SEPT['index']
PR_SEPT = PR_SEPT.rename(columns={'Temp'})

#%%
#Lets do a very very basic function
def f(t,a,b,c):
    return a*np.sin(b*x)+c
    
#%% Curve Fit
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
popt,pcov = curve_fit(f,np.linspace(0,1,23),PR_SEPT)

##MY next steps
1. Get the curve fit of this simple model working
2. Then make it more advanced
3. Get this working so it uses M by N rows and spits out a, b and c and d ...
    4. 