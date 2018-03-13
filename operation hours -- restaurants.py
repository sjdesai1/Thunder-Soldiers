from config import api_key
from yelpapi import YelpAPI
import requests
import pandas as pd
import numpy as np
from pprint import pprint

#get business_id
cities = ["Irvine", "Santa Ana", "Costa Mesa", "Lake Forest", "Newport Beach", "Tustin", "Gardon Grove", "Fullerton",
          "Mission Viejo", "Laguna Beach"]
url = "https://api.yelp.com/v3/businesses/search"
headers = {'Authorization': 'Bearer %s' % api_key}
business_id = []
for c in cities:
    params = {'term': "restaurant", "location": c, "limit": 50, "radius": 5000}
    responses = requests.get(url, headers=headers, params=params).json()
    for response in responses["businesses"]:
        business_id.append(response["id"])
#get their operation hours and ratings
yelp_api = YelpAPI(api_key)
responses = []
for b in business_id:
    responses.append(yelp_api.business_query(id = b))
dates_time = []
ratings = []
for r in responses:
    try:
        dates_time.append(r["hours"][0]["open"])
        ratings.append(r["rating"])
    except KeyError: #some stores didn't list out operation hours
        continue
pprint(dates_time)
#calculate the average of operation hours
for date_time in dates_time:
    total = 0
    for x in range(len(date_time)):
        if int(date_time[x]["end"]) == 0:
            total += 2400 - int(date_time[x]["start"])
        elif int(date_time[x]["end"]) < 600:
            #             print(date_time[x]["day"])
            total += int(date_time[x]["end"]) + 2400 - int(date_time[x]["start"])
        else:
            total += int(date_time[x]["end"]) - int(date_time[x]["start"])
            if total < 0:
                print(total)
                print(date_time[x]["end"])
    avg = round(total / (len(date_time) * 100))

    print(avg)

