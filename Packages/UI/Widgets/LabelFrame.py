import customtkinter as ctk
from tkinter import ACTIVE

class LabelFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.fontStyle = ('Arial', 20)
        self.paddingx = 50
        self.paddingy = 10

        self.checkbox = ctk.CTkCheckBox(self, width=20, height=20, text='')
        self.checkbox.select()
        self.checkbox.grid(row=0, column=0, padx=self.paddingx, pady=self.paddingy)

        self.codeField = ctk.CTkLabel(self, font=self.fontStyle, text='Code Ipsum Dolor')
        self.codeField.grid(row=0, column=1, padx=self.paddingx, pady=self.paddingy)

        self.barcodeField = ctk.CTkLabel(self, font=self.fontStyle, text='Barcode Ipsum Dolor')
        self.barcodeField.grid(row=0, column=2, padx=self.paddingx, pady=self.paddingy)

        self.nameField = ctk.CTkLabel(self, font=self.fontStyle, text='Name Ipsum Dolor')
        self.nameField.grid(row=0, column=3, padx=self.paddingx, pady=self.paddingy)

        self.oldPriceField = ctk.CTkLabel(self, font=self.fontStyle, text='OldPrice Ipsum Dolor')
        self.oldPriceField.grid(row=0, column=4, padx=self.paddingx, pady=self.paddingy)

        self.newPriceField = ctk.CTkTextbox(self, font=('Arial', 30), height=30, width=100)
        self.newPriceField.grid(row=0, column=5, padx=self.paddingx, pady=self.paddingy)

    def setPrice(self, value):
        self.newPriceField.delete('0.0', 'end')
        self.newPriceField.insert('0.0', value)
    
    def getPrice(self, value):
        return self.newPriceField.get("0.0", "end").strip()
