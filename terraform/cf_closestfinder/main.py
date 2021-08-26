from google.cloud import bigquery

client = bigquery.Client()

#Example function json payload required:
#{"longitude":"-85.48", "latitude": "42.95"}
def findclosest(request):
    request_json = request.get_json(silent=True)
    approxlongitude = float(request_json.get("longitude"))
    approxlatitude = float(request_json.get("latitude"))
    data = ""
    margin = 0.05

    while True:
        query = f"SELECT name FROM `week9-2-323806.Breweries.names` WHERE (longitude BETWEEN ({approxlongitude}-{margin}) AND ({approxlongitude}+{margin})) AND (latitude BETWEEN ({approxlatitude}-{margin}) AND ({approxlatitude}+{margin})) LIMIT 1"
        query_job = client.query(query)
        for x in query_job:
            data = x[0]
        if data == "":
            margin *= 2
        else:
            break
        if margin > 5:
            return "Sorry, there is no pub close to those coordinates"
        
    return data