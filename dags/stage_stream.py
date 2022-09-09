from airflow import DAG
from datetime import datetime
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from user_functions.queries_sf import *

default_args={
        'start_date': datetime(2022, 9, 8),
        'owner':'Airflow'
    }

dag = DAG(
    "stage_stream_dag",
    default_args=default_args,
    schedule_interval=None
)



data_from_stage_into_master = SnowflakeOperator(
    task_id='data_from_stage_into_master',
    sql=q_data_from_stage_into_master,
    snowflake_conn_id='Snowflake_conn',
    dag=dag
)

