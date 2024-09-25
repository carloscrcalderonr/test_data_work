import pandas as pd
import logging

logging.basicConfig(filename='data_processing.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def read_file(filename):
    """Lee un archivo CSV y devuelve un DataFrame en chunks."""
    try:
        logging.info(f'Intentando leer el archivo: {filename}')

        df = pd.read_csv(filename, dtype=str, chunksize=50000, header=0)

        for chunk in df:
            logging.info(f'Datos leídos (primeras filas):\n{chunk.head()}')
            yield chunk

    except FileNotFoundError:
        logging.error(f'El archivo {filename} no fue encontrado.')
        raise
    except Exception as e:
        logging.error(f'Error al leer el archivo {filename}: {e}')
        raise


def validate_data(df):
    """Valida y limpia los datos en el DataFrame."""
    try:
        logging.info('Validando datos...')

        logging.info(f'Datos leídos:\n{df.head()}')

        original_fecha = df['Fecha'].copy()
        original_costo = df['Costo'].copy()

        df['ID'] = pd.to_numeric(df['ID'], errors='coerce')

        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d', errors='coerce')
        logging.info('Conversión de fechas completa.')

        df['Costo'] = pd.to_numeric(df['Costo'], errors='coerce')
        logging.info('Conversión de costos completa.')

        invalid_df = df[df.isnull().any(axis=1)]

        if not invalid_df.empty:
            logging.warning(f'Se encontraron {len(invalid_df)} filas inválidas.')
            invalid_df = invalid_df.copy()

            invalid_df['Reason'] = invalid_df.apply(lambda row: generate_reason(row, original_fecha, original_costo),
                                                    axis=1)
            invalid_df['Fecha_Original'] = original_fecha[invalid_df.index]
            invalid_df['Costo_Original'] = original_costo[invalid_df.index]

            save_deleted_data(invalid_df[['ID', 'Nombre', 'Fecha_Original', 'Costo_Original', 'Reason']])

        valid_df = df.dropna()
        logging.info('Validación completa, se eliminaron filas con valores faltantes.')
        logging.info(f'Número de filas válidas después de la validación: {len(valid_df)}')
        return valid_df

    except KeyError as e:
        logging.error(f'Columna faltante en el DataFrame durante la validación: {e}')
        raise
    except Exception as e:
        logging.error(f'Error al validar datos: {e}')
        raise


def generate_reason(row, original_fecha, original_costo):
    """Genera una razón para los datos inválidos en el DataFrame."""
    reasons = []
    if pd.isnull(row['Fecha']):
        reasons.append(f"Fecha inválida: {original_fecha[row.name]}")
    if pd.isnull(row['Costo']):
        reasons.append(f"Costo inválido: {original_costo[row.name]}")
    if pd.isnull(row['ID']):
        reasons.append(f"ID inválido: {row['ID']}")
    return "Datos Inválidos: " + ", ".join(reasons)


def normalize_data(df):
    """Normaliza los datos en el DataFrame, convirtiendo nombres a mayúsculas."""
    try:
        logging.info('Normalizando datos...')
        df.loc[:, 'Nombre'] = df['Nombre'].str.upper()  # Usar .loc para evitar el SettingWithCopyWarning
        logging.info('Normalización completa, se han convertido los nombres a mayúsculas.')
        return df
    except KeyError as e:
        logging.error(f'Columna faltante en el DataFrame durante la normalización: {e}')
        raise
    except Exception as e:
        logging.error(f'Error al normalizar datos: {e}')
        raise


def delete_duplicates(df):
    """Elimina entradas duplicadas en el DataFrame, manteniendo una fila por cada ID duplicado."""
    try:
        logging.info('Eliminando duplicados...')

        duplicate_ids = df[df.duplicated(subset=['ID'], keep=False)]['ID'].unique()

        if len(duplicate_ids) > 0:
            logging.warning(f'Se encontraron {len(duplicate_ids)} IDs duplicados.')

            df_no_duplicates = df.drop_duplicates(subset=['ID'], keep='first')

            duplicates_to_delete = df[df['ID'].isin(duplicate_ids) & ~df.index.isin(df_no_duplicates.index)].copy()
            duplicates_to_delete.loc[:, 'Reason'] = 'ID duplicado'
            duplicates_to_delete.loc[:, 'ID'] = duplicates_to_delete['ID'].astype('Int64')

            save_deleted_data(duplicates_to_delete[['ID', 'Nombre', 'Fecha', 'Costo', 'Reason']])

        else:
            df_no_duplicates = df.copy()

        logging.info('Eliminación de duplicados completa.')
        logging.info(f'Número de filas después de la eliminación de duplicados: {len(df_no_duplicates)}')

        return df_no_duplicates

    except Exception as e:
        logging.error(f'Error al eliminar duplicados: {e}')
        raise


def save_deleted_data(df):
    """Guarda los datos eliminados junto con la razón en un archivo CSV."""
    try:
        df.to_csv('deleted_data.csv', mode='a', index=False, header=not pd.io.common.file_exists('deleted_data.csv'))
        logging.info(f'Datos eliminados guardados en deleted_data.csv, total registros: {len(df)}')
    except Exception as e:
        logging.error(f'Error al guardar datos eliminados: {e}')


def generate_csv_with_aggregations(input_csv, output_csv):
    """Genera un archivo CSV con estadísticas a partir de los datos procesados."""
    try:
        aggregated_data = pd.DataFrame()
        logging.info(f'Comenzando a generar estadísticas a partir del archivo: {input_csv}')

        for chunk in read_file(input_csv):
            validated_chunk = validate_data(chunk)
            normalized_chunk = normalize_data(validated_chunk)
            final_chunk = delete_duplicates(normalized_chunk)

            aggregated_data = pd.concat([aggregated_data, final_chunk], ignore_index=True)

        aggregated_data['ID'] = aggregated_data['ID'].astype('Int64')  # Asegurarse de que ID sea de tipo entero
        aggregated_data.to_csv('data_clean.csv', index=False)
        logging.info('Datos limpios guardados en data_clean.csv')

        aggregated_results = aggregated_data.groupby('Nombre').agg(
            Suma_Costo=('Costo', 'sum'),
            Promedio_Costo=('Costo', 'mean')
        ).reset_index()

        # Guardar las estadísticas en un nuevo archivo CSV
        aggregated_results.to_csv(output_csv, index=False)
        logging.info(f'Estadísticas guardadas en {output_csv}')
    except Exception as e:
        logging.error(f'Error en la generación de CSV y agregaciones: {e}')
        raise
