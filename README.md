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
- Setting up Infrastructure

## Notable issues
- Compressing json files
- Airflow Setup

