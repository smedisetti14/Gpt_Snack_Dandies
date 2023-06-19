import googlemaps
import requests
from dotenv import load_dotenv
import os

class GooglePlaceHelper():
    def find_expert(lat, long, radius, type, doctor_type):
        # call google places API to find the expert in the given lat, long
        load_dotenv()
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{long}&radius={radius}&type={type}&keyword={doctor_type}&key={GOOGLE_API_KEY}"
        url = url.format(lat=lat,long=long,radius=radius,type=type,doctor_type=doctor_type,GOOGLE_API_KEY=GOOGLE_API_KEY)
        print(url)
        payload = {}
        headers = {}
        response = requests.request("GET", url)
        #print(response)
        return response
    
    #sample code to find expert
    #print(find_expert(-33.8670522,151.1957362,1500,"doctor","pediatrician"))