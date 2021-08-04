#!/usr/bin/env python
# coding: utf-8

# <b><h1>Peer-graded Assignment: Segmenting and Clustering Neighborhoods in Toronto</h1></b>

# <b><h2>For this assignment, I will be required to explore and cluster the neighbourhoods in Toronto</h2></b>

# <b>Install and import all the required libraries for the project</b>

# In[44]:


#install required modules to webscrape the page 
get_ipython().system('pip install bs4')
get_ipython().system('pip install requests ')
get_ipython().system('pip install lxml')
get_ipython().system('ipip install geopandas')
get_ipython().system('pip install geopy')
print('complete installation done!')

import pandas as pd #for data analysis 
import requests #to handle requests
import numpy as np #to handle data in a vecorized manner
import random #to generate random numbers
get_ipython().system('conda install -c conda-forge geopy --yes')
from geopy.geocoders import Nominatim #to generate longiude and latitude from a given address

#libraries to display images
from IPython.display import Image
from IPython.core.display import HTML

from pandas.io.json import json_normalize #llibrary to convert json to a pandas dataframe

get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes')
import folium
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans
import matplotlib.cm as cm 
import matplotlib.colors as colors

print('all libraries successfully installed and imported!')


# <b>Scraping the Webpage and Passing into a Pandas Dataframe</b>
# 
# The dataframe will consist of three columns: PostalCode, Borough, and Neighborhood

# In[45]:


data = pd.read_excel('G:\\Personal\personal courses study\data sc course\\toronto_postal_code_file.xlsx')
data.head() #to check if the datafrane has been successfully passed and has all the required columns 


# <b>Data Wrangling</b>

# In[46]:


#lets check the size of the dataframe
data.shape


# We can see that the dataframe has 288 rows, which will lessen as we remove the rows that are not required.

# First we can drop the rows with 'Not assigned' int the 'neighborhood' column

# In[47]:


#dropping the rows that have 'Not Assigned' in the 'Neighborhood' Column
data_1 = data[data['Neighbourhood'] != 'Not assigned']
data_1.head()


# We can see that the required dataframe has eliminated the rows specified and now has only 210 rows

# More than one neighborhood can exist in one postal code area. For example, in the table on the Wikipedia page, you will notice that M5A is listed twice and has two neighborhoods: Harbourfront and Regent Park. These two rows will be combined into one row with the neighborhoods separated with a comma.

# In[48]:


data_2 = data_1.groupby(['Postcode','Borough'], sort=False).agg(', '.join)
data_2.reset_index(inplace=True)
data_2.head()           
    


# If a cell has a borough but a Not assigned  neighborhood, then the neighborhood will be the same as the borough.

# In[49]:


data_2['Neighborhood'] = np.where(data_2['Neighbourhood'] == 'Not assigned', data_2['Borough'], data_2['Neighbourhood'])
data_2.head()


# In[50]:


data_2.shape


# So now the dataframe has 102 rows from the original 288

# <b>Import the CSV with the Latitude and Longitude Data for the Neighbourhoods
# </b>

# In[51]:


coordinates = pd.read_csv('G:\\Personal\personal courses study\data sc course\\Geospatial_Coordinates.csv')
coordinates.head()


# <b>Merge the Postal Code Dataframe with the Coordindates Dataframe to Create One Complete Dataset</b>

# In[52]:


coordinates.rename(columns = {'Postal Code':'Postcode'}, inplace = True)
data_3 = pd.merge(data_2, coordinates, on = 'Postcode')
data_3.drop('Neighborhood', axis = 1, inplace = True)
data_3.head()


# <b>Exploring and Clustering the Neighborhoods in Toronto With the Generated Dataframe</b>
# <nl>Now we can explore and cluster the neighborhoods in Toronto. 

# First, let's get all the rows which contain the term 'Toronto' in them 

# In[53]:


data_4 = data_3[data_3['Borough'].str.contains('Toronto', regex = False)]
data_4


# <b>Visualize the Neighbourhoods Onto a Map </b>

# In[54]:


#first we get the Latitude and longitude of Toronto,CA
address = 'Toronto, CA'
geolocator = Nominatim(user_agent = 'myGeocoder')
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('THe geographic coordinates of {} are: Latitude: {}, Longitude: {}'.format(address, latitude, longitude))

#now we can map the city 
map_toronto = folium.Map(location = [latitude, longitude], zoom_start = 10)

for lat, long, borough, neighbourhood in zip(data_4['Latitude'], 
                                            data_4['Longitude'], 
                                            data_4['Borough'], 
                                            data_4['Neighbourhood']):
    label = '{},{}'.format(neighbourhood, borough)
    label = folium.Popup(label, parse_html = True)
    folium.CircleMarker([lat, long], 
                        radius = 5, 
                        color = 'blue',
                        fill = True,
                        fill_color = '#3186cc', 
                        fill_opacity = True,
                        parse_HTML = False).add_to(map_toronto)
map_toronto



# <b>Clustering Using KMeans</b> Now we can start the clustering using KMeans 

# In[58]:


k = 5 #defining value of k
toronto_cluster_data = data_4.drop(['Postcode', 'Borough', 'Neighbourhood'],1)
kmeans = KMeans(n_clusters = k, random_state = 0).fit(toronto_cluster_data)
kmeans.labels_
data_4.insert(0, 'Cluster Labels', kmeans.labels_)
data_4.head()


# <b>Visualize the Clustered Neighbourhoods</b>

# In[59]:


map_clustered_neighbourhoods = folium.Map(location = [latitude, longitude], zoom_start = 10)

#set colors  for the clusters
x = np.arange(k)
ys = [i + x + (i*x)**2 for i in range(k)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# add markers to the map
markers_colors = []
for lat, lon, neighbourhood, cluster in zip(data_4['Latitude'],
                                            data_4['Longitude'],
                                            data_4['Neighbourhood'], 
                                            data_4['Cluster Labels']):
    label = folium.Popup(' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color=rainbow[cluster-1],
        fill=True,
        fill_color=rainbow[cluster-1],
        fill_opacity=0.7).add_to(map_clustered_neighbourhoods)
       
map_clustered_neighbourhoods


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




