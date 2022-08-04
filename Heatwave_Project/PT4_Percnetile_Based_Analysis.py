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

MaxT_1911_1940 = MaxT_Perth[366:11323]
MaxT_1991_2020 =MaxT_Perth[29586:40543]
# Apply datetime
MaxT_1911_1940['date'] = pd.to_datetime(MaxT_1911_1940['date'],format="%d/%m/%Y")

# Apply groupby functiom
MaxT_1911_1940['year']=MaxT_1911_1940['date'].dt.year
MaxT_1911_1940['month']=MaxT_1911_1940['date'].dt.month
MaxT_1911_1940['day']=MaxT_1911_1940['date'].dt.day

Dist1 = (MaxT_1911_1940.loc[MaxT_1911_1940['month']>=11])
Dist12 =  MaxT_1911_1940.loc[MaxT_1911_1940['month']<=3]
Dist1 = pd.concat([Dist1,Dist12]).sort_values(by=['date'], ascending=True)
Dist1 = Dist1['maximum temperature (degC)'][~np.isnan(Dist1['maximum temperature (degC)'])].values
# Apply datetime
MaxT_1991_2020['date'] = pd.to_datetime(MaxT_1991_2020['date'],format="%d/%m/%Y")
MaxT_1991_2020['year']=MaxT_1991_2020['date'].dt.year
MaxT_1991_2020['month']=MaxT_1991_2020['date'].dt.month
MaxT_1991_2020['day']=MaxT_1991_2020['date'].dt.day

Dist2 = (MaxT_1991_2020.loc[MaxT_1991_2020['month']>=11])
Dist22 =  MaxT_1991_2020.loc[MaxT_1991_2020['month']<=3]
Dist2 = pd.concat([Dist2,Dist22]).sort_values(by=['date'], ascending=True)
Dist2 = Dist2['maximum temperature (degC)'][~np.isnan(Dist2['maximum temperature (degC)'])].values


#%% Test
import numpy as np
import pandas as pd
import seaborn as sns
from fitter import Fitter, get_common_distributions, get_distributions
f1 = Fitter(Dist1, distributions=['gamma', 'lognorm',  "beta","burr","norm"])
f1.fit()
f1.summary()
f1.get_best(method = 'sumsquare_error')
Param1 = f1.fitted_param["beta"]



f2 = Fitter(Dist2, distributions=['gamma', 'lognorm',  "beta","burr","norm"])
f2.fit()
f2.summary()
f1.title('f2 (1991-2020)')
f2.get_best(method = 'sumsquare_error')
Param2 = f2.fitted_param["beta"]
#%% Beta






xmin = min(min(Dist1),min(Dist2))
xmax =max(max(Dist1),max(Dist2))

import numpy as np
from scipy.stats import norm,gamma,beta
import matplotlib.pyplot as plt

plt.figure(6)
# Generate some data for this demonstration.

# Fit a normal distribution to the data:
a1, a2,a3,a4= beta.fit(Dist1)

# Plot the histogram.
#plt.hist(Dist1, bins=25, density=True, alpha=0.6, color='g')

# Plot the PDF.
#xmin, xmax = plt.xlim()
x1 = np.linspace(xmin, xmax, 100)
p1 = beta.pdf(x1,a1,a2,a3,a4)
plt.plot(x1, p1, 'k', linewidth=2,color ='black',label = '1911-1940')
#title = "Fit results: mu = %.2f,  std = %.2f" % (mu1, std1)
#plt.title(title)





# Fit a normal distribution to the data:
a5, a6, a7, a8 = beta.fit(Dist2)

# Plot the histogram.
#plt.hist(Dist2, bins=25, density=True, alpha=0.6, color='g')

# Plot the PDF.
xmin, xmax = plt.xlim()
p2 = beta.pdf(x1,a5,a6,a7,a8)
plt.plot(x1, p2, 'k', linewidth=2,color ='red',label = '1991-2020')
#title = "Fit results: mu = %.2f,  std = %.2f" % (mu1, std1)
#plt.title(title)
#plt.hist(Dist2, bins=25, density=True, alpha=0.6, color='g')
plt.title('Perth Maximum Temperature Distribution (Nov-Mar)')
plt.legend()
#In conclusion within the extended summer, the normal distubtion of maximum days has only shifted around 1.8C warmer with no change in variance.
#This means that there is no indication that cold spells are getting colder and more extreme it is that the chance of a cold spell
#is less liekly and the chance of a heatwave is more likely.


plt.figure(7)
plt.plot(x1, p1, 'k', linewidth=2,color ='black')
plt.hist(Dist1, bins=30, density=True, alpha=0.3, color='b')
plt.title('Perth Maximum Temperature Distribution (Nov-Mar) 1911-1940')


plt.figure(11)
plt.plot(x1, p2, 'k', linewidth=2,color ='black')
plt.hist(Dist2, bins=30, density=True, alpha=0.3, color='b')
plt.title('Perth Maximum Temperature Distribution (Nov-Mar) 1991-2020')








#%%











xmin = min(min(Dist1),min(Dist2))
xmax =max(max(Dist1),max(Dist2))

import numpy as np
from scipy.stats import norm,gamma
import matplotlib.pyplot as plt

plt.figure(6)
# Generate some data for this demonstration.

# Fit a normal distribution to the data:
a1, a2 = norm.fit(Dist1)

# Plot the histogram.
#plt.hist(Dist1, bins=25, density=True, alpha=0.6, color='g')

# Plot the PDF.
#xmin, xmax = plt.xlim()
x1 = np.linspace(xmin, xmax, 100)
p1 = norm.pdf(x1,a1, a2)
plt.plot(x1, p1, 'k', linewidth=2,color ='black',label = '1911-1940')
#title = "Fit results: mu = %.2f,  std = %.2f" % (mu1, std1)
#plt.title(title)





# Fit a normal distribution to the data:
a4, a5 = norm.fit(Dist2)

# Plot the histogram.
#plt.hist(Dist2, bins=25, density=True, alpha=0.6, color='g')

# Plot the PDF.
xmin, xmax = plt.xlim()
p2 = norm.pdf(x1,a4, a5)
plt.plot(x1, p2, 'k', linewidth=2,color ='red',label = '1991-2020')
#title = "Fit results: mu = %.2f,  std = %.2f" % (mu1, std1)
#plt.title(title)
#plt.hist(Dist2, bins=25, density=True, alpha=0.6, color='g')
plt.title('Perth Maximum Temperature Distribution (Nov-Mar)')
plt.legend()
#In conclusion within the extended summer, the normal distubtion of maximum days has only shifted around 1.8C warmer with no change in variance.
#This means that there is no indication that cold spells are getting colder and more extreme it is that the chance of a cold spell
#is less liekly and the chance of a heatwave is more likely.


plt.figure(7)
plt.plot(x1, p1, 'k', linewidth=2,color ='black')
plt.hist(Dist1, bins=30, density=True, alpha=0.3, color='b')
plt.title('Perth Maximum Temperature Distribution (Nov-Mar) 1911-1940')


plt.figure(11)
plt.plot(x1, p2, 'k', linewidth=2,color ='black')
plt.hist(Dist2, bins=30, density=True, alpha=0.3, color='b')
plt.title('Perth Maximum Temperature Distribution (Nov-Mar) 1991-2020')
#Thought experience:might suggest the synoptic conditions arent changed that much the world is warmed but actually the weather patterns havent changed, so weather patterns and only a hotter experience, if there was a change in synoptic systems, possible vairance change
#%% gamma fit
plt.figure(8)
# Generate some data for this demonstration.

# Fit a normal distribution to the data:
a1, a2,a3 = gamma.fit(Dist1)

# Plot the histogram.
#plt.hist(Dist1, bins=25, density=True, alpha=0.6, color='g')

# Plot the PDF.
#xmin, xmax = plt.xlim()
x1 = np.linspace(xmin, xmax, 100)
p1 = gamma.pdf(x1,a1, a2,a3)
plt.plot(x1, p1, 'k', linewidth=2,color ='black',label = '1910-1940')
#title = "Fit results: mu = %.2f,  std = %.2f" % (mu1, std1)
#plt.title(title)





# Fit a normal distribution to the data:
a4, a5,a6 = gamma.fit(Dist2)

# Plot the histogram.
#plt.hist(Dist2, bins=25, density=True, alpha=0.6, color='g')

# Plot the PDF.
xmin, xmax = plt.xlim()
p2 = gamma.pdf(x1,a4, a5, a6)
plt.plot(x1, p2, 'k', linewidth=2,color ='red',label = '1990-2020')
plt.title('Perth Maximum Temperature Distribution (Nov-Mar)')
plt.legend()



plt.figure(9)
plt.plot(x1, p1, 'k', linewidth=2,color ='black',label = '1910-1940')
plt.hist(Dist1, bins=30, density=True, alpha=0.3, color='b')
plt.title('Perth Maximum Temperature Distribution (Nov-Mar) 1911-1940')
plt.figure(10)
plt.plot(x1, p2, 'k', linewidth=2,color ='black')
plt.hist(Dist2, bins=30, density=True, alpha=0.3, color='b')
plt.title('Perth Maximum Temperature Distribution (Nov-Mar) 1991-2020')


MaxT_1991_2020['date'] = pd.to_datetime(MaxT_1991_2020['date'],format="%d/%m/%Y")

# Apply groupby functiom
MaxT_1991_2020['year']=MaxT_1991_2020['date'].dt.year

np.mean(Dist1)
np.mean(Dist2)
#%%minimum variant

MinT_1911_1940 = MinT_Perth[366:11323]
MinT_1991_2020 =MinT_Perth[29586:40543]
# Apply datetime
MinT_1911_1940['date'] = pd.to_datetime(MinT_1911_1940['date'],format="%d/%m/%Y")

# Apply groupby functiom
MinT_1911_1940['year']=MinT_1911_1940['date'].dt.year
MinT_1911_1940['month']=MinT_1911_1940['date'].dt.month
MinT_1911_1940['day']=MinT_1911_1940['date'].dt.day

Dist1 = (MinT_1911_1940.loc[MinT_1911_1940['month']>=11])
Dist12 =  MinT_1911_1940.loc[MinT_1911_1940['month']<=3]
Dist1 = pd.concat([Dist1,Dist12]).sort_values(by=['date'], ascending=True)
Dist1 = Dist1['minimum temperature (degC)'][~np.isnan(Dist1['minimum temperature (degC)'])].values
# Apply datetime
MinT_1991_2020['date'] = pd.to_datetime(MinT_1991_2020['date'],format="%d/%m/%Y")
MinT_1991_2020['year']=MinT_1991_2020['date'].dt.year
MinT_1991_2020['month']=MinT_1991_2020['date'].dt.month
MinT_1991_2020['day']=MinT_1991_2020['date'].dt.day

Dist2 = (MinT_1991_2020.loc[MinT_1991_2020['month']>=11])
Dist22 =  MinT_1991_2020.loc[MinT_1991_2020['month']<=3]
Dist2 = pd.concat([Dist2,Dist22]).sort_values(by=['date'], ascending=True)
Dist2 = Dist2['minimum temperature (degC)'][~np.isnan(Dist2['minimum temperature (degC)'])].values

#%% Test
import numpy as np
import pandas as pd
import seaborn as sns
from fitter import Fitter, get_common_distributions, get_distributions
f1 = Fitter(Dist1, distributions=['gamma', 'lognorm',  "beta","burr","norm"])
f1.fit()
f1.summary()
print(f1.get_best(method = 'sumsquare_error'))
Param1 = f1.fitted_param["beta"]


#%%
f2 = Fitter(Dist2, distributions=['gamma', 'lognorm',  "beta","burr","norm"])
f2.fit()
f2.summary()
print(f2.get_best(method = 'sumsquare_error'))
Param2 = f2.fitted_param["beta"]


#%%
xmin = min(min(Dist1),min(Dist2))
xmax =max(max(Dist1),max(Dist2))

import numpy as np
from scipy.stats import norm,gamma,beta
import matplotlib.pyplot as plt

plt.figure(6)
# Generate some data for this demonstration.

# Fit a normal distribution to the data:
a1, a2,a3,a4= beta.fit(Dist1)

# Plot the histogram.
#plt.hist(Dist1, bins=25, density=True, alpha=0.6, color='g')

# Plot the PDF.
#xmin, xmax = plt.xlim()
x1 = np.linspace(xmin, xmax, 100)
p1 = beta.pdf(x1,a1,a2,a3,a4)
plt.plot(x1, p1, 'k', linewidth=2,color ='black',label = '1911-1940')
#title = "Fit results: mu = %.2f,  std = %.2f" % (mu1, std1)
#plt.title(title)





# Fit a normal distribution to the data:
a5, a6, a7, a8 = beta.fit(Dist2)

# Plot the histogram.
#plt.hist(Dist2, bins=25, density=True, alpha=0.6, color='g')

# Plot the PDF.
xmin, xmax = plt.xlim()
p2 = beta.pdf(x1,a5,a6,a7,a8)
plt.plot(x1, p2, 'k', linewidth=2,color ='red',label = '1991-2020')
#title = "Fit results: mu = %.2f,  std = %.2f" % (mu1, std1)
#plt.title(title)
#plt.hist(Dist2, bins=25, density=True, alpha=0.6, color='g')
plt.title('Perth Minimum Temperature Distribution (Nov-Mar)')
plt.legend()
#In conclusion within the extended summer, the normal distubtion of maximum days has only shifted around 1.8C warmer with no change in variance.
#This means that there is no indication that cold spells are getting colder and more extreme it is that the chance of a cold spell
#is less liekly and the chance of a heatwave is more likely.


plt.figure(7)
plt.plot(x1, p1, 'k', linewidth=2,color ='black')
plt.hist(Dist1, bins=30, density=True, alpha=0.3, color='b')
plt.title('Perth Minimum Temperature Distribution (Nov-Mar) 1911-1940')


plt.figure(11)
plt.plot(x1, p2, 'k', linewidth=2,color ='black')
plt.hist(Dist2, bins=30, density=True, alpha=0.3, color='b')
plt.title('Perth Minimum Temperature Distribution (Nov-Mar) 1991-2020')
