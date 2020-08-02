import tkinter as TK
from table_v4 import MyTable, Cell

# Add wdigets combobox, entry, checkbox, button
# However, the data is not changed by any interaction with the widgets

class MainGUI(object):
    def __init__(self,root):
        self.root = root
        frm = TK.Frame(self.root)
        frm.pack(padx=20, pady=20)
        self.tableFrame = TK.Frame(frm)
        # How to define columns (text, width, colors)?
        columns = self.createColumns_1()
        noRows = 6
        data = self.createMatrix_1(10, len(columns))
        option = 2  # Modify this to demonstrate 5 options
        # ----------------------------------------------------------------------
        # Put widgets in table (Entry, Combobox, Checkbox, Button)
        if option == 1:
            self.table = MyTable(self.tableFrame, columns, rows=noRows, scroll=True)
            self.table.setData(data)
        # ----------------------------------------------------------------------
        # Option 2, use Cell dictionary when data created - overwrite default drawCell
        # Need to get feedback when combobox selection is changed
        # Currently the combo selection is bound to the click event - so for a combobox
        # the click event is called twice, once when the widget is selected (and options
        # drop down) and again when the selection is made - this could be made
        # mode sophisticated 
        if option == 2:
            data = self.createCellMatrix(10, len(columns))
            self.table = MyTable(self.tableFrame, columns, rows=noRows, scroll=True)
            self.table.drawCell = self.drawCell
            self.table.setData(data)


        # Get table dimensions if needed
        print (f'Table size w:{self.table.width} h:{self.table.height}')

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

    def createMatrix_1(self, noRows=10, noColumns=8):
        data = []
        for i in range(noRows):
            row = []
            for j in range(noColumns):
                row.append(str(i)+':'+str(j))
            data.append(row)
        return data

    def createCellMatrix(self, noRows, noColumns):
        # Add options for Combobox
        data = []
        for i in range(noRows):
            row = []
            for j in range(noColumns):
                row.append(Cell(data=str(i)+':'+str(j), fg='blue'))
            data.append(row)
        for row in data:
            row[4] = {'data':'One', 'options':['One','Two','Three']}
        return data

    def createColumns_1(self):
        cols = [
            {'text':'Column 1', 'bg':'blue', 'fg':'white','width': 60},
            {'text':'Column 2', 'bg':'blue', 'fg':'white','width': 100},
            {'text':'Column 3', 'bg':'blue', 'fg':'white','width': 60},
            {'text':'Column 4', 'bg':'blue', 'fg':'white','width': 60},
            {'text':'Column 5', 'bg':'blue', 'fg':'white','width': 60, 'widget':'Combobox'},
            {'text':'Column 6', 'bg':'blue', 'fg':'white','width': 60, 'widget':'TextBox'},
            {'text':'Column 7', 'bg':'blue', 'fg':'white','width': 60, 'widget':'Button'},
            {'text':'Column 8', 'bg':'blue', 'fg':'white','width': 140, 'widget':'Checkbox'}
        ]
        return cols


if __name__ == "__main__":
    root = TK.Tk()
    main = MainGUI(root)
    TK.mainloop()
