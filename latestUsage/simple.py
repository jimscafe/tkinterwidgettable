import tkinter as TK
from table_nf import MyTable
import sampleData

class Main:
    def __init__(self, parent):
        self.parent=parent
        #parent.geometry("500x200")
        mainFrame = TK.Frame(parent, borderwidth=5, bg='yellow')
        mainFrame.pack()
        self.table = MyTable(mainFrame, createColumns(),  
                                rows=10, scroll=True,  # Vertical scroll forced
                                drawCell=None,         # These are three callback functions
                                cellClick=None,
                                dataChanged=None)
        self.table.setData(sampleData.data1)

def createColumns():
    columns = [
        {'text':'ID', 'width': 6, 'bg':'blue', 'fg':'white'},
        {'text':'Name', 'width': 18, 'bg':'blue', 'fg':'white'},
        {'text':'Age', 'width': 10, 'bg':'blue', 'fg':'white', 'align':'center'},
        {'text':'Sex', 'width': 6, 'bg':'blue', 'fg':'white', 'align':'center',}
    ]
    return columns


root = TK.Tk()
main = Main(root)

TK.mainloop()
