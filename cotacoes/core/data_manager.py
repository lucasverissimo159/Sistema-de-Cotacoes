import pandas as pd
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from pathlib import Path
from typing import List, Dict, Any
from ..config import COLUNAS_IMPORTANTES

class DataManager:
    def __init__(self):
        self.df = None
        self.file_path = None
    
    def load_excel(self, file_path: str):
        """Carrega arquivo Excel"""
        try:
            self.df = pd.read_excel(file_path)
            self.file_path = file_path
            return True
        except Exception as e:
            raise Exception(f"Erro ao carregar Excel: {str(e)}")
    
    def save_excel(self, file_path: str = None):
        """Salva DataFrame no Excel com formatação"""
        if self.df is None:
            raise ValueError("Nenhum dado para salvar")
        
        save_path = file_path or self.file_path
        if not save_path:
            raise ValueError("Caminho do arquivo não especificado")
        
        self.df.to_excel(save_path, index=False, engine='openpyxl')
        
        wb = load_workbook(save_path)
        ws = wb.active
        
        yellow_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
        header_font = Font(bold=True, size=11)
        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        for col_idx, col_name in enumerate(self.df.columns, 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center', vertical='center')
            
            if col_name in COLUNAS_IMPORTANTES:
                cell.fill = yellow_fill
        
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            for cell in row:
                cell.border = thin_border
        
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[column].width = min(max_length + 2, 50)
        
        wb.save(save_path)
        return save_path
    
    def add_rows(self, data: List[Dict[str, Any]]):
        """Adiciona novas linhas ao DataFrame"""
        if self.df is None:
            self.df = pd.DataFrame(data)
        else:
            new_df = pd.DataFrame(data)
            self.df = pd.concat([self.df, new_df], ignore_index=True)
    
    def get_dataframe(self):
        """Retorna o DataFrame atual"""
        return self.df
    
    def create_comparison(self, output_path: str):
        """Cria planilha de comparação de preços"""
        if self.df is None or self.df.empty:
            raise ValueError("Nenhum dado para comparar")
        
        comparison_df = self.df[COLUNAS_IMPORTANTES].copy()
        
        comparison_df['PREÇO'] = pd.to_numeric(comparison_df['PREÇO'], errors='coerce')
        
        comparison_df = comparison_df.sort_values(by=['PRODUTO', 'PREÇO'])
        
        comparison_df.to_excel(output_path, index=False, engine='openpyxl')
        
        wb = load_workbook(output_path)
        ws = wb.active
        
        green_fill = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')
        header_font = Font(bold=True, size=12, color='FFFFFF')
        header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
        
        for col_idx in range(1, len(COLUNAS_IMPORTANTES) + 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        current_product = None
        for row_idx in range(2, ws.max_row + 1):
            product_cell = ws.cell(row=row_idx, column=2)
            price_cell = ws.cell(row=row_idx, column=4)
            
            if product_cell.value != current_product:
                current_product = product_cell.value
                for col_idx in range(1, len(COLUNAS_IMPORTANTES) + 1):
                    ws.cell(row=row_idx, column=col_idx).fill = green_fill
        
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[column].width = min(max_length + 2, 50)
        
        wb.save(output_path)
        return output_path
    
    def clear_data(self):
        """Limpa todos os dados"""
        self.df = None
        self.file_path = None
