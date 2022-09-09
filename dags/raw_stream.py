from airflow import DAG
from datetime import datetime
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from user_functions.queries_sf import *
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

default_args={
        'start_date': datetime(2022, 9, 8),
        'owner':'Airflow'
    }

dag = DAG(
    "raw_stream_dag",
    default_args=default_args,
    schedule_interval=None
)


data_from_raw_into_stage = SnowflakeOperator(
    task_id='data_from_raw_into_stage',
    sql=q_data_from_raw_into_stage,
    snowflake_conn_id='Snowflake_conn',
    dag=dag
)

triger_dag_stage = TriggerDagRunOperator(
    task_id='triger_dag_stage',
    trigger_dag_id='stage_stream_dag',
    dag=dag
)

data_from_raw_into_stage >> triger_dag_stage
