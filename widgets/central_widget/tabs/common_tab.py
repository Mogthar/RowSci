from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from data.data_manager import dataManager
from data.data_source import DataSource


class CommonTab(QWidget):
    def __init__(self, data_source: DataSource):
        super().__init__()
        self.data_source = data_source
        self.data = dataManager.get_data(self.data_source)

        self.layout = QVBoxLayout()
        self.status_text = QLabel()
        self.layout.addWidget(self.status_text)
        self.setLayout(self.layout)

        self.update()

    def update(self):
        if self.data.main_table is not None:
            self.status_text.setText(f"{self.data_source.value} data loaded")
        else:
            self.status_text.setText("No data loaded")