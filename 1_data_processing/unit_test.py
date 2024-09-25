import pandas as pd
import unittest

from functions import normalize_data, delete_duplicates, validate_data


# Importar las funciones del módulo que estás probando
# from your_module import read_file, validate_data, normalize_data, delete_duplicates, generate_reason

class TestDataProcessing(unittest.TestCase):



    def test_validate_data_valid(self):
        df = pd.DataFrame({'ID': [1], 'Nombre': ['Test'], 'Fecha': ['2023-01-01'], 'Costo': ['100']})
        valid_df = validate_data(df)
        self.assertEqual(len(valid_df), 1)

    def test_validate_data_invalid(self):
        df = pd.DataFrame({'ID': [1, 2], 'Nombre': ['Test', 'Invalid'], 'Fecha': ['2023-01-01', 'invalid_date'],
                           'Costo': ['100', 'invalid_cost']})
        valid_df = validate_data(df)
        self.assertEqual(len(valid_df), 1)  # Solo una fila válida

    def test_normalize_data(self):
        df = pd.DataFrame({'ID': [1], 'Nombre': ['test']})
        normalized_df = normalize_data(df)
        self.assertEqual(normalized_df['Nombre'].iloc[0], 'TEST')

    def test_delete_duplicates(self):
        df = pd.DataFrame({'ID': [1, 1, 2], 'Nombre': ['Test', 'Test', 'Another'],
                           'Fecha': ['2023-01-01', '2023-01-01', '2023-01-02'], 'Costo': [100, 100, 200]})
        df_no_duplicates = delete_duplicates(df)
        self.assertEqual(len(df_no_duplicates), 2)  # Debe eliminar uno de los duplicados


if __name__ == '__main__':
    unittest.main()
