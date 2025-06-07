from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QWidget, QHBoxLayout, QPushButton, QFileDialog, QLabel
from data.data_manager import dataManager
from data.data_source import DataSource

class DataPicker(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Picker")
        self.width = 400
        self.height = 200

        self.setup_geometry()

        self.layout = QVBoxLayout()
        for source in dataManager.data_loaders.keys():
            self.layout.addWidget(DataSourceInput(self, source))
        self.error_message = QLabel()
        self.error_message.setStyleSheet("color: red")
        self.layout.addWidget(self.error_message)

        self.setLayout(self.layout)


    def setup_geometry(self):
        geometry = self.screen().availableGeometry()
        # place the dialog window in the center of the screen
        self.setGeometry(geometry.width() * 0.5 - self.width / 2,
                         geometry.height() * 0.5 - self.height / 2,
                         self.width,
                         self.height)
    
class DataSourceInput(QWidget):
    def __init__(self, parent: DataPicker, source: DataSource):
        super().__init__()
        self.data_picker = parent
        self.source = source

        self.layout = QHBoxLayout()
        self.input = QLineEdit(f"{source.value} File path")
        self.input.setReadOnly(True)
        
        self.button = QPushButton("Load")
        self.button.clicked.connect(self.pick_a_file)
        
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def pick_a_file(self):
        url, _ = QFileDialog.getOpenFileUrl(self)
        url = url.toLocalFile()
        if url:
            self.input.setText(url)
            try:
                dataManager.load_data(self.source, url)
                self.data_picker.error_message.setText("")
            except Exception as e:
                print(e)
                self.data_picker.error_message.setText(f"Failed to load data for source: {self.source}")


        

