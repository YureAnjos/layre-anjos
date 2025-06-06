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
    
    def setup(self, listedProducts):
        for product in listedProducts:
            data = self.DSService.findProductByName(product['name'])


            try:
                indexes = data.index.to_list()
                for i in indexes:
                    newFrame = LabelFrame(self.scrollFrame)
                    newFrame.configure(width=self.scrollFrame.size()[0])
                    
                    newFrame.codeField.configure(text=data.at[i, 'Código'])
                    newFrame.barcodeField.configure(text=data.at[i, 'Código de Barras'])
                    newFrame.nameField.configure(text=data.at[i, 'Descrição'])
                    newFrame.oldPriceField.configure(text=data.at[i, 'Preço de Venda'])
                    newFrame.setPrice(product['price'])

                    newFrame.grid(row=len(self.frames), column=1)

                    self.frames.append(newFrame)
            except:
                continue