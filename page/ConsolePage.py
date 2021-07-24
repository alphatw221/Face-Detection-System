import tkinter as tk

class ConsolePage(tk.Frame):
    def __init__(self,parent,application):
        tk.Frame.__init__(self,parent)
        self.grid()
        self.application=application
        self._createWidgets()

    def _createWidgets(self):
        pass
        