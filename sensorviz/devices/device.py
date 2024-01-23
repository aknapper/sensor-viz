import pandas as pd

from helpers import setup_data_file

class Device:
    def __init__(self, dev_name):
        self.recording_data = False
        self.dataFrame = pd.DataFrame({'Timestamp': [''], 'Runtime (s)': [''],"Temperature (°C)": ['']})
        self.csvFileLoc = setup_data_file(dev_name, "Temperature (°C)")
    