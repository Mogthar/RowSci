from __future__ import annotations

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor
import pandas as pd


class CommonTableModel(QAbstractTableModel):
    def __init__(self, data: pd.DataFrame | None = None):
        QAbstractTableModel.__init__(self)
        self.load_data(data)

    def load_data(self, data: pd.DataFrame | None = None):
        self.table = data
        if data is not None:
            self.column_count = len(data.columns)
            self.row_count = len(data)
        else:
            self.column_count = 0
            self.row_count = 0

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.table.columns[section]
        else:
            return f"{section}"

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            data_point = self.table.iloc[row, column]
            return str(data_point)
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None