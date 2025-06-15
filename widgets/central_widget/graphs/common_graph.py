from PySide6.QtCharts import QChartView, QChart, QLineSeries
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
from PySide6.QtCharts import QValueAxis
import numpy as np

class CommonGraph(QChartView):
    def __init__(self, x_data: np.ndarray = None, y_data: np.ndarray = None, x_label = 'x', y_label = 'y', width = 700, height = 500):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)
        self.chart: QChart = QChart()
        # self.chart.setAnimationOptions(QChart.AllAnimations)
        self.setChart(self.chart)
        self.setFixedSize(width, height)
        self.add_series(x_data, y_data, x_label, y_label)
        self.x_data = x_data
        self.y_data = y_data

    def set_limits(self, min_limit: float, max_limit: float):
        self.axis_x.setRange(min_limit, max_limit)
        # automatically set y-axis range to the min and of the y data within the new x-axis range
        y_data_in_range = self.y_data[np.where((self.x_data >= min_limit) & (self.x_data <= max_limit))]
        y_max, y_min = max(y_data_in_range), min(y_data_in_range)
        span = y_max - y_min
        self.axis_y.setRange(y_min - 0.1 * span, y_max + 0.1 * span)

    def add_series(self, x_data, y_data, x_label = 'x', y_label = 'y'):
        if x_data is None or y_data is None:
            self.chart.removeAllSeries()
            return
        # Create QLineSeries
        self.series = QLineSeries()
        self.series.setName(y_label)
        
        for x_val, y_val in zip(x_data, y_data):
            self.series.append(x_val, y_val)

        self.chart.addSeries(self.series)

        # Setting X-axis
        self.axis_x = QValueAxis()
        self.axis_x.setTickCount(10)
        self.axis_x.setTitleText(x_label)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)
        # Setting Y-axis
        self.axis_y = QValueAxis()
        self.axis_y.setTickCount(10)
        self.axis_y.setTitleText(y_label)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)
