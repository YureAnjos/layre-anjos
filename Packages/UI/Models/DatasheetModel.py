import pandas as pd
import os
import sys

class DataSheet:
    def __init__(self, file):
        self.file = pd.read_excel(file)
        self.uploadPath = 'files/upload/upload.xlsx'

    def show(self):
        print(self.file.to_string())
    
    def getRowByColumnValue(self, column, value):
        data = self.file[self.file[column].str.contains(value)]

        return data

    def update(self, key, kidentifier, value, videntifier):
        condition = self.file[kidentifier] == key
        self.file.loc[condition, videntifier] = value

        return True
    
    def save(self):
        rootPath = sys.path[0]
        folderPath = rootPath + '\\' + 'files\\upload'

        if not os.path.exists(folderPath):
            os.mkdir(folderPath)
            
            try:
                f = open(self.uploadPath, 'x')
                f.close()
            except FileExistsError:
                pass
            except Exception as e:
                print(e)
                return True, None
        
        if not os.path.exists(rootPath + '\\' + self.uploadPath):
            return True, None

        self.file.to_excel(self.uploadPath, index=False)
        return False, rootPath + '\\' + self.uploadPath
