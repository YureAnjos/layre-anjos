import customtkinter as ctk
from .Model.Page import Page
from ..Widgets.LabelFrame import LabelFrame

class ConfirmPage(Page):
    def __init__(self, master, DSService):
        super().__init__(master)
        
        self.DSService = DSService

        self.frames = []

        self.scrollFrame = ctk.CTkScrollableFrame(self, label_text='Update                     Code                     Barcode                     Name                     Old Price                     New Price')
        self.scrollFrame.pack(fill='both', expand=True)

        self.uploadButton = ctk.CTkButton(self, text='Upload', command=self.upload)
        self.uploadButton.pack(padx=10, pady=10, side='right')

        self.returnButton = ctk.CTkButton(self, text='Return', command=self.returnCommand)
        self.returnButton.pack(padx=10, pady=10, side='left')
    
    def setup(self, listedProducts):
        for product in listedProducts:
            data = self.DSService.findProductByName(product['name'])


            try:
                indexes = data.index.to_list()
                self.scrollFrame.grid_columnconfigure(0, weight=1)
                for i in indexes:
                    newFrame = LabelFrame(self.scrollFrame)
                    newFrame.configure(width=self.scrollFrame.size()[0])
                    
                    newFrame.codeField.configure(text=data.at[i, 'Código'])
                    newFrame.barcodeField.configure(text=data.at[i, 'Código de Barras'])
                    newFrame.nameField.configure(text=data.at[i, 'Descrição'])
                    newFrame.oldPriceField.configure(text=data.at[i, 'Preço de Venda'])
                    newFrame.setPrice(product['price'])

                    newFrame.grid(row=len(self.frames), column=0, sticky="ew")

                    self.frames.append(newFrame)
            except:
                continue
    
    def returnCommand(self):
        self.framesForget()
        self.frames.clear()

        self.navigate('selection')

    def upload(self):
        for frame in self.frames:
            if frame.checkbox.get() == 1:
                code = frame.codeField._text
                price = frame.getPrice()

                self.DSService.updateFieldsByCode(code, {'Preço de Venda': float(price)})
        
        self.iconify()
        self.DSService.saveAndUpload()
        self.deiconify()
    
    def framesForget(self):
        for frame in self.frames:
            frame.grid_forget()
