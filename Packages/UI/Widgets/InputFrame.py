import customtkinter as ctk

class InputFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.nameInput = ctk.CTkTextbox(self, height=40, width=300, font=('Arial', 20))
        self.nameInput.grid(row=0, column=0, padx=10)        

        self.priceInput = ctk.CTkTextbox(self, height=40, width=100, font=('Arial', 20))
        self.priceInput.grid(row=0, column=1)
    
    def getName(self):
        return self.nameInput.get("0.0", "end").strip()

    def getPrice(self):
        return self.priceInput.get("0.0", "end").strip()
    
    def resetValues(self):
        self.nameInput.delete('0.0', 'end')
        self.priceInput.delete('0.0', 'end')
    
    def setName(self, value):
        self.nameInput.delete('0.0', 'end')
        self.nameInput.insert('0.0', value)
    
    def setPrice(self, value):
        self.priceInput.delete('0.0', 'end')
        self.priceInput.insert('0.0', value)