"""
   By using a callback function to display each cell, formatting individual cells,
   rows of cells or columns of cells is possible.
   Typically formatting is changing foreground and background colors
   but could also include alignment changes, formatting numbers
   Widgets could also be disabled/enabled
"""
import tkinter as TK

from table import MyTable, Column
import sampleData

class Main():
    def __init__(self, parent):
        self.parent = parent
        self.frame = TK.Frame(self.parent)
        self.parent.protocol("WM_DELETE_WINDOW", self.quit)
        self.frame.pack()
        self.titleFrame = TK.Frame(self.frame)
        self.titleFrame.grid(row=0, column=0, pady=10)
        self.title = TK.Label(self.titleFrame, text='Simple Data - Cell Formatting')
        self.title.pack()

        self.tableFrame = TK.Frame(self.frame)
        self.tableFrame.grid(row=1, column=0, padx=20, pady=20)
        self.tableTitle = TK.Label(self.tableFrame, text='Simple Data Table')
        self.tableTitle.pack()


        columns = [Column('One', align='left'),Column('Two'), Column('Three'),Column('Four')]
        self.table = MyTable(self.tableFrame, columns, rows=10, drawCell=self.drawCell)
        self.table.setData(sampleData.data1) 
    
        self.buttonFrame = TK.Frame(self.frame)
        self.buttonFrame.config(bg='light grey')
        self.buttonFrame.grid(row=2, column=0, pady=10, sticky=TK.NSEW)
        self.quitButton = TK.Button(self.buttonFrame, text='Quit', command=self.quit)
        self.quitButton.pack(pady=10, padx=20, anchor='e')

    def drawCell(self, widget, cellObject):
        # In this case, using simple data, the cell object is the data (string, integer etc.)
        if widget.tableColumn == 1:
            widget.config(bg='light blue')
        elif widget.tableColumn == 2:
            if int(cellObject) < 21:
                widget.config(bg='red', fg='white')
            else:
                widget.config(bg='light grey', fg='blue')
        widget.setText(cellObject)

    def quit(self):
        self.parent.destroy()

if __name__ == "__main__":
    root = TK.Tk()
    main = Main(root)
    TK.mainloop()