import csv, urllib.request
from google.cloud import bigquery
from google.cloud import storage

def download_csv():
    url = 'https://raw.githubusercontent.com/openbrewerydb/openbrewerydb/master/breweries.csv'
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]

    with open("csv.csv", "w") as file:
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

def create_and_upload_blob(source_file_name):
    storage_client = storage.Client()
    storage_client.create_bucket("mikkotreenaa")
    bucket = storage_client.bucket("mikkotreenaa")
    blob = bucket.blob("mikontreenifilu")
    blob.upload_from_filename(source_file_name)

def upload_to_bq():
    PROJECT_ID = 'week9-2-323806'
    client = bigquery.Client(project=PROJECT_ID, location="US")
    file_name = "csv.csv"
    dataset_id = "Breweries-testi"
    table_id = "names2-testi"
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.autodetect = True
    with open(file_name, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
    job.result()
    print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))


def main():
    download_csv()
    create_and_upload_blob("csv.csv")
    upload_to_bq()