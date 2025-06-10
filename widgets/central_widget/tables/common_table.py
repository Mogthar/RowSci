from PySide6.QtWidgets import QTableView
from widgets.central_widget.tables.common_table_model import CommonTableModel
import pandas as pd


class CommonTable(QTableView):
    def __init__(self, data: pd.DataFrame | None = None):
        super().__init__()
        self.set_data(data)
        self.setStyleSheet("QTableView { color: black; background-color: white; }")

    def set_data(self, data: pd.DataFrame | None = None):
        self.model = CommonTableModel(data)
        self.setModel(self.model)

\

