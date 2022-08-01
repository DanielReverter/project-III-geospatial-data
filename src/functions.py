import os
import requests
import json
from dotenv import load_dotenv
import pandas as pd
import geopandas as gpd
from cartoframes.viz import Map, Layer, popup_element
from pymongo import MongoClient
from pymongo import GEOSPHERE
import math
import numpy as np
import folium
from folium import Choropleth, Circle, Marker, Icon, Map, features
from folium.plugins import HeatMap, MarkerCluster

# This file has all the functions that are used in the project

load_dotenv()
key = os.getenv("KEY")

def spain_offices():
    client = MongoClient("localhost:27017")
    db = client.get_database("Ironhack")    
    companies = db.get_collection("companies")
    valencia_companies = list(companies.find({"offices.city":"Valencia"}))
    barcelona_companies = list(companies.find({"offices.city":"Barcelona"}))
    madrid_companies = list(companies.find({"offices.city":"Madrid"}))
    spain_companies = [valencia_companies, barcelona_companies, madrid_companies]
    name = []
    city = []
    office_number = []
    address = []
    latitude = []
    longitude = []
    for each_city in spain_companies:
        for company in each_city:
            try:
                for i in range(len(company["offices"])):
                    n = 0
                    if company["offices"][i]["city"] in ["Valencia", "Barcelona", "Madrid"]:
                        n += 1
                        name.append(company["name"])
                        city.append(company["offices"][i]["city"])
                        office_number.append(n)
                        address.append(company["offices"][i]["address1"])
                        latitude.append(company["offices"][i]["latitude"])
                        longitude.append(company["offices"][i]["longitude"])
            except:
                pass
    spain_dict = {"name":name, "city":city, "office_number":office_number, "address":address, "latitude":latitude, "longitude":longitude}
    df = pd.DataFrame.from_dict(spain_dict)
    return df