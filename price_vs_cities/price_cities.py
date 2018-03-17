
# coding: utf-8

# In[3]:


from config import api_key
from yelpapi import YelpAPI
import requests
import pandas as pd
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt


# In[4]:


cities = ["Anaheim,CA", "Santa Ana,CA", "Irvine,CA", "Huntington Beach,CA", "Garden Grove,CA", "Orange,CA", "Fullerton,CA", "Costa Mesa,CA", "Mission Viejo,CA","Westminster,CA"]
url = "https://api.yelp.com/v3/businesses/search"
headers = {'Authorization': 'Bearer %s' %api_key}
price_locations = {}

for city in cities:
    locations={}
    params = {"term":"restaurant",
              "location":city,
              "limit":50,
             "radius":5000}
    responses=requests.get(url,headers = headers, params = params).json()
    for response in responses["businesses"]:
        try:
            money= response["price"]
            if money not in locations:
                locations[money]=1
                
            else:
                locations[money]+=1
        except KeyError:
            continue  
    price_locations[city]=locations 
    url_params = {"term":"restaurant",
                  "location":city,
                  "limit":50,
                 "offset":50,
                  "radius":5000}
    results = requests.get(url,headers = headers, params = url_params).json()
    for r in results["businesses"]:
        try:
            m = r["price"]
            if m not in locations:
                locations[m]=1
            else:
                locations[m]+=1
        except KeyError:
            continue
    price_locations[city]=locations
print(price_locations)        
     


# In[6]:


columns = ["Cheap","Affordable","Expensive","Luxury"]
DF=pd.DataFrame.from_dict(price_locations).T #.T means transpose, switch columns and rows
DF = DF.reset_index()
# df.rename(columns = {'index':'City','$':'Cheap'}, inplace = True)
df = DF.rename(columns={"$":"Cheap","$$":"Affordable","$$$":"Expensive","$$$$":"Luxury","index":"City"})
# DF.to_csv("output.csv")

df = df.fillna(0)
df

