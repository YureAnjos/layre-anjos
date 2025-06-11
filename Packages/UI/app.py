import customtkinter as ctk
from .PageLoader import PageLoader
from .Services.DatasheetService import DataSheetService
from ..driver.Driver import Driver
import threading

ctk.set_default_color_theme('dark-blue')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.driver = Driver()
        self.DSService = DataSheetService(self.driver)
        self.loader = PageLoader(self, 'selection', self.DSService)

        self.title('Layre Anjos')
        self.geometry('1066x600')

        self.loader.start()

    def loadDriver(self):
        self.driver.load()

def runAsyncioInThread(app: App):
    app.loadDriver()

def bootstrap():
    app = App()
    
    thread = threading.Thread(target=runAsyncioInThread, args=(app,), daemon=True)
    thread.start()

    app.attributes('-topmost', True)
    app.update()
    app.attributes('-topmost', False)
    app.focus_force()

    app.mainloop()

