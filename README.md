# BeingHereMap

The Python Script parses the Excel file [argument 1 to the script] and grabs the data in the OnDemandRegional tab. It puts this into a pandas dataframe and iterates through the country names, sending them to the Google Maps API to get information about each country. 

Specifically, we want the latitude & longitude, which are then put into an array. After the program finishes looping through all the countries in the dataframe, the array is saved to a .js file [which is the name of the argument file with a .js appended]

The html file is hardcoded to look for "Being_Here_Stats.xls.js" which should now contain all the countries. The html contains javascript code to render each country by invoking the Google Maps API
