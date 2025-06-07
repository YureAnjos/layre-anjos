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
                return False
            else:
                return True

    def findProductByName(self, name):
        error = self.getLatest()

        if error:
            return None

        data = self._usingDatasheet.getRowByColumnValue('Descrição', name)

        if data.empty:
            return None

        return data

    def updateFieldsByCode(self, code, updateValues):
        for k, v in updateValues.items():
            self._usingDatasheet.update(code, 'Código', v, k)
    
    def saveAndUpload(self):
        error, path = self._usingDatasheet.save()

        if error: return

        self.driver.uploadProducts(path)


