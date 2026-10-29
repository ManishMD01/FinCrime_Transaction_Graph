#!/bin/bash
pkill -f "airflow scheduler"
pkill -f "airflow api-server"
pkill -f "airflow webserver"
echo "Airflow stopped"
