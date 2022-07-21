'''

'''
import pandas as pd, numpy as np,matplotlib.pyplot as plt

'''


This is my rough draft of defining heatwaves.
There are a few components for this, and they all require different problems 
work out before I can finilise the results.

The goal of this section is to generate the necessary code that will be 
vital in understanding heatwave and warmwave events in Perth and in order for 
that to be true we must explain a few things before hand so I and you can get
a really good idea of where I am heading with how I will define my heatwaves.

There will be a few different ways in defining heatwaves, and a few different metrics
that will be imprecial for my analysis in each of the definitions. There are 3 
definitions I must account for and I hope all three capture the signifincatn heatwave events
and also other events that may not have been seen at the time, which will be 
important in discussing synoptic setups using the 20CR reanalysis.

So the 3 catergories that I will look at are:
    Absolute Heatwave Threshold (AHT):
        This is bascially the heatwaves that are KNOWN to cause significant health 
        issues and its aboove a temperautre threshold that is SPECIFIC to Perth
        that begins to see a spike in heat related deaths/hospital calls.
        
    Relative Heatwave Threshold (RHT):
        This is using a moving mean and this sets a moving threshold that alters over
        the year. In order to define, it should use a percentile based idea.
        Moderate-Extreme:
            I aim to achieve capturing as many heatwave/warmwave events as possible 
            that are known and furthermore see trends with this threshold that has a 
            low percentile base compared to the extreme. As long as it does not overcapture
            the heat/warm waves it should be fine.
        Extreme:
            This will be used to compare the synotpic setup overall for the 20CR
            these should have captured most or all of the absolute heatwaves, however
            since there will be less of them, it will have enough data to show the 
            how a snyptoic setup will occur from 5 days before that generates these
            extrme setups.
    Heatwave with Breaks (HWB):
        This is my last one and I beleive has not really been done before, I aim 
        generate a timeline that hopefully captures all the heatwvaes and also 
        a heatwave that may have had a cool day in betweenthe heatwave event.
        This should lead to lower heatwave events but shuld capture all known events
        still. If this works I will implement this as a full time working code for the 
        rest of my masters degree.


Now we have the catergories for the heatwaves now we need to generate the definitions
for each of them. The definitions will remain mostly the same but will some tweaks.
I think the first main thing is defining the time that a heatwave should initially last. 
Well all previous studies have reported that 3 days is the minimum and with its in
agreementr with the medical.infrustrucal papers that I have read that agree o this time.

A heatwave should last 3 or more days, so then what does this mean for HWB, well
I beleive that IF the heatwave definition is greater the AHT and RHT for 3 days straight
then I willstart the HWB then, if there is 2 days, then 1 day of cooler weather 
then another day of hot weather, this WILL not count.

Now the mathematical definitions, I will use from the Nairn paper 2013 and Perkins Paper, t

Since nairn and perken uses a summing system that uses Ti-+1 and Ti-+2, I have used this to show how it affects 
the graphical representation of the moving mean.
'''
Test = [4,3,5,7,3,4,5,7,5,6,3,6,4,3,5,6,7,3,5,6,4,4,3,5,6,7,4,2,4,6,1,6,7,8,6,4,6,10,11,13,9,6,5,4,2,4,5,6,3,5,7,3,1,3,5,7,8,9,3,4,5,7]
import pandas as pd, matplotlib.pyplot as plt
df = pd.DataFrame(Test, columns = ['Testing'])
plt.plot(df['Testing'])

TA1=[]
TA2 = []
TA3 = []
for i in range(3,len(Test)-3):
    Test_Ave1 = (Test[i] + Test[i-1] + Test[i-2])/3
    Test_Ave2 = (Test[i] + Test[i-1] + Test[i+1])/3
    Test_Ave3 = (Test[i] + Test[i+1] + Test[i+2])/3
    TA1.append(Test_Ave1)
    TA2.append(Test_Ave2)
    TA3.append(Test_Ave3)
    

plt.plot(TA1)
plt.plot(TA2)
plt.plot(TA3)
plt.legend(('T1','T2','T3'))
'''
It can be shown from this test that the heatwave would appear1 day later if using precednet 
data to caluclate the heatwave as Perkens 2013 and Nairn 2009 suggests and this means that if the start of the heat wave occured
on day 47, we would not know until day 48 which in the way of predicting these is not good. But in terms of 
being there at the time and recording this overall data, this is all they had to base it off. And I tend 
to agree with the logic behind it, if doing the T2 approach this may show the heatwave on the day, but the inssue is that is it
long lasting, and the effect health and human wise dnt really occur on that day. T3
is not a great one becasue it predicts the heatwave before it actually occurs therefore 
not a viable soliution.
Based on how observations were recorded IU believe the precident one will be ideal so samee as Nairn and Perkins.and furthermore
it is universally accepted for Australia heatwave definition (Trancoso 2014) this is the first definition

the second definition will be the period that both max and min temperatures are above a __% percentile

The final definition will be the twe3aking of the WSDI index from Alexander 2006 which is the warm spell indictaor
which means that above a certain percentile, average over a period of 3-6 days, does the warm spell exceed the 
90th perctile or something in a row within this, I am still pondering this idea.

The above are relative terms

For the absolute it is much easier, once the absolute temperature thresho;ld is found due to health issue causes
if this is exceeded three or more days then it counts as an absolute heatwave, this should occur in Summer generally




These are a few definitions to think about over the course of the next couple of weeks and refining 
these to get the best output for the duration and onset of the heatwave is vital.


Now some other definitions that explain heatwaves.
So I want to explore beyond the duration aspect with amplitude of the event which is 
the height above the preceding 30 days from the initial beginning of the event, and also
the hottest day of the heatwave. Another metric I want to explore is the amount of 
extra heat added into the region each day with two metrics one with a sum and the other
with the average for the heat wave event. This will also be similar to the area under a half
sinusiodal graph.

So far I can draft up these diferent metrics and when I get to them later on in my coding, 
I will explain them in more detail. I have to terst them so I can acquire the right information.

With the break, once I complete the above, I can figure out jjhow to implement a break.
'''
'''DEFINITION 1 DURATION AND DETERMING THE HEATWAVE'''
'''Excess Heatwave Index '''



'''
My Next Quest is to look at a percentile based code tnx, which will help show all times a day is above that percentilke.
The base will be set to the 90th percentile.
'''
#%%
import pandas as pd, numpy as np
'''PART 1: LOAD THE DATA'''
MaxT_Perth_Data = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\tmax.009021.daily.csv")
MaxT_Perth = MaxT_Perth_Data.copy()
MaxT_Perth = MaxT_Perth.drop(0)

MinT_Perth_Data = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\tmin.009021.daily.csv")
MinT_Perth = MinT_Perth_Data.copy()
MinT_Perth = MinT_Perth.drop(0)
import pandas as pd, numpy as np
#Note MaxT has missing dates: 26/01/1913, 27/01/1913, 26/12/1943, 27/12/1943, 18-23/09/2008
#Note MinT has many points missing from 1942/1943
#I would have to exclude any of these points by using an if check or something when generating the tn






## PART 2 A BASIC Tn for the rolling comparison
#Concanate Min and Max values into a single dataset
Max_Min_Perth = pd.concat((MaxT_Perth['date'], MaxT_Perth['maximum temperature (degC)'], MinT_Perth['minimum temperature (degC)']), axis = 1)
Max_Min_Perth['date'] = pd.to_datetime(Max_Min_Perth['date'],format="%d/%m/%Y")

#For the rolling I need to set all NaN values to -99999999 and so whenever a day uses a NaN value it becomes extremely negative and I can remove it.
#Max_Min_Perth_NaN_To_Large = Max_Min_Perth.fillna(-9999999)
#We know the lowest temperautee value is -2.2
#Now in order to smooth the data out and create a tnx90 I am going to do 2 comparisons,
#I plan to first do the rolling for 7 days and then the 15 days as KirkFITz has done herself.
#Once I do the rolling any values that have a mean below -3 will be remove as these are all the NaN and also the 1910 data's coldest max/min temp is -2.2C

#%%Rolling the entire period

#Rolling with 7 days, this is 3 days nbefre and after and the centred day.
Max_7Day_Roll = Max_Min_Perth['maximum temperature (degC)'].rolling(7,center = True).mean()
Min_7Day_Roll = Max_Min_Perth['minimum temperature (degC)'].rolling(7,center = True).mean()
#Append this back with the time
Max_Rolling = pd.concat((MaxT_Perth['date'], Max_7Day_Roll), axis = 1)
Min_Rolling = pd.concat((MaxT_Perth['date'], Min_7Day_Roll), axis = 1)

#Remove NaNs
Max_Rolling = Max_Rolling.fillna(-9999999)
Min_Rolling = Min_Rolling.fillna(-9999999)
#Remove years where the rolling is less the -3C
Index_For_Drop_Max = Max_Rolling[Max_Rolling['maximum temperature (degC)'] < -5].index
Max_Rolling.drop(Index_For_Drop_Max, inplace = True)
Index_For_Drop_Min = Min_Rolling[Min_Rolling['minimum temperature (degC)'] < -5].index
Min_Rolling.drop(Index_For_Drop_Min, inplace = True)

#Now the fun begins, I must use a groupby function to get each day out, then apply my function for percentile then I can plot this percentile for each day.
#Start  with max first
Max_Rolling['date'] = pd.to_datetime(Max_Rolling['date'],dayfirst = True)
#First I want to compare the calender day mean with the 90th percentile
mean_Max = Max_Rolling.groupby([(Max_Rolling.date.dt.month),(Max_Rolling.date.dt.day)]).mean()
tn90_max = Max_Rolling.groupby([(Max_Rolling.date.dt.month),(Max_Rolling.date.dt.day)]).quantile(q = 0.90)
plt.figure(1)
mean_Max['maximum temperature (degC)'].plot()
tn90_max['maximum temperature (degC)'].plot()
'''It is very interesting to see that there are some dips that
happen at the end of the month for Jan, I need to make sure it is working properly'''

#Now for the minimum.
Min_Rolling['date'] = pd.to_datetime(Min_Rolling['date'],dayfirst = True)
#First I want to compare the calender day mean with the 90th percentile
mean_Min = Min_Rolling.groupby([(Min_Rolling.date.dt.month),(Min_Rolling.date.dt.day)]).mean()
tn90_min = Min_Rolling.groupby([(Min_Rolling.date.dt.month),(Min_Rolling.date.dt.day)]).quantile(q = 0.90)
plt.figure(2)
mean_Min['minimum temperature (degC)'].plot()
tn90_min['minimum temperature (degC)'].plot()

plt.figure(3)
tn90_max['maximum temperature (degC)'].plot()
tn90_min['minimum temperature (degC)'].plot()



#%%Rolling the entire period

#Rolling with 15 days, this is 7 days nbefre and after and the centred day.
Max_15Day_Roll = Max_Min_Perth_NaN_To_Large['maximum temperature (degC)'].rolling(15,center = True).mean()
Min_15Day_Roll = Max_Min_Perth_NaN_To_Large['minimum temperature (degC)'].rolling(15,center = True).mean()
#Append this back with the time
Max_Rolling = pd.concat((MaxT_Perth['date'], Max_15Day_Roll), axis = 1)
Min_Rolling = pd.concat((MaxT_Perth['date'], Min_15Day_Roll), axis = 1)

#Remove NaNs
Max_Rolling = Max_Rolling.fillna(-9999999)
Min_Rolling = Min_Rolling.fillna(-9999999)
#Remove years where the rolling is less the -3C
Index_For_Drop_Max = Max_Rolling[Max_Rolling['maximum temperature (degC)'] < -5].index
Max_Rolling.drop(Index_For_Drop_Max, inplace = True)
Index_For_Drop_Min = Min_Rolling[Min_Rolling['minimum temperature (degC)'] < -5].index
Min_Rolling.drop(Index_For_Drop_Min, inplace = True)

#Now the fun begins, I must use a groupby function to get each day out, then apply my function for percentile then I can plot this percentile for each day.
#Start  with max first
Max_Rolling['date'] = pd.to_datetime(Max_Rolling['date'],dayfirst = True)
#First I want to compare the calender day mean with the 90th percentile
mean_Max = Max_Rolling.groupby([(Max_Rolling.date.dt.month),(Max_Rolling.date.dt.day)]).mean()
tn90_max15 = Max_Rolling.groupby([(Max_Rolling.date.dt.month),(Max_Rolling.date.dt.day)]).quantile(q = 0.90)
plt.figure(4)
mean_Max['maximum temperature (degC)'].plot()
tn90_max15['maximum temperature (degC)'].plot()
'''It is very interesting to see that there are some dips that
happen at the end of the month for Jan, I need to make sure it is working properly'''

#Now for the minimum.
Min_Rolling['date'] = pd.to_datetime(Min_Rolling['date'],dayfirst = True)
#First I want to compare the calender day mean with the 90th percentile
mean_Min = Min_Rolling.groupby([(Min_Rolling.date.dt.month),(Min_Rolling.date.dt.day)]).mean()
tn90_min15 = Min_Rolling.groupby([(Min_Rolling.date.dt.month),(Min_Rolling.date.dt.day)]).quantile(q = 0.90)
plt.figure(5)
mean_Min['minimum temperature (degC)'].plot()
tn90_min15['minimum temperature (degC)'].plot()

plt.figure(6)
tn90_max15['maximum temperature (degC)'].plot()
tn90_min15['minimum temperature (degC)'].plot()


plt.figure(7)
tn90_max['maximum temperature (degC)'].plot()
tn90_min['minimum temperature (degC)'].plot()
tn90_max15['maximum temperature (degC)'].plot()
tn90_min15['minimum temperature (degC)'].plot()
plt.legend('max7','min7','max15','min15')
#Not really any different when comparing the two let me look at the 30 day as well

#%%

#Rolling with 15 days, this is 7 days nbefre and after and the centred day.
Max_30Day_Roll = Max_Min_Perth_NaN_To_Large['maximum temperature (degC)'].rolling(30,center = True).mean()
Min_30Day_Roll = Max_Min_Perth_NaN_To_Large['minimum temperature (degC)'].rolling(30,center = True).mean()
#Append this back with the time
Max_Rolling = pd.concat((MaxT_Perth['date'], Max_30Day_Roll), axis = 1)
Min_Rolling = pd.concat((MaxT_Perth['date'], Min_30Day_Roll), axis = 1)

#Remove NaNs
Max_Rolling = Max_Rolling.fillna(-9999999)
Min_Rolling = Min_Rolling.fillna(-9999999)
#Remove years where the rolling is less the -3C
Index_For_Drop_Max = Max_Rolling[Max_Rolling['maximum temperature (degC)'] < -5].index
Max_Rolling.drop(Index_For_Drop_Max, inplace = True)
Index_For_Drop_Min = Min_Rolling[Min_Rolling['minimum temperature (degC)'] < -5].index
Min_Rolling.drop(Index_For_Drop_Min, inplace = True)

#Now the fun begins, I must use a groupby function to get each day out, then apply my function for percentile then I can plot this percentile for each day.
#Start  with max first
Max_Rolling['date'] = pd.to_datetime(Max_Rolling['date'],dayfirst = True)
#First I want to compare the calender day mean with the 90th percentile
mean_Max = Max_Rolling.groupby([(Max_Rolling.date.dt.month),(Max_Rolling.date.dt.day)]).mean()
tn90_max30 = Max_Rolling.groupby([(Max_Rolling.date.dt.month),(Max_Rolling.date.dt.day)]).quantile(q = 0.90)
plt.figure(8)
mean_Max['maximum temperature (degC)'].plot()
tn90_max30['maximum temperature (degC)'].plot()
'''It is very interesting to see that there are some dips that
happen at the end of the month for Jan, I need to make sure it is working properly'''

#Now for the minimum.
Min_Rolling['date'] = pd.to_datetime(Min_Rolling['date'],dayfirst = True)
#First I want to compare the calender day mean with the 90th percentile
mean_Min = Min_Rolling.groupby([(Min_Rolling.date.dt.month),(Min_Rolling.date.dt.day)]).mean()
tn90_min30 = Min_Rolling.groupby([(Min_Rolling.date.dt.month),(Min_Rolling.date.dt.day)]).quantile(q = 0.90)
plt.figure(9)
mean_Min['minimum temperature (degC)'].plot()
tn90_min30['minimum temperature (degC)'].plot()

plt.figure(10)
tn90_max30['maximum temperature (degC)'].plot()
tn90_min30['minimum temperature (degC)'].plot()


plt.figure(11,figsize=(50,10))
tn90_max['maximum temperature (degC)'].plot()
tn90_min['minimum temperature (degC)'].plot()
tn90_max15['maximum temperature (degC)'].plot()
tn90_min15['minimum temperature (degC)'].plot()
tn90_max30['maximum temperature (degC)'].plot()
tn90_min30['minimum temperature (degC)'].plot()
plt.legend(['max7','min7','max15','min15','max30','min30'])
#Not really any different when comparing the two let me look at the 30 day as well




#mean of the 90th percentile
#23rd Feb
#5x 110 then do 90th percentile of that
#justr keep NaNs and python removes them look for key word.


#%%I did the wrong way above so this is the right way below:
    '''
    How to do the right way?
    STEP 1:
        Get it into daily data vectors
    STEP 2:
           x, x+-1, ... x-+i matrix
        y1
        y2
        ...         
        yi
        
    STEP 3: 
        Get The Tn90 from this matrix and movie to the next day
    STEP 4:
        Then plot, the rolling is already done.
    '''
#STEP 1
Max = pd.concat((Max_Min_Perth['date'], Max_Min_Perth['maximum temperature (degC)']), axis = 1)
Max['date'] = pd.to_datetime(Max['date'],dayfirst = True)
mean_Max = Max.groupby([(Max.date.dt.month)='Month',(Max.date.dt.day)='Day']).mean()
mean_Max.plot()

mean_Max['date'][1,1]    

Max=Max.reset_index()
Max['date']=Max.to_datetime(Max['date'])
Max['year']=Max['date'].dt.year
Max['month']=Max['date'].dt.month
Max['day']=Max['date'].dt.day

mean_Max = Max.groupby(['month','day']).mean()
mean_Max = Max.groupby(['month','day'])
for groups in mean_Max:
    print(groups)


df_grouped=Max.pivot(index=('month','day'),rows = 'maximum temperature (degC)')

