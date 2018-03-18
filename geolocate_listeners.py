import urllib.request, json, time, csv, sys
import pandas as pd

def GoogGeoAPI(address,api="",delay=5):
  base = r"https://maps.googleapis.com/maps/api/geocode/json?"
  addP = "address=" + address.replace(" ","+")
  GeoUrl = base + addP + "&key=" + api

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
df1 = xl.parse('OnDemandRegional')

# f = open(sys.argv[1], 'r') # opens the csv file
try:
    # reader = csv.reader(f)  # creates the reader object
    # next(reader, None)
    #for row in reader:   # iterates the rows of the file in orders
    for index, row in df1.iterrows():
        if index > 0:
          print (row)    # prints each row
        # geoR= GoogGeoAPI(address=row[0])
          geoR= GoogGeoAPI(address=row[0])

        # locations_list.append({"country":row[0],"num_listeners":row[1],"lat":geoR[1],"lon":geoR[2]})
          locations_list.append({"country":row[0],"lat":geoR[1],"lon":geoR[2]})

finally:
    # f.close()      # closing
    print("BYE!")      # closing

print(locations_list)

fname = sys.argv[1]+".js"
print (fname)

with open(sys.argv[1]+".js", 'w') as outfile:
    outfile.write("var listener_locations = " + json.dumps(locations_list) + ";")


