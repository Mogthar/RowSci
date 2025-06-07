from PySide6.QtWidgets import QTabWidget
from data.data_source import DataSource
from widgets.central_widget.tabs.cortex_tab import CortexTab
from widgets.central_widget.tabs.artinis_tab import ArtinisTab


class DataTabs(QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.addTab(CortexTab(), DataSource.CORTEX.value)
        self.addTab(ArtinisTab(), DataSource.ARTINIS.value)

