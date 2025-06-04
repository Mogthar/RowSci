from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QWidget, QHBoxLayout, QPushButton, QFileDialog
from data.data_manager import dataManager

class DataPicker(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Picker")
        self.width = 400
        self.height = 200

        self.setup_geometry()

        self.layout = QVBoxLayout()
        for source in dataManager.data_sources.keys():
            self.layout.addWidget(DataSourceInput(source))

        self.setLayout(self.layout)


    def setup_geometry(self):
        geometry = self.screen().availableGeometry()
        # place the dialog window in the center of the screen
        self.setGeometry(geometry.width() * 0.5 - self.width / 2,
                         geometry.height() * 0.5 - self.height / 2,
                         self.width,
                         self.height)
    
class DataSourceInput(QWidget):
    def __init__(self, source: str):
        super().__init__()
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
        if url:
            self.input.setText(url)
            dataManager.load_data(self.source, url)


        

