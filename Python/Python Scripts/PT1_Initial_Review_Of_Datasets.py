'''
My Masters Project Data Breakdown
'''
import pandas as pd, numpy as np,  matplotlib.pyplot as plt
#First lets load the data
PerthGardens_Extreme_T_Jan1880_Dec1900 = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\perthgardens_daily_1880-1900.csv")
#Note converting to datetime, there is a issue where 1899->1900 goes like 1800-03-22 to 31/12/1900
Perth_Gardens_Corr_Extreme_T_Jan1880_Dec1900 = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\perthgardens_daily_corrected_1880-1900.csv")
Swan_River_Extreme_T_April1830_Dec1875 = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\swanriver_subdaily_1830-1875.csv")
MaxT_Jan1910_Jun2021 = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\tmax.009021.daily.csv")
MinT_Jan1910_Jun2021 = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\tmin.009021.daily.csv")


#Use datetime for MaxT and MinT to test
MaxT_Jan1910_Jun2021['date'] = pd.to_datetime(MaxT_Jan1910_Jun2021['date'])#,format="%Y/%m/%d")
MaxT_Jan1910_Jun2021.set_index('date', inplace=True)
MinT_Jan1910_Jun2021['date'] = pd.to_datetime(MinT_Jan1910_Jun2021['date'])#,format="%Y/%m/%d")
MinT_Jan1910_Jun2021.set_index('date', inplace=True)


plt.figure(1)
plt.plot(PerthGardens_Extreme_T_Jan1880_Dec1900['time'],PerthGardens_Extreme_T_Jan1880_Dec1900['tmax'])
plt.plot(Perth_Gardens_Corr_Extreme_T_Jan1880_Dec1900['time'],Perth_Gardens_Corr_Extreme_T_Jan1880_Dec1900['tmax'])

plt.figure(2)
plt.plot(MaxT_Jan1910_Jun2021['maximum temperature (degC)'])
plt.plot(MinT_Jan1910_Jun2021['minimum temperature (degC)'])
'''
Key notes:
    - Maximums and Minimums are found for 1880 onward data, this means that I will have to 
    intepolate the max and mins for the 1835-1875 data to be consistent.
    - 5 year gap between 1875 to 1880 and 1900 to 1910 I hope we can find data to fill the void
    - Will need to concatenate the 1835 to 1875 data due to that the day is the vertical and the time is the horizontal
    this means that i will have to figure out how to assign a temp value that spits out a date with the time on the vertical 
    and in the next column have temperature.
    - There are two 1880 to 1900, I think the corrected one is better as removes the temp error out of
    the old data, so will have to study going further.
    - Will have to concatonate all the data into one data series, but with these gaps, this makes it 
    quite difficult, is there anywhere where I can insert this data into it.
    -
    -
'''
