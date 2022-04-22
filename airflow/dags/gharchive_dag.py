import os
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.contrib.operators.dataproc_operator import DataProcPySparkOperator
from google.cloud import storage

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
REGION = os.environ.get("GCP_REGION")
BUCKET_NAME = os.environ.get("GCP_GCS_BUCKET")
CLUSTER_NAME = os.environ.get("GCP_DATAPROC_CLUSTER_NAME")
DATASET_NAME = os.environ.get("GCP_BIGQUERY_DATASET_NAME")

URL_TEMPLATE = "https://data.gharchive.org/" + \
    "{{ execution_date.strftime('%Y-%m-%d') }}-{0..23}.json.gz"
OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + \
    "/output-{{ execution_date.strftime('%Y-%m-%d') }}.json.gz"
GCS_PATH_TEMPLATE = "raw/gh_archive/" + \
    "{{ execution_date.strftime('%Y') }}/" + \
    "{{ execution_date.strftime('%Y-%m') }}/" + \
    "{{ execution_date.strftime('%Y-%m-%d') }}.json.gz"
PYSPARK_JOB = f"{AIRFLOW_HOME}/dataproc/spark_job.py"

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
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}
with DAG(
    dag_id="gharchive_dag",
    description="Pipeline for Data Engineering Zoomcamp Project",
    default_args=default_args,
    schedule_interval="0 8 * * *",
    start_date=datetime(2022, 4, 1),
    max_active_runs=1,
    catchup=True
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

    processing_task = DataProcPySparkOperator(
        task_id="batch_processing_with_dataproc",
        job_name="pyspark_job_{{ execution_date.strftime('%Y-%m-%d') }}",
        cluster_name=f"{CLUSTER_NAME}",
        dataproc_jars=["gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"],
        gcp_conn_id="google_cloud_default",
        region=f"{REGION}",
        main="gs://gharchive_bucket_endless-context-344913/dataproc/spark_job.py",
        arguments = [
            "--input_file", f"gs://gharchive_bucket_endless-context-344913/{GCS_PATH_TEMPLATE}",
            "--general_activity", f"{DATASET_NAME}.general_activity",
            "--active_users", f"{DATASET_NAME}.active_users"
        ]
    )

    download_task >> upload_task >> delete_task >> processing_task