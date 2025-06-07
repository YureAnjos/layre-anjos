import customtkinter as ctk
from .PageLoader import PageLoader
from .Services.DatasheetService import DataSheetService

ctk.set_default_color_theme('dark-blue')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.DSService = DataSheetService()
        self.loader = PageLoader(self, 'selection', self.DSService)

        self.title('Layre Anjos')
        self.geometry('1066x600')

        self.loader.start()


def bootstrap():
    app = App()

    app.attributes('-topmost', True)
    app.update()
    app.attributes('-topmost', False)
    app.focus_force()

    app.mainloop()

