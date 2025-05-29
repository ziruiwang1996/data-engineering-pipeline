from datetime import datetime, timedelta
from airflow import DAG
from docker.types import Mount
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
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
    schedule="@daily",
    start_date=datetime(2025, 5, 28),
    catchup=False,
) as dag:
    
    t1 = S3KeySensor(
        task_id="wait_for_raw_csv",
        bucket_key="raw-data/*.csv",
        bucket_name="raw-data",
        aws_conn_id="minio_default",
        poke_interval=60,
        timeout=60*60,
        mode="poke"
    )

    t2 = DockerOperator(
        task_id="clean_and_normalize_data",
        image="apache/spark-py:latest",
        container_name="pyspark",
        api_version="auto",
        auto_remove="success",
        command=[
            "spark-submit", 
            "--jars", 
            "/app/postgresql-42.7.6.jar", 
            "/app/clean_and_normalize.py",
            "/mnt/minio/{{ task_instance.xcom_pull(task_ids='wait_for_raw_csv')}}"
        ],
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=[
            Mount(source='minio_data', target='/mnt/minio', type='bind'),   # mount MinIO data for shared access
            Mount(source='pyspark', target='/app', type='bind'),            # map local directory to the container
        ]
    )

    t1 >> t2