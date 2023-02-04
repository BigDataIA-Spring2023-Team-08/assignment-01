import requests
import boto3
import re
import os
import logging
from dotenv import load_dotenv
import plotly.graph_objects as go

#load env variables and change logging level to info
load_dotenv()
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=LOGLEVEL,
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='logs.log')

def scrape_nexrad_locations():
    #initialise containers for relevant data
    nexrad=[]
    satellite_metadata = {
            'state': [],
            'county': [],
            'latitude': [],
            'longitude': [],
            'elevation': []
    }
    #url used to scrape NEXRAD satellite location data to plot on map
    url = "https://www.ncei.noaa.gov/access/homr/file/nexrad-stations.txt"
    #recording the response from the webpage
    response = requests.get(url)
    #traverse extracted txt data line by line
    lines = response.text.split('\n')
    for line in lines:
        line=line.strip()   #strip leading and trailing whitespaces
        word_list = line.split(" ")
        if (word_list[-1].upper() == 'NEXRAD'): #logic to check if the data belongs to a NEXRAD satellite
            nexrad.append(line)
    nexrad = [i for i in nexrad if 'UNITED STATES' in i]    #only consider satellites over USA

    #extracting state and county information 
    for satellite in nexrad:
        satellite = satellite.split("  ")
        satellite =  [i.strip() for i in satellite if i != ""]
        for i in range(len(satellite)):
            if (re.match(r'\b[A-Z][A-Z]\b',satellite[i].strip())):      #use regex to match with the state field containing 2 capital letters
                #state_county = satellite[i].split()
                satellite_metadata['state'].append(satellite[i][:2])    #append state field to final dict
                satellite_metadata['county'].append(satellite[i][2:])   #append county field to final dict

    #extracting latitude, longitude and elevation information 
    for satellite in nexrad:
        satellite = satellite.split(" ")
        satellite =  [i.strip() for i in satellite if i != ""]      #strip for any whitespaces if the string is not empty
        for i in range(len(satellite)):
            if (re.match(r'^-?[0-9]\d(\.\d+)?$',satellite[i])):     #use regex to match with the coordinate string
                state_county = satellite[i].split()
                satellite_metadata['latitude'].append(satellite[i])     #append latitude as string to final dict
                satellite_metadata['longitude'].append(satellite[i+1])  #append longtidue as string to final dict
                satellite_metadata['elevation'].append(int(satellite[i+2]))     #append elevation as int to final dict
                break
    
    return satellite_metadata   #this dict has the final scraped data

def plot_nexrad_locations():
    satellite_metadata = scrape_nexrad_locations()
    #plotting the coordinates extracted on a map
    hover_text = []
    for j in range(len(satellite_metadata['county'])):      #building the text to display when hovering over each point on the plot
        hover_text.append(satellite_metadata['county'][j] + ", " + satellite_metadata['state'][j])

    #use plotly to plot
    fig = go.Figure(data=go.Scattergeo(
            lon = satellite_metadata['longitude'],
            lat = satellite_metadata['latitude'],
            text = hover_text,
            marker= {
                "color": satellite_metadata['elevation'],
                "colorscale": "Viridis",
                "colorbar": {
                    "title": "Elevation"
                },
                "size": 14,
                "symbol": "circle",
                "line" : {
                    "color": 'black',
                    "width": 1
                }
            }
        ))

    #plot layout
    fig.update_layout(
            title = 'All NEXRAD satellite locations along with their elevations',
            geo_scope='usa',
            mapbox = {
                    "zoom": 12,
                    "pitch": 0,
                    "center": {
                        "lat": 31.0127195,
                        "lon": 121.413115
                    }
            },
            font = {
                "size": 18
            },
            autosize= True
        )

    fig.update_layout(height=700)
    #fig.show()

    return fig

def main():
    plot = plot_nexrad_locations()

if __name__ == "__main__":
    logging.info("NEXRAD statellite map data scraper script starts")
    main()
    logging.info("NEXRAD statellite map data scraper script ends")