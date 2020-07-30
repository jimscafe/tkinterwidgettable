import tkinter as TK
from table_v2 import MyTable

# Add mousewheel scrolling

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
        option = 1  # Modify this to demonstrate 5 options
        # ----------------------------------------------------------------------
        # Option to draw table before data created?
        if option == 1:
            self.table = MyTable(self.tableFrame, columns, rows=noRows, scroll=True)
            self.table.setData(data)
        # ----------------------------------------------------------------------
        # Get table dimensions if needed
        print (f'Table size w:{self.table.width} h:{self.table.height}')


    def createMatrix_1(self, noRows=10, noColumns=8):
        data = []
        for i in range(noRows):
            row = []
            for j in range(noColumns):
                row.append(str(i)+':'+str(j))
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