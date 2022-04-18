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

## Airflow notes
- What happened on 12th September 2019 from 8am
- Something occured at 8am that day.. there is no more record.. that broke the pipeline since I downloaded by day and not hours
- curl compresses the result together. wget downloads by hour
- No recorded data for 2020-08-21 from 9am
- No recorded data for 2020-08-22 at all
8GB RAM would have been enough for this project 

# Data processing
- The files I have on GCS are terabytes
- I am officially going to use DataProc
- But I want to test Apache Spark again by watching those videos by Alexey

### Goals
- Set up Spark on VM
- Refresh knowledge of Spark and understand the dataset better

### Issues
- The schema inferred by spark.read.json tries to account for every key-value pair and they are different with the event type. It created a struct type that had many deep levels. I used MapType for now in the forces schema. Lets see how it goes
- I don't really understand the payload part. I'll try not to work with it at all in creating my dashboard to avoid complications
- When I tested with 2019-08-30-0, the json gzipped file is 25MB, On loading into a spark df, enforcing a schema, repartitioning(24), the file is 44MB

### Testing
- I want to connect to my GCS to my Spark cluster, work with 2019/01. run my business logic and pudh my results back to GCS.
- I have finished with the logic of how my processing would be

## Restructuring
### Outline
- I'm ingesting GH Archive data daily. I'll start from the beginning of this month..
- GH Archive --> GCS --> DataProc --> BigQuery --> Google Data Studio