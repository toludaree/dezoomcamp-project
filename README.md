# Data Engineering Zoomcamp Project

## Elements
- Proposed Dataset - [Github Archive Dataset](https://www.gharchive.org/)
- Proposed Tools
    - Docker - Containerisation
    - Terraform - Infrastructure management
    - GCP - Cloud Services
        - Google Compute Engine - Virtual Machine
        - Google Cloud Storage - Data Lake
        - BigQuery - Data Warehouse
        - Google DataProc
    - Airflow - Workflow Orchestration
    - Spark
    - Google Data Studio / Metabase - Visualisation

## About the Dataset
Github Archive is a project to record the public Github timeline, archive it, and make it accessible for further analysis.

## Problem Description
- A company {company name} aims to provide a tool for developers.
- They wish to carry out a survey to understand developer activity in the years 2019 and 2020.
- This would give them insights on how to develop their tool
- Proposed end-goal questions are below:

## Proposed End-goal Questions
- What month and day of the week is Github most active?
- How did corona virus affect developer activity?
- What are the most active repositories each year grouped by event
- Most popular organisation
- ... 

## Architecture
GHArchive -->  GCS --> Spark/DataProc --> BigQuery --> Data Studio

## Todo
- Architecture and Workflow walkthrough
- Setting up Infrastructure on GCP
- Ingest into GCS
- Spark
- BigQuery
- Data Studio

## Notable issues
- Compressing json files
- Airflow Setup


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
    - 