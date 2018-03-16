
# coding: utf-8

# In[6]:


from config import api_key
from yelpapi import YelpAPI
import requests
import pandas as pd
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt


# In[ ]:


cities = ["Anaheim,CA", "Santa Ana,CA", "Irvine,CA", "Tustin,CA", "Garden Grove,CA", 
          "Orange,CA", "Fullerton,CA", "Costa Mesa,CA", "Cypress,CA", "Westminster,CA"]
types = ["Chinese", "Mexican", "French", "Japanese", "Mediterranean","American", "Italian", 
         "Korean", "Thai", "Indian"]
url = "https://api.yelp.com/v3/businesses/search"
headers = {'Authorization': 'Bearer %s' %api_key}

types_summary = {}
ratings_summary = {}

for city in cities:
    restaurant_types={}
    ratings={}
    restaurant_ratings = {}
    for t in types:
        results = []
        params = {"term":t,"location":city,"limit":50,"radius":5000}
        responses = requests.get(url,headers = headers,params = params).json()
        for response in responses["businesses"]:
            results.append(response)
        url_params = {"term":t,"location":city,"limit":50,"offset":50,"radius":5000}
        answers = requests.get(url,headers = headers,params = url_params).json()
        for answer in answers["businesses"]:
            results.append(answer)
        for result in results:
            if t not in restaurant_types:
                restaurant_types[t]=1
                ratings[t]=result["rating"]
            else:
                restaurant_types[t]+=1
                ratings[t]+=result["rating"]
    for cuisine in ratings:
        restaurant_ratings[cuisine]=round(ratings[cuisine]/restaurant_types[cuisine],2)
    ratings_summary[city]=restaurant_ratings
    types_summary[city]=restaurant_types


# In[ ]:


print(types_summary)


# In[ ]:


types_summary_df = pd.DataFrame.from_dict(types_summary)
types_summary_df


# In[ ]:


print(ratings_summary)


# In[ ]:


ratings_summary_df = pd.DataFrame.from_dict(ratings_summary)
ratings_summary_df

