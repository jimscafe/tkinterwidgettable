"""
   This is inspired by easygui.py
   Possible usage is to insert into non-gui application and display current data
   in a teable in a way to show the application status.
   If there is quite a bit of data - this is easier than just printing variables to the
   console.
   The data does not need to be structured like a matrix of data - see example.py
   Column widths are in chars, not pixels unlike in table.py
"""
import tkinter as TK 

DEFAULTWIDTH = 10

class _table():
    def __init__(self, root, heading, columns, data, choices = [], max_rows = 10):
        self.clicked = 'OK'
        # Scrolling stuff
        self.data = data
        self.columns = columns
        self.vertical_scrolling = False
        self.top_row = 0
        self.view_rows = len(data)
        if len(data) > max_rows:
            self.vertical_scrolling = True
            self.view_rows = max_rows
        # Frames
        self.top_frame = TK.Frame(root, bd=2, relief=TK.SUNKEN)
        #frame.grid(row=0,column=0, ipadx=10, sticky=TK.W)
        self.top_frame.pack(side=TK.TOP, fill=TK.BOTH, padx=20, pady=20)
        #frame.pack()
        message_frame = TK.Frame(self.top_frame, bd=2, relief=TK.SUNKEN)
        #button_frame.grid(row=0,column=0, ipadx=10, sticky=TK.W)
        message_frame.pack(side=TK.TOP, fill=TK.X)

        labels_frame = TK.Frame(self.top_frame)
        labels_frame.pack(side=TK.TOP, fill=TK.BOTH)

        buttons_frame = TK.Frame(self.top_frame, bd=2, relief=TK.SUNKEN)
        #button_frame.grid(row=0,column=0, ipadx=10, sticky=TK.W)
        buttons_frame.pack(side=TK.BOTTOM, fill=TK.X)

        heading = TK.Label(message_frame, text=heading)
        heading.pack(side=TK.LEFT, expand=TK.YES, fill=TK.BOTH, padx='1m', pady='1m')

        if choices:
            for txt in choices:
                button = TK.Button(buttons_frame, text=txt, command=lambda m=txt: self.button_clicked(m))
                button.pack(expand=TK.YES, side=TK.LEFT, padx='1m', pady='1m', ipadx='2m', ipady='1m')
        else: # OK button
            okButton = TK.Button(buttons_frame, takefocus=1, text="OK", command=top_frame.quit)
            okButton.pack(expand=1, side=TK.RIGHT, padx='3m', pady='3m', ipadx='2m', ipady='1m')

        for i, col in enumerate(self.columns):
            #var = TK.Label(labels_frame, text=col.text, width=col.width, bd=1, relief=TK.SUNKEN)
            # Use Entry rather than Label to match the cells
            var = TK.Entry(labels_frame, width=col['width'], bd=1, relief=TK.SUNKEN)
            var.insert(0,col['text'])
            var.configure(state='normal')
            var.configure(bg='royalblue', fg='white')
            var.configure(disabledforeground='lightblue')
            var.configure(disabledbackground='green yellow')
            var.grid(row=0,column=i)
        if self.vertical_scrolling:
            col = len(self.columns)
            x = len(self.data) - max_rows
            vertical_scroll = TK.Scale(labels_frame, orient=TK.VERTICAL, from_=0, to=x, command=self.v_scroll, showvalue=0)
            vertical_scroll.grid(row=1,column=col, rowspan=max_rows, sticky=TK.N+TK.S)

        # Draw data
        self.cells = []
        for i in range(self.view_rows):
            row = i + self.top_row
            cell_row = []
            for j, col in enumerate(self.columns):
                # Using Label
                #var = TK.Label(labels_frame, text=data[row][j], width=col.width, bd=1, relief=TK.SUNKEN)
                #var.grid(row=row+1,column=j)
                # Using Entry
                value = TK.StringVar()
                var = TK.Entry(labels_frame, width=col['width'], textvariable=value,
                               relief=TK.SUNKEN, name=':{}:{}'.format(row,j))
                #var.insert(0,data[row][j])
                var.bind("<Button-1>", self.click) 
                #var.configure(state=col['state'])
                var.configure(disabledforeground='black')
                var.grid(row=row+1,column=j)
                value.set(f'{data[row][j]}')
                cell_row.append(value)
            self.cells.append(cell_row)

    def click(self, event):
        print ('Clicked')
        print (event.widget)

    def populate_labels(self):
        for i in range(self.view_rows):
            row = i + self.top_row
            for j, col in enumerate(self.columns):
                var = self.cells[i][j]
                var.set(self.data[row][j])

    def v_scroll(self, x):
        self.top_row = int(x)
        self.populate_labels()

    def button_clicked(self, txt='OK'):
        self.clicked = txt
        self.top_frame.quit()

def easygui_table(title='', heading='', columns = [], data = [], choices = [], max_rows = 10):
    if not data: return
    root = TK.Tk()
    root.title(title)
    root.protocol("WM_DELETE_WINDOW", __callback)  # Stop user closing window by pressing X
    app = _table(root, heading, columns, data, choices, max_rows)
    root.mainloop()
    root.destroy()
    return app.clicked

def __callback():
    pass

def table_v(master, heading='', columns = [], data = [], choices = [], max_rows = 10): # Called by other tkinter application
    if not data: return
    app = _table(master, heading, columns, data, choices, max_rows)
    return app.clicked

# ------------------------------------------------------------------------------
#           Testing/Sample
# ------------------------------------------------------------------------------

def create_column(text, width=None, state='normal'):
    col = {}
    if not width: width = DEFAULTWIDTH
    col['text'] = text
    col['width'] = width
    col['state'] = 'normal'
    return col


def main():
    # Demonstrate the table
    # No row names, just data columns
    # Column has title, width, editable
    # Data is string
    title = 'Test table'
    heading = 'Test Table Heading'
    columns = [create_column('One'), create_column('Two'), create_column('Three', width=20), create_column('Four')]
    data = []
    rows = 15
    for r in range(rows):
        row = []
        for j, col in enumerate(columns):
            row.append('{}-{}'.format(r, j))
        data.append(row)
    ans = easygui_table(title, heading, columns, data, choices=['Yes','No'], max_rows = 10)
    print ('Response: {}'.format(ans))

def table(title, heading, columns, data, choices=['OK'], max_rows=15, widths=None):
    if not widths:
        widths = {}
    expandRows(data)
    print ('Show table')
    cols = []
    for col in columns:
        cols.append(create_column(col, width=widths.get(col, DEFAULTWIDTH)))
    print (widths)
    ans = easygui_table(title, heading, cols, data, choices, max_rows)
    return ans

def expandRows(data):
    # data is two dimensional matrix, we need all the rows to be the same length
    # so we add spaces to the rows shorter thas the longest row
    maxCells = 0
    for row in data:
        maxCells = max(maxCells, len(row))
    for row in data:
        cells = len(row)
        if cells < maxCells:
            for i in range(cells, maxCells):
                row.append(' ')



if __name__ == '__main__':
    main()