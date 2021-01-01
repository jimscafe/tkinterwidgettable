# tkinterwidgettable
Jan 1 2021
The table without frames has been developed and used, though I am not convinced that omitting frames has changed the display speed significantly. Using frames allows a more precise setting of cell dimensions using pixels.

I have not, as yet, kept this project up-to-date on github, if there is interest in using the table then I will do so. I do use the table a lot in my applications, it is easy to implement for simple jobs and can handle quite complex requirements.

Horizontal scrolling has been used, though currently the code for this is currently held in the calling module rather than as part of the table class This scrolling only works in a simple way, there is no attempt to change the cell types or the cell widths when moving data horizontally.

When an application using a table was run onan macBook, the change in font size that the Apple operating system uses resulted in the application being far too large. Changing the default font (for most widgets) corrects this. Using pixels to size the cells might negate this possibility or make the text too large for the cell so non-frame tables are perhaps best for use in this way (i.e. applications designed to run on Linux, windows and mac). I have done no further testing of this problem.


Update Aug 21 2020
In order to make the cells have heights and widths specified in pixels, each cell widget
has a frame around it. This might be causing slow rendering of the application.
If no frame, then widgets sizes will refer to the widget width (and height) which depends 
upon the font I understand. More difficult to lign up the widgets - will test this further


The initial design included a dictionary for every data item - in this way individual items
can be processed separate from the others in the same column or row.

The current version does not do this and any individual processing or formatting can be
applied when the parent application processes the drawing of each table cell using a 
callback.

The SampleDataEditCell.py illustrates all the table features.

Simpler examples can be seen in the examples directory.

There are options to provide a callback function for each mouse click, for changed data
and for drawing each table cell. 

Columns in the table can be Labels (default), Entry widget (Textbox), Button, Combobox
and Checkbox.

The column header can be clicked which allows for the parent application to carry out
sorting of data etc.

The table is intended to be a quick way of displaying tabular data (no callbacks required)
or a more complex data processing requirements.

Still to do is filtering.

The table should be quite felixible and able to handle large data - perhaps in a
database.

For examples see the examples folder and look at all the py files beginning with the text Simple (simple)


Perhaps the widgets.py file code should be placed in the table.py file to avoid the table
requiring any imports
