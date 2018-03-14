from config import api_key
from yelpapi import YelpAPI
import requests
import pandas as pd
import numpy as np
from pprint import pprint

cities = ["Anaheim", "Santa Ana", "Irvine", "Huntington Beach", "Garden Grove", "Orange", "Fullerton", "Costa Mesa", "Mission Viejo", "Westminster"]
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
    price = {}
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
                    price[city]=response["price"]
                else:
                    restaurant_types[t] += 1
                    ratings[t]+=response['rating'] #sum of ratings
                    review_counts[t]+=response["review_count"] #sum of review_counts
                    price[city]=response["price"]
            except KeyError: #some restaurants don't have the dollar sign.
                price[city]= np.nan  
    types_summary[city]=restaurant_types
    for rating in ratings:
        type_rating.append(round(ratings[rating]/restaurant_types[rating],2))
    ratings_summary[city]=type_rating

print(types_summary)
print(ratings_summary)