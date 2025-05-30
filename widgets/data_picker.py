from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QWidget, QHBoxLayout, QPushButton, QFileDialog
from data.config import DATA_SOURCE
from data.data_manager import DataManager

class DataPicker(QDialog):
    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.setWindowTitle("Data Picker")
        self.width = 300
        self.height = 200

        self.setup_geometry()

        self.layout = QVBoxLayout()
        for source in DATA_SOURCE.keys():
            self.layout.addWidget(DataSourceInput(source, data_manager))

        self.setLayout(self.layout)


    def setup_geometry(self):
        geometry = self.screen().availableGeometry()
        self.setGeometry(geometry.width() * 0.5 - self.width / 2,
                         geometry.height() * 0.5 - self.height / 2,
                         self.width,
                         self.height)
    
class DataSourceInput(QWidget):
    def __init__(self, source: str, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager
        self.source = source

        self.layout = QHBoxLayout()
        self.input = QLineEdit(f"{source} File path")
        self.input.setReadOnly(True)
        
        self.button = QPushButton("Load")
        self.button.clicked.connect(self.pick_a_file)
        
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def pick_a_file(self):
        url, _ = QFileDialog.getOpenFileUrl(self)
        url = url.toLocalFile()
        self.input.setText(url)
        self.data_manager.load_data(self.source, url)


        

