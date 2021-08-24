from google.cloud import bigquery

client = bigquery.Client()

def findclosest(request):
    request_json = request.get_json(silent=True)
    approxlongitude = request_json.get("longitude")
    approxlatitude = request_json.get("latitude")
    
    while True:
        margin = 0.05
        query = f"SELECT name FROM `week9-2-323806.Breweries.names` WHERE (longitude BETWEEN ({approxlongitude}-{margin}) AND ({approxlongitude}+{margin})) AND (latitude BETWEEN ({approxlatitude}-{margin}) AND ({approxlatitude}+{margin})) LIMIT 1"
        query_job = client.query(query)  # Make an API request.
        if len(query_job) > 0 or margin > 5:
            break
        else:
            margin *= 2
    if margin > 5:
        return "Sorry, there is no pub close to those coordinates"
    return query_job[0]