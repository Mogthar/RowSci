import pandas as pd

class DataManager:
    def __init__(self):
        self.cortex_data: pd.DataFrame = None
        self.paddlemate_data: pd.DataFrame = None
        self.powerline_data: pd.DataFrame = None
        self.artinis_data: pd.DataFrame = None

        self.data_sources = {
            "CORTEX" : self.load_cortex_data,
            "DEFAULT" : self.load_default
        }
    
    def load_data(self, source: str, url: str):
        if source in self.data_sources:
            loader = self.data_sources.get(source)
        else:
            print("Undefined source")
            loader = self.load_default
        loader(url)

    def load_cortex_data(self, url: str):
        df = pd.read_excel(url,
                           skiprows=[i for i in range(38)] + [39],
                           na_values = ['-'])
        df['t'] = df['t'].apply(self.convert_hh_mm_ss_to_seconds)
        self.cortex_data = df

    def convert_hh_mm_ss_to_seconds(self, time_string: str):
        hh_mm_ss = time_string.split(":")
        return int(hh_mm_ss[0]) * 3600 + int(hh_mm_ss[1]) * 60 + int(hh_mm_ss[2])
    
    def load_default(self):
        pass

dataManager = DataManager()

# dataManager.load_data("CORTEX", "C:/Users/kucer/Downloads/CPET__Boldišová_Ella_2025.05.20_11.19.00_.xlsx")
# print(dataManager.cortex_data['t'])
# dataManager.cortex_data.info()