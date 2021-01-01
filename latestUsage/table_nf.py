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
"""

import tkinter as TK
from tkinter import ttk

#DEFAULTCELLWIDTH = 50
#DEFAULTCELLHEIGHT = 25
#DEFAULTSTYLE = TK.SUNKEN
DEFAULTBACKGROUND = 'white'

#ANCHOR = {'left':'w', 'right':'e', 'center':'center'}

class MyTable:
    def __init__(self, parent, columns, data=None, rows=None, scroll=None,
                 drawCell=None, cellClick = None, dataChanged=None):
        # Configure parent frame
        self.parent = parent
        self.tableFrame = TK.Frame(self.parent)
        self.tableFrame.config(bg='black')
        self.tableFrame.grid(row=0,column=0)
        #self.tableFrame.pack(side=TK.TOP, fill=TK.BOTH, padx=1)
        self.tableFrame.bind_all("<MouseWheel>", self._on_mousewheel)
        # Stop the mousewheel affecting other widgets
        self.tableFrame.bind('<Enter>', self._inTable)
        self.tableFrame.bind('<Leave>', self._leaveTable)
        self.inTable = False  # True when mouse is in the table frame
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
        self.columnWidgets = []
        self.widgets = []  # Two dimension array
        self.drawWidgets()
        if self.data:
            self.setData(data)

    def drawWidgets(self):
        # First create column headers
        pad = (1,1)
        for j in range(self.noColumns):
            # widgetFrame = TK.Frame(self.tableFrame,width=self.columns[j]['width'],
            #                        height=DEFAULTCELLHEIGHT) 
            # widgetFrame.pack_propagate(0) # Stops child widgets of label_frame from resizing it
            cell = Label(self.tableFrame)
            cell.configure(bg=self.columns[j]['bg'], fg=self.columns[j]['fg'], relief=TK.RAISED)
            self.columnWidgets.append(cell)
            #cell.config(width=self.columns[j]['width'])

            cell.grid(row=0,column=j, sticky='ew')
            #cell.pack(expand=TK.YES, fill=TK.BOTH)
            cell.setText(self.columns[j]['text'])
            cell.tableRow = -1
            cell.tableColumn = j
            cell.bind("<Button-1>", self._click) 
            pad = (1,1)
            if j == 0: pad = (2,1)
            if j == self.noColumns -1: pad=(1,2)

        # Second create cell widgets
        for i in range(self.visibleRows):
            widgetRow = []
            for j in range(self.noColumns):
                widgetName = self.columns[j].get('widget', 'Label') # Default to label
                # widgetFrame = TK.Frame(self.tableFrame,width=self.columns[j]['width'],
                #                        height=DEFAULTCELLHEIGHT) #,
                # widgetFrame.pack_propagate(0) # Stops child widgets of label_frame from resizing it
                if widgetName == 'Textbox':
                    cellWidget = Textbox(self.tableFrame)
                    #cellWidget.config(width=columns[j]['width')
                    cellWidget.bind('<Return>', self._dataChanged)
                    cellWidget.bind('<Escape>', self._cancelChange)
                    #cellWidget.bind("<FocusOut>", self._dataChanged)
                    #cellWidget.bind("<Leave>", self._click) # Must decide if this is sensible behaviour
                elif widgetName == 'Button':
                    cellWidget = Button(self.tableFrame) #, command=self._dataChanged)
                    cellWidget.bind('<ButtonRelease>', self._dataChanged)
                    # cellWidget.config(command=self.dataChanged)
                elif widgetName == 'Checkbox':
                    cellWidget = Checkbox(self.tableFrame)
                elif widgetName == 'Combobox':
                    cellWidget = Combobox(self.tableFrame)
                    cellWidget.bind("<<ComboboxSelected>>", self._dataChanged)
                else:
                    cellWidget = Label(self.tableFrame)
                    cellWidget.config(relief=TK.RAISED)
                cellWidget.config(width=self.columns[j]['width'])
                cellWidget.widgetType = widgetName
                #cellWidget.pack(expand=TK.YES, fill=TK.BOTH)
                align = self.columns[j].get('align', '')
                #print (widgetName)
                if align:
                    cellWidget.align(align)
                    # try:
                    #     cellWidget.configure(anchor=ANCHOR[align])
                    # except:
                    #     cellWidget.configure(justify=align)

                cellWidget.grid(row=i+1, column=j, stick='ewns')
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
                #widgetFrame.grid(row=i+1, column=j, padx=pad, pady=ypad)
            self.widgets.append(widgetRow)
        if self.data:    
            if len(self.data) > self.visibleRows:
                self.scroll = True  
                col = len(self.columns)
                x = len(self.data) - self.visibleRows
                self.addVerticalScroll(x)
                #self.vertical_scroll = TK.Scale(self.tableFrame, orient=TK.VERTICAL, from_=0, to=x, command=self.v_scroll, showvalue=0)
                #self.vertical_scroll.grid(row=1,column=col, rowspan=self.visibleRows, sticky=TK.N+TK.S)
        elif self.scroll:
            col = len(self.columns)
            x = 0
            self.addVerticalScroll(x)
            #self.vertical_scroll = TK.Scale(self.tableFrame, orient=TK.VERTICAL, from_=0, to=x, command=self.v_scroll, showvalue=0)
            #self.vertical_scroll.grid(row=1,column=col, rowspan=self.visibleRows, sticky=TK.N+TK.S)

        # Get parent frame width and height - x and y coordinates can also be accessed
        self.tableFrame.update() # Required to get frame width and height at this time
        self.width = self.tableFrame.winfo_width()
        self.height = self.tableFrame.winfo_height()

    def populateCells(self):
        #dataRowLength = len(self.data[0])
        if len(self.data) <= self.visibleRows: self.topRow = 0
        elif self.topRow + self.visibleRows >= len(self.data) + 1:
            self.topRow = len(self.data) - self.visibleRows + 1
        #print (self.topRow)
        #self.topRow = max(0, self.visibleRows-len(self.data))
        for i in range(min(self.visibleRows, len(self.data))): 
            rowIndex = i + self.topRow
            for j in range(self.noColumns):
                if j < len(self.data[rowIndex]): # dataRowLength: 
                    cellObject = self.data[rowIndex][j] # For more complex formatting this is a Cell dictionary
                    self.widgets[i][j].enabled(True)  # This can be overwritten by drawCell function
                    self.widgets[i][j].dataCoords = (rowIndex, j)
                    self.drawCell(self.widgets[i][j], cellObject)
                else:
                    self.widgets[i][j].setText('') # Need to disable them too 
                    self.drawCell(self.widgets[i][j], '')
                    self.widgets[i][j].enabled(False)
        if self.visibleRows > len(self.data): # Need to blank the lower rows
            for i in range(len(self.data), self.visibleRows):
                for j in range(self.noColumns):
                    self.widgets[i][j].setText('') # Need to disable them too 
                    self.widgets[i][j].enabled(False)
                    self.widgets[i][j].configure(bg=DEFAULTBACKGROUND)

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
                # col = len(self.columns)
                # x = len(self.data) - self.visibleRows
                # self.vertical_scroll = TK.Scale(self.tableFrame, orient=TK.VERTICAL, from_=0, to=x, command=self.v_scroll, showvalue=0)
                # self.vertical_scroll.grid(row=1,column=col, rowspan=self.visibleRows, sticky=TK.N+TK.S)
                # print ('Setting vertical scroll')
                # # Try to add frame to remove black rectangle top right
                # self.topRight = TK.Frame(self.tableFrame)
                # self.topRight.grid(row=0,column=col, sticky=TK.NSEW)
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
        self.vertical_scroll = TK.Scale(self.tableFrame, orient=TK.VERTICAL, from_=0, to=x, command=self.v_scroll, showvalue=0)
        self.vertical_scroll.grid(row=1,column=col, rowspan=self.visibleRows, sticky=TK.N+TK.S)
        # Try to add frame to remove black rectangle top right
        self.topRight = TK.Frame(self.tableFrame)
        self.topRight.grid(row=0,column=col, sticky=TK.NSEW)

    def setScroll(self):
        # Reset the scroll bar
        self.vertical_scroll.configure(to=len(self.data) - self.visibleRows)

    def v_scroll(self, x):
        if self.scroll:
            self.topRow = int(x)
            self.populateCells()

    # ------------------------------------------------------------------------------------
    # Mousewheel control
    # ------------------------------------------------------------------------------------
    def _inTable(self,e):
        #print ('In Table')
        self.inTable = True

    def _leaveTable(self,e):
        #print ('Leave Table')
        self.inTable = False

    def _on_mousewheel(self, event):
        # <- Calls the table mousewheel function - scrolls the table and moves the scroll bar
        if self.inTable:
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


    def clicked(self, widget): # Overwrite this in parent module/class
        print ('Cell clicked (if row is -1, the column header was clicked')
        print (f'row={widget.tableRow} : column={widget.tableColumn}')
        print (widget.getText())
        print ('This function should be overwritten by the client function for handling click event')

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
# def Column(text, *args, **kwargs):
#     return {'text': text, 'width':10, 'widget': 'Label', 'bg':'white','fg':'black', **kwargs}

# def Cell(data='', **kwargs):
#     # Default values for background and foregraound colors - can be overwritten by kwargs
#     return {'data': data, 'bg':'white', 'fg':'black',  **kwargs}


# ------------------------------------------------------------------------------------
# Widgets defined for table usage
# ------------------------------------------------------------------------------------

class DefaultWidget(object):
    def setText(self, txt):
        self.config(text = txt)
    def getText(self):
        return self.get()
    def justifyText(self, txt):
        self.config(justify=txt)
    def enabled(self, b):
        s = 'disabled'
        if b: s = 'normal'
        self.config(state=s)
    def align(self, s):
        self.config(anchor=s)

class Label(TK.Label, DefaultWidget):
    def __init__(self, parent, **kwargs):
        TK.Label.__init__(self, parent)
    #def setText(self, txt):
    #    self.config(text = txt)
    def getText(self):
        return self.cget('text')

class Button(TK.Button, DefaultWidget):
    def __init__(self, parent, **kwargs):
        TK.Button.__init__(self, parent)
    def click(self, fnc):
        self.config(command=fnc)
    def getText(self):
        return 'Button Text'


class Textbox(TK.Entry, DefaultWidget):
    def __init__(self, parent, **kwargs):
        TK.Entry.__init__(self, parent)
    def setText(self, txt):
        self.delete(0, TK.END)
        self.insert(0, txt)
    def align(self, s):
        self.config(justify=s)

class Combobox(ttk.Combobox):  # , DefaultWidget):
    def __init__(self, parent, **kwargs):
        ttk.Combobox.__init__(self, parent)
        self.textSelection = TK.StringVar()
        self.config(textvariable = self.textSelection)
    def setOptions(self, options):
        #self['values'] = options
        self.configure(values=options)
    def setSelection(self, index):
        self.current(index)
    def setText(self, txt):
        self.textSelection.set(txt)
    def getText(self):
        return self.textSelection.get()
    def enabled(self, b):
        s = 'disabled'
        if b: s = 'normal'
        self.config(state=s)

class Checkbox(TK.Checkbutton):
    def __init__(self, parent, **kwargs):
        TK.Checkbutton.__init__(self, parent)
        self.var = TK.IntVar()
        self.config(variable=self.var)
    def setText(self, txt):
        if txt:
            self.select()
        else:
            self.deselect()
        #print ('Set text')
    def getText(self):
        #print ('Get Text')
        return self.var.get()    
    def enabled(self, b):
        s = 'disabled'
        if b: s = 'normal'
        self.config(state=s)