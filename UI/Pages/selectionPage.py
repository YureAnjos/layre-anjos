import customtkinter as ctk
from .Model.page import Page
from time import time

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

class SelectionPage(Page):
    def __init__(self, master):
        super().__init__(master)

        self.frames = []

        self.mainFrame = ctk.CTkScrollableFrame(self, label_text='Products')
        self.mainFrame.pack(fill='both', expand=True)

        self.mainInput = InputFrame(self.mainFrame)
        self.mainInput.grid(row=0, column=0, pady=10, padx=10)
        self.addButton = ctk.CTkButton(self.mainFrame, text='+', width=40, height=40, font=('Arial', 20), command=lambda: self.newProduct(self.mainInput.getName(), self.mainInput.getPrice()))
        self.addButton.grid(row=0, column=1)

        self.NextButton = ctk.CTkButton(self, text='Next', width=150, height=35)
        self.NextButton.pack(pady=10, padx=10, side='right')
    
    def newProduct(self, name, price):
        if name == '' or price == '': return

        newFrame = ctk.CTkFrame(self.mainFrame, fg_color='transparent')

        newInput = InputFrame(newFrame)
        newInput.setName(name)
        newInput.setPrice(price)
        newInput.grid(row=0, column=0, padx=10)

        delButton = ctk.CTkButton(newFrame, text='-', width=40, height=40, font=('Arial', 20), command=lambda: self.delProduct(newFrame))
        delButton.grid(row=0, column=1)

        newFrame.grid(row=len(self.frames)+1, column=0, pady=10)
        self.frames.append(newFrame)

        self.mainInput.resetValues()

    def delProduct(self, frameObj):
        for frame in self.frames:
            frame.grid_forget()
        
        self.frames.remove(frameObj)
        frameObj.destroy()
        
        for i, frame in enumerate(self.frames):
            frame.grid(row=i+1, column=0)
