<?php
header('Content-Type: application/json');
$cmd = "cd /home/pritsingh000/Git/FinCrime_Transaction_Graph && GOOGLE_APPLICATION_CREDENTIALS='' PYTHONPATH=/home/pritsingh000/Git/FinCrime_Transaction_Graph:/home/pritsingh000/Git/FinCrime_Transaction_Graph/src:/home/pritsingh000/Git/FinCrime_Transaction_Graph/bigquery /home/pritsingh000/Git/FinCrime_Transaction_Graph/venv/bin/python -c \"
from src.bigquery.bq_client import BigQueryClient
import json, os
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=''
try:
    c = BigQueryClient()
    df = c.query_to_dataframe(f\\\"SELECT * FROM \`{c.dataset_ref}.aml_alerts\` ORDER BY alert_timestamp DESC LIMIT 100\\\")
    print(df.to_json(orient='records'))
except Exception as e:
    print(json.dumps({'error': str(e)}))
\" 2>&1";
exec($cmd, $output, $ret);
$json = implode("\n", $output);
$lines = explode("\n", $json);
$last = end($lines);
while ($last !== false && trim($last) !== '' && ($last[0] !== '[' && $last[0] !== '{')) { array_pop($lines); $last = end($lines); }
echo trim($last);
