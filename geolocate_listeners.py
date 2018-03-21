import urllib.request, json, time, csv, sys
import pandas as pd

def GoogGeoAPI(address,api="",delay=5):
  base = r"https://maps.googleapis.com/maps/api/geocode/json?"
  addP = "address=" + address.replace(" ","+")
  GeoUrl = base + addP #+ "&key=" + api

  response = urllib.request.urlopen(GeoUrl)
  jsonRaw = response.read().decode('utf-8')

  jsonData = json.loads(jsonRaw)

  if jsonData['status'] == 'OK':
    resu = jsonData['results'][0]
    finList = [resu['formatted_address'],resu['geometry']['location']['lat'],resu['geometry']['location']['lng']]
  else:
    finList = [None,None,None]
  time.sleep(delay) #in seconds
  return finList

locations_list = []

xl = pd.ExcelFile(sys.argv[1])
df_ondemand = xl.parse('OnDemandRegional')
df_ondemand = df_ondemand[pd.notnull(df_ondemand['Country'])]


df_live = xl.parse('LiveRegional')
df_live = df_live[pd.notnull(df_live['Country'])]

countries = set()

# Parse the live set of countries and throw them into a set
for index, row in df_live.iterrows():
  if (row[0]=="United States"):
    countries.add(row[1]) # if country is USA, need to add the region which is the state
  else:
    countries.add(row[0])


for index, row in df_ondemand.iterrows():
  if index == 0:
    continue
  if row[0] != "United States": # we ignore USA because the states will be covered above
    countries.add(row[0])


print(countries)

while bool(countries):
  print("Num of countries remaining: ", len(countries))
  c = countries.pop()
  # print(c)
  geoR=GoogGeoAPI(address=c)
  if geoR != [None, None, None]:
    locations_list.append({"country":c,"lat":geoR[1],"lon":geoR[2]})
    # countries.discard(c)
    print(geoR)
  else:
    print("google rejected: ", c, " and will try later")
    countries.add(c)

fname = sys.argv[1]+".js"
print (fname)

with open(sys.argv[1]+".js", 'w') as outfile:
    outfile.write("var listener_locations = " + json.dumps(locations_list) + ";")


