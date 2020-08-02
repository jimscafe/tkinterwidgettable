"""
   Allow editing of data and provide feedback of any changes to the parent widget (Frame)
   <Enter> key and 'lost focus; used to determine when data is entered in the Enter Widget
   <ESC> key used to cancel data changes
   The changes are then reflected in the table.data matrix and also a signal sent to the client
   class
   Currently to enter data with the Entry widget, that data is saved only when the return
   key is pressed. If no return key is pressed the table.data is not updated. 
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
        self.dataChanged = False
        self.visibleRows = rows
        self.scroll = scroll
        if rows == None:
            self.visibleRows = len(data)
        self.noColumns = len(columns)
        self.topRow = 0
        self.data = data
        self.columns = columns
        self.width = 0 # Pixels
        self.height = 0
        self.cells = []  # Two dimension array
        self.drawWidgets()
        if self.data:
            self.setData(data)

    def drawWidgets(self):
        # First create column headers
        pad = (1,1)
        for j in range(self.noColumns):
            widgetFrame = TK.Frame(self.parent,width=self.columns[j]['width'],
                                   height=DEFAULTCELLHEIGHT) 
            widgetFrame.pack_propagate(0) # Stops child widgets of label_frame from resizing it
            cell = widgets.Label(widgetFrame)
            cell.configure(bg=self.columns[j]['bg'], fg=self.columns[j]['fg'])
            cell.pack(expand=TK.YES, fill=TK.BOTH)
            cell.setText(self.columns[j]['text'])
            cell.trow = -1
            cell.tcol = j
            cell.bind("<Button-1>", self._click) 
            pad = (1,1)
            if j == 0: pad = (2,1)
            if j == self.noColumns -1: pad=(1,2)
            widgetFrame.grid(row=0, column=j, padx=pad, pady=(2,1))

        # Second create cell widgets
        for i in range(self.visibleRows):
            cell_row = []
            for j in range(self.noColumns):
                widgetName = self.columns[j].get('widget', 'Label') # Default to label
                widgetFrame = TK.Frame(self.parent,width=self.columns[j]['width'],
                                       height=DEFAULTCELLHEIGHT) #,
                widgetFrame.pack_propagate(0) # Stops child widgets of label_frame from resizing it
                if widgetName == 'Textbox':
                    cell = widgets.Textbox(widgetFrame)
                    cell.bind('<Return>', self._click)
                    cell.bind('<Escape>', self._cancelChange)
                elif widgetName == 'Button':
                    cell = widgets.Button(widgetFrame)
                elif widgetName == 'Checkbox':
                    cell = widgets.Checkbox(widgetFrame)
                elif widgetName == 'Combobox':
                    cell = widgets.Combobox(widgetFrame)
                    cell.bind("<<ComboboxSelected>>", self._click)
                else:
                    cell = widgets.Label(widgetFrame)
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
                widgetFrame.grid(row=i+1, column=j, padx=pad, pady=ypad)
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
                cell = self.data[rowIndex][j] # For more complex formatting this is a Cell dictionary
                self.drawCell(self.cells[i][j], cell)

    def drawCell(self, widget, cellObject):
        widget.setText(cellObject) # cellObject in this simple case is a string

    def setData(self, data):
        # Check and set scrolling
        self.dataChanged = False
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

    def _on_mousewheel(self, event):
        # <- Calls the table mousewheel function - scrolls the table and moves the scroll bar
        self.mousewheel(event.delta/120)

    def mousewheel(self, x): 
        if self.scroll:
            if x > 0:
                y = max(self.topRow - 1,0)
            else:
                y = min(self.topRow + 1, len(self.data) - self.visibleRows )
            self.topRow = y
            self.populateCells()
            self.vertical_scroll.set(y)
    # ------------------------------------------------------------------------------------
    # Click on cell - can be just a click, or can be a cell data change
    # ------------------------------------------------------------------------------------
    def _click(self, event):
        if event.widget.trow < 0: # Column Header - handle this in parent
            self.clicked(event.widget)
        tableRow = event.widget.trow + self.topRow
        tableColumn = event.widget.tcol
        if self.data[tableRow][tableColumn].get('Enabled', True): # If data element not disabled
            if self.columns[event.widget.tcol].get('widget', '') == 'Button':
                self.clicked(event.widget)
            if self._isDataModified(event.widget):
                if self.columns[tableColumn].get('widget', '') == 'Checkbox':
                    print ('Check box clicked <- in table')
                    value = event.widget.getText() # Value when clicked - before changed
                    newValue = (value + 1) % 2
                    print ('New value', newValue)
                    # Change the table.data
                    self.data[tableRow][tableColumn]['data'] = newValue
                    self.dataUpdated({'row': tableRow, 'column':tableColumn, 'newvalue': newValue})
                elif self.columns[tableColumn].get('widget', '') == 'Combobox':
                    print ('Combobox selection made <- table')
                    print (event.widget.getText())
                    print (self.data[tableRow][tableColumn]['data'])
                    self.data[tableRow][tableColumn]['data'] = event.widget.getText()
                    self.dataUpdated({'row': tableRow, 'column':tableColumn, 'newvalue': event.widget.getText()})
                elif self.columns[tableColumn].get('widget', '') == 'Textbox':
                    print ('New entry data')
                    self.data[tableRow][tableColumn]['data'] = event.widget.getText()
                    self.dataUpdated({'row': tableRow, 'column':tableColumn, 'newvalue': event.widget.getText()})

                print ('Data Modified')
                self.dataChanged = True
            self.clicked(event.widget) # Parent callback if implemented

    def clicked(self, widget): # Overwrite this in parent module/class
        print ('Cell clicked (if row is -1, the column header was clicked')
        print (f'row={widget.trow} : column={widget.tcol}')
        print (widget.getText())
        print ('This function should be overwritten by the client function for handling click event')

    # ------------------------------------------------------------------------------------
    # Modifying data
    # ------------------------------------------------------------------------------------
    def _isDataModified(self, widget):
        # Check if checkbox or button - then data has changed
        # Else check if the data has changed
        if self.columns[widget.tcol].get('widget', '') == 'Checkbox':
            return True
        if self.columns[widget.tcol].get('widget', '') == 'Button':
            return True
        return widget.getText() != self.data[widget.trow + self.topRow][widget.tcol]['data']

    # def _updateCell(self, widget):
    #     pass

    def dataUpdated(self, widget): # callback to parent
        pass


    def _cancelChange(self, event):
        # Reset the widget value
        print ('Escape key pressed')
        widget = event.widget
        widget.setText(self.data[widget.trow + self.topRow][widget.tcol]['data'])

# This dictionary is a template for cell objects
def Cell(data='', **kwargs):
    # Default values for background and foregraound colors - can be overwritten by kwargs
    return {'data': data, 'bg':'white', 'fg':'black',  **kwargs}

