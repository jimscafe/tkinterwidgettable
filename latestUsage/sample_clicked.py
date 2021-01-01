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
                                cellClick=self.clicked,
                                dataChanged=None)
        self.table.setData(sampleData.data1)

    def drawCell(self,widget, data):
        #print ('Table row', widget.tableRow, 'Column',widget.tableColumn)  # Visible cells
        #print ('Data  row', widget.dataCoords[0], 'Column',widget.dataCoords[1]) # actual data cells
        widget.setText(data)
        widget.configure(bg='light grey')
        if widget.tableColumn == 2: # Age
            if data > 20:
                widget.configure(bg='light green')

    def clicked(self, widget): # Row, column the same as drawCell
        print ('Cell Text   :', widget.getText()) 
        if widget.tableRow < 0: # Header - maybe sort data and reset into table
            print ('Header clicked')
            sortedData = sorted(sampleData.data1, key=lambda x: x[widget.tableColumn])  
            self.table.setData(sortedData)    

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
