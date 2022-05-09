import pandas as pd, numpy as np,  matplotlib.pyplot as plt

'''Import 1835_1875 Data'''
Swan_River_1830_1875 = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\swanriver_subdaily_1830-1875.csv")
'''
Just from what I can see, there are 16696 rows and 60 columns which
is definitely more then 24hr time period which would be 24 columns.

Upon looking deeper there are soooo many different colomns its hard
to figure out where the data will lie
The first issue is the time, there are many different times, some just say interval 1/2/a/b/c...
And for the purposes of this I think will be removed out of the 
concatentation due to not being with a designated time stamp, as the Gergis
paper suggest that is may possibly be the "It may be that the interval temperatureobservations
 represent the maxima and minima betweenthe fixed-time observations or that they represent
 themaxima and minima of the day. " So further analysis will \be needed. Therefore since I am only
 using this dataset to anaylis what is already there. i believe it is beyond the scope
 of this paper as have Gergis have also done.
 There is another column called night which it could be just some point at night, but with no refernbce
 to the time this was taken, I will be exlcduing tjhis from the study too.
 
 there are two columns called 5pma and 5pmb which suggest that its actually 5pma == am and 5pmb == pm, but there 
 only 2 points that actually use this description, so I think we can exclude from the dataset, 
 
 I have been looking further into the 1835-1975 dataset and I need some clarification on a few of the column names.

1. 5pma and 5pmb

So my initial guess from what information they show is that 5pma is 5am and 5pmb is 5pm, as the temperature is
 10C lower for the two available dates in 5pma then 5pmb. Is this what you also believe as well?


2. noona and noob

This one is much more interesting, as there are 100 or so dates that use these columns. My first assumption 
was that, noona would be 12am and noonb would be 12pm (due to the definition of noon being at 12). But the issue 
is some dates have similar temperatures or in some cases noona temperature either will be higher or lower than the 
noonb temperature. Now I am not so certain which times these noon columns take. Is there any information you have 
that explains these column names?
'''

'''Now split and name each of the column names'''
list(Swan_River_1830_1875)
#So we will have to create datetime then separate each column and refer to a universal time code for all so we can concatenate.
Swan_River_1830_1875['Date'] = pd.to_datetime(Swan_River_1830_1875['Unnamed: 0'],format="%Y/%m/%d")
Swan_River_1830_1875.set_index('Date', inplace=True)

Column_Name = list(Swan_River_1830_1875)

for i in (1,range(Column_Name)):
    Date_Time_{}.format(Column_Name[i] =Swan_River_1830_1875[Column_Name[i]]

                    