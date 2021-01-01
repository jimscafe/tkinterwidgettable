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
                                drawCell=self.drawCell,         # These are three callback functions
                                cellClick=None,
                                dataChanged=self.dataChanged)
        self.dataMatrix = sampleData.data1
        self.table.setData(self.dataMatrix)

    def dataChanged(self, widget):
        # Make validate, make changes to original data, or other actions
        print (widget.getText(), widget.tableRow, widget.tableColumn, widget.dataCoords)
        if widget.tableColumn == 2: # Age
            dataRow = widget.dataCoords[0]
            dataColumn = widget.dataCoords[1] # No horizontal scrolling so the same as tableColumn
            self.dataMatrix[dataRow][dataColumn] = int(widget.getText())
            self.table.setData(self.dataMatrix)

    def drawCell(self,widget, data):
        widget.setText(data)
        widget.configure(bg='light grey')
        if widget.tableColumn == 2: # Age
            if data > 20:
                widget.configure(bg='light green')


def createColumns():
    columns = [
        {'text':'ID', 'width': 6, 'bg':'blue', 'fg':'white'},
        {'text':'Name', 'width': 18, 'bg':'blue', 'fg':'white'},
        {'text':'Age', 'width': 10, 'bg':'blue', 'fg':'white', 'align':'center', 'widget':'Textbox'},
        {'text':'Sex', 'width': 6, 'bg':'blue', 'fg':'white', 'align':'center'},
        {'text':'Member', 'width': 5, 'bg':'blue', 'fg':'white', 'widget':'Checkbox'}
    ]
    return columns


root = TK.Tk()
main = Main(root)

TK.mainloop()
