from Pages.selectionPage import SelectionPage

class PageLoader:
    def __init__(self, master, current):
        self.current = current
        self.pages = {
            'selection': SelectionPage(master),
        }
    
    def start(self):
        for page in self.pages.values():
            page.unload()
        self.pages[self.current].load()
    
    def navigate(self, page, *setupParams):
        last = self.pages[self.current]
        if last.loaded:
            self.pages[self.current].unload()
        self.pages[page].load()
        if hasattr(self.pages[page], 'setup'):
            self.pages[page].setup(setupParams)
        self.current = page
