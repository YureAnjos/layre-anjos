import customtkinter as ctk
from .Model.Page import Page
from ..Widgets.InputFrame import InputFrame

class SelectionPage(Page):
    def __init__(self, master, DSService):
        super().__init__(master)
        
        self.DSService = DSService
        self.frames = []

        self.mainFrame = ctk.CTkScrollableFrame(self, label_text='Products')
        self.mainFrame.pack(fill='both', expand=True)

        self.mainInput = InputFrame(self.mainFrame)
        self.mainInput.grid(row=0, column=0, pady=10, padx=10)
        self.addButton = ctk.CTkButton(self.mainFrame, text='+', width=40, height=40, font=('Arial', 20), command=lambda: self.newProduct(self.mainInput.getName(), self.mainInput.getPrice()))
        self.addButton.grid(row=0, column=1)

        self.downloadLatestButton = ctk.CTkButton(self, text='Download Latest', width=300, height=40, font=('Arial', 20), command=DSService.downloadLatest)
        self.downloadLatestButton.pack(pady=10, padx=10, side='left')

        self.NextButton = ctk.CTkButton(self, text='Next', width=150, height=35, command=self.next)
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
    
    def next(self):
        listedProducts = []

        for frame in self.frames:
            inputFrame = frame.children['!inputframe']

            name = inputFrame.getName()
            price = inputFrame.getPrice()

            if name == '' or name == None or price == '' or price == None or not price.isnumeric(): continue

            product = {
                'name': name,
                'price': price
            }

            listedProducts.append(product)
        
        if len(listedProducts) > 0:
            self.navigate('confirm', listedProducts)
