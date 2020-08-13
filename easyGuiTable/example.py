from easyguitable import table, create_column

# table(title, heading, columns, data, choices=['OK'], max_rows=15, widths=None)

title = 'Test table'
heading = 'Test Table Heading'
columns = [create_column('One'), create_column('Two'), create_column('Three', width=20), create_column('Four')]
columns = ['One', 'Two', 'Three', 'Four']
data = []
rows = 15 # Visible rows
# Examples of displaying status data
data.append(['Variables', 'Values'])
data.append(['Name', 'Paul'])
data.append(['Age', 'Old'])
data.append(['Hobby', 'Tennis'])
data.append(['Town List'])
towns = ['Rome','Helsinki', 'Manila', 'Cairo']
data.append(towns)


# Additional data
for r in range(rows):
    row = []
    for j, col in enumerate(columns):
        row.append('{}-{}'.format(r, j))
    data.append(row)
# choices is list of buttons
ans = table(title, heading, columns, data, choices=['Yes','No'], max_rows = 10, 
            widths={'One':40,'Two':20})
# Find which button was clicked
print ('Response: {}'.format(ans))