import tkinter as TK

from table import MyTable, Column
import sampleData

class Main():
    def __init__(self, parent):
        self.parent = parent
        self.frame = TK.Frame(self.parent)
        self.parent.protocol("WM_DELETE_WINDOW", self.quit)
        self.frame.pack()
        self.titleFrame = TK.Frame(self.frame)
        self.titleFrame.grid(row=0, column=0, pady=10)
        self.title = TK.Label(self.titleFrame, text='Data Filtering Example (Name field)')
        self.title.pack()

        self.tableFrame = TK.Frame(self.frame)
        self.tableFrame.grid(row=1, column=0, padx=20, pady=20)
        self.tableTitle = TK.Label(self.tableFrame, text='Simple Table')
        self.tableTitle.pack()

        columns = [Column('ID'),Column('Name'), Column('Age'),Column('Gender')]
        self.table = MyTable(self.tableFrame, columns, rows=10)
        self.table.setData(sampleData.data2) 

        self.buttonFrame = TK.Frame(self.frame)
        self.buttonFrame.config(bg='light grey')
        self.buttonFrame.grid(row=2, column=0, pady=10, sticky=TK.NSEW)
        self.filterLabel = TK.Label(self.buttonFrame, text = 'Filter:')
        self.filterLabel.pack(pady=10, padx=20, side=TK.LEFT)
        self.entryText = TK.StringVar()
        self.filterText = TK.Entry(self.buttonFrame, textvariable=self.entryText)
        self.filterText.pack(pady=10, padx=0, side=TK.LEFT) # anchor='w')
        self.filterText.bind("<KeyRelease>", self.print_key) 
        self.quitButton = TK.Button(self.buttonFrame, text='Quit', command=self.quit)
        self.quitButton.pack(pady=10, padx=20, side=TK.RIGHT) # anchor='e')

    def print_key(self, event): 
        args = event.keysym, event.keycode, event.char
        if ('Shift' in event.keysym) or ('Control' in event.keysym):
            pass
        else: 
            print("Symbol: {}, Code: {}, Char: {}".format(*args))
            print (self.entryText.get())
            txt = self.entryText.get()
            if txt: # Text in filter entry widget
                filterData = []
                for row in sampleData.data2:
                    if txt in row[1]: # Name column
                        filterData.append(row)
                self.table.setData(filterData)
            else: # Reset entire data
                self.table.setData(sampleData.data2) 


    def quit(self):
        self.parent.destroy()

if __name__ == "__main__":
    root = TK.Tk()
    main = Main(root)
    TK.mainloop()