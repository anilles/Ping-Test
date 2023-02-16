#Import necessary modules
from xml.etree.ElementTree import fromstringlist
import pandas as pd
import numpy
from collections import defaultdict
import folium
import json

#Ask for the filename
Tickets = input("What file would you like to pull Location data from?\n")

#Create the Dataframe
df = pd.read_excel(Tickets)

#Asssign the Location column to a list
Agent_Loc = df["Location"].to_numpy()

#Dictionary of each location and it's state prefix id

SAC_Dict = {
    "Alabama": "01-", "Mississippi": "24-", "Greater California": "55-", "N. California": "05-", "S. California": "75-", "North Carolina": "33-", "Virginia": "46-",
    "Florida": "59-", "Georgia": "11-", "South Carolina": "40-", "Illinois": "13-", "Indiana": "14-", "Michigan": "22-", "Arkansas": "04-", "Louisiana": "18-",
    "Missouri": "25-", "Colorado": "06-", "Utah": "44-", "Wyoming": "50-", "Connecticut": "97-", "Maine": "19-", "Massachusetts": "21-", "New Hampshire": "29-",
    "New York": "52-", "Rhode Island": "39-", "Vermont": "45-", "Minnesota": "23-", "Wisconsin": "49-", "New Jersey": "30-", "N. New York": "32-", "Ohio": "35-",
    "Kansas": "16-", "Oklahoma": "36-", "Alaska":"02-", "Hawaii": "52-", "Idaho": "12-", "Montana": "26-", "Oregon": "37-", "Washington": "47-", "Pennsylvania": "38-",
    "Delaware": "08-", "District of Columbia": "09-", "Maryland": "20-", "West Virginia": "48-", "Kentucky": "17-", "Tennessee": "42-", "Arizona": "03-", "Nevada": "28-",
    "New Mexico": "31-", "N. Texas": "43-", "S. Texas": "53-", "Iowa": "15-", "Nebraska": "27-", "North Dakota": "34-", "South Dakota": "41-"
}

#Loop to iterate through the locations column and make a list of all the occurrences of a State.
State_Tickets = []
for i in Agent_Loc:
    for key, value in SAC_Dict.items():
        if value in i:
            State_Tickets.append(key)

#Create a list of States from the SAC Keys
#Create an Create a dictionary where the keys are the States and the Values are 0 so we can count the StateTickets
States = list(SAC_Dict.keys())
TicketCount = {} 
for i in States:
    TicketCount[i]=0
#iterate through State Tickets and if the key matches the current value of State Tickets add 1 to the keys : value.
for i in State_Tickets:
    TicketCount[i] += 1
#convert TicketCount to a dataframe that wi11 merge with the follum overlay
df = pd.DataFrame()
df = pd.DataFrame (TicketCount.items())
df.columns = ["State", "Count"]

#Aggregate the rows that fall in the same State
df["State"].replace({"S. California": "California", "N. California": "California", "Greater California": "California", "N. Texas": "Texas", "S. Texas" : "Texas", "N. New York": "New York"},inplace=True)
df.rename(columns={"State": "name"}, inplace=True)
agg_functions = {"name":" first", "Count": "sum"}
df = df.groupby(df ["name"]).aggregate(agg_functions)
print (df)

#create a map file with the map centered and framed
map = folium.Map(location=[40.407847, -97.689061], zoom_start=5, tooltip="Click for Count") 
state_borders = f"US_State.json" 
folium.GeoJson(state_borders, name="State Borders").add_to(map)
#Create the Choropleth overlay and bind the Geoison File and the TicketCount df together. 
cp=folium.Choropleth(
    geo_data=state_borders,
    name="State Ticket Count", 
    data=df,
    columns=["name", "Count"],
    key_on="feature .properties .name",
    bins=9,
    fill_color="Reds", 
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Ticket Count",
    reset=True, 
    highlight=True
).add_to (map)
#add geojson data to the map from the choropleth function cp.geojson.add_to(map)
#add ticket count to geoson data so it can be referenced in the tooltip 
for feature in cp.geojson.data['features']:
    name = feature['properties']['name']
    feature['properties']['Count'] = 'Count: ' + str(df.loc[name, 'Count'] if name in list (df.index) else 'N/A')
#add tooltip to give state data on mouse over,
cp.geojson. add_child(
    folium.features.GeoJsonTooltip(['name', 'Count'], labels=False)
)
#adding layercontrol 
folium.LayerControl().add_to(map)
map.save('map. html')

