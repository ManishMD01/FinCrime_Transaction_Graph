#!/bin/bash
PROJECT_ROOT="/home/pritsingh000/Git/FinCrime_Transaction_Graph"
export AIRFLOW_HOME=$PROJECT_ROOT/airflow
cd $PROJECT_ROOT
source venv/bin/activate
airflow dags trigger fincrime_complete_etl_pipeline
