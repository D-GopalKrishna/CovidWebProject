import pandas as pd
import shapefile as shp
import seaborn as sns


sns.set(style="whitegrid", palette="pastel", color_codes=True)
sns.mpl.rc("figure", figsize=(10,6))
shp_path = "3e11a5e.shp"
sf = shp.Reader(shp_path)

def read_shapefile(sf):
    """
    Read a shapefile into a Pandas dataframe with a 'coords' 
    column holding the geometry information. This uses the pyshp
    package
    """
    fields = [x[0] for x in sf.fields][1:]
    records = sf.records()
    shps = [s.points for s in sf.shapes()]
    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(coords=shps)
    return df

dpp1 = read_shapefile(sf)
dpp1.drop([3,5], axis=0, inplace=True)
dpp1.reset_index(inplace=True)
dpp1.drop('index', axis=1, inplace=True)

state_name1 = dpp1['State_Name'].values

state_name1[2] = 'Jammu and Kashmir'
state_name1[12] = 'Delhi'
state_name1[19] = 'Andaman and Nicobar Islands'
state_name1[20] = 'Puducherry'
state_name1[28] = 'Odisha'
state_name1[29] = 'Chhattisgarh'

coordi_1 = dpp1.iloc[:,-1]

from geojson import Polygon, Feature, FeatureCollection

xyz = []
for i in range(34):
    aa = Polygon(coordi_1[i])
    bb = Feature(geometry=aa, id=state_name1[i])
    xyz.append(bb)
    
feature_collection = FeatureCollection(xyz)

dww1 = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv', encoding='utf-8')

for i in range(len(dww1.iloc[:,1])):
    if dww1.iloc[i,0]=='Dadra and Nagar Haveli and Daman and Diu':
        dww1.drop(i, axis=0, inplace=True)
        break

for i in range(len(dww1.iloc[:,1])):
    if dww1.iloc[i,0]=='Ladakh':
        dww1.drop(i, axis=0, inplace=True)
        break
    
for i in range(len(dww1.iloc[:,1])):
    if dww1.iloc[i,0]=='State Unassigned':
        dww1.drop(i, axis=0, inplace=True)
        break

for i in range(len(dww1.iloc[:,1])):
    if dww1.iloc[i,0]=='Total':
        dww1.drop(i, axis=0, inplace=True)
        break
    
dww1.reset_index(inplace=True)
dww1.drop(['index', 'Recovered', 'Deaths', 'Active', 'Last_Updated_Time', 'Migrated_Other', 'State_code', 'Delta_Confirmed', 'Delta_Recovered', 'Delta_Deaths', 'State_Notes'], axis=1, inplace=True)





import plotly.graph_objects as go

fig = go.Figure(go.Choroplethmapbox(geojson=feature_collection, locations=dww1.State, z=dww1.Confirmed,
                                    colorscale="Viridis", zmin=0, zmax=1000000,
                                    marker_opacity=0.5, marker_line_width=0))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()