from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from widgets.central_widget.graphs.common_graph import CommonGraph
import numpy as np

class GraphView(QWidget):
    def __init__(self, x_data: np.ndarray = None, y_data: np.ndarray = None, x_label = 'x', y_label = 'y'):
        super().__init__()
        self.graph = CommonGraph(x_data, y_data, x_label, y_label)
        self.stats = Stats(x_data, y_data)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.graph)
        self.layout.addWidget(self.stats)
        self.setLayout(self.layout)

    def set_limits(self, min_limit: float, max_limit: float):
        self.graph.set_limits(min_limit, max_limit)
        self.stats.set_limits(min_limit, max_limit)


class Stats(QWidget):
    def __init__(self, x_data: np.ndarray = None, y_data: np.ndarray = None):
        super().__init__()
        self.x_data = x_data
        self.y_data = y_data
        
        self.layout = QVBoxLayout()
        self.min_label = QLabel()
        self.max_label = QLabel()
        self.avg_label = QLabel()
        self.layout.addWidget(self.min_label)
        self.layout.addWidget(self.max_label)
        self.layout.addWidget(self.avg_label)
        self.setLayout(self.layout)

        self.set_limits(np.amin(x_data), np.amax(x_data))

    def set_limits(self, min_limit: float, max_limit: float):
        mask = (self.x_data >= min_limit) & (self.x_data <= max_limit)
        masked_y_data = self.y_data[mask]
        self.min_label.setText(f"Min: {np.amin(masked_y_data):.2f}")
        self.max_label.setText(f"Max: {np.amax(masked_y_data):.2f}")
        self.avg_label.setText(f"Avg: {np.mean(masked_y_data):.2f}")
