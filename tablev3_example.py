import tkinter as TK
from table_v3 import MyTable, Cell

# Cell formatting

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
        # Simple formatting - data matrix is text only - no formatting
        if option == 1:
            self.table = MyTable(self.tableFrame, columns, rows=noRows, scroll=True)
            self.table.setData(data)
        # ----------------------------------------------------------------------
        # Option 2, use Cell dictionary when data created - overwrite default drawCell
        # in Table class with self.drawCell() function
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
        widget.configure(bg=cellObject['bg'], fg=cellObject['fg']) 

    def createMatrix_1(self, noRows=10, noColumns=8):
        # Matrix of text values
        data = []
        for i in range(noRows):
            row = []
            for j in range(noColumns):
                row.append(str(i)+':'+str(j))
            data.append(row)
        return data

    def createCellMatrix(self, noRows, noColumns):
        # Matrix of dictionary values (Cell() creates the dictionary)
        data = []
        for i in range(noRows):
            row = []
            for j in range(noColumns):
                row.append(Cell(data=str(i)+':'+str(j), fg='blue'))
            data.append(row)
        return data

    def createColumns_1(self):
        cols = [
            {'text':'Column 1', 'bg':'blue', 'fg':'white','width': 60},
            {'text':'Column 2', 'bg':'blue', 'fg':'white','width': 100},
            {'text':'Column 3', 'bg':'blue', 'fg':'white','width': 60},
            {'text':'Column 4', 'bg':'blue', 'fg':'white','width': 60},
            {'text':'Column 5', 'bg':'blue', 'fg':'white','width': 60},
            {'text':'Column 6', 'bg':'blue', 'fg':'white','width': 60},
            {'text':'Column 7', 'bg':'blue', 'fg':'white','width': 60},
            {'text':'Column 8', 'bg':'blue', 'fg':'white','width': 140}
        ]
        return cols


if __name__ == "__main__":
    root = TK.Tk()
    main = MainGUI(root)
    TK.mainloop()
