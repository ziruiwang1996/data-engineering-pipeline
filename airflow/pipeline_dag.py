from datetime import timedelta
from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3_key import S3KeySensor
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="etl",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=...,
    catchup=False,
) as dag:
    
    t1 = S3KeySensor(
        task_id="wait_for_raw_csv",
        bucket_key="raw-data/{{ ds }}/.*\\.csv",
        bucket_name="raw-data",
        aws_conn_id="minio_default",
        poke_interval=60,
        timeout=60*60,
    )

    t2 = DockerOperator()

    t3 = DockerOperator()

    t1 >> t2 >> t3