"""
  Modify code - better API, better data design  

  If modified data is saved in parent, then changed flag reset?

  Handle the scroll bar better.
"""
import tkinter as TK
from tkinter import messagebox
from table_v6 import MyTable, Cell

class MainGUI(object):
    def __init__(self,root):
        self.root = root
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        frm = TK.Frame(self.root)
        frm.pack(padx=20, pady=20)
        self.tableFrame = TK.Frame(frm)
        # How to define columns (text, width, colors)?
        columns = self.createColumns_1()
        noRows = 8
        option = 3 # Modify this to demonstrate options
        # ----------------------------------------------------------------------
        # Improve code encapsulation
        if option == 1:
            self.table = MyTable(self.tableFrame, columns, rows=noRows, scroll=True, 
            drawCell = self.drawCell, cellClick=self.clicked, dataChanged=self.dataChanged)
            
            data = self.createCellMatrix(noRows=12, noColumns=len(columns))
            self.table.setData(data)
        # ----------------------------------------------------------------------
        # No scroll bar initially, then data requires scroll bar
        if option == 2:
            self.table = MyTable(self.tableFrame, columns, rows=noRows, scroll=False)
            data = self.createCellMatrix(noRows=12, noColumns=len(columns))
            self.table.setData(data)
        # ----------------------------------------------------------------------
        # Data requires scroll bar initially, then data reduced and scroll not needed
        if option == 3:
            self.table = MyTable(self.tableFrame, columns, rows=noRows, scroll=True)
            data = self.createCellMatrix(noRows=12, noColumns=len(columns))
            self.table.setData(data)
            #self.table.setData(data[:6])

        # Get table dimensions if needed
        print (f'Table size w:{self.table.width} h:{self.table.height}')

    def dataChanged(self, changes):
        # Need the coordinates of the original data - to update if required
        # Perhaps each row has an ID?
        print ('Data changed')
        print (changes)

    def clicked(self, widget):
        print (f'Parent:Clicked : row={widget.tableRow} : column={widget.tableColumn}')
        print (f'Datat Coordinates ({widget.dataCoords[0]},{widget.dataCoords[1]})')
        row= widget.tableRow
        column= widget.tableColumn
        if self.table.columns[column].get('widget', '') == 'Button':
            self.buttonAction(widget)

    def buttonAction(self, widget):
        print ('Activate required button action')

        print ('Data Row:', widget.tableRow + self.table.topRow, 'Data Column:', widget.tableColumn)

    def drawCell(self, widget, cellDict):
        # There are many different ways this effect can be implemented
        # The data could have a key 'enabled' - to disable the widget
        data = cellDict['data']
        widget.setText(data)
        try: # Not applicable to Combobox
            widget.configure(bg=cellDict['bg'], fg=cellDict['fg']) 
        except: # Assume Combobox
            widget.setOptions(cellDict['options'])
            widget.textSelection.set(data)

    def createCellMatrix(self, noRows, noColumns):
        # Add options for Combobox
        data = []
        for i in range(noRows):
            row = []
            for j in range(noColumns):
                row.append(Cell(data=str(i)+':'+str(j), bg='light grey', fg='blue'))
            data.append(row)
        for row in data:
            row[4] = {'data':'One', 'options':['One','Two','Three']} # Combobox column
            row[7]['data'] = 0 # Check box column
        return data

    def createColumns_1(self):
        cols = [
            {'text':'Column 1', 'bg':'blue', 'fg':'white','width': 60, 'align':'left'},
            {'text':'Column 2', 'bg':'blue', 'fg':'white','width': 100},
            {'text':'Column 3', 'bg':'blue', 'fg':'white','width': 60, 'align':'right'},
            {'text':'Column 4', 'bg':'blue', 'fg':'white','width': 60, 'align':'center'},
            {'text':'Combo Box', 'bg':'blue', 'fg':'white','width': 60, 'widget':'Combobox'},
            {'text':'Entry', 'bg':'blue', 'fg':'white','width': 60, 'widget':'Textbox'},
            {'text':'Button', 'bg':'blue', 'fg':'white','width': 60, 'widget':'Button'},
            {'text':'Check Box', 'bg':'blue', 'fg':'white','width': 140, 'widget':'Checkbox'}
        ]
        return cols

    def on_closing(self):
        if self.table.dataChanged:
            if messagebox.askokcancel("Data Changed", "Data not saved! Do you want to quit?"):
                self.root.destroy()
        else:
            self.root.destroy()



if __name__ == "__main__":
    root = TK.Tk()
    main = MainGUI(root)
    TK.mainloop()
