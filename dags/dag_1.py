from airflow import DAG
from datetime import datetime
from datetime import timedelta
from airflow.operators.python import PythonOperator
from user_functions.clean import to_clean
from user_functions.queries_sf import *
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

default_args={
        'start_date': datetime(2022, 9, 8),
        'owner':'Airflow'
    }

dag = DAG(
    "Snowflake_DAG",
    default_args=default_args,
    schedule_interval=timedelta(days=10)
)

prep_data = PythonOperator(
    task_id='prep_csv',
    python_callable=to_clean,
    dag=dag
)

create_db = SnowflakeOperator(
    task_id='create_db',
    sql=q_create_db,
    snowflake_conn_id='Snowflake_conn',
    dag=dag
)

create_stage = SnowflakeOperator(
    task_id='create_stage',
    sql=q_create_stage,
    snowflake_conn_id='Snowflake_conn',
    dag=dag
)

create_file_format = SnowflakeOperator(
    task_id='create_file_format',
    sql=q_create_format_csv,
    snowflake_conn_id='Snowflake_conn',
    dag=dag
)

create_table = SnowflakeOperator(
    task_id='create_table',
    sql=q_create_table,
    snowflake_conn_id='Snowflake_conn',
    dag=dag
)

put_csv_into_stage = SnowflakeOperator(
    task_id='put_csv_into_stage',
    sql=q_put_csv_into_stage,
    snowflake_conn_id='Snowflake_conn',
    dag=dag
)

copy_into_table = SnowflakeOperator(
    task_id='coppy_into_table',
    sql=q_copy_into_table,
    snowflake_conn_id='Snowflake_conn',
    dag=dag
)
triger_dag_raw = TriggerDagRunOperator(
    task_id='triger_dag_raw',
    trigger_dag_id='raw_stream_dag',
    dag=dag
)



prep_data >> create_db >> create_stage >> create_file_format >> create_table >> put_csv_into_stage >> copy_into_table >> triger_dag_raw


