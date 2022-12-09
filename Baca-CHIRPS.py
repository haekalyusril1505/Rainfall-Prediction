#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd # for dataframe
import numpy as np # for trigonometry and array
import gdal, osr
from datetime import datetime, timedelta


# In[25]:


year_awal = 2003
year_akhir= 2020
n_year = year_akhir - year_awal + 1


# In[26]:


"""DATA PREP"""
# os.environ['GDAL_DATA'] = os.environ['CONDA_PREFIX'] + r'\Library\share\gdal'
# os.environ['PROJ_LIB'] = os.environ['CONDA_PREFIX'] + r'\Library\share'

gdal.UseExceptions()

#lat_max = 2.5 #350
#lat_min = -0.95 #420
#lon_max = 115.45 #510
#lon_min =112 #440

#n_year = 30
#n_year = 1
n_ts = n_year * 12 * 3
#n_ts = 163
layer_rain = np.zeros(shape = (640,1480,n_ts))
layer_lat = np.zeros(shape = (640,1480))
layer_lon = np.zeros(shape = (640,1480))

ts = -1

for year in range (year_awal, year_akhir + 1):
#for year in range (2018, 2019):
    for month in range (1, 37):
        ts = ts + 1
        
        if month < 10:
            datestring = str(year) + "0" + str(month)
        else:
            datestring = str(year) + str(month)
            
        print(datestring)
        
        fname = 'D:/Works/Inovastek/DATABASE/SICA/Raw_Data/CHIRPS/' + datestring + '.tif'
        
        tiff = gdal.Open(fname)
        
        if ts == 0:
            grid_geotransform = tiff.GetGeoTransform()

            for y in range(0,640):
                for x in range(0,1480):
                    layer_lon[y,x] = grid_geotransform[0] + x*grid_geotransform[1]        
                    layer_lat[y,x] = grid_geotransform[3] + y*grid_geotransform[5]
        
        data = tiff.ReadAsArray()
        
        layer_rain[:,:,ts] = data

layer_rain[layer_rain == -32768] = -9999


# In[4]:


layer_data = np.dstack((layer_lon,layer_lat))
layer_data = np.concatenate((layer_data, layer_rain), axis = 2)
#for ts in range(n_ts):
#    print(ts)
#    layer_data = np.dstack((layer_data,layer_rain[:,:,ts]))
    
layer_data = layer_data.reshape(-1,layer_data.shape[2])
layer_data = layer_data[~np.isnan(layer_data).any(axis=1)]

np.savetxt("CHIRPS-Cek.csv", layer_data, delimiter=",", fmt='%.2f')


# In[21]:


#cek_df = pd.DataFrame(layer_data)
#cek_df = layer_data
lon = 115.63138694538216 #Titik Tinjau
lat = -3.64155011191288 #Titik Tinjau
a = cek_df[1].sub(lat).abs() + cek_df[0].sub(lon).abs()


# In[22]:


index = a.idxmin()
df = pd.DataFrame(layer_data)
df_data = df.iloc[index]
df_data = pd.DataFrame(df_data).transpose()


# In[24]:


df_data.to_csv('Data-CHIRPS.csv')


# In[ ]:




