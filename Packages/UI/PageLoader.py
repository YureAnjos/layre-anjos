from .Pages.SelectionPage import SelectionPage
from .Pages.ConfirmPage import ConfirmPage

class PageLoader:
    def __init__(self, master, current, DSService):
        self.current = current
        self.pages = {
            'selection': SelectionPage(master, DSService),
            'confirm': ConfirmPage(master, DSService)
        }
    
    def start(self):
        for page in self.pages.values():
            page.unload()
        self.pages[self.current].load(self.navigate)
    
    def navigate(self, page, *setupParams):
        last = self.pages[self.current]
        if last.loaded:
            self.pages[self.current].unload()
        self.pages[page].load(self.navigate)
        if hasattr(self.pages[page], 'setup'):
            self.pages[page].setup(*setupParams)
        self.current = page
