
from google.cloud import bigquery
from google.cloud import storage

def download_csv():
    import csv, urllib.request

    url = 'https://raw.githubusercontent.com/openbrewerydb/openbrewerydb/master/breweries.csv'
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]

    with open("/tmp/pubs.csv", "w") as file:
        csv_reader = csv.reader(lines, delimiter=',')
        for row in csv_reader:
            if row[15]!="":
                try:
                    row[1] = row[1].replace(" ", "")
                    row[1] = row[1].replace(",", "")
                    row[2] = row[2].replace("#", "")
                    row[3] = row[3].replace(",","")
                    file.write(f"{row[0]},{row[1]},{row[3]},{row[6]},{float(row[15])},{float(row[16])}\n")
                except:
                    pass

def create_and_upload_blob():
    storage_client = storage.Client()
    #storage_client.create_bucket("leonpaipline")
    bucket = storage_client.bucket("breweries_data")
    blob = bucket.blob("pubs")
    blob.upload_from_filename("/tmp/pubs.csv")

def upload_to_bq():
    PROJECT_ID = 'leo820'
    client = bigquery.Client(project=PROJECT_ID, location="US")
    file_name = "/tmp/pubs.csv"
    dataset_id = "Breweries"
    table_id = "names"
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.autodetect = True
    with open(file_name, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
    job.result()
    print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))


def main(request):
    download_csv()
    create_and_upload_blob()
    upload_to_bq()