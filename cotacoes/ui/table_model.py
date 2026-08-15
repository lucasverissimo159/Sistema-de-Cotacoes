from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from PyQt6.QtGui import QColor
import pandas as pd

from ..core.data_manager import parse_price

class PandasModel(QAbstractTableModel):
    def __init__(self, df=None):
        super().__init__()
        self._df = df if df is not None else pd.DataFrame()
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._df)
    
    def columnCount(self, parent=QModelIndex()):
        return len(self._df.columns)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return QVariant()
        
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            value = self._df.iloc[index.row(), index.column()]
            return str(value) if pd.notna(value) else ""
        
        if role == Qt.ItemDataRole.BackgroundRole:
            if index.row() % 2 == 0:
                return QColor(250, 250, 250)
        
        return QVariant()
    
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole:
            self._df.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._df.columns[section])
            if orientation == Qt.Orientation.Vertical:
                return str(section + 1)
        
        if role == Qt.ItemDataRole.BackgroundRole:
            if orientation == Qt.Orientation.Horizontal:
                return QColor(70, 130, 180)
        
        if role == Qt.ItemDataRole.ForegroundRole:
            if orientation == Qt.Orientation.Horizontal:
                return QColor(255, 255, 255)
        
        return QVariant()
    
    def flags(self, index):
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable
    
    def sort(self, column, order=Qt.SortOrder.AscendingOrder):
        """Ordena a tabela ao clicar no cabeçalho.

        Usa ordenação numérica quando a coluna parece conter números (ex.:
        PREÇO em formatos diversos); caso contrário, ordena como texto
        (case-insensitive). Sem isso, o clique no cabeçalho não faz nada.
        """
        if self._df is None or self._df.empty:
            return
        if column < 0 or column >= len(self._df.columns):
            return

        col = self._df.columns[column]
        ascending = (order == Qt.SortOrder.AscendingOrder)

        numeric = self._df[col].map(parse_price)
        if numeric.notna().sum() >= max(1, len(self._df) // 2):
            order_key = numeric.values          # maioria numérica -> ordena por número
        else:
            order_key = self._df[col].astype(str).str.lower().values

        self.layoutAboutToBeChanged.emit()
        self._df = (
            self._df.assign(_sort_key=order_key)
            .sort_values('_sort_key', ascending=ascending,
                         kind='mergesort', na_position='last')
            .drop(columns='_sort_key')
            .reset_index(drop=True)
        )
        self.layoutChanged.emit()

    def update_dataframe(self, df):
        self.beginResetModel()
        self._df = df
        self.endResetModel()
    
    def get_dataframe(self):
        return self._df.copy()
    
    def insertRows(self, row, count, parent=QModelIndex()):
        self.beginInsertRows(parent, row, row + count - 1)
        for _ in range(count):
            new_row = pd.DataFrame([[None] * len(self._df.columns)], columns=self._df.columns)
            self._df = pd.concat([self._df.iloc[:row], new_row, self._df.iloc[row:]]).reset_index(drop=True)
        self.endInsertRows()
        return True
    
    def removeRows(self, row, count, parent=QModelIndex()):
        if row < 0 or row + count > len(self._df):
            return False
        
        self.beginRemoveRows(parent, row, row + count - 1)
        self._df = self._df.drop(self._df.index[row:row + count]).reset_index(drop=True)
        self.endRemoveRows()
        return True
