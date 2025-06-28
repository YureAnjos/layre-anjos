import pandas as pd
import os
import sys
from rapidfuzz import fuzz

class DataSheet:
    def __init__(self, file):
        self.file = pd.read_excel(file)
        self.uploadPath = 'files\\upload\\upload.xlsx'

    def show(self):
        print(self.file.to_string())
    
    def getRowByColumnValue(self, column, value, threshold = 70):
        if self.file is None:
            raise ValueError("Nenhum arquivo carregado. Use load_file primeiro.")
        
        if column not in self.file.columns:
            raise ValueError(f"A coluna '{column}' não existe no DataFrame.")
        
        value_normalized = value.lower().strip()
        
        mask = self.file[column].apply(
            lambda x: fuzz.ratio(str(x).lower().strip(), value_normalized) >= threshold 
            if pd.notna(x) else False
        )
        
        return self.file[mask]

    def update(self, key, kidentifier, value, videntifier):
        condition = self.file[kidentifier] == key
        self.file.loc[condition, videntifier] = value

        return True
    
    def save(self):
        rootPath = sys.path[0]
        folderPath = rootPath + '\\' + 'files\\upload'

        if not os.path.exists(folderPath):
            try:
                os.mkdir(folderPath)
            except Exception as e:
                return True, None
        
        if not os.path.exists(rootPath + '\\' + self.uploadPath):
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
