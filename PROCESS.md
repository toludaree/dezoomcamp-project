## Infrastructure Setup
- Create a GCP account if you do not have one. Google gives $300 free credits
- Create a new project.
- This project might get compute-intensive so it is better to use a VM instance on GCP for this project. This video explains how to set it up excellently well
- Go to IAM & Admin and Create a service account and download the JSON credentials. Put it in ${HOME}/.google/credentials
    - This service account would handle all our project resources e.g BigQuery, GCS, DataProc
    - Give the service account a name, e.g project admin
    - The ID would be generated automatically
    - At the sidebar, go to `manage keys`. Add a key and download the JSON private key file

- Google Compute Engine comes with gcloud pre-installed. If not, you can install gcloud SDk here

- Normal way of authenticating
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS=~/.google/credentials
    gcloud auth aplication-default login #  OAuth
    ```
    This would not work ina VM so we'd use this:
    ```bash
    gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
    ```

### Terraform
- I want to create GCS, BigQuery and Dataproc (maybe later sha)
- We need to edit the permissions in our service account
    - Storage Admin, Storage Object Admin, BigQuery Admin, DataProc Administrator
- Enable this APIs for your project
    - https://console.cloud.google.com/apis/library/iam.googleapis.com
    - https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com
- I'm using version 1.1.7 in my `.terraform-version` file. Change this value if you're using another version. Check `terraform -v`
- cd into terraform directory
- run `terraform init`
- `terrafrom plan` - an overview of what will hapen
- `terraform apply` - this would perform the tasks
> If you're in a new session, export he google application credentials again

## Ingest data into GCS
- The goal is to ingest data into the GCS bucket using Airflow
- Airflow tasks
    - Download the dataset
    - Transfer it to GCS
    - Delete the dataset

###  Basic Steps
- Set up Airflow (the light version)
- Create the DAGS
- Run the DAGS

### Verbose Steps
- cd into airflow directory
- Run `docker-compose build`
- Run `docker-compose up airflow-init`
- Run `docker-compose up`