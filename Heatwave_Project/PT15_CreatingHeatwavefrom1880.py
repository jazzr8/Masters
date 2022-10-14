#%%Pt 14 Putting Full Record Together
import pandas as pd
#BOM PERTH REGIONAL OFFICE
Perth_Temperature = pd.read_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\Perth_Max_Min_1880_2021.csv")
Perth_Temperature.to_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Analysis\Heatwave Events\Perth_1880_2021.csv")
#Clean Data
Perth_Temperature['date']= pd.to_datetime(Perth_Temperature[['Day', 'Month', 'Year']], format('%d/%m/%y %H:%M:%S'), dayfirst=True)

Perth_Temperature.columns.str.match("Unnamed")
Perth_Temperature = Perth_Temperature.loc[:,~Perth_Temperature.columns.str.match("Unnamed")]
del Perth_Temperature['Month']
del Perth_Temperature['Day']
del Perth_Temperature['Year']

pd.to_datetime(df['date'], format('%d/%m/%y %H:%M:%S'), dayfirst=True).apply(lambda x: dt.datetime.strftime(x, '%m/%d/%y %H:%M:%S'))

pd.to_datetime(Perth_Temperature['date']).apply(lambda x: Perth_Temperature.datetime.strftime(x, '%d/%m/%y %H:%M:%S'))
Perth_Temperature = Perth_Temperature.set_index('date')
Perth_Temperature.to_csv(r"D:\LIBRARY\UNIVERSITY\Masters Research\Python\Data\Perth_1880_2021.csv")
