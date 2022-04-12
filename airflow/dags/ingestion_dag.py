import os
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from google.cloud import storage

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET_NAME = os.environ.get("GCP_GCS_BUCKET")

URL_TEMPLATE = "https://data.gharchive.org/" + \
    "{{ execution_date.strftime('%Y-%m-%d') }}-{0..23}.json.gz"
OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + \
    "/output-{{ execution_date.strftime('%Y-%m-%d') }}.json.gz"
GCS_PATH_TEMPLATE = "raw/gh_archive/" + \
    "{{ execution_date.strftime('%Y') }}/" + \
    "{{ execution_date.strftime('%Y-%m') }}/" + \
    "{{ execution_date.strftime('%Y-%m-%d') }}.json.gz"

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """
    Ref: 
    https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

default_args = {
    "depends_on_past": False,
    "retries": 1,
}
with DAG(
    dag_id="gh_ingestion_dag",
    description="Ingests GH Archive data to GCS.",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2019, 1, 1),
    end_date=datetime(2020, 12, 31),
    max_active_runs=3,
) as dag:

    download_task = BashOperator(
        task_id="download_gharchive_dataset",
        bash_command=f"curl -sSLf {URL_TEMPLATE} > {OUTPUT_FILE_TEMPLATE}"
    )

    upload_task = PythonOperator(
        task_id="upload_to_gcs",
        python_callable=upload_to_gcs,
        op_kwargs = {
            "bucket_name": BUCKET_NAME,
            "source_file_name": OUTPUT_FILE_TEMPLATE,
            "destination_blob_name": GCS_PATH_TEMPLATE,
        }
    )

    delete_task = BashOperator(
        task_id="delete_dataset_from_local",
        bash_command=f"rm {OUTPUT_FILE_TEMPLATE}"
    )

    download_task >> upload_task >> delete_task