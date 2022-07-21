'''PART 2'''
'''
VICTORIA DROUGHT FUNCTIONS
'''
#%%Extract_Map_Shape
def Extract_Map_Shape(Data, ShapeFile):
    '''
    This is to extract the shape of the xarray dataset using a ShapeFile.
    
    Data: This is the xarray .nc file to be used
    ShapeFile: This is the .shp file to be used 
    '''    
    
    
    import pandas as pd, numpy as np, xarray as xr, dask, geopandas as gpd, rasterio as rio, matplotlib.pyplot as plt, rioxarray
    from shapely.geometry import mapping 
    
    # Mask the Data
    Data.rio.set_spatial_dims(x_dim="lon", y_dim="lat", inplace=True)
    Data.rio.write_crs("epsg:4326",inplace=True)

    # Clip the Data into the Shape from the .shp file used
    Data_Shape = Data.rio.clip(ShapeFile.geometry.apply(mapping), Data.rio.crs,drop=True)
    Data_Shape = Data_Shape.where(Data_Shape>=0,drop=True)
    
    
    return(Data_Shape)



#%%Month_Year_MovingAve_Location_Spec
def Month_Year_MovingAve_Location_Spec(data, Latitude, Longitude, Period, town_name):
    '''
    This function uses the location of a place with latitude and longititude coordinations
    with the nearest grid box of data to be used in calculating the moving means of: 
    a) Standardised Moving Mean of Annual Precipiation
    b) Moving Mean of the Seasonal Precipitation
    The data has to be in a netCDF format with latitude and longitude coordinates, in this 
    version the Data was found in the Australian Gridded Climate Data (AGCD) file on the NCI.
    The moving mean will be centred on the specified period.
    
    
    data: netCDF dataset (AGCD)
    Latitude: North\South plane, using negatives to define South direction
    Longitude: East\West plane, using negatives to define West direction
    Period: Timelength of the moving mean to be calculated (Years)
    town_name:  Name of location to observe
    '''
    #Import Packages That Will Be Useful
    import pandas as pd, numpy as np,xarray as xr, dask,geopandas as gpd, matplotlib.pyplot as plt, statistics, csv
    from datetime import datetime
    
    #Define a font for the graphs.
    plt.rcParams["font.family"] = 'sans-serif'
    
    
    #------------------------------STANDARDISED YEARLY MOVING MEAN------------------------#
    #Extract annual precipitation for each year.
    RAW_Annual_Precip = data.resample(time='AS-JAN').sum(dim='time')
    RAW_Annual_Precip = RAW_Annual_Precip[1:len(RAW_Annual_Precip)-1]
    #Remove negative values defined in the Moving Mean script that define the edge of the shape extracted from the shapefile function.
    Annual_Precip_Fixed =RAW_Annual_Precip.where(RAW_Annual_Precip>=0)
    
    
    #Define the location using latitude and longitude
    Precip_Totals =Annual_Precip_Fixed.sel(lat=Latitude,lon=Longitude, method='nearest')
    
    #Generate the precipitation mean of the location.
    Precip_Mean= Precip_Totals.mean(dim='time')
    
    #Generate the Anomoly using the annual precipiation and mean.
    Anomoly = Precip_Totals -  Precip_Mean    
    
    #Create a standard devation for the anomoly.
    stdev = Anomoly.std()
    
    #Standardise the anomoly by dividing it by the standard deviation
    Standardised = Anomoly/stdev
    
    #Generate the Moving Mean with the standardised data centred and using the Period defined.
    Moving_Mean = Standardised.rolling(time=Period,center=True).mean()
    
    #A degree unit used in the plot's title
    degs = u"\N{DEGREE SIGN}"
    
    
    #Plot the Standardised Moving Mean
    plt.figure(1)
    fig,ax = plt.subplots(figsize = (11,7))
    ax.plot(Standardised['time'],Moving_Mean, label = r"{}-Year Moving Mean".format(Period))
    ax.plot(Standardised['time'],Standardised, label = r"Annual Standardised Score",linestyle = 'None',marker = '.',markersize = '8')
    ax.legend(loc=0)
    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.set_title("{}-Year Moving Mean Of Annual Standardised Precipitation: {} ({}{}, {}{})". format(Period,town_name,Latitude,degs, Longitude,degs),fontname="Sans-serif", size=14,fontweight="bold")
    ax.set_xlabel('Date',fontname="Sans-serif", size=12)
    ax.set_ylabel('Standardised Precipitation Score',fontname="Sans-serif", size=12)
    #These are the defined drought periods that are shaded on the plot.
    ax.axvspan(datetime(1895,1,1),datetime(1902,1,1), color = 'lightgray')
    ax.axvspan(datetime(1937,1,1),datetime(1945,1,1), color = 'lightgray')
    ax.axvspan(datetime(1997,1,1),datetime(2009,1,1), color = 'lightgray')
    ax.axvspan(datetime(2013,1,1),datetime(2019,1,1), color = 'lightgray')
    
    #Save the figure
    plt.savefig(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\Images\Moving Mean Specific Location\Moving Mean Yearly {}.tif".format(town_name), dpi=300, bbox_inches='tight')
    
    
    
    
    #--------------------------------------- SEASONAL MOVING MEAN------------------------#
    
    #Create a figure that creates 5 equally sized plots to be used to plot the seasonal data.
    plt.figure(2)
    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, figsize=(10,25), sharex=True,sharey=True)
    
    #Create a list which define the seasons in order to extract the seasonal data from the resampled seasonal dataset. 
    list = ['DJF','MAM','JJA','SON']

    #Resampling the data into seasonal data where Q-MAY signifies the end of the seasonal period, so it starts in March and Finishes in May. Then extends into doing quartely with all the other seasons.
    #Note: Summer season calculate the December of year n-1 into January and February of year n.
    
    #Secondly it also sums the precipitation of the 3 months so it is the seasonal precipitation.
    Seasonal_Precip = data.resample(time='Q-MAY').sum()
    
    #Grouping the datasets to easily extract the seasons by the list with seasons.
    Seasonal_Groups=Seasonal_Precip.groupby('time.season')
    
    #Remove the negative values that are that define the shape of region.
    Seasonal_Precip_Fixed = Seasonal_Precip.where(Seasonal_Precip>=0)

    #This plots the moving mean and the individual events for ALL seasons using the the Period multiplied by 4 due to 4 seasons in a year for the specific location.
    ax1.plot(Seasonal_Precip_Fixed['time'],Seasonal_Precip_Fixed.sel(lat=Latitude,lon=Longitude,method='nearest').rolling(time=int(Period)*4, center = True).mean(), color = 'black',label = r"Seasonal {}-Year Moving Mean".format(Period))
    ax1.plot(Seasonal_Precip_Fixed['time'],Seasonal_Precip_Fixed.sel(lat=Latitude,lon=Longitude,method='nearest'), color = 'black',label = r"Seasonal Total", linestyle = 'None',marker='.',markersize = '2')
    ax1.grid(True, which='both')
    ax1.set_xlabel('Date',fontname="Sans-serif", size=12)
    ax1.set_ylabel('Seasonal Precipitation (mm)',fontname="Sans-serif", size=12)
    ax1.set_title('{}-Year Moving Mean Of Seasonal Precipitation: {} ({}{}, {}{})'. format(Period,town_name,Latitude,degs, Longitude,degs),fontname="Sans-serif", size=16,fontweight="bold")
    ax1.legend(loc=0)
    #These are the defined drought periods that are shaded on the plot.
    ax1.axvspan(datetime(1895,1,1),datetime(1902,1,1), color = 'lightgray')
    ax1.axvspan(datetime(1937,1,1),datetime(1945,1,1), color = 'lightgray')
    ax1.axvspan(datetime(1997,1,1),datetime(2009,1,1), color = 'lightgray')
    ax1.axvspan(datetime(2013,1,1),datetime(2019,1,1), color = 'lightgray')
    
    #Now create a list of the other 4 plots that will be used for the individual seasons.
    Q = [ax2, ax3, ax4, ax5]
    #List of the colours for each season, they are supposed to represent a colour that matches the season.
    COLOUR = ['orange', 'brown', 'blue', 'green']
    #List of the season names
    SEASON_NAME = ['Summer','Autumn','Winter','Spring']

    #This is the for loop to generate the moving mean for  years for each season with the specified period.
    for i in range(0,4):
        #Remove the negative values that are that define the shape of region.
        Seasonal_Groups_Season=Seasonal_Groups[list[i]].where(Seasonal_Groups[list[i]]>=0)
        #This plots the moving mean and the individual events for A SPECIFIC season using the the Period for the specific location.
        Q[i].plot(Seasonal_Groups_Season['time'],Seasonal_Groups_Season.sel(lat=Latitude,lon=Longitude,method='nearest').rolling(time=int(Period), center = True).mean(),color = '{}'.format(COLOUR[i]),label = r"{}-Year Moving Mean".format(Period)) 
        Q[i].plot(Seasonal_Groups_Season['time'],Seasonal_Groups_Season.sel(lat=Latitude,lon=Longitude,method='nearest'),color = '{}'.format(COLOUR[i]),label = r"Seasonal Precipitation",linestyle = 'None',marker = '.',markersize = '2')
        Q[i].set_title(SEASON_NAME[i], fontname="Sans-serif", size=15,fontweight="bold")
        Q[i].grid(True, which='both')
        Q[i].set_xlabel('Date',fontname="Sans-serif", size=12)
        Q[i].set_ylabel('Seasonal Precipitation (mm)',fontname="Sans-serif", size=12)
        Q[i].legend(loc=0)
        #These are the defined drought periods that are shaded on the plot.
        Q[i].axvspan(datetime(1895,1,1),datetime(1902,1,1), color = 'lightgray')
        Q[i].axvspan(datetime(1937,1,1),datetime(1945,1,1), color = 'lightgray')
        Q[i].axvspan(datetime(1997,1,1),datetime(2009,1,1), color = 'lightgray')
        Q[i].axvspan(datetime(2013,1,1),datetime(2019,1,1), color = 'lightgray')
        
    #Save the plot generated    
    plt.savefig(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\Images\Moving Mean Specific Location\Moving Mean Seasonally {}.tif".format(town_name), dpi=300, bbox_inches='tight')
    return (plt.figure(1),plt.figure(2))



#%%Month_Year_MovingAve_Region_Spec
def Month_Year_MovingAve_Region_Spec(Region, data, Period):
    '''
    This is a function that uses uses the location of a specific place to
    create a moving mean of time both annually and monthly. By stating the data to use
        which must be a netCDF file format and stating the location (lat,lon)
    of where you want to look at and the time period(period) for the moving mean to work on it will generate
    plots both throughout all the periods or during each of the seasonal periods which will
    generate a unique take on the periods.
    
    This function uses the location of a region that will be averaged to calculate the moving means of: 
    a) Standardised Moving Mean of Annual Precipiation
    b) Moving Mean of the Seasonal Precipitation
    The data has to be in a netCDF format with latitude and longitude coordinates, in this 
    version the Data was found in the Australian Gridded Climate Data (AGCD) file on the NCI.
    The moving mean will be centred on the specified period.
    
    
    Region:  Name of region
    data: netCDF dataset (AGCD).
    Period: Timelength of the moving mean to be calculated (Years)
    '''
    #Import Packages That Will Be Useful
    import pandas as pd, numpy as np,xarray as xr, dask,geopandas as gpd, matplotlib.pyplot as plt, statistics, csv
    from datetime import datetime
    
    #Define a font for the graphs.
    plt.rcParams["font.family"] = 'sans-serif'
    
    #------------------------------STANDARDISED YEARLY MOVING MEAN------------------------#
    #Extract annual precipitation for each year.
    
    RAW_Annual_Precip = RAW_Annual_Precip[1:len(RAW_Annual_Precip)-1]
    #Remove negative values defined in the Moving Mean script that define the edge of the shape extracted from the shapefile function.
    Annual_Precip_Fixed =RAW_Annual_Precip.where(RAW_Annual_Precip>=0)
    
    #Using the region data, generate the mean of the region for each year.
    Precip_Totals =Annual_Precip_Fixed.mean(dim =('lon','lat'))
    
    #Using the yearly region mean, generate the mean of the entire time period.
    Precip_Mean= Precip_Totals.mean(dim='time')
    
    #Generate the Anomoly using the annual precipiation and mean.
    Anomoly = Precip_Totals -  Precip_Mean
    
    #Create a standard devation for the anomoly.
    stdev = Anomoly.std()
    
    #Standardise the anomoly by dividing it by the standard deviation
    Standardised= Anomoly/stdev
    
    #Generate the Moving Mean with the standardised data centred and using the Period defined.
    Moving_Mean = Standardised.rolling(time=Period,center=True).mean()
       
    #Plot the Standardised Moving Mean
    plt.figure(1)
    fig,ax = plt.subplots(figsize=(11,6))
    ax.plot(Standardised['time'],Moving_Mean, label = r"{}-Year Moving Mean".format(5))
    ax.plot(Standardised['time'],Standardised,label = r"Standardised Score",linestyle = 'None',marker = '.',markersize = '8')
    ax.legend(loc=0)
    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.set_title("{}-Year Moving Mean Of Annual Standardised Precipitation: {}". format(Period,Region),fontname="Sans-serif", size=14,fontweight="bold")
    ax.set_xlabel('Date',fontname="Sans-serif", size=12)
    ax.set_ylabel('Standardised Precipitation Score',fontname="Sans-serif", size=12)
    #These are the defined drought periods that are shaded on the plot.
    ax.axvspan(datetime(1895,1,1),datetime(1902,1,1), color = 'lightgray')
    ax.axvspan(datetime(1937,1,1),datetime(1945,1,1), color = 'lightgray')
    ax.axvspan(datetime(1997,1,1),datetime(2009,1,1), color = 'lightgray')
    ax.axvspan(datetime(2013,1,1),datetime(2019,1,1), color = 'lightgray')
   
    #Save the figure
    plt.savefig(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\Images\Moving Mean Region\Moving Mean Yearly {}.tif".format(Region), dpi=300, bbox_inches='tight')
    
    #--------------------------------------- SEASONAL MOVING MEAN------------------------#
    
    #Create a figure that creates 5 equally sized plots to be used to plot the seasonal data.
    plt.figure(2)
    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, figsize=(10,25), sharex=True,sharey=True)
    
    #Create a list which define the seasons in order to extract the seasonal data from the resampled seasonal dataset. 
    list = ['DJF','MAM','JJA','SON']

    #Resampling the data into seasonal data where Q-MAY signifies the end of the seasonal period, so it starts in March and Finishes in May. Then extends into doing quartely with all the other seasons.
    #Note: Summer season calculate the December of year n-1 into January and February of year n.
    
    #Secondly it also sums the precipitation of the 3 months so it is the seasonal precipitation.
    Seasonal_Precip = data.resample(time='Q-MAY').sum()
    
    #Grouping the datasets to easily extract the seasons by the list with seasons.
    Seasonal_Groups=Seasonal_Precip.groupby('time.season')
    
    
    #Remove the negative values that are that define the shape of the region.
    Seasonal_Precip_Fixed = Seasonal_Precip.where(Seasonal_Precip>=0)
    
    #This plots the moving mean and the individual events for ALL seasons using the the Period multiplied by 4 due to 4 seasons in a year for the region.
    ax1.plot(Seasonal_Precip_Fixed['time'],Seasonal_Precip_Fixed.mean(dim=('lat','lon')).rolling(time=int(Period)*4, center = True).mean(), color = 'black',label = r"Seasonal {}-Year Moving Mean".format(Period))
    ax1.plot(Seasonal_Precip_Fixed['time'],Seasonal_Precip_Fixed.mean(dim=('lat','lon')), color = 'black',linestyle = 'None',label = r"Seasonal Total", marker='.',markersize = '2')
    ax1.grid(True, which='both')
    ax1.set_xlabel('Time',fontname="Sans-serif", size=12)
    ax1.set_ylabel('Seasonal Precipitation',fontname="Sans-serif", size=12)
    ax1.set_title('{}-Year Moving Mean Of Seasonal Precipitation: {}'. format(Period,Region),fontname="Sans-serif", size=16,fontweight="bold")
    ax1.legend(loc=0)
    
    #These are the defined drought periods that are shaded on the plot.
    ax1.axvspan(datetime(1895,1,1),datetime(1902,1,1), color = 'lightgray')
    ax1.axvspan(datetime(1937,1,1),datetime(1945,1,1), color = 'lightgray')
    ax1.axvspan(datetime(1997,1,1),datetime(2009,1,1), color = 'lightgray')
    ax1.axvspan(datetime(2013,1,1),datetime(2019,1,1), color = 'lightgray')
    
    
    #Now create a list of the other 4 plots that will be used for the individual seasons
    Q = [ax2, ax3, ax4, ax5]
    #List of the colours for each season, they are supposed to represent a colour that matches the season.
    COLOUR = ['orange', 'brown', 'blue', 'green']
    #List of the season names
    SEASON_NAME = ['Summer','Autumn','Winter','Spring']
    
    #This is the for loop to generate the moving mean for  years for each season with the specified period.
    for i in range(0,4):
        #Remove the negative values that are that define the shape of region.
        Seasonal_Groups_Season=Seasonal_Groups[list[i]].where(Seasonal_Groups[list[i]]>=0)
        ##This plots the moving mean and the individual events for A SPECIFIC season using the the Period for the specific location.
        Q[i].plot(Seasonal_Groups_Season['time'],Seasonal_Groups_Season.mean(dim=('lat','lon')).rolling(time=int(Period), center = True).mean(),color = '{}'.format(COLOUR[i]),label = r"{}-Year Moving Mean".format(Period)) 
        Q[i].plot(Seasonal_Groups_Season['time'],Seasonal_Groups_Season.mean(dim=('lat','lon')),color = '{}'.format(COLOUR[i]),marker='.',label = r"Seasonal Precipitation",linestyle = 'None',markersize = '2') 
        Q[i].set_title(SEASON_NAME[i], fontname="Sans-serif", size=15,fontweight="bold")
        Q[i].grid(True, which='both')
        Q[i].set_xlabel('Date',fontname="Sans-serif", size=12)
        Q[i].set_ylabel('Seasonal Precipitation (mm)',fontname="Sans-serif", size=12)
        Q[i].legend(loc=0)
        #These are the defined drought periods that are shaded on the plot.
        Q[i].axvspan(datetime(1895,1,1),datetime(1902,1,1), color = 'lightgray')
        Q[i].axvspan(datetime(1937,1,1),datetime(1945,1,1), color = 'lightgray')
        Q[i].axvspan(datetime(1997,1,1),datetime(2009,1,1), color = 'lightgray')
        Q[i].axvspan(datetime(2013,1,1),datetime(2019,1,1), color = 'lightgray')
    
    #Save the plot generated   
    plt.savefig(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\Images\Moving Mean Region\Moving Mean Seasonally {}.tif".format(Region), dpi=300, bbox_inches='tight')
        
    
    return (plt.figure(1),plt.figure(2))


 

#%%summingthing
def summingthing(x):
    '''

    Parameters
    ----------
    x : the data that will need to be summed

    Returns
    -------
    Sum of the data by the time period

    '''
    return x.sum(dim='time', skipna = True)




#%%Moving_Average_Yearyly
def Moving_Average_Yearyly(DATA,period):
    '''
    

    Parameters
    ----------
    DATA : Data to be used within the function.
    period : its the specified moving mean.

    Returns
    -------
    DATA4 : A moving mean for a specified period.

    '''
    
    #Groups the data into boxes of years
    DATA1 = DATA.groupby("time.year")
    #Uses the summingthing function to get the total rainfall for the year
    DATA2 = DATA1.map(summingthing)
    #Does a rolling average of the entire year for the entire region.
    DATA3 =DATA2.where(DATA2>0).mean(dim =('lon','lat'), skipna = True)
    #Does a moving mean of the specified period of the entire year for the entire region.
    DATA4= DATA3.rolling(year = period,center=True).mean()
    return DATA4



 
#%%Drought_Period
def Drought_Period(Region_Name, dataset, datashape, start_YEAR, end_YEAR,standard_Score_Lower,standard_Score_Upper):
    '''
    

    Parameters
    ----------
    Region_Name : The region you are looking at (Used in title)
    dataset : xarray netCDF file
        Set of data to be used within the function of the region
    datashape : .shp file (shape file)
        The shape file of the region you are looking at
    start_YEAR : float64
        Year that is determined to start from
    end_YEAR : float64
        Year that is determined to finish at
    standard_Score_Lower : float64
        Generates the lower bound of the normalised standardised score for the precipitation..
    standard_Score_Upper : float64
        Generates the upper bound of the normalised standardised score for the precipitation.
    File_Path: Place where the image will be saved
    Returns
    -------
    A set of pages displaying 5 high resolution maps that have the annual standarised precipitation for that region from December of the previous year to December the current year and
    a set of 4 smaller plots illustrating the seasonal values within this range.

    '''
    #Define the packages that are useful
    import pandas as pd, numpy as np,xarray as xr, dask,geopandas as gpd, matplotlib.pyplot as plt, statistics, csv
    from pysal.lib import cg as geometry
    import matplotlib.gridspec as gridspec
    
    #Define the font that will be used.
    plt.rcParams["font.family"] = 'sans-serif'
    
    
    #----------------------Standardised Yearly Precipitation-----------------#
    #Resample into yearly and make sure to offset this by 1 month so it becomes Dec[year-1] to Dec[Year]
    Yearly_Vic = dataset.resample(time='AS-DEC').sum()
    
    #Extract the values only wthin the shape by removing the negative values that were used inplace of NaNs
    Yearly_Vic= Yearly_Vic.where(Yearly_Vic>=0)
    
    
    #Generate a mean for each individual gridpoint in the region.
    Mean_Total_Vic_Y = Yearly_Vic.mean(dim='time')
    
    #Generate the Anomoly for each individual gridpoint in the region.
    Anom_Rain_Y = Yearly_Vic -  Mean_Total_Vic_Y
    
    #Generate the standard devitation for each individual gridpoint in the region.
    Rain_STD_Y = Anom_Rain_Y.std()
    
    #Create the yearly standardised data by dividing the anomoly by the standard deviation at each individual gridpoint in the region.
    Standardised_Y= Anom_Rain_Y/Rain_STD_Y
    
    #------------------Standardised Seasonal Precipitation------------------#
    #Resampling the data into seasonal data where QS-DEC signifies the start of the seasonal period aka Summer, so it starts in December and Finishes in Febuarary. Then extends into doing quartely with all the other seasons.
    #Note: Summer season calculate the December of year n-1 into January and February of year n.
    
    #Secondly it also sums the precipitation of the 3 months so it is the seasonal precipitation.
    SEASONAL_DATA_ST_MAR = dataset.resample(time='QS-DEC').sum()
    
    #Grouping the datasets to easily extract the seasons by the list with seasons.
    SD=SEASONAL_DATA_ST_MAR.groupby('time.season')
    
    #Generate the Seasonal list
    list = ['DJF','MAM','JJA','SON']
    
    #This sets the miminum year from the yearly plot that will be used to find the seasonal plots.
    zerovalue_setter=Standardised_Y['time.year'].min()
    
    #This is the range and it goes up to and including the end_Year value (hence why +1 is included)
    Q=range(start_YEAR,end_YEAR+1,1)
        
        
    #Generate the plots in this for loop for each year that is specified.    
    for i in Q:
        Tlist = ['Summer: D({}) JF({})'.format(i-1,i),'Autumn: MAM({})'.format(i),'Winter: JJA({})'.format(i),'Spring: SON({})'.format(i)]
        #Create a skeleton of a figure to be filled by all the plots
        fig = plt.figure(figsize=(15,6))
        #Title of the plot
        fig.suptitle('Map Of Standardised Precipitation: {} (01/DEC/{} to 30/NOV/{})'.format(Region_Name,i-1,i),fontname="Sans-serif", size=21,fontweight="bold") 
        #Setup axes
        gs = gridspec.GridSpec(2,4)
        axs = {}
        axs['Annual'] = fig.add_subplot(gs[:,:2])
        axs['DJF'] = fig.add_subplot(gs[0,2])
        axs['JJA'] = fig.add_subplot(gs[1,2])
        axs['MAM'] = fig.add_subplot(gs[0,3])
        axs['SON'] = fig.add_subplot(gs[1,3])
        
        #Disable axis ticks
        for ax in axs.values():
            ax.tick_params(bottom=False, labelbottom=False, left=False, labelleft=False)
            
        #Add titles
        for name, ax in axs.items():
            ax.set_title(name,fontname="Sans-serif", size=14)
            
        #This is how the index is achieved going from 0 to the length for the seasonal maps.
        Setter = i - zerovalue_setter - 1
        
        #Add Standardised Annual Precipiation Plot to the largest map on the page
        Standardised_Y[Setter].plot(cmap='RdBu',vmin=standard_Score_Lower,vmax=standard_Score_Upper,ax=axs['Annual'], add_labels=False, add_colorbar='Right')
        axs['Annual'].set_facecolor('xkcd:black')
        
        #This is the for loop for each of the individual seasons.
        for a in range(0,4):
            #Extract the values only wthin the shape by removing the negative values that were used inplace of NaNs.
            SDI=SD[list[a]].where(SD[list[a]]>=0)
    
            #Generate a mean for each individual gridpoint in the region for that specific season.
            Mean_Total_Vic_S = SDI.mean(dim='time')
        
            #Generate the Anomoly for each individual gridpoint in the region for that specific season.
            Anom_Rain_S = SDI -  Mean_Total_Vic_S
            
            #Generate the standard devitation for each individual gridpoint in the region for that specific season.
            Rain_STD_S = Anom_Rain_S.std()
            
            #Create the seasonal standardised data by dividing the anomoly by the standard deviation at each individual gridpoint in the region.
            Standardised_S= Anom_Rain_S/Rain_STD_S
            
            #Seasonal Normalised map added that will fill the page of plots.
            Standardised_S[Setter].plot(cmap='RdBu',vmin=standard_Score_Lower,vmax=standard_Score_Upper,ax=axs[list[a]], add_labels=False, add_colorbar=False)
            axs[list[a]].set_facecolor('xkcd:black')
            axs[list[a]].set_title(Tlist[a])
            
    #Save the plots (gifs use JPEG and tifs are used for the website)   
        plt.savefig(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\Images\Gifs Folder for Drought Periods\{}{}.jpeg".format(Region_Name,i), dpi=300, bbox_inches='tight')
           
          
#%%Consecutive Days
def Number_Wet_Days_Precip(Data,Rolling,Town_Name,Day_Rain):
    '''

    Parameters
    ----------
    Data : CSV
        A file of daily precipiation for the specific location.
    Rolling : Yearly
        Used for the moving mean.
    Town_Name : Used in the title of the plot
        Place where precipitation was extracted for.
    Day_Rain : Precipitation (mm) exceedence 
        Total daily precipitation that it must exceed to be counted as a wet day.

    Returns
    -------
    Plot
        It shows a plot of the yearly count of wet days and the moving mean.

    '''
    #Import useful packages.
    import pandas as pd, numpy as np,xarray as xr, matplotlib.pyplot as plt, statistics, csv
    from datetime import datetime
    
    #Define the font
    plt.rcParams["font.family"] = 'sans-serif' 
    
    #Create a datetime index for the data
    cols=["Year","Month","Day"]
    Data['date'] = Data[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")
    Data['date'] = pd.to_datetime(Data['date'])#,format="%Y/%m/%d")
    Data.set_index('date', inplace=True)
    
   #Group the data into yearly datasets
    Yearly = [g for n, g in Data.groupby(pd.Grouper(freq='Y'))]
    
    #Since its group and cannot use the yearly to extract the data we must use a index of 0 to ranger in order for the for loop to work
    Max_Y = Data['Year'].max()
    Min_Y = Data['Year'].min()
    ranger =Max_Y - Min_Y 

    #Create vectors to add the number of wet days per year and the year it happened.
    Yearly_Count_Wet_Days = []
    Yearly_Count_Wet_Days_Date = []

     
    #This for loop extracts the precipitation data for each year and calculates the number of days in that year it exceeded a certina Day_Rain value.
    for p in range(0,ranger):
        Yearly_Data = Yearly[p]
        i = 0
        ran =int(len(Yearly_Data))
        for q in range(0,ran,1):
            if Yearly_Data['Rainfall amount (millimetres)'][q]>=Day_Rain:
                i = i+1
            else:
                i = i
                
        Yearly_Count_Wet_Days_Date.append(p+Min_Y)
        Yearly_Count_Wet_Days.append(i)

    #Concatenate the two vectors produced within the for loop
    Yearly_Wet = pd.concat([pd.Series(Yearly_Count_Wet_Days_Date,name = 'Year'), pd.Series( Yearly_Count_Wet_Days,name='Wet Days')], axis=1)


    #Plot the moving mean and the individual annual wet days
    plt.figure(1)
    plt.plot(Yearly_Wet['Year'],Yearly_Wet['Wet Days'],linestyle = 'None',marker = '.',markersize = '2')
    plt.plot(Yearly_Wet['Year'],Yearly_Wet['Wet Days'].rolling(Rolling,center=True).mean())
    plt.title('{} Annual Wets Days (>={}mm)'.format(Town_Name,Day_Rain), fontname="Sans-serif", size=15,fontweight="bold")
    plt.grid(True, which='both')
    plt.xlabel('Date',fontname="Sans-serif", size=12)
    plt.ylabel('Wet Days',fontname="Sans-serif", size=12)
    plt.legend(loc=0)   
    #These are the specified drought periods.
    plt.axvspan(1895,1902, color = 'lightgray')
    plt.axvspan(1937,1945, color = 'lightgray')
    plt.axvspan(1997,2009, color = 'lightgray')
    plt.axvspan(2013,2019, color = 'lightgray')
    
    #Save the plot
    #plt.savefig(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\Images\Moving Mean Specific Location\Moving Mean Seasonally {}.tif".format(Town_Name), dpi=300, bbox_inches='tight')

    return (plt.figure(1))


#%%Wet Spells
def Wet_Spells(Data,Rolling,Town_Name,Consec_Wet,Day_Rain):
    '''
    

    Parameters
    ----------
    Data : CSV
        A file of daily precipiation for the specific location.
    Rolling : Yearly
        Used for the moving mean.
    Town_Name : Used in the title of the plot
        Place where precipitation was extracted for.
    Consec_Wet : Number of days
        Defined as when the precipiation exceedence occurs more then Consec_Wet or more it counts as a wet period.
    Day_Rain : Precipitation (mm) exceedence 
        Total daily precipitation that it must exceed to be counted as a wet day.

    Returns
    -------
    Plot
        It shows a plot of the yearly count of consecutive wet periods and the moving mean of this.

    '''
    #Import packages that are useful.
    import pandas as pd, numpy as np,xarray as xr, matplotlib.pyplot as plt, statistics, csv
    
    #Define font
    plt.rcParams["font.family"] = 'sans-serif'    
    
    #Group the data into yearly
    Data_Year = [g for n, g in Data.groupby(pd.Grouper(freq='Y'))]
    
    #Since its group and cannot use the yearly to extract the data we must use a index of 0 to ranger in order for the for loop to work
    Max_Y = Data['Year'].max()
    Min_Y = Data['Year'].min()
    ranger =Max_Y - Min_Y

    #Create vectors to add the number of wet days per year and the year it happened.
    Yearly_Count_Wet_Spells = []
    Yearly_Count_Wet_Spells_Date = []
     
    #This for loop extracts the precipitation data for each year and calculates the number of consecutive periods in that year it exceeded a certin Day_Rain value.
    for p in range(0,ranger):
        Yearly_Data = Data_Year[p]
        CountCOND = 0
        WetSpell = 0
        
        for i in range(len(Yearly_Data)):
            if Yearly_Data['Rainfall amount (millimetres)'][i]>=Day_Rain:
                CountCOND = CountCOND+1
            else:
                if CountCOND>=Consec_Wet:
                    WetSpell = WetSpell+1
                    CountCOND = 0
                else:
                    CountCOND = 0
        Yearly_Count_Wet_Spells_Date.append(p+Min_Y)
        Yearly_Count_Wet_Spells.append(WetSpell)   
    
        
    
    
    #Concatenate the two vectors produced within the for loop
    Yearly_Consec = pd.concat([pd.Series(Yearly_Count_Wet_Spells_Date,name = 'Year'), pd.Series( Yearly_Count_Wet_Spells,name='Consecutive Wet Days')], axis=1)

    #Plot the moving mean and the individual annual wet days
    plt.figure(1)
    plt.plot(Yearly_Consec['Year'],Yearly_Consec['Consecutive Wet Days'],linestyle = 'None',marker = '.',markersize = '2')
    plt.plot(Yearly_Consec['Year'],Yearly_Consec['Consecutive Wet Days'].rolling(Rolling,center=True).mean())
    plt.title('{} Annual Consecutive Wet Days ({}+ Days of >={}mm)'.format(Town_Name,Consec_Wet,Day_Rain), fontname="Sans-serif", size=15,fontweight="bold")
    plt.grid(True, which='both')
    plt.xlabel('Date',fontname="Sans-serif", size=12)
    plt.ylabel('Annual Consecutive Wet Days',fontname="Sans-serif", size=12)
    plt.legend(loc=0)   
    #These are the specified drought periods.
    plt.axvspan(1895,1902, color = 'lightgray')
    plt.axvspan(1937,1945, color = 'lightgray')
    plt.axvspan(1997,2009, color = 'lightgray')
    plt.axvspan(2013,2019, color = 'lightgray')
    
    #Save the plot
    #plt.savefig(r"D:\LIBRARY\UNIVERSITY\SUMMER 2021-22\Images\Moving Mean Specific Location\Moving Mean Seasonally {}.tif".format(Town_Name), dpi=300, bbox_inches='tight')
    
    return (plt.figure(1))
#%%ComparisonCount/Consec
def Comp_Count_Consec_Wet(Data,Rolling,Town_Name,Consec_Wet,Day_Rain):
    import pandas as pd, numpy as np,xarray as xr, matplotlib.pyplot as plt, statistics, csv
    





































    return(plt.figure())
    
#%%Location Specific Correlation Seasons
def Loc_Spec_Corr_Seasons(data, Latitude, Longitude, town_name,Season_1,Season_2):
    #Resampling the data into seasonal data where Q-MAY starts that the quartely ends in MAY and starts in March that simulates Autumn, and this
    #continues to do this for each season. Secondly it also sums the precipitation of the 3 months so it is the total seasonal precipitation.
    SEASONAL_DATA_ST_MAR = data.resample(time='Q-MAY').sum()
    
    #Grouping the datasets so I can easily extract the seasons by the list stated above.
    SD=SEASONAL_DATA_ST_MAR.groupby('time.season')    
    
    Seasonal_Data_1=SD[Season_1]
    Seasonal_Data_2= SD
    


