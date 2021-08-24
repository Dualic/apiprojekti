# importing the requests library
#import requests
#import json

# api-endpoint
from google.cloud import bigquery

def get_satellites(parameter):
    import requests
    import json
    import re
    

    # read the name of the pub

    pubsname = parameter.args.get('name_of_the_pub')

    # edit pub name

    list_name = re.findall('[A-Z][^A-Z]*', pubsname)

    edited_name = ""

    for word in list_name:
        edited_name+=word + " "

    final_name = edited_name.strip()

    # Query lat and lon from BigQuery table

    client = bigquery.Client()
  
    query = """SELECT latitude,longitude FROM `week9-2-323806.Breweries.names` WHERE name = @var """

    job_config = bigquery.QueryJobConfig(
      query_parameters=[bigquery.ScalarQueryParameter("var", "STRING", final_name),]
    )

    query_job = client.query(query, job_config=job_config)  # Make an API request.


    results = query_job.result()  # Waits for job to complete.

    for row in results:
      lat = row[0]
      lon = row[1]

    str_lat = str(lat)
    str_lon = str(lon)

    coordinates = {"lat":str_lat, "long":str_lon}

    begin_url = "https://satellites.fly.dev/passes/43144"
    latitude_url = "?lat="+str(coordinates["lat"])
    longitude_url = "&lon="+str(coordinates["long"])
    days_url = "&days=1"
    final_url = begin_url+latitude_url+longitude_url+days_url



# get satellite data:
    URL = final_url
    datareq = requests.get(URL)
    data = datareq.json()
    times = str(len(data))
    #myjson = json.dumps(data)

    return f"Your boss has {times} chances today to catch you drinking beers!"

#SELECT latitude,longitude FROM `week9-2-323806.Breweries.names` WHERE name = 'Gravel Bottom Craft Brewery'

