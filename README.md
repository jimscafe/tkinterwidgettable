# tkinterwidgettable

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
