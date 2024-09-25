# main.py

from dotenv import load_dotenv
import os
import logging
from functions import (
    create_bucket_s3,
    upload_file_s3,
    create_bucket_gcs,
    upload_file_gcs
)

# Configurar el logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log',  # Guarda los logs en un archivo
                    filemode='a')  # 'a' para añadir, 'w' para sobrescribir

# Cargar variables de entorno desde el archivo .env
load_dotenv()


def main():
    nombre_bucket_s3 = "name-bucket-s3"  # Cambia esto por tu nombre de bucket deseado
    nombre_bucket_gcs = "name-bucket-gcs"  # Cambia esto por tu nombre de bucket deseado
    nombre_archivo = "data.csv"  # Cambia esto por el archivo que deseas subir
    ruta_archivo = "./" + nombre_archivo  # Asegúrate de que el archivo esté en esta ruta

    # Intentar crear y subir en S3
    try:
        logging.info(f"Creando bucket S3: {nombre_bucket_s3}...")
        print(f"Creando bucket S3: {nombre_bucket_s3}...")
        create_bucket_s3(nombre_bucket_s3)

        logging.info(f"Subiendo archivo a S3: {nombre_archivo}...")
        print(f"Subiendo archivo a S3: {nombre_archivo}...")
        upload_file_s3(nombre_bucket_s3, nombre_archivo, ruta_archivo)
    except Exception as e:
        logging.error(f"Error en S3: {e}")
        print(f"Error en S3: {e}")

    # Intentar crear y subir en GCS
    try:
        logging.info(f"Creando bucket GCS: {nombre_bucket_gcs}...")
        print(f"Creando bucket GCS: {nombre_bucket_gcs}...")
        create_bucket_gcs(nombre_bucket_gcs)

        logging.info(f"Subiendo archivo a GCS: {nombre_archivo}...")
        print(f"Subiendo archivo a GCS: {nombre_archivo}...")
        upload_file_gcs(nombre_bucket_gcs, nombre_archivo, ruta_archivo)
    except Exception as e:
        logging.error(f"Error en GCS: {e}")
        print(f"Error en GCS: {e}")


if __name__ == "__main__":
    main()
