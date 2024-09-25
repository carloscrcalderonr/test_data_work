# functions.py

import boto3
from google.cloud import storage
import os
import logging
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log',
                    filemode='a')

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION', 'us-east-1')


def create_bucket_s3(nombre_bucket):
    """Crea un bucket en S3."""
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )
        s3.create_bucket(Bucket=nombre_bucket)
        logging.info(f'Bucket S3 "{nombre_bucket}" creado exitosamente en la región {aws_region}.')
        print(f'Bucket S3 "{nombre_bucket}" creado exitosamente en la región {aws_region}.')
    except Exception as e:
        logging.error(f'Error al crear el bucket S3: {e}')
        print(f'Error al crear el bucket S3: {e}')


def upload_file_s3(nombre_bucket, nombre_archivo, ruta_archivo):
    """Sube un archivo a un bucket de S3."""
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        s3.upload_file(ruta_archivo, nombre_bucket, nombre_archivo)
        logging.info(f'Archivo "{nombre_archivo}" subido exitosamente a "{nombre_bucket}".')
        print(f'Archivo "{nombre_archivo}" subido exitosamente a "{nombre_bucket}".')
    except Exception as e:
        logging.error(f'Error al subir el archivo "{nombre_archivo}" a S3: {e}')
        print(f'Error al subir el archivo "{nombre_archivo}" a S3: {e}')


def create_bucket_gcs(nombre_bucket):
    """Crea un bucket en Cloud Storage."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.create_bucket(nombre_bucket)
        logging.info(f'Bucket GCS "{nombre_bucket}" creado exitosamente.')
        print(f'Bucket GCS "{nombre_bucket}" creado exitosamente.')
    except Exception as e:
        logging.error(f'Error al crear el bucket GCS: {e}')
        print(f'Error al crear el bucket GCS: {e}')


def upload_file_gcs(nombre_bucket, nombre_archivo, ruta_archivo):
    """Sube un archivo a un bucket de Cloud Storage."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(nombre_bucket)
        blob = bucket.blob(nombre_archivo)
        blob.upload_from_filename(ruta_archivo)
        logging.info(f'Archivo "{nombre_archivo}" subido exitosamente a "{nombre_bucket}".')
        print(f'Archivo "{nombre_archivo}" subido exitosamente a "{nombre_bucket}".')
    except Exception as e:
        logging.error(f'Error al subir el archivo "{nombre_archivo}" a GCS: {e}')
        print(f'Error al subir el archivo "{nombre_archivo}" a GCS: {e}')
