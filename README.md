# tkinterwidgettable
Tkinter table with each cell a widget, vertical scrolling only
Version 1 shows the basic principle and can be used for simple
presentation of table data

* Version 1 (_v1) - simple table with scroling
* Version 2 (_v2) - click event, mousewheel scrolling
* Version 3 (_v3) - Individual cell formatting via callback to parent module/class
* Version 4 (_v4) - Use entry widget for some columns, allow cell editing in those columns
* Version 5 (_v5) - Allow different widgets, check box, combo box, button

Currently the cells are wrapped in a frame to allow the cell dimensions to be set in pixels rather than characters.
The widgets are inherited into classes (widgets.py) to allow similar command to get and update their content (e.g. widget.setText('123')  widget.getText())
There is padding around the cells to allow the background color from the parent frame to give grid
lines around the cells. This can be easily modified as required. Later might set the as possible parameters
Horizontal scrolling is not implemented due to using widgets. Not sure if this will be added later.
Cell formatting can be set in a callback function to allow complete formatting of the cell. For
example negative numbers with a red background, text alignment in different columns etc.




