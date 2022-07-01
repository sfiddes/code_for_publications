# Functions for analysis
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
import numpy as np

#*******************************************************************************************************

# Create simple time series 
def create_time(date1,date2,freq='MS'):
        return [i for i in pd.date_range(start=date1, end=date2, freq=freq)]

# chop colourmap (taken from https://stackoverflow.com/questions/18926031/how-to-extract-a-subset-of-a-colormap-as-a-new-colormap-in-matplotlib)
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

#*******************************************************************************************************

# Simple plotting funciton 
def plot_biases(data,label,subplot,vmin,vmax,cmap='RdBu_r',norm='Norm',line='yes',cbar=False,sea='Ann'):
    if norm == 'Norm':
        norm = matplotlib.colors.Normalize(vmin=vmin,vmax=vmax)
    if isinstance(subplot,int):
        ax = plt.subplot(subplot, projection=ccrs.Orthographic(140, -90))
    else: 
        ax = plt.subplot(subplot[0],subplot[1],subplot[2], projection=ccrs.Orthographic(140, -90))
        
    p = data.plot(
                cmap=cmap,
                transform=ccrs.PlateCarree(),
                ax = ax,
                norm=norm,
                add_colorbar=False,
                );
    ax.coastlines();
    plt.title('')
    plt.title(label,loc='left')
    
    if line=='yes':
        plot_line(sea=sea)
        
    if cbar==True: 
        plt.colorbar(p,orientation='horizontal',pad=0.05)
    return p


# Add latitudinal lines to plots 
def plot_line(col='black',sea='Ann'):
    ln = np.arange(0,360,1)
    lt = np.zeros(360)
    
    if sea != 'Ann':
        SIC = xr.open_dataset('/g/data/p66/slf563/OBS/SSTS-SIC/MODEL.ICE.HAD187001-198110.OI198111-202008.nc')
        # sea ice data from https://gdex.ucar.edu/dataset/158_asphilli.html
        SIC = SIC.sel(time=slice('2015','2019')).SEAICE
        SIC = SIC.groupby('time.season').mean()
        
        plt.contour(SIC.lon,SIC.lat,SIC.sel(season=sea),[15],
                colors='goldenrod',transform=ccrs.PlateCarree())
    
    lt[:] = -69    
    plt.plot(ln, lt,
         color=col, linewidth=1,linestyle=':',
         transform=ccrs.PlateCarree(),)
    
    lt[:] = -43
    plt.plot(ln, lt,
         color=col, linewidth=1,linestyle=':',
         transform=ccrs.PlateCarree(),)
    
    lt[:] = -58
    plt.plot(ln, lt,
         color=col, linewidth=1,linestyle=':',
         transform=ccrs.PlateCarree(),)
    
    lt[:] = -30
    plt.plot(ln, lt,
         color=col, linewidth=1,linestyle=':',
         transform=ccrs.PlateCarree(),)

#*******************************************************************************************************