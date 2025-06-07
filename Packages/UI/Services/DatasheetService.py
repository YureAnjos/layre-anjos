import os
from ..Models.DatasheetModel import DataSheet
from ...driver.Driver import Driver

class DataSheetService:
    def __init__(self):
        self._usingDatasheet = None
        self.driver = Driver()
    
    def downloadLatest(self):
        path = self.driver.downloadLatestProducts()

        if os.path.exists(path):
            newDS = DataSheet(path)
            
            self._usingDatasheet = newDS
    
    def getLatest(self):
        if not self._usingDatasheet:
            path = self.driver.getLatestProducts()

            if os.path.exists(path):
                newDS = DataSheet(path)

                self._usingDatasheet = newDS

    def findProductByName(self, name):
        self.getLatest()

        data = self._usingDatasheet.getRowByColumnValue('Descrição', name)

        if data.empty:
            return None

        return data
