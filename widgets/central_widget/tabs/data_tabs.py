from PySide6.QtWidgets import QTabWidget, QWidget, QLabel, QVBoxLayout
from data.data_manager import dataManager

class DataTabs(QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)
        for source in dataManager.data_sources.keys():
            self.addTab(SingleTab(source), source)


class SingleTab(QWidget):
    def __init__(self, source):
        super().__init__()
        self.source = source
        self.layout = QVBoxLayout()

