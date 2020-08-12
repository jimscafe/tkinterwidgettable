"""
   Make a column of entry widgets, not the default label
   Allow editing of the cell with feedback via callback
   Data is held in two places
     1. The widget
     2. The data matrix in the table class
"""
import tkinter as TK
from tkinter import messagebox

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


        columns = [Column('ID', align='left'),Column('Name'),
                   Column('Age', widget='Textbox', type='integer'),
                   Column('Gender', widget='Combobox'),
                   Column('Member', widget='Checkbox'),
                   Column('Delete', widget='Button')]
        columns[3]['options'] = ['Male', 'Female']
        self.table = MyTable(self.tableFrame, columns, rows=10, drawCell=self.drawCell, 
                             dataChanged=self.dataChanged )
        self.mainData = sampleData.data3  # These are the same matrix, when changed in table
                                          # Change is reflected here also
        self.table.setData(self.mainData) 
    
        self.buttonFrame = TK.Frame(self.frame)
        self.buttonFrame.config(bg='light grey')
        self.buttonFrame.grid(row=2, column=0, pady=10, sticky=TK.NSEW)
        self.saveButton = TK.Button(self.buttonFrame, text='Save Changes', command=self.saveChanges)
        self.saveButton.pack(pady=10, padx=20, side=TK.LEFT) # anchor='w')
        self.quitButton = TK.Button(self.buttonFrame, text='Quit', command=self.quit)
        self.quitButton.pack(pady=10, padx=20, side=TK.RIGHT) # anchor='e')

    def drawCell(self, widget, cellObject):
        # In this case, using simple data, the cell object is the data (string, integer etc.)
        if widget.widgetType == 'Combobox':
            widget.setOptions(self.table.columns[widget.tableColumn]['options'])
            widget.textSelection.set(cellObject)
        else:
            if widget.tableColumn == 1:
                widget.config(bg='light blue')
            elif widget.tableColumn == 2:
                if int(cellObject) < 21:
                    widget.config(bg='red', fg='white')
                else:
                    widget.config(bg='light grey', fg='blue')
            widget.setText(cellObject)

    def dataChanged(self, widget):
        print ('Data modified - parent')
        # Local data value
        dataRow = widget.dataCoords[0]
        dataColumn = widget.dataCoords[1]
        newValue = widget.getText()
        dataType = self.table.columns[dataColumn].get('type', 'string')
        print ('Table Data :', self.mainData[dataRow][dataColumn])
        print ('Widget text:', newValue)
        print ('Cell type', self.table.columns[dataColumn].get('type', 'string'))
        # Redraw cell if format changed with the data change
        if widget.widgetType == 'Checkbox':
            # Do not call self.drawCell() for checkbox
            newValue = (newValue + 1) % 2
            print ('Check box value', newValue)
            self.mainData[dataRow][dataColumn] = newValue
        elif widget.widgetType == 'Button': # Call function to implement button click
            self.deleteRow(widget) 
        else:
            if dataType == 'integer':
                self.mainData[dataRow][dataColumn] = int(newValue)
            else:
                self.mainData[dataRow][dataColumn] = newValue
            self.drawCell(widget, newValue) # In case this affects formatting

    def deleteRow(self,widget):
        name = self.table.data[widget.dataCoords[0]][1] # Name
        if messagebox.askokcancel("Delet Row", "Delete Data Row " + name): 
            print ('Delete row')
            self.table.data.pop(widget.dataCoords[0])
            self.table.setData(self.table.data)
            print (widget['state'])       

    def saveChanges(self):
        print ('Saving changes')
        self.table.dataChanged = False

    def quit(self):
        if self.table.dataChanged:
            if messagebox.askokcancel("Data Changed", "Data not saved! Do you want to quit?"):
                self.parent.destroy()
        else:
            self.parent.destroy()
        #self.parent.destroy()

if __name__ == "__main__":
    root = TK.Tk()
    main = Main(root)
    TK.mainloop()
