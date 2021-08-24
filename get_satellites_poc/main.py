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

    # Query lat and lon from BigQuery table

    client = bigquery.Client()
  
    query = """SELECT latitude,longitude FROM `week9-2-323806.Breweries.namesfinal` WHERE name = @var """

    job_config = bigquery.QueryJobConfig(
      query_parameters=[bigquery.ScalarQueryParameter("var", "STRING", pubsname),]
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
    limit_url = "&limit=1"
    final_url = begin_url+latitude_url+longitude_url+limit_url



# get satellite data:
    URL = final_url
    datareq = requests.get(URL)
    data = datareq.json()
    
    rise_time = data[0]["rise"]["utc_datetime"]
    set_time = data[0]["set"]["utc_datetime"]
    
    #myjson = json.dumps(data)
    time_dict = {'rises':rise_time, 'sets':set_time}
    
    

    return f"This satellite rises at {rise_time} and sets at {set_time}"


#SELECT latitude,longitude FROM `week9-2-323806.Breweries.names` WHERE name = 'Gravel Bottom Craft Brewery'

