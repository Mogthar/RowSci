import pandas as pd

class DataManager:
    def __init__(self):
        self.cortex_data = None
        self.paddlemate_data = None
        self.powerline_data = None
        self.artinis_data = None

        self.load_mapper = {
            "CORTEX" : self.load_cortex_data
        }
    
    def load_data(self, source: str, url: str):
        loader = self.load_mapper.get(source, self.load_default)
        loader(url)

    def load_cortex_data(self, url: str):
        def skip_row(index: int):
            if index < 38 or index == 39:
                return True 
        df = pd.read_excel(url, header=38, skiprows=skip_row)
        print(df)

    def load_default(self):
        pass
