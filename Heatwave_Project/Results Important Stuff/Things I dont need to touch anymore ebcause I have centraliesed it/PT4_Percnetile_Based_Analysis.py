'''
The percentile based stuff
'''
#%% PACKAGES
import pandas as pd, numpy as np,matplotlib.pyplot as plt
from scipy import stats
import sys
sys.path.append(r"C:\Users\jarra\Desktop\Masters\Heatwave_Project")

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
#MaxT_1911_1940 = MaxT_Perth[304:821]
#MaxT_1991_2020 =MaxT_Perth[29524:30040]
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
from fitter import Fitter, get_common_distributions, get_distributionsimport seaborn as sns
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
#plt.hist(Dist2, bins=25, density=True, alpha=0.6, color='g'

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
MinT_Perth =MinT_Perth.set_index('date')
MaxT_Perth = MaxT_Perth.set_index('date')
#%%


MinT_1911_1940 = MinT_Perth.loc['1920-01-01':'1930-04-01']
MinT_1991_2020 =MinT_Perth['1920-01-01':'1929-12-01']

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
from scipy.stats import norm,gamma,beta,lognorm
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
plt.xlabel('Temperature (\N{DEGREE SIGN}C)')
plt.ylabel('PDF values')
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



#%% New distribution stuff with what I know now
MaxT_Perth = MaxT_Perth.set_index('date')
MinT_Perth = MinT_Perth.set_index('date')
#%%

#MaxT_Perth = Dist2.set_index('date')



MaxT_1920 = MaxT_Perth.loc['1920-01-01':'1929-12-31']
MaxT_1920 = MaxT_1920.reset_index()
MaxT_1920['month']=MaxT_1920['date'].dt.month


Dist1 = (MaxT_1920.loc[MaxT_1920['month']>=12])
Dist22 =  MaxT_1920.loc[MaxT_1920['month']<=2]
Dist2 = pd.concat([Dist1,Dist22]).sort_values(by=['date'], ascending=True)
MaxT_1920 = Dist2['maximum temperature (degC)'][~np.isnan(Dist2['maximum temperature (degC)'])].values






MaxT_2010 = MaxT_Perth.loc['2010-01-01':'2019-12-31']


MaxT_2010 = MaxT_2010.reset_index()
MaxT_2010['month']=MaxT_2010['date'].dt.month


Dist1 = (MaxT_2010.loc[MaxT_2010['month']>=12])
Dist22 =  MaxT_2010.loc[MaxT_2010['month']<=2]
Dist2 = pd.concat([Dist1,Dist22]).sort_values(by=['date'], ascending=True)
MaxT_2010 = Dist2['maximum temperature (degC)'][~np.isnan(Dist2['maximum temperature (degC)'])].values


#chc40more2010 = 100*len(MaxT_2010[MaxT_2010>=40])/len(MaxT_2010)
#chc40more1920 = 100*len(MaxT_1920[MaxT_1920>=40])/len(MaxT_1920)
#print(chc40more2010,chc40more1920)













f1 = Fitter(MaxT_2010, distributions=['gamma', 'lognorm',  "beta","burr","norm"])
f1.fit()
f1.summary()
print(f1.get_best(method = 'sumsquare_error'))
Param1 = f1.fitted_param["beta"]
f2 = Fitter(MaxT_1920, distributions=['gamma', 'lognorm',  "beta","burr","norm"])
f2.fit()
f2.summary()
print(f2.get_best(method = 'sumsquare_error'))
Param1 = f1.fitted_param["beta"]

#Best is Gamma




plt.figure(6)








# Generate some data for this demonstration.

# Fit a gamma distribution to the data:
    
fit_alpha, fit_loc, fit_beta = stats.gamma.fit(MaxT_2010)
print(fit_alpha, fit_loc, fit_beta )

gamma.ppf(40, fit_alpha,loc =fit_loc, scale = fit_beta)
#fit_loc loccation of where the first point starts
Temp1 = MaxT_2010
chc40more = 100*len(Temp1[Temp1>=40])/len(Temp1)












# Plot the histogram.
plt.hist(MaxT_2010, bins=25, density=True, alpha=0.6, color='g')

# Plot the PDF.
xmax = MaxT_Perth['maximum temperature (degC)'].max()
xmin = MaxT_Perth['maximum temperature (degC)'].min()
#xmin, xmax = plt.xlim()
x1 = np.linspace(xmin, xmax, 100)
#p1 = gamma.rsv(fit_alpha,fit_loc,fit_beta)
plt.plot(x1, p1, 'k', linewidth=2,color ='black',label = '1911-1940')
#title = "Fit results: mu = %.2f,  std = %.2f" % (mu1, std1)
#plt.title(title)





# Fit a normal distribution to the data:
a5, a6, a7 = gamma.fit(MaxT_1920['maximum temperature (degC)'])
Temp2 = MaxT_1920['maximum temperature (degC)']
chc40more1920 = 100*len(Temp2[Temp2>=40])/len(Temp2)
# Plot the histogram.
plt.hist(MaxT_1920['maximum temperature (degC)'], bins=25, density=True, alpha=0.6, color='g')

# Plot the PDF.

p2 = gamma.pdf(x1,a5,a6,a7)
plt.plot(x1, p2, 'k', linewidth=2,color ='red',label = '1991-2020')
#title = "Fit results: mu = %.2f,  std = %.2f" % (mu1, std1)
#plt.title(title)
#plt.hist(Dist2, bins=25, density=True, alpha=0.6, color='g')
plt.title('Perth Minimum Temperature Distribution (Nov-Mar)')
plt.legend()

from scipy.stats import gamma,burr

#Chnace above 40C
Y_1920 = gamma.pdf(x = 25, a = a1,scale = a2, loc = a3)
Y_2010 = gamma.pdf(x = 25, a = a5,scale = a6, loc = a7)




print(Y_2010.pdf(40))
print(gamma.pdf(x=2, a=2, scale=1, loc=0))

chc40more2010 = 100*len(Temp1[Temp1>=40])/len(Temp1)
chc40more1920 = 100*len(Temp2[Temp2>=40])/len(Temp2)


















#%%
#Load Data In
MaxT_Perth_Data = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\tmax.009021.daily.csv")
MaxT_Perth = MaxT_Perth_Data.copy()
MaxT_Perth = MaxT_Perth.drop(0)

MaxT_Perth['date'] = pd.to_datetime(MaxT_Perth['date'],format="%d/%m/%Y")

#Load Data only using min Temperature for the initial start
MinT_Perth_Data = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\tmin.009021.daily.csv")
MinT_Perth = MinT_Perth_Data.copy()
MinT_Perth = MinT_Perth.drop(0)

MinT_Perth['date'] = pd.to_datetime(MinT_Perth['date'],format="%d/%m/%Y")

MaxT_Perth = MaxT_Perth.set_index('date')
MinT_Perth = MinT_Perth.set_index('date')


















#%% Get Extended Summer only between 1920-1929 and 2010-2019


#1920-1929
MaxT_1920 = MaxT_Perth.loc['1920-01-01':'1929-12-31']
MaxT_1920 = MaxT_1920.reset_index()
MaxT_1920['month']=MaxT_1920['date'].dt.month

Dist1 = (MaxT_1920.loc[MaxT_1920['month']>=12])
Dist22 =  MaxT_1920.loc[MaxT_1920['month']<=2]
MaxES1920 = pd.concat([Dist1,Dist22]).sort_values(by=['date'], ascending=True)
MaxT_1920 = MaxES1920['maximum temperature (degC)'][~np.isnan(MaxES1920['maximum temperature (degC)'])].values

MinT_1920 = MinT_Perth.loc['1920-01-01':'1929-12-31']
MinT_1920 = MinT_1920.reset_index()
MinT_1920['month']=MinT_1920['date'].dt.month

Dist12 = (MinT_1920.loc[MinT_1920['month']>=12])
Dist223 =  MinT_1920.loc[MinT_1920['month']<=2]
MinES1920 = pd.concat([Dist12,Dist223]).sort_values(by=['date'], ascending=True)
MinT_1920 = MinES1920['minimum temperature (degC)'][~np.isnan(MinES1920['minimum temperature (degC)'])].values


#2010-2019
MaxT_2010 = MaxT_Perth.loc['2010-01-01':'2019-12-31']
MaxT_2010 = MaxT_2010.reset_index()
MaxT_2010['month']=MaxT_2010['date'].dt.month


Dist11 = (MaxT_2010.loc[MaxT_2010['month']>=12])
Dist222 =  MaxT_2010.loc[MaxT_2010['month']<=2]
MaxES2010 = pd.concat([Dist11,Dist222]).sort_values(by=['date'], ascending=True)
MaxT_2010 = MaxES2010['maximum temperature (degC)'][~np.isnan(MaxES2010['maximum temperature (degC)'])].values

MinT_2010 = MinT_Perth.loc['2010-01-01':'2019-12-31']
MinT_2010 = MinT_2010.reset_index()
MinT_2010['month']=MinT_2010['date'].dt.month


Dist112 = (MinT_2010.loc[MinT_2010['month']>=12])
Dist2223 =  MinT_2010.loc[MinT_2010['month']<=2]
MinES2010 = pd.concat([Dist112,Dist2223]).sort_values(by=['date'], ascending=True)
MinT_2010 = MinES2010['minimum temperature (degC)'][~np.isnan(MinES2010['minimum temperature (degC)'])].values



#%%Get the distributions
from scipy.stats import gamma,burr

plt.figure(10)

f1 = Fitter(MaxT_2010, distributions=['gamma', 'lognorm',  "beta","burr","norm"])
f1.fit()
f1.summary()
print(f1.get_best(method = 'sumsquare_error'))
a1, a2,a3,a4 = f1.fitted_param["beta"]



f2 = Fitter(MaxT_1920, distributions=['gamma', 'lognorm',  "beta","burr","norm"])
f2.fit()
f2.summary()
print(f2.get_best(method = 'sumsquare_error'))
a5, a6,a7,a8 = f2.fitted_param["beta"]


f3 = Fitter(MinT_2010, distributions=['gamma', 'lognorm',  "beta","burr","norm"])
f3.fit()
f3.summary()
print(f3.get_best(method = 'sumsquare_error'))
a9,a10,a11,a12 = f3.fitted_param["burr"]



f4= Fitter(MinT_1920, distributions=['gamma', 'lognorm',  "beta","burr","norm"])
f4.fit()
f4.summary()
print(f4.get_best(method = 'sumsquare_error'))
a13,a14,a15,a16 = f4.fitted_param["beta"]

#Plot them
xmax = MaxT_Perth['maximum temperature (degC)'].max()
xmin = MaxT_Perth['maximum temperature (degC)'].min()
xmax2 = MinT_Perth['minimum temperature (degC)'].max()
xmin2 = MinT_Perth['minimum temperature (degC)'].min()

x1 = np.linspace(xmin, xmax, 100)
x2 = np.linspace(xmin2, xmax2, 100)


plt.figure(1)
plt.hist(MaxT_2010, bins=25, density=True, alpha=0.6, color='y')
plt.hist(MaxT_1920, bins=25, density=True, alpha=0.6, color='red')

p1 = beta.pdf(x1,a1,a2,a3,a4)
plt.plot(x1, p1, 'k', linewidth=2,color ='y',label = '2010-2019')


p2 = beta.pdf(x1,a5,a6,a7,a8)
plt.plot(x1, p2, 'k', linewidth=2,color ='red',label = '1920-1929')
plt.legend()
plt.title("Perth Maximum Temperature Distribution (Nov-Mar)",fontsize =14)
plt.xlabel("Temperature (\N{DEGREE SIGN}C)",fontsize =12)
plt.ylabel("Density",fontsize =12)
plt.xlim([15,47])

plt.figure(2)
plt.hist(MinT_2010, bins=25, density=True, alpha=0.6, color='green')
plt.hist(MinT_1920, bins=25, density=True, alpha=0.6, color='blue')

p3 = burr.pdf(x2,a9,a10,a11,a12)
plt.plot(x2, p3, 'k', linewidth=2,color ='green',label = '2010-2019')


p4 = beta.pdf(x2,a13,a14,a15,a16)
plt.plot(x2, p4, 'k', linewidth=2,color ='blue',label = '1920-1929')
plt.legend()
plt.title("Perth Minimum Temperature Distribution (Nov-Mar)",fontsize =14)
plt.xlabel("Temperature (\N{DEGREE SIGN}C)",fontsize =12)
plt.ylabel("Density",fontsize =12)
plt.xlim([3,30])










