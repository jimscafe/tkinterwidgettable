# Data used to demonstrate the various table modes

# Simple data matrix - all strings
data1 = [
    ['001','Geoff', '35', 'Male'],
    ['002','Jane', '32', 'Female'],
    ['003','Michael', '36', 'Male'],
    ['004','Rubin', '37', 'Male'],
    ['005','Gary', '38', 'Male'],
    ['006','Graham', '39', 'Male'],
    ['007','Nicholas', '15', 'Male'],
    ['008','Bertrand', '31', 'Male'],
    ['009','Joel', '32', 'Male'],
    ['010','Lionel', '33', 'Male']
]

data2 = data1
data2.append(['011','Paris', 35, 'Male'])
data2.append(['012','Saint', 35, 'Male'])
data2.append(['013','Regan', 35, 'Male'])
data2.append(['014','Alan', 35, 'Male'])

data3 = data2
for i,row in enumerate(data2):
    if i < 8:
        row.append(1)
        
    else:
        row.append(0)
    row.append('X') # The button cell