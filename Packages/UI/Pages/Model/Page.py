from customtkinter import CTkFrame

class Page(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color='transparent')
        self.loaded = False
    
    def load(self, navigate):
        self.place(relwidth=1, relheight=1)
        self.loaded = True
        self.navigate = navigate
    
    def unload(self):
        self.place_forget()
        self.loaded = False