# tkinterwidgettable
Tkinter table with each cell a widget, vertical scrolling only
Version 1 shows the basic principle and can be used for simple
presentation of table data

* Version 1 (_v1) - simple table with scroling
* Version 2 (_v2) - click event, mousewheel scrolling
* Version 3 (_v3) - Individual cell formatting via callback to parent module/class
* Version 4 (_v4) - Allow different widgets, check box, combo box, button
* Version 5 (_v5) - Use entry widget for some columns, allow cell editing in those columns
* Version 5a(_v5a)- Embed most of the code in the table class, not the client
* Version 6 (_v6)  = Filter the data

Currently the cells are wrapped in a frame to allow the cell dimensions to be set in pixels rather than characters.
The widgets are inherited into classes (widgets.py) to allow similar command to get and update their content (e.g. widget.setText('123')  widget.getText())
There is padding around the cells to allow the background color from the parent frame to give grid
lines around the cells. This can be easily modified as required. Later might set the as possible parameters
Horizontal scrolling is not implemented due to using widgets. Not sure if this will be added later.
Cell formatting can be set in a callback function to allow complete formatting of the cell. For
example negative numbers with a red background, text alignment in different columns etc.

Cell Formatting

a)It is possible to decouple the data from the table completely and have a callback prosess each widget
as the cell is populated. The client would keep all the necessary data and formatting parameters.
The scrolling parameters would require setting rather than use len(self.data) - which is currently
the way it is done. If filtering is done, there would need to be an original matrix of data 
and a currently displayed matrix.

b)Alternatively the table.data matrix could contain only text while a 'mirror' matrix in the parent client or even in the table object could contain all the logic to populate and format the cell. If
the logic matrix is not supplied, one could be automatically created

c)Finally the data matrix stored in the table could be a complex object containing all the necessary
information for populating and formatting each cell. (e.g. Cell class/object)

d)How do any of these fit with the data being in a database and not all available at the time the 
table is drawn (very large data)

e) How does using combobox or check box affect options a-c?

f) Should the cell formatting be done in the table or the client logic?

Trying to avoid the more complicated implementation used by some other graphic libraries.

Although in Version 4, widgets can be placed in the table, the effects of using those
widgets is not passed to the data, either in the table or external to the table. Any
data entry or changes would have to be implemented through the click event generated
and this would not work for the Entry widget (no click event to end the data entry)
