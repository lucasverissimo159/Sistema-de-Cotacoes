import unittest
import pandas as pd

from cotacoes.core.data_manager import DataManager


class DataManagerValidationTest(unittest.TestCase):
    def test_validate_dataframe_reports_missing_and_blank_required_fields(self):
        dm = DataManager()
        df = pd.DataFrame([
            {
                'FORNECEDOR': 'Fornecedor A',
                'PRODUTO': '',
                'QUANTIDADE': '1 KG',
                'PREÇO': 'R$ 12,00',
                'VALIDADE': '',
                'ORIGEM': 'Brasil',
            }
        ])

        report = dm.validate_dataframe(df)

        self.assertFalse(report['is_valid'])
        self.assertEqual(report['empty_required_cells'], 2)
        self.assertIn('PRODUTO', report['empty_columns'])
        self.assertIn('VALIDADE', report['empty_columns'])


if __name__ == '__main__':
    unittest.main()
