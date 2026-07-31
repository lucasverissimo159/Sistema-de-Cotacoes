from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from PyQt6.QtGui import QColor
import pandas as pd

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
