"""
   A remake of the table widget that used entry widgets
   Simplify some items and allow greater flexibility
   Including other widgets as table cells (checkbox, combo box)
   Allow scroling without scrollbar using mousewheel as an option

   Need number of visible rows, and widths of columns
   30 July 2020 - adding mousewheel scrolling
                - add cell click event (double click can be added in the same way)
"""
import tkinter as TK
import widgets

DEFAULTCELLWIDTH = 50
DEFAULTCELLHEIGHT = 25
DEFAULTSTYLE = TK.SUNKEN

class MyTable:
    def __init__(self, parent, columns, data=None, rows=None, scroll=None):
        # Configure parent frame
        parent.config(bg='black')
        parent.pack(side=TK.TOP, fill=TK.BOTH, padx=1)
        parent.bind_all("<MouseWheel>", self._on_mousewheel)
        self.parent = parent
        self.visibleRows = rows
        self.scroll = scroll
        if rows == None:
            self.visibleRows = len(data)
        #self.visibleRows = noRows
        self.noColumns = len(columns)
        self.topRow = 0
        self.data = data
        self.columns = columns
        self.width = 0 # Pixels
        self.height = 0
        self.cells = []  # Two dimension array
        #self.t()
        self.drawWidgets()
        if self.data:
            self.populateCells()

    def drawWidgets(self):
        # First column header
        pad = (1,1)
        for j in range(self.noColumns):
            label_frame = TK.Frame(self.parent,width=self.columns[j]['width'],
                                   height=DEFAULTCELLHEIGHT) 
            label_frame.pack_propagate(0) # Stops child widgets of label_frame from resizing it
            cell = widgets.Label(label_frame)
            cell.configure(bg=self.columns[j]['bg'], fg=self.columns[j]['fg'])
            cell.pack(expand=TK.YES, fill=TK.BOTH)
            cell.setText(self.columns[j]['text'])
            cell.trow = -1
            cell.tcol = j
            cell.bind("<Button-1>", self._click) 
            pad = (1,1)
            if j == 0: pad = (2,1)
            if j == self.noColumns -1: pad=(1,2)
            label_frame.grid(row=0, column=j, padx=pad, pady=(2,1))

        # Second draw cell widgets
        for i in range(self.visibleRows):
            cell_row = []
            for j in range(self.noColumns):
                # Try with labels first - use frame round widget to set width, height in pixels
                label_frame = TK.Frame(self.parent,width=self.columns[j]['width'],
                                       height=DEFAULTCELLHEIGHT) #,
                label_frame.pack_propagate(0) # Stops child widgets of label_frame from resizing it
                cell = widgets.Label(label_frame)
                cell.pack(expand=TK.YES, fill=TK.BOTH)
                cell.setText('')
                cell.trow = i
                cell.tcol = j
                cell.bind("<Button-1>", self._click) 
                cell_row.append(cell)
                pad = (1,1)
                ypad = (1,1)
                if j == 0: pad = (2,1)
                if j == self.noColumns -1: pad=(1,2)
                if i == self.visibleRows -1: ypad = (1,2)
                label_frame.grid(row=i+1, column=j, padx=pad, pady=ypad)
            self.cells.append(cell_row)
        if self.data:    
            if len(self.data) > self.visibleRows:
                self.scroll = True  
                col = len(self.columns)
                x = len(self.data) - self.visibleRows
                self.vertical_scroll = TK.Scale(self.parent, orient=TK.VERTICAL, from_=0, to=x, command=self.v_scroll, showvalue=0)
                self.vertical_scroll.grid(row=1,column=col, rowspan=self.visibleRows, sticky=TK.N+TK.S)
        elif self.scroll:
            col = len(self.columns)
            x = 0
            self.vertical_scroll = TK.Scale(self.parent, orient=TK.VERTICAL, from_=0, to=x, command=self.v_scroll, showvalue=0)
            self.vertical_scroll.grid(row=1,column=col, rowspan=self.visibleRows, sticky=TK.N+TK.S)

        # Get parent frame width and height - x and y coordinates can also be accessed
        self.parent.update() # Required to get frame width and height at this time
        self.width = self.parent.winfo_width()
        self.height = self.parent.winfo_height()

    def populateCells(self):
        for i in range(min(self.visibleRows, len(self.data))): 
            rowIndex = i + self.topRow
            for j in range(self.noColumns): 
                cell = self.data[rowIndex][j] # Later we make this a more complex object
                self.cells[i][j].setText(cell)

    def setData(self, data):
        # Check and set scrolling
        self.data = data
        if len(self.data) > self.visibleRows: # Should be a scroll bar
            self.vertical_scroll.configure(to=len(self.data) - self.visibleRows)
        self.populateCells()

    def setScroll(self):
        # Reset the scroll bar
        self.vertical_scroll.configure(to=len(self.data) - self.visibleRows)

    def v_scroll(self, x):
        self.topRow = int(x)
        self.populateCells()

    def _on_mousewheel(self, event): # <- Calls the table mousewheel function - scrolls the table and moves the scroll bar
        self.mousewheel(event.delta/120)

    def mousewheel(self, x): 
        if self.scroll:
            #print (self.vertical_scroll.get())
            if x > 0:
                y = max(self.topRow - 1,0)
            else:
                y = min(self.topRow + 1, len(self.data) - self.visibleRows )
            self.topRow = y
            self.populateCells()
            self.vertical_scroll.set(y)
    # ------------------------------------------------------------------------------------
    # Click on cell
    def _click(self, event):
        print ('Clicked')
        print (event.widget)
        self.clicked(event.widget)

    def clicked(self, event): # Overwrite this in parent module/class
        print ('Cell clicked (-1 == column header')
        print (f'row={event.trow} : column={event.tcol}')