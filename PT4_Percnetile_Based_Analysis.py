'''
The percentile based stuff
'''
#%% PACKAGES
import pandas as pd, numpy as np,matplotlib.pyplot as plt
from scipy import stats


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
Daily_Data = []
for groups,days in group_days:
    Dailypre = group_days.get_group(groups).reset_index()
    Values= Dailypre['maximum temperature (degC)']
    Values = Values.to_frame()
    Daily_Data.append(Values['maximum temperature (degC)'])




import PT5_Functions_For_Masters as function_M
YearlyMax = function_M.TnX_Rolling(3, Daily_Data, 50)
plt.plot(YearlyMax)


#%%
'''
Now the code is done, now to:
    1. Use the min one to see if it is fully opporational
    2. Get an average of the min and max and do it
    3. Split into 1910-1940 and 1990-2020 and compare
'''    
#%% 1.
#Load Data only using min Temperature for the initial start
MinT_Perth_Data = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\tmin.009021.daily.csv")
MinT_Perth = MinT_Perth_Data.copy()
MinT_Perth = MinT_Perth.drop(0)

#%% Apply datetime
MinT_Perth['date'] = pd.to_datetime(MinT_Perth['date'],format="%d/%m/%Y")

#%% Apply groupby functiom
MinT_Perth['year']=MinT_Perth['date'].dt.year
MinT_Perth['month']=MinT_Perth['date'].dt.month
MinT_Perth['day']=MinT_Perth['date'].dt.day

group_days = MinT_Perth.groupby(['month','day'])
Daily_Data = []
for groups,days in group_days:
    Dailypre = group_days.get_group(groups).reset_index()
    Values= Dailypre['minimum temperature (degC)']
    Values = Values.to_frame()
    Daily_Data.append(Values['minimum temperature (degC)'])




import PT5_Functions_For_Masters as function_M
YearlyMin = function_M.TnX_Rolling(3, Daily_Data, 50)
plt.plot(YearlyMin)


plt.figure(1)
plt.plot(YearlyMin)
plt.plot(YearlyMax)
#%% 2.
Ave = (MaxT_Perth['maximum temperature (degC)'] + MinT_Perth['minimum temperature (degC)'])/2
Ave = pd.DataFrame(Ave,columns = ['Average Temp'])

Ave_T_Perth = pd.concat((MaxT_Perth['date'], Ave['Average Temp']), axis = 1)

#%% Apply datetime
Ave_T_Perth['date'] = pd.to_datetime(Ave_T_Perth['date'],format="%d/%m/%Y")
#%% Apply groupby functiom
Ave_T_Perth['year']=Ave_T_Perth['date'].dt.year
Ave_T_Perth['month']=Ave_T_Perth['date'].dt.month
Ave_T_Perth['day']=Ave_T_Perth['date'].dt.day

group_days = Ave_T_Perth.groupby(['month','day'])
Daily_Data = []
for groups,days in group_days:
    Dailypre = group_days.get_group(groups).reset_index()
    Values= Dailypre['Average Temp']
    Values = Values.to_frame()
    Daily_Data.append(Values['Average Temp'])




import PT5_Functions_For_Masters as function_M
YearlyAve = function_M.TnX_Rolling(3, Daily_Data, 50)
plt.plot(YearlyAve)


plt.figure(3)
plt.plot(YearlyMin)
plt.plot(YearlyMax)
plt.plot(YearlyAve)


#%% 3.

MaxT_1910_1940 = MaxT_Perth[1:11323]
MaxT_1990_2020 =MaxT_Perth[29221:40543]
#1910 to 1940
group_days = MaxT_1910_1940.groupby(['month','day'])
Daily_Data = []
for groups,days in group_days:
    Dailypre = group_days.get_group(groups).reset_index()
    Values= Dailypre['maximum temperature (degC)']
    Values = Values.to_frame()
    Daily_Data.append(Values['maximum temperature (degC)'])

import PT5_Functions_For_Masters as function_M
YearlyMax_1910_1940 = function_M.TnX_Rolling(7, Daily_Data, 95)

#1990 to 2020
group_days = MaxT_1990_2020.groupby(['month','day'])
Daily_Data = []
for groups,days in group_days:
    Dailypre = group_days.get_group(groups).reset_index()
    Values= Dailypre['maximum temperature (degC)']
    Values = Values.to_frame()
    Daily_Data.append(Values['maximum temperature (degC)'])

import PT5_Functions_For_Masters as function_M
YearlyMax_1990_2020 = function_M.TnX_Rolling(7, Daily_Data,95)


plt.figure(4)
plt.plot(YearlyMax_1910_1940)
plt.plot(YearlyMax_1990_2020)
plt.legend(['1910-1940','1990-2020'])
'''
Somw Stats:
    difference of each date and see how many above 0 to make it obvs there is a differenc
    average diff, 90th perc and diff, 95th percentile and diff make it clear have a changing clear that there is a changing climate
    site moves throughout history of these, small changes in poistion, and quantile based mapping based on extremes
    on extremes, note dont mention in lit rev.
    Summary plot nice, 93% calendar dates
    check if nans being removed create 
    Western north America heatwave from last year broke records by a large margin and indicates what future heatwaves might look like 
The advantage, recent enough and couple peer review papers, instead of the india Pakistan one that is happen

Bam extreme article, European heatwave in 2018
Phillip
'''
#%%
'''
QUALITY CHECK THAT THE QUANTILE IS DOING THE PERCENTILE BASED STUUF
'''
#Vector 1 with NaNs and the other with just values
NaN = np.NaN
VecCheck_nan = pd.Series([1, 2, 3, 4, 5, 100, 50, 25, 10, 5, 2, 1, NaN, NaN, NaN, NaN , 30, 40, 50, 60, 70, 80, NaN,NaN,NaN])
VecCheck = pd.Series([1, 2, 3, 4, 5, 100, 50, 25, 10, 5, 2, 1, 30, 40, 50, 60, 70, 80])
VecCheck.quantile(q=0.95)
VecCheck_nan.quantile(q=0.95)
#So this checks out it removes the NaN or avoids them so great.
np.nanpercentile(VecCheck_nan,95)
np.percentile(VecCheck,95)
#So with the this in mind, we know the quanitle and the percentile functions produce the same variable and 
#on top of this the quantile is much better as NaNs are skipped. however adding the nan front of the percentile produces
#the same result that skips NaNs
#%% Comparison of results.
Clim_Change_Change = YearlyMax_1990_2020 - YearlyMax_1910_1940
Clim_Change_Change = pd.DataFrame(Clim_Change_Change,columns = ['Temp Change'])
#Generate a plot
plt.figure(5)
plt.plot(Clim_Change_Change['Temp Change'])
#Generate the average
Stats_Diff = stats.describe(Clim_Change_Change['Temp Change'])

#Generate number of days above the non climatic change
count = 0
for i in range(366):
    if (Clim_Change_Change['Temp Change'][i] > 0):
        count = count + 1
Percent_days_above_non_CC = 100*count/len(range(366))
print(Percent_days_above_non_CC)
print(Stats_Diff)

#%%Now a dsitribution for the 90% and 95% 
Dist1 = MaxT_1910_1940['maximum temperature (degC)']
Dist2 = MaxT_1990_2020['maximum temperature (degC)']



import numpy as np
from scipy.stats import norm,gamma
import matplotlib.pyplot as plt

plt.figure(6)
# Generate some data for this demonstration.
Dist1 = Ave_T_Perth['Average Temp'][~np.isnan(Ave_T_Perth['Average Temp'])]
data1 = Dist1

# Fit a normal distribution to the data:
a1, a2, a3 = gamma.fit(data1)

# Plot the histogram.
plt.hist(data1, bins=25, density=True, alpha=0.6, color='g')

# Plot the PDF.
xmin, xmax = plt.xlim()
x1 = np.linspace(xmin, xmax, 100)
p1 = gamma.pdf(x1,a1, a2,a3)
plt.plot(x1, p1, 'k', linewidth=2)
#title = "Fit results: mu = %.2f,  std = %.2f" % (mu1, std1)
#plt.title(title)

plt.show()

plt.figure(7)
# Generate some data for this demonstration.
Dist2 = Dist2[~np.isnan(Dist2)]
data2 = Dist2

# Fit a normal distribution to the data:
mu2, std2 = norm.fit(data2)

# Plot the histogram.
plt.hist(data2, bins=25, density=True, alpha=0.6, color='g')

# Plot the PDF.
xmin, xmax = plt.xlim()
x2 = np.linspace(xmin, xmax, 100)
p2 = norm.pdf(x2, mu2, std2)
plt.plot(x2, p2, 'k', linewidth=2)
title = "Fit results: mu = %.2f,  std = %.2f" % (mu2, std2)
plt.title(title)

plt.show()


plt.figure(8)
# Plot the histogram.
plt.hist(data1, bins=25, density=True, alpha=0.6, color='b')

# Plot the PDF.
xmin, xmax = plt.xlim()
x1 = np.linspace(xmin, xmax, 100)
p1 = norm.pdf(x1, mu1, std1)
plt.plot(x1, p1, 'k', linewidth=2)

# Plot the histogram.
plt.hist(data2, bins=25, density=True, alpha=0.6, color='g')


xmin, xmax = plt.xlim()
x2 = np.linspace(xmin, xmax, 100)
p2 = norm.pdf(x2, mu2, std2)
plt.plot(x2, p2, 'k', linewidth=2)



So the temperature record fits a gamma plot. it is intere