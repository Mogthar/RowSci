from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from data.data_manager import dataManager
from data.data_source import DataSource
from widgets.central_widget.tables.common_table import CommonTable
from widgets.central_widget.graphs.common_graph import CommonGraph
from pandas.api.types import is_numeric_dtype
from PySide6.QtWidgets import QHBoxLayout, QCheckBox
from PySide6.QtCore import Qt


class CommonTab(QWidget):
    def __init__(self, data_source: DataSource):
        super().__init__()
        self.data_source = data_source
        self.data = dataManager.get_data(self.data_source)

        self.layout = QHBoxLayout()
        # status text
        self.status_text = QLabel()
        self.layout.addWidget(self.status_text)
        
        # Add checkbox container
        self.checkbox_layout = QHBoxLayout()
        self.layout.addLayout(self.checkbox_layout)
        
        # table
        self.table = CommonTable(self.data.main_table)
        self.layout.addWidget(self.table)
        # graph
        self.graphs: dict[str, CommonGraph] = {}
        self.checkboxes: dict[str, QCheckBox] = {}
    
        self.setLayout(self.layout)
        self.update()

    def update(self):
        self.update_table()
        self.update_status_text()
        self.update_graphs()
    
    def update_table(self):
        self.table.set_data(self.data.main_table)
    
    def update_status_text(self):
        if self.data.main_table is not None:
            self.status_text.hide()
        else:
            self.status_text.show()
            self.status_text.setText("No data loaded")

    def update_graphs(self):
        self.graphs = {}
        for checkbox in self.checkboxes.values():
            self.checkbox_layout.removeWidget(checkbox)
            checkbox.deleteLater()
        self.checkboxes.clear()

        if self.data.main_table is None:
            return

        first_column = self.data.main_table.columns[0]
        for column in self.data.main_table.columns[1:3]:
            print("column", column, is_numeric_dtype(self.data.main_table[column]), self.data.main_table[column].dtype)
            if is_numeric_dtype(self.data.main_table[column]):
                print("adding graph for", column)
                # Create checkbox
                checkbox = QCheckBox(column)
                checkbox.setChecked(True)
                checkbox.stateChanged.connect(lambda state, col=column: self.toggle_graph(col, state))
                self.checkboxes[column] = checkbox
                self.checkbox_layout.addWidget(checkbox)
                
                graph = CommonGraph(self.data.main_table[first_column].values, self.data.main_table[column].values, first_column, column)
                self.graphs[column] = graph
                self.layout.addWidget(graph)

    def toggle_graph(self, column, state):
        print("toggle_graph", column, state)
        if state == 2:
            self.graphs[column].show()
        else:
            self.graphs[column].hide()
