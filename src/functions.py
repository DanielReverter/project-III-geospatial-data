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
    '''
    This function creates a dataframe of all the offices in our mongoDB dataset that are in Madrid, Barcelona and Valencia.
    The columns of the resulting dataframe are: 
    The name of the company owning the office, the city it's in, office_number(in case one company has more than 2 offices in the same city),
    the adress, latitude and longitude.
    '''
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

def get_coordinates (place):
    '''
    A function that gets the latitude and longitude of a place using geocode app. If it doesn't find it, [NaN, NaN] is returned
    '''
    try:
        res = requests.get(f"https://geocode.xyz/{place}?json=1").json()
        return [res["longt"],res["latt"]]
    except:
        return [np.nan, np.nan]

def clean_offices(df):
    '''
    A function that cleans a dataframe. It drops any rows containing NaN in address, latitude and longitude at the same time,
    then if there are some rows that have address but no lat-lon, it tries to fill those using the geocode function.
    Finally, it drops any rows with missing lat-lon or lat-lons not in Spain
    '''
    df['address'].replace('', np.nan, inplace=True)
    df = df.dropna(subset=["address", "latitude", "longitude"], how='all')
    for i in df.index.values.tolist():
        if math.isnan(df.at[i, "latitude"]) or df.at[i, "latitude"]==0:
            address_complete = df.at[i, "address"] + ", " + df.at[i, "city"] + ", Spain"
            coordinates = get_coordinates(address_complete)
            df.at[i, "latitude"]= float(coordinates[1])
            df.at[i, "longitude"]= float(coordinates[0])
    for i in df.index.values.tolist():
        if df.at[i, "latitude"] < 20:
            latitude = df.at[i, "latitude"]
            longitude = df.at[i, "longitude"]
            df.at[i, "latitude"] = longitude    
            df.at[i, "longitude"] = latitude
    df['latitude'] = df['latitude'].fillna(0)
    df.drop(df[df.latitude < 30].index, inplace=True)
    df.drop(df[df.longitude < -10].index, inplace=True)
    return df

def company_positions():
    '''
    Function that creates a dataframe of all the positions in the company, their salaries and how many employees in each position
    '''
    position = ["Designers", "UI/UX Engineers", "Frontend Developers", "Data Engineers", 
             "Backend Developers", "Account Managers", "Maintenance", "Executives", "CEO"]
    number_of_employees = [20, 5, 10, 15, 5, 20, 1, 10, 1]
    salary = [30000, 33000, 33000, 44000, 39000, 25000, 20000, 60000, 80000]
    employees_dict = {"position":position, "number_of_employees":number_of_employees, "salary":salary}
    return pd.DataFrame.from_dict(employees_dict)

def requirements(df2):
    '''
    Function that creates a dataframe with every requirement and its relaive weight
    '''
    requirements = ["Design company", "Schools", "Successful tech startup", "Starbucks", "Airport", "Party", 
                "Vegan restaurant", "Basketball stadium", "Dog hairdresser"]
    related_employees = ["Designers", "30% of All", "Frontend Developers/Backend Developers", "Executives", "Account Managers", "All", 
                        "CEO", "Maintenance", "All"]
    weight = [80, 100, 80, 40, 100, 10, 300, 500, 1]
    requirements_dict = {"requirements":requirements, "related_employees":related_employees, "weight":weight}
    df3 = pd.DataFrame.from_dict(requirements_dict)
    final_weight = []
    everyone = list(df2["position"].values)
    related_employees = [["Designers"], everyone, ['Frontend Developers', 'Backend Developers'], ['Executives'], ['Account Managers'], everyone, ['CEO'], ['Maintenance'], everyone] 
    for i, employee_types in enumerate(related_employees):
        weight = df3.at[i, "weight"]
        final = 0
        for employee_type in employee_types:
            number_of_employees = list(df2.loc[df2['position'] == employee_type]["number_of_employees"].values)[0]
            salary = list(df2.loc[df2['position'] == employee_type]["salary"].values)[0]
            final += weight*number_of_employees*salary
        if i == 1: 
            final *= 0.3
        final_weight.append(int(final))
    df3['final_weight'] = final_weight
    return df3

def get_results_from_foursquare(query, location, limit):
    '''
    This function gets query results from foursquare
    '''
    url = f"https://api.foursquare.com/v3/places/search?query={query}&ll={location[0]}%2C{location[1]}&radius=100000&sort=RELEVANCE&limit={limit}"
    headers = {
        "Accept": "application/json",
        "Authorization": key
    }
    response = requests.get(url, headers=headers)
    return response.json()["results"]

def get_distance_column(query, df):
    '''
    Function used to add a column as described in the notebook
    '''
    limit = 10
    distance_list = []
    for index in df.index.values.tolist():
        location = [df.at[index, "latitude"], df.at[index, "longitude"]]
        results = get_results_from_foursquare (query, location, limit)
        temp_distances = []
        for result in results:
            temp_distances.append(result["distance"])
        if len(temp_distances)>0:
            distance_list.append(min(temp_distances))
        else:
            distance_list.append(100000)
    return distance_list

def ordered_df(df):
    '''
    Function that reorders the requirements dataframe column as described in the notebook
    '''
    cols = df.columns.tolist()
    cols2 = cols[0:6] + [cols[-2]] + [cols[6]] + [cols[-1]] + cols[7:9] + [cols[-4]] + cols[9:11] + [cols[-3]]
    return df[cols2]

def sum_column(df, df3):
    '''
    Function that adds a final column to the requirements df used to determine the best venue as described in the notebook
    '''
    sum_of_distances = []
    list_of_columns_to_add = list(df.columns)[6:]
    for index in df.index.values.tolist():
        sum_ = 0
        i = 0
        for column in list_of_columns_to_add:
            weight = df3.at[i, "final_weight"]
            sum_ += df.at[index, column]*weight
            i += 1
        sum_of_distances.append(sum_)
    return sum_of_distances

