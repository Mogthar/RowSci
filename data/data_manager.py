import pandas as pd
from event_manager.event_manager import event_manager, Event
from data.data_source import DataSource
import os


class DataPacket:
    def __init__(self, main_table: pd.DataFrame = None, metadata: any = None):
        self.main_table = main_table
        self.metadata = metadata

class DataManager:
    def __init__(self):
        self.cortex_data: DataPacket = DataPacket()
        self.paddlemate_data: DataPacket = DataPacket()
        self.powerline_data: DataPacket = DataPacket()
        self.artinis_data: DataPacket = DataPacket()

        self.data_loaders = {
            DataSource.CORTEX : self.load_cortex_data,
            DataSource.ARTINIS : self.load_artinis_data,
        }

        self.data_getters = {
            DataSource.CORTEX : self.cortex_data,
            DataSource.ARTINIS : self.artinis_data,
        }
    
    def load_data(self, source: DataSource, url: str):
        if source in self.data_loaders:
            load_func = self.data_loaders.get(source)
        else:
            raise ValueError(f"Undefined source: {source}")
        load_func(url)

    def get_data(self, source: DataSource):
        if source in self.data_getters:
            return self.data_getters.get(source)
        else:
            raise ValueError(f"Undefined source: {source}")

    def convert_hh_mm_ss_to_seconds(self, time_string: str):
        hh_mm_ss = time_string.split(":")
        return int(hh_mm_ss[0]) * 3600 + int(hh_mm_ss[1]) * 60 + int(hh_mm_ss[2])
    
    def load_cortex_data(self, url: str):
        df = pd.read_excel(url,
                           skiprows=[i for i in range(38)] + [39],
                           na_values = ['-'])
        df['t'] = df['t'].apply(self.convert_hh_mm_ss_to_seconds)
        self.cortex_data.main_table = df
        event_manager.trigger_event(Event.CORTEX_DATA_LOADED)

    def load_artinis_data(self, url: str):
        raw_df = pd.read_excel(url, header=None)
        # search for Legend
        legend_start_index = None
        for row_idx, row in raw_df.iterrows():
            if row[0] == "Legend":
                legend_start_index = row_idx + 2
                break
        if legend_start_index is None:
            raise ValueError("Legend not found")
        
        column_name_map = {}
        main_data_start_index = None
        for row_idx, row in raw_df.iloc[legend_start_index:].iterrows():
            if isinstance(row[0], int):
                column_name_map[row[0]] = row[1]
            else:
                main_data_start_index = row_idx + 2
                break
        print("column name map", column_name_map)
        if main_data_start_index is None:
            raise ValueError("Real data not found")
        
        main_data_df = raw_df.iloc[main_data_start_index:, 0:len(column_name_map)]
        main_data_df.columns = column_name_map.values()

        self.artinis_data.main_table = main_data_df
        self.artinis_data.metadata = column_name_map
        event_manager.trigger_event(Event.ARTINIS_DATA_LOADED)
        
    def load_default(self):
        pass

dataManager = DataManager()

# dataManager.load_data("CORTEX", "C:/Users/kucer/Downloads/CPET__Boldišová_Ella_2025.05.20_11.19.00_.xlsx")
# print(dataManager.cortex_data['t'])
# dataManager.cortex_data.info()
print(os.getcwd())
dataManager.load_data(DataSource.ARTINIS, "/Users/jure/Downloads/artinis_data.xlsx")
dataManager.artinis_data.main_table.info()