import os
from ..Models.DatasheetModel import DataSheet
from ...driver.Driver import Driver

class DataSheetService:
    def __init__(self):
        self._usingDatasheet = None
        self.driver = Driver()
    
    def register(self):
        a = DataSheet(self.driver.downloadLatestProducts())
        a.show()

        # if os.path.exists(path):
        #     newDS = DataSheet(path)
            
        #     self._usingDatasheet = newDS
