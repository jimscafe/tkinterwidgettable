"""
  Implementation example of data editing for each of the wdigets Entry, Checkbox, Combobox, Button
  Button -> click event
  Clickbox -> Change data, cell updated
"""
import tkinter as TK
from tkinter import messagebox
from table_v5a import MyTable, Cell

# Add wdigets combobox, entry, checkbox, button
# Handle the data changes
# Check box original data - should be changed to 0 or 1 in table.data
# Can modify this if necessary
# Need option for combo to be initially empty

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
        option = 1  # Modify this to demonstrate options
        # ----------------------------------------------------------------------
        # Improve code encapsulation
        if option == 1:
            self.table = MyTable(self.tableFrame, columns, rows=noRows, scroll=True)
            data = self.createCellMatrix(noRows=12, noColumns=len(columns))
            # The three callbacks below could all be placed in one function in the table class
            self.table.drawCell = self.drawCell
            self.table.clicked = self.clicked
            self.table.dataUpdated = self.dataChanged
            self.table.setData(data)

        # Get table dimensions if needed
        print (f'Table size w:{self.table.width} h:{self.table.height}')

    def dataChanged(self, changes):
        print ('Data changed')
        print (changes)

    def clicked(self, widget):
        print (f'Parent:Clicked : row={widget.trow} : column={widget.tcol}')
        row= widget.trow
        column= widget.tcol
        if self.table.columns[column].get('widget', '') == 'Button':
            self.buttonAction(widget)

    def buttonAction(self, widget):
        print ('Activate required button action')
        print ('Data Row:', widget.trow + self.table.topRow, 'Data Column:', widget.tcol)

    def drawCell(self, widget, cellObject):
        # There are many different ways this effect can be implemented
        data = cellObject['data']
        widget.setText(data)
        # Background and foregraound could be set when data matrix created
        if data == '2:1': # Format cell with specific data value
            cellObject['bg'] = 'green'
            cellObject['fg'] = 'white'
        if widget.tcol == 3: # Format column
            cellObject['bg'] = 'pink'
        # Does this apply to all possible widgets - can depend upon column?
        try: # Not applicable to Combobox
            widget.configure(bg=cellObject['bg'], fg=cellObject['fg']) 
        except: # Assume Combobox
            #print (data)
            widget.setOptions(cellObject['options'])
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
            {'text':'Column 1', 'bg':'blue', 'fg':'white','width': 60},
            {'text':'Column 2', 'bg':'blue', 'fg':'white','width': 100},
            {'text':'Column 3', 'bg':'blue', 'fg':'white','width': 60},
            {'text':'Column 4', 'bg':'blue', 'fg':'white','width': 60},
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
