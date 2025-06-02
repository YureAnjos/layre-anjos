import customtkinter as ctk
from .PageLoader import PageLoader
from .Services.DatasheetService import DataSheetService

ctk.set_default_color_theme('dark-blue')

class App(ctk.CTk):
    def __init__(self, driver):
        super().__init__()
        self.loader = PageLoader(self, 'selection')
        self.DSService = DataSheetService(driver)

        self.title('Layre Anjos')
        self.geometry('1066x600')

        self.loader.start()
        self.DSService.register()

def bootstrap():
    app = App()

    app.mainloop()
