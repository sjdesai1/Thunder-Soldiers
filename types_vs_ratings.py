
# coding: utf-8

# In[1]:


from config import api_key
from yelpapi import YelpAPI
import requests
import pandas as pd
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt


# In[14]:


cities = ["Anaheim,CA", "Santa Ana,CA", "Irvine,CA", "Garden Grove,CA", "Cypress","Tustin","Orange,CA", "Fullerton,CA", "Costa Mesa,CA", "Westminster,CA"]
types = ["Chinese", "Mexican", "French", "Japanese", "Mediterranean","American", "Italian", "Korean", "Thai", "Indian"]
url = "https://api.yelp.com/v3/businesses/search"
headers = {'Authorization': 'Bearer %s' %api_key}

types_summary = {}
ratings_summary = {}
reviews_summary = {}

for city in cities:
    restaurant_types = {}
    ratings={}
    review_counts = {}
    type_rating = []
    for t in types:
        params = {'term':t ,'location': city,'limit': 50,'radius': 5000}
        responses = requests.get(url,headers = headers, params = params).json()
        for response in responses['businesses']:
            try:
                if t not in restaurant_types:
                    restaurant_types[t] = 1
                    ratings[t] = response['rating']
                    review_counts[t]=response["review_count"]
                    
                else:
                    restaurant_types[t] += 1
                    ratings[t]+=response['rating'] #sum of ratings
                    review_counts[t]+=response["review_count"] #sum of review_counts
                    
            except KeyError: #some restaurants don't have the dollar sign.
                continue  
    types_summary[city]=restaurant_types
    for rating in ratings:
        type_rating.append(round(ratings[rating]/restaurant_types[rating],2))
    ratings_summary[city]=type_rating
#     reviewCount = [value for key, value in typeReview.items()]
#     countReviews[x] = ReviewCount


# In[15]:


print(types_summary)


# In[16]:


df = pd.DataFrame.from_dict(types_summary)
df


# In[17]:


print(ratings_summary)
DF = pd.DataFrame.from_dict(ratings_summary)
DF['Types']=types
DF = DF.set_index("Types")
DF


# In[ ]:



    

