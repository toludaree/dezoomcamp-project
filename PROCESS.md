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

    
