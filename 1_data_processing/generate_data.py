import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

num_records = 250000
product_names = [f'Producto {chr(65 + i)}' for i in range(26)]  # Producto A, Producto B, ..., Producto Z
start_date = datetime(2024, 1, 1)

ids = np.random.randint(1, 10001, size=num_records)  # IDs entre 1 y 10,000
names = np.random.choice(product_names, size=num_records)  # Nombres aleatorios de la lista
dates = [start_date + timedelta(days=random.randint(0, 30)) for _ in range(num_records)]  # Fechas aleatorias en enero de 2024
costs = np.round(np.random.uniform(50, 300, size=num_records), 2)  # Costos aleatorios entre 50 y 300

data = {
    'ID': ids,
    'Nombre': names,
    'Fecha': [date.strftime('%Y-%m-%d') for date in dates],
    'Costo': costs
}

df = pd.DataFrame(data)

df.to_csv('datos_aleatorios.csv', index=False)
print('CSV generado con éxito: datos_aleatorios.csv')
