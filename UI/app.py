import customtkinter as ctk
from pageLoader import PageLoader

ctk.set_default_color_theme('dark-blue')

class App(ctk.CTk):
    def __init__(self, WebDriver):
        super().__init__()
        self.driver = WebDriver
        self.loader = PageLoader(self, 'selection')

        self.title('Layre Anjos')
        self.geometry('1066x600')

        self.loader.start()


if __name__ == '__main__':
    app = App('default')

    app.mainloop()
