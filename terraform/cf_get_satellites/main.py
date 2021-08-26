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

    #loop
    
    norad_id_list = [43114,43800,44229,44389,44390]
    sat_names={43114:"ICEYE-X1",43800:"ICEYE-X2",44229:"HARBRINGER",44389:"ICEYE-X5",44390:"ICEYE-X4"}
    results_list = []

    for sat_id in norad_id_list:

      begin_url = "https://satellites.fly.dev/passes/"
      sat_id_url = str(sat_id)
      latitude_url = "?lat="+str(coordinates["lat"])
      longitude_url = "&lon="+str(coordinates["long"])
      limit_url = "&limit=1"
      final_url = begin_url+sat_id_url+latitude_url+longitude_url+limit_url

      # get satellite data:
      URL = final_url
      datareq = requests.get(URL)
      data = datareq.json()
      
      #error handling
      if len(data) != 0:
      
        rise_time = data[0]["rise"]["utc_datetime"]

        edited_rise_time = rise_time.split(".")
        sec_rise_time = edited_rise_time[0]
        second_split = sec_rise_time.split(":")
        final_rise_time = second_split[0]+":"+second_split[1]

        set_time = data[0]["set"]["utc_datetime"]
        edited_set_time = set_time.split(".")
        sec_set_time = edited_set_time[0]
        set_second_split = sec_set_time.split(":")
        final_set_time = set_second_split[0]+":"+set_second_split[1]

        info = f"The satellite {sat_names[sat_id]} rises at {final_rise_time} and sets at {final_set_time}"
        results_list.append(info)


    results_json = "\n".join(results_list)

    if len(results_json) == 0:
      return f"No satellites over this pub today"
    else:
      return results_json
