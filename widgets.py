# Classes for the gui widgets
import tkinter as TK
from tkinter import ttk
#from Gui.userTable import UserTable

class DefaultWidget(object):
    def setText(self, txt):
        self.config(text = txt)
    def getText(self):
        return self.get()
    def justifyText(self, txt):
        self.config(justify=txt)
    def enabled(self, b):
        s = 'disabled'
        if b: s = 'normal'
        self.config(state=s)

class Label(TK.Label, DefaultWidget):
    def __init__(self, parent, **kwargs):
        TK.Label.__init__(self, parent)
    #def setText(self, txt):
    #    self.config(text = txt)
    def getText(self):
        return self.cget('text')

class Button(TK.Button, DefaultWidget):
    def __init__(self, parent, **kwargs):
        TK.Button.__init__(self, parent)
    def click(self, fnc):
        self.config(command=fnc)
    def getText(self):
        return 'Button Text'

class Textbox(TK.Entry, DefaultWidget):
    def __init__(self, parent, **kwargs):
        TK.Entry.__init__(self, parent)
    def setText(self, txt):
        self.delete(0, TK.END)
        self.insert(0, txt)

class Combobox(ttk.Combobox):  # , DefaultWidget):
    def __init__(self, parent, **kwargs):
        ttk.Combobox.__init__(self, parent)
        self.textSelection = TK.StringVar()
        self.config(textvariable = self.textSelection)
    def setOptions(self, options):
        #self['values'] = options
        self.configure(values=options)
    def setSelection(self, index):
        self.current(index)
    def setText(self, txt):
        self.textSelection.set(txt)
    def getText(self):
        return self.textSelection.get()
    def enabled(self, b):
        s = 'disabled'
        if b: s = 'normal'
        self.config(state=s)

# Not used in table examples
class Listbox(TK.Listbox):
    def __init__(self, parent, **kwargs):
        TK.Listbox.__init__(self, parent)
    def add(self, txt):
        self.insert(TK.END, txt)
    def getRows(self): # Overwrites existing get
        return self.get(0, TK.END)

class Checkbox(TK.Checkbutton):
    def __init__(self, parent, **kwargs):
        TK.Checkbutton.__init__(self, parent)
        self.var = TK.IntVar()
        self.config(variable=self.var)
    def setText(self, txt):
        if txt:
            self.select()
        else:
            self.deselect()
        #print ('Set text')
    def getText(self):
        #print ('Get Text')
        return self.var.get()    
    def enabled(self, b):
        s = 'disabled'
        if b: s = 'normal'
        self.config(state=s)
        
# Not used in table version
class RadioButton(TK.Radiobutton, DefaultWidget):
    # Need a container and a TK variable to get which radio button as selected
    # The variable shared by all the radio buttons is put in the container
    def __init__(self, parent, **kwargs):
        TK.Radiobutton.__init__(self, parent)
