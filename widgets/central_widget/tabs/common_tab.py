from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QCheckBox, QScrollArea, QGridLayout, QLineEdit, QPushButton
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Qt
from data.data_manager import dataManager
from data.data_source import DataSource

from widgets.central_widget.tables.common_table import CommonTable
from widgets.central_widget.graphs.graph_view import GraphView

from pandas.api.types import is_numeric_dtype


class CommonTab(QWidget):
    def __init__(self, data_source: DataSource):
        super().__init__()
        self.data_source = data_source
        self.data = dataManager.get_data(self.data_source)

        self.layout = QHBoxLayout()
        self.table_section = TableSection(self)
        self.graph_section = GraphSection(self)

        self.layout.addWidget(self.table_section, 2)
        self.layout.addWidget(self.graph_section, 3)

        self.setLayout(self.layout)
        self.update()

    def update(self):
        self.table_section.update()
        self.graph_section.update()


class TableSection(QWidget):
    def __init__(self, parent_tab: CommonTab):
        super().__init__()
        self.parent_tab = parent_tab
        
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Create container widget for the table
        self.container = QWidget()
        self.layout = QVBoxLayout()
        self.table = CommonTable(self.parent_tab.data.main_table)
        self.layout.addWidget(self.table)
        self.container.setLayout(self.layout)
        
        # Set the container as the scroll area's widget
        self.scroll_area.setWidget(self.container)
        
        # Create main layout for the section
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

    def update(self):
        self.table.set_data(self.parent_tab.data.main_table)
        
class GraphSection(QWidget):
    def __init__(self, parent_tab: CommonTab):
        super().__init__()
        self.parent_tab = parent_tab
        
        self.layout = QVBoxLayout()
        
        self.status_text = QLabel()
        self.layout.addWidget(self.status_text)

        self.checkboxes = Checkboxes(self.parent_tab, self)
        self.layout.addWidget(self.checkboxes)

        self.limit_controller = LimitController(self)
        self.layout.addWidget(self.limit_controller)

        self.graphs = Graphs(self.parent_tab)
        self.layout.addWidget(self.graphs)
        
        self.setLayout(self.layout)

    def update(self):
        self.update_status_text()
        self.checkboxes.update()
        self.limit_controller.update()
        self.graphs.update()

    def update_status_text(self):
        if self.parent_tab.data.main_table is not None:
            self.status_text.hide()
        else:
            self.status_text.show()
            self.status_text.setText("No data loaded")

class LimitController(QWidget):
    def __init__(self, graph_section: GraphSection):
        super().__init__()
        self.graph_section = graph_section
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.min_limit = QLineEdit()
        self.min_limit.textChanged.connect(self.reset_style)
        self.min_value = 0

        self.max_limit = QLineEdit()
        self.max_limit.textChanged.connect(self.reset_style)
        self.max_value = 0

        self.min_limit.setValidator(QDoubleValidator())
        self.max_limit.setValidator(QDoubleValidator())

        self.set_limits_button = QPushButton("Set Limits")
        self.set_limits_button.clicked.connect(self.set_limits)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_limits)

        self.layout.addWidget(QLabel("Min:"))
        self.layout.addWidget(self.min_limit)
        self.layout.addWidget(QLabel("Max:"))
        self.layout.addWidget(self.max_limit)
        self.layout.addWidget(self.set_limits_button)

    def reset_style(self):
        self.min_limit.setStyleSheet("color: white;")
        self.max_limit.setStyleSheet("color: white;")
    
    def set_limits(self):
        if float(self.min_limit.text()) > float(self.max_limit.text()):
            self.min_limit.setStyleSheet("color: red;")
            self.max_limit.setStyleSheet("color: red;")
            return
        elif float(self.min_limit.text()) < self.min_value:
            self.min_limit.setStyleSheet("color: red;")
            return
        elif float(self.max_limit.text()) > self.max_value:
            self.max_limit.setStyleSheet("color: red;")
            return
        else:
            self.graph_section.graphs.set_limits(float(self.min_limit.text()), float(self.max_limit.text()))

    def reset_limits(self):
        self.min_limit.setText(str(self.min_value))
        self.max_limit.setText(str(self.max_value))
        self.graph_section.graphs.set_limits(self.min_value, self.max_value)

    def update(self):
        if self.graph_section.parent_tab.data.main_table is None:
            return
        fist_column = self.graph_section.parent_tab.data.main_table.columns[0]
        time_values = self.graph_section.parent_tab.data.main_table[fist_column].values
        self.min_value = time_values.min()
        self.max_value = time_values.max()
        self.min_limit.setText(str(self.min_value))
        self.max_limit.setText(str(self.max_value))

class Graphs(QWidget):
    def __init__(self, parent_tab: CommonTab):
        super().__init__()
        self.parent_tab = parent_tab
        self.graph_views: dict[str, GraphView] = {}

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.container = QWidget()
        self.container_layout = QVBoxLayout()
        self.container.setLayout(self.container_layout)

        self.scroll_area.setWidget(self.container)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)
    
    def update(self):
        for graph in self.graph_views.values():
            self.container_layout.removeWidget(graph)
            graph.deleteLater()
        self.graph_views.clear()

        if self.parent_tab.data.main_table is None:
            return

        for column in self.parent_tab.data.main_table.columns[1:]:
            if is_numeric_dtype(self.parent_tab.data.main_table[column]):
                self.add_graph(column)

    def add_graph(self, column: str):
        first_column = self.parent_tab.data.main_table.columns[0]
        x_values = self.parent_tab.data.main_table[first_column].values
        y_values = self.parent_tab.data.main_table[column].values
        graph = GraphView(x_values, y_values, first_column, column)
        self.graph_views[column] = graph
        self.container_layout.addWidget(graph)

    def toggle_graph(self, column, state):
        if state == 2:
            self.graph_views[column].show()
        else:
            self.graph_views[column].hide()

    def set_limits(self, min_limit: float, max_limit: float):
        for graph_view in self.graph_views.values():
            graph_view.set_limits(min_limit, max_limit)

class Checkboxes(QWidget):
    def __init__(self, parent_tab: CommonTab, graph_section: GraphSection):
        super().__init__()
        self.parent_tab = parent_tab
        self.graph_section = graph_section
        self.checkboxes: dict[str, QCheckBox] = {}
        self.layout = QGridLayout()
        self.setLayout(self.layout)

    def update(self):
        for checkbox in self.checkboxes.values():
            self.layout.removeWidget(checkbox)
            checkbox.deleteLater()
        self.checkboxes.clear()

        if self.parent_tab.data.main_table is None:
            return

        n_cols = len(self.parent_tab.data.main_table.columns[1:])
        for i, column in enumerate(self.parent_tab.data.main_table.columns[1:]):
            if is_numeric_dtype(self.parent_tab.data.main_table[column]):
                self.add_checkbox(column, i, n_cols)

    def add_checkbox(self, column: str, idx: int, n_cols: int):
        checkbox = QCheckBox(column)
        checkbox.setChecked(True)
        checkbox.stateChanged.connect(lambda state, col=column: self.graph_section.graphs.toggle_graph(col, state))
        self.checkboxes[column] = checkbox

        cutoff = n_cols // 2
        row = idx % cutoff
        col = idx // cutoff
        self.layout.addWidget(checkbox, row, col)