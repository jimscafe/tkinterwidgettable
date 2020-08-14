"""
   Allow editing of data and provide feedback of any changes to the parent widget (Frame)
   <Enter> key and 'lost focus; used to determine when data is entered in the Enter Widget
   <ESC> key used to cancel data changes
   The changes are NOT reflected in the table.data matrix 
   Currently to enter data with the Entry widget, that data is saved only when the return
   key is pressed or Tab key.  The ESC key will cancel the change.
   
   Added column alignment of text (anchor) 

   Decided to handle button click with <ButtonReleased> event and cancel the click event
   for Button widgets
   But this can easily be reversed and button clicks handle in the click callback
   in the parent

   Added Frame to top right when there is a scroll bar - to cover the black rectangle
   the gap in widgets exposes
"""

import tkinter as TK
try:
    import widgets
except:
    from Libs import widgets

DEFAULTCELLWIDTH = 50
DEFAULTCELLHEIGHT = 25
DEFAULTSTYLE = TK.SUNKEN

ANCHOR = {'left':'w', 'right':'e', 'center':'center'}

class MyTable:
    def __init__(self, parent, columns, data=None, rows=None, scroll=None,
                 drawCell=None, cellClick = None, dataChanged=None):
        # Configure parent frame
        self.parent = parent
        self.tableFrame = TK.Frame(self.parent)
        self.tableFrame.config(bg='black')
        self.tableFrame.pack(side=TK.TOP, fill=TK.BOTH, padx=1)
        self.tableFrame.bind_all("<MouseWheel>", self._on_mousewheel)
        if drawCell:
            self.drawCell = drawCell
        if cellClick:
            self.clicked = cellClick
        if dataChanged:
            self.dataUpdated = dataChanged
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
        self.widgets = []  # Two dimension array
        self.drawWidgets()
        if self.data:
            self.setData(data)

    def drawWidgets(self):
        # First create column headers
        pad = (1,1)
        for j in range(self.noColumns):
            widgetFrame = TK.Frame(self.tableFrame,width=self.columns[j]['width'],
                                   height=DEFAULTCELLHEIGHT) 
            widgetFrame.pack_propagate(0) # Stops child widgets of label_frame from resizing it
            cell = widgets.Label(widgetFrame)
            cell.configure(bg=self.columns[j]['bg'], fg=self.columns[j]['fg'])
            cell.pack(expand=TK.YES, fill=TK.BOTH)
            cell.setText(self.columns[j]['text'])
            cell.tableRow = -1
            cell.tableColumn = j
            cell.bind("<Button-1>", self._click) 
            pad = (1,1)
            if j == 0: pad = (2,1)
            if j == self.noColumns -1: pad=(1,2)
            widgetFrame.grid(row=0, column=j, padx=pad, pady=(2,1))

        # Second create cell widgets
        for i in range(self.visibleRows):
            widgetRow = []
            for j in range(self.noColumns):
                widgetName = self.columns[j].get('widget', 'Label') # Default to label
                widgetFrame = TK.Frame(self.tableFrame,width=self.columns[j]['width'],
                                       height=DEFAULTCELLHEIGHT) #,
                widgetFrame.pack_propagate(0) # Stops child widgets of label_frame from resizing it
                if widgetName == 'Textbox':
                    cellWidget = widgets.Textbox(widgetFrame)
                    cellWidget.bind('<Return>', self._dataChanged)
                    cellWidget.bind('<Escape>', self._cancelChange)
                    cellWidget.bind("<FocusOut>", self._dataChanged)
                    #cellWidget.bind("<Leave>", self._click) # Must decide if this is sensible behaviour
                elif widgetName == 'Button':
                    cellWidget = widgets.Button(widgetFrame) #, command=self._dataChanged)
                    cellWidget.bind('<ButtonRelease>', self._dataChanged)
                    # cellWidget.config(command=self.dataChanged)
                elif widgetName == 'Checkbox':
                    cellWidget = widgets.Checkbox(widgetFrame)
                elif widgetName == 'Combobox':
                    cellWidget = widgets.Combobox(widgetFrame)
                    cellWidget.bind("<<ComboboxSelected>>", self._dataChanged)
                else:
                    cellWidget = widgets.Label(widgetFrame)
                cellWidget.widgetType = widgetName
                cellWidget.pack(expand=TK.YES, fill=TK.BOTH)
                align = self.columns[j].get('align', '')
                if align:
                    cellWidget.configure(anchor=ANCHOR[align])
                cellWidget.setText('')
                cellWidget.tableRow = i
                cellWidget.tableColumn = j
                cellWidget.dataCoords = []  # The row/column in the data matrix - set when table populated
                cellWidget.bind("<Button-1>", self._click) 
                widgetRow.append(cellWidget)
                pad = (1,1)
                ypad = (1,1)
                if j == 0: pad = (2,1)
                if j == self.noColumns -1: pad=(1,2)
                if i == self.visibleRows -1: ypad = (1,2)
                widgetFrame.grid(row=i+1, column=j, padx=pad, pady=ypad)
            self.widgets.append(widgetRow)
        if self.data:    
            if len(self.data) > self.visibleRows:
                self.scroll = True  
                col = len(self.columns)
                x = len(self.data) - self.visibleRows
                self.addVerticalScroll(x)
        elif self.scroll:
            col = len(self.columns)
            x = 0
            self.addVerticalScroll(x)

        # Get parent frame width and height - x and y coordinates can also be accessed
        self.tableFrame.update() # Required to get frame width and height at this time
        self.width = self.tableFrame.winfo_width()
        self.height = self.tableFrame.winfo_height()

    def populateCells(self):
        for i in range(min(self.visibleRows, len(self.data))): 
            rowIndex = i + self.topRow
            for j in range(self.noColumns): 
                cellObject = self.data[rowIndex][j] # For more complex formatting this is a Cell dictionary
                self.widgets[i][j].enabled(True)  # This can be overwritten by drawCell function
                self.widgets[i][j].dataCoords = (rowIndex, j)
                self.drawCell(self.widgets[i][j], cellObject)
        if self.visibleRows > len(self.data): # Need to blank the lower rows
            for i in range(len(self.data), self.visibleRows):
                for j in range(self.noColumns):
                    self.widgets[i][j].setText('') # Need to disable them too 
                    self.widgets[i][j].enabled(False)

    def drawCell(self, widget, cellObject):
        # Widget has attribute dataCoords -> (row,column) of the data matrix
        widget.setText(cellObject) # cellObject in this simple case is a string

    def setData(self, data):
        # Check and set scrolling
        self.dataChanged = False
        self.data = data
        if len(self.data) > self.visibleRows: # Should be a scroll bar
            if not self.scroll:
                self.addVerticalScroll(len(self.data) - self.visibleRows)
            self.vertical_scroll.configure(to=len(self.data) - self.visibleRows)
            self.scroll = True
        else:
            self.scroll = False
            try:
                self.vertical_scroll.destroy()
            except:
                pass # No scrollbar to destroy
        self.populateCells()

    def addVerticalScroll(self, x):
        col = len(self.columns)
        #x = len(self.data) - self.visibleRows
        self.vertical_scroll = TK.Scale(self.tableFrame, orient=TK.VERTICAL, from_=0, to=x, command=self.v_scroll, showvalue=0)
        self.vertical_scroll.grid(row=1,column=col, rowspan=self.visibleRows, sticky=TK.N+TK.S)
        # Add frame to remove black rectangle top right - above scroll bar
        self.topRight = TK.Frame(self.tableFrame)
        self.topRight.grid(row=0,column=col, sticky=TK.NSEW)

    def setScroll(self):
        # Reset the scroll bar
        self.vertical_scroll.configure(to=len(self.data) - self.visibleRows)

    def v_scroll(self, x):
        if self.scroll:
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
    # Click on cell - can be just a click
    # ------------------------------------------------------------------------------------
    def _click(self, event):
        if event.widget.tableRow < 0: # Column Header - handle this in parent
            self.clicked(event.widget)
        else:
            if event.widget.cget('state') == 'normal': # Widget is enabled
                if event.widget.widgetType == 'Checkbox': # Data changed
                    self._dataChanged(event)
                elif event.widget.widgetType == 'Button': # Button click
                    pass # Stop click calling click event for button
                else:
                    self.clicked(event.widget) # Parent callback if implemented

                # tableRow = event.widget.tableRow + self.topRow
                # tableColumn = event.widget.tableColumn
                # Ignore complex cell where each cell can be enabled/disabled
                # rather than having the widget enabled/disabled in parent drawCell
                #if self.data[tableRow][tableColumn].get('Enabled', True): # If data element not disabled

                # Need to sort out the button click in the following code.
                # if self.columns[event.widget.tableColumn].get('widget', '') == 'Button':
                #     self.clicked(event.widget)
                # if self._isDataModified(event.widget):
                #     # When combobox or checkbox clicked, data is changed
                #     print ('Data Modified')
                #     self.dataChanged = True
                #     if self.columns[tableColumn].get('widget', '') == 'Checkbox':
                #         print ('Check box clicked <- in table')
                #         value = event.widget.getText() # Value when clicked - before changed
                #         newValue = (value + 1) % 2
                #         print ('New value', newValue)
                #         # Change the table.data
                #         self.data[tableRow][tableColumn]['data'] = newValue
                #         self.dataUpdated({'row': tableRow, 'column':tableColumn, 'newvalue': newValue})
                #     elif self.columns[tableColumn].get('widget', '') == 'Combobox':
                #         print ('Combobox selection made <- table')
                #         print (event.widget.getText())
                #         print (self.data[tableRow][tableColumn]['data'])
                #         self.data[tableRow][tableColumn]['data'] = event.widget.getText()
                #         self.dataUpdated({'row': tableRow, 'column':tableColumn, 'newvalue': event.widget.getText()})
                #     elif self.columns[tableColumn].get('widget', '') == 'Textbox':
                #         print ('New entry data')
                #         # Line below modified to accept just string data, not dictionary
                #         self.data[tableRow][tableColumn] = event.widget.getText()
                #         self.dataUpdated({'row': tableRow, 'column':tableColumn, 'newvalue': event.widget.getText()})
                # Currently this is called even when return key pressed in Entry widget
                #self.clicked(event.widget) # Parent callback if implemented

    def clicked(self, widget): # Overwrite this in parent module/class
        print ('Cell clicked (if row is -1, the column header was clicked')
        print (f'row={widget.tableRow} : column={widget.tableColumn}')
        print (widget.getText())
        print ('This function should be overwritten by the client function for handling click event')

    # ------------------------------------------------------------------------------------
    # Modifying data
    # ------------------------------------------------------------------------------------
    # def _isDataModified(self, widget):
    #     # Check if checkbox or button - then data has changed
    #     # Else check if the data has changed
    #     if self.columns[widget.tableColumn].get('widget', '') == 'Checkbox':
    #         return True
    #     if self.columns[widget.tableColumn].get('widget', '') == 'Button':
    #         return True
    #     # The following line has been modified to remove the cell data as a dictionary
    #     # Now handles simple data
    #     print (widget.getText())
    #     print (self.data[widget.tableRow + self.topRow][widget.tableColumn]) 
    #     return widget.getText() != str(self.data[widget.tableRow + self.topRow][widget.tableColumn]) 

    # def _updateCell(self, widget):
    #     pass

    def _dataChanged(self, event):
        self.dataChanged = True
        self.dataUpdated(event.widget)

    def dataUpdated(self, widget): # callback to parent
        pass


    def _cancelChange(self, event):
        # Reset the widget value
        print ('Escape key pressed')
        widget = event.widget
        # Line below modified to work with simple strings, not dictionaries
        widget.setText(self.data[widget.tableRow + self.topRow][widget.tableColumn])

# This dictionary is a template for cell objects
def Column(text, *args, **kwargs):
    return {'text': text, 'width':60, 'widget': 'Label', 'bg':'white','fg':'black', **kwargs}

def Cell(data='', **kwargs):
    # Default values for background and foregraound colors - can be overwritten by kwargs
    return {'data': data, 'bg':'white', 'fg':'black',  **kwargs}

