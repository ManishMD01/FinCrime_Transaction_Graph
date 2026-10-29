#!/bin/bash
PROJECT_ROOT="/home/pritsingh000/Git/FinCrime_Transaction_Graph"
export AIRFLOW_HOME=$PROJECT_ROOT/airflow
export PYTHONPATH=$PROJECT_ROOT:$PROJECT_ROOT/src:$PROJECT_ROOT/bigquery
export GOOGLE_APPLICATION_CREDENTIALS=""
export AIRFLOW__CORE__EXECUTOR=SequentialExecutor
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=sqlite:///$AIRFLOW_HOME/airflow.db

cd $PROJECT_ROOT
source venv/bin/activate

mkdir -p $AIRFLOW_HOME/{dags,logs,plugins}
cp $PROJECT_ROOT/airflow/dags/*.py $AIRFLOW_HOME/dags/ 2>/dev/null

PYTHON="$PROJECT_ROOT/venv/bin/python"

if [ ! -f "$AIRFLOW_HOME/airflow.db" ]; then
    $PYTHON -c "from airflow.utils import db; db.initdb()" 2>&1 | tail -1
    $PYTHON -c "
from airflow.models import User
from airflow.utils.session import create_session
from airflow.auth.managers.models.resource_details import ResourceDetails
" 2>&1 | tail -1
fi

nohup $PYTHON -m airflow scheduler >> $AIRFLOW_HOME/logs/scheduler.log 2>&1 &
nohup $PYTHON -m airflow webserver --port 8081 >> $AIRFLOW_HOME/logs/webserver.log 2>&1 &
sleep 30
echo "Done"
ps aux | grep "[a]irflow" | wc -l
