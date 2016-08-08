# coding: utf-8

# In[ ]:

#import libraries

# Date time manipulation libraries
from time import strptime
from time import strftime

# download files
from ftplib import FTP     #conectarme a un ftp para conseguir los datos
import os

# Data-handling and plotting routines libraries
import pygrib    #para trabajar con archivos grib
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib as mpl

# Get handler for figure and setup colormap
def generate_figure():
    # Initiate figure
    # llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
    # are the lat/lon values of the lower left and upper right corners
    # of the map.
    # lat_ts is the latitude of true scale.
    # resolution = 'c' means use crude resolution coastlines.
    m = Basemap(projection='merc',llcrnrlat=-60,urcrnrlat=10,        llcrnrlon=360-85,urcrnrlon=360-30,lat_ts=20,resolution='c')
    # Draw coastlines, etc.
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    
    # Configure colormap
    cmap = plt.cm.jet
    
    return m, cmap
    
# Plot data 
def plot_data(fig_handler, x, y, data, cmap):

    # Latitude and longitudes projection
    x,y= np.meshgrid(x,y)
    x,y = fig_handler(x,y)

    # Plot
    cs = fig_handler.contourf(x,y,data[0,:,:]-273,cmap=cmap)
    
    # Configure colorbar
    cb = fig_handler.colorbar(cs,"right", size="5%", pad='2%')
    cb.set_label('°C')

# In[ ]:

# Abstract model class
class Model(object):
    # Constructor
    def __init__(self, initial_time, lead_time):
        self.initial_time = initial_time
        self.lead_time = lead_time

# CFS V2 subclass
class CFSV2(Model):
    # Constructor
    def __init__(self,initial_time, lead_time):
        Model.__init__(self,initial_time, lead_time)
    
    # Convert month name to month string number
    def get_datetime_object(self):
                       
        #creates month number as string
        self.initial_time = strftime('%m',strptime(self.initial_time,'%b'))
        
    # Download files 
    def download_files(self):
        URL = 'ftp.cpc.ncep.noaa.gov'
        directorio = '/NMME/clim'
        print ("Connecting FTP ")
        ftp = FTP(URL)     # connect to host, default port
        print("Log")
        ftp.login()  # user anonymous, passwd anonymous@ruta = 'ftp.cpc.ncep.noaa.gov'
        #genero nombre de archivo    
        nombre_archivo = 'tmpsfc.'+self.initial_time+'.CFSv2.clim.1x1.grb'
        # Downloads grib file
        ftp.cwd(directorio)   #ingreso al directorio      /NMME/clim/
        local_filename = os.path.join('data', nombre_archivo) #ruta para archivo que se escribe
        file = open(local_filename, 'wb')   #abro el archivo donde se va a alojar
        print("Writing GRIB file")
        ftp.retrbinary('RETR '+ nombre_archivo, file.write)  #recibo info y guardo en archivo
        file.close()       #cierro archivo
        ftp.quit()      # This is the “polite” way to close a connection  me voy del ftp
        return nombre_archivo
    
    # Extract data from grib and compute mean
    def extract_data (self, grib_file):
        # Opens file
        grbs=pygrib.open(os.path.join('data', grib_file))
        for grb in grbs:
            print (grb)  #print grib records
        grbs.rewind() # rewind the iterator
        t2mens = []
        i_month = self.lead_time
        grb= grbs[i_month]
        t2mens.append(grb.values)   
        t2mens = np.array(t2mens)
        lats, lons = grb.latlons()  # get the lats and lons for the grid.
        lats = lats[:,1]
        lons = lons[1,:]
        # Return values of interest
        return lats, lons, t2mens

"""    
class OTROMODELO(object):
    
    
    
"""

