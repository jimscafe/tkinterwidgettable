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
        self.title = TK.Label(self.titleFrame, text='Title')
        self.title.pack()

        self.tableFrame = TK.Frame(self.frame)
        self.tableFrame.grid(row=1, column=0, padx=20, pady=20)
        self.tableTitle = TK.Label(self.tableFrame, text='Simple Table')
        self.tableTitle.pack()


        columns = [Column('One', align='left'),Column('Two'), Column('Three'),Column('Four')]
        self.table = MyTable(self.tableFrame, columns, rows=10)
        self.table.setData(sampleData.data1) 

        """
           or
           self.table = MyTable(self.tableFrame, columns, data=sample.data1) Rows calculated automatically
        """

    
        self.buttonFrame = TK.Frame(self.frame)
        self.buttonFrame.config(bg='light grey')
        self.buttonFrame.grid(row=2, column=0, pady=10, sticky=TK.NSEW)
        self.quitButton = TK.Button(self.buttonFrame, text='Quit', command=self.quit)
        self.quitButton.pack(pady=10, padx=20, anchor='e')

    def quit(self):
        self.parent.destroy()

if __name__ == "__main__":
    root = TK.Tk()
    main = Main(root)
    TK.mainloop()