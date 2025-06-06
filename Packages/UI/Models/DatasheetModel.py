import pandas as pd

class DataSheet:
    def __init__(self, file):
        self.file = pd.read_excel(file)

    def show(self):
        print(self.file.to_string())
    
    def getRowByColumnValue(self, column, value):
        data = self.file[self.file[column].str.contains(value)]

        return data