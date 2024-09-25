import logging
import time
from memory_profiler import memory_usage  # Importar memory_usage

from functions import generate_csv_with_aggregations

logging.basicConfig(filename='data_processing.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def run_process():
    input_csv = 'data.csv'
    output_csv = 'statistics.csv'

    start_time = time.time()

    try:
        generate_csv_with_aggregations(input_csv, output_csv)
    except Exception as e:
        logging.error(f'Error en el procesamiento del archivo: {e}')
    finally:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f'Tiempo de ejecución: {elapsed_time:.2f} segundos')

if __name__ == "__main__":
    mem_usage = memory_usage((run_process, ))
    print(f'Máxima memoria utilizada: {max(mem_usage)} MB')