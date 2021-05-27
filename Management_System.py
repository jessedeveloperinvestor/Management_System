#import libraries
import os
import tempfile
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import sqlite3

#function to define database
def Database():
    global conn, cursor
    #creating student database
    conn = sqlite3.connect("management.db")
    cursor = conn.cursor()
    #creating STUD_REGISTRATION table
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS REGISTRATION (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, CODE TEXT, DATE TEXT, CONTACT TEXT, PRICE TEXT)")

#defining function for creating GUI Layout
def DisplayForm():
    #creating window
    display_screen = Tk()
    #setting width and height for window
    display_screen.geometry("1200x600")
    #setting title for window
    display_screen.title("Jesse Softwares                                                             https://relaxed-dijkstra-f2b25b.netlify.app")
    global tree
    global SEARCH
    global name,code,date,contact,price
    SEARCH = StringVar()
    name = StringVar()
    code = StringVar()
    date = StringVar()
    contact = StringVar()
    price = StringVar()
    #creating frames for layout
    #topview frame for heading
    TopViewForm = Frame(display_screen, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    #first left frame for registration from
    LFrom = Frame(display_screen, width="350")
    LFrom.pack(side=LEFT, fill=Y)
    #seconf left frame for search form
    LeftViewForm = Frame(display_screen, width=500,bg="gray")
    LeftViewForm.pack(side=LEFT, fill=Y)
    #mid frame for displaying students record
    MidViewForm = Frame(display_screen, width=600)
    MidViewForm.pack(side=RIGHT)
    #label for heading
    lbl_text = Label(TopViewForm, text="Rubens Amexeira", font=('verdana', 18), width=600,bg="#1C2833",fg="white")
    lbl_text.pack(fill=X)
    #creating registration form in first left frame
    Label(LFrom, text="Nome  ", font=("Arial", 12)).pack(side=TOP)
    Entry(LFrom,font=("Arial",10,"bold"),textvariable=name).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Placa ", font=("Arial", 12)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=code).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Data ", font=("Arial", 12)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=date).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Fone ", font=("Arial", 12)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=contact).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Preço(R$) ", font=("Arial", 12)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=price).pack(side=TOP, padx=10, fill=X)
    Button(LFrom,text="Salvar",font=("Arial", 10, "bold"),command=register).pack(side=TOP, padx=10,pady=5, fill=X)

    #creating search label and entry in second frame
    lbl_txtsearch = Label(LeftViewForm, text="Insira o nome para pesquisar", font=('verdana', 10),bg="gray")
    lbl_txtsearch.pack()
    #creating search entry
    search = Entry(LeftViewForm, textvariable=SEARCH, font=('verdana', 15), width=10)
    search.pack(side=TOP, padx=10, fill=X)
    #creating search button
    btn_search = Button(LeftViewForm, text="Pesquisar", command=SearchRecord)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    #creating view button
    btn_view = Button(LeftViewForm, text="Ver tudo", command=DisplayData)
    btn_view.pack(side=TOP, padx=10, pady=10, fill=X)
    #creating reset button
    btn_reset = Button(LeftViewForm, text="Imprimir", command=Print)
    btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
    #creating delete button
    btn_delete = Button(LeftViewForm, text="Apagar", command=Delete)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
   #setting scrollbar
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm,columns=("Id", "Nome", "Placa","Data","Fone", "Preço(R$)"),
                        selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    #setting headings for the columns
    tree.heading('Id', text="Id", anchor=W)
    tree.heading('Nome', text="Nome", anchor=W)
    tree.heading('Placa', text="Placa", anchor=W)
    tree.heading('Data', text="Data", anchor=W)
    tree.heading('Fone', text="Fone", anchor=W)
    tree.heading('Preço(R$)', text="Preço(R$)", anchor=W)
    #setting width of the columns
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=100)
    tree.column('#2', stretch=NO, minwidth=0, width=150)
    tree.column('#3', stretch=NO, minwidth=0, width=80)
    tree.column('#4', stretch=NO, minwidth=0, width=120)
    tree.pack()
    DisplayData()
#function to insert data into database
def register():
    Database()
    #getting form data
    name1=name.get()
    code1=code.get()
    date1=date.get()
    contact1=contact.get()
    price1=price.get()
    #applying empty validation
    if name1=='' or code1=='' or date1==''or contact1=='' or price1=='':
        x=0
        # tkMessageBox.showinfo("Aviso","Preencha o campo vazio!!!")
    else:
        #execute query
        conn.execute('INSERT INTO REGISTRATION (NAME,CODE,DATE,CONTACT,PRICE) \
              VALUES (?,?,?,?,?)',(name1,code1,date1,contact1,price1));
        conn.commit()
        tkMessageBox.showinfo("Messagem","Salva com sucesso")
        #refresh table data
        DisplayData()
        conn.close()
def Print():
        #open database
    Database()
    if not tree.selection():
        tkMessageBox.showwarning("Aviso","Selecione a linha a ser impressa")
    else:
        result = tkMessageBox.askquestion('Confirm', 'Are you sure you want to delete this record?',
                                          icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            cursor=conn.execute("SELECT * FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            cursor.close()
            conn.close()
        #PRINT
    q=str(fetch)
    filename=tempfile.mktemp(".txt")
    open (filename, "w"). write(q)
    os.startfile(filename, "print")
def Delete():
    #open database
    Database()
    if not tree.selection():
        tkMessageBox.showwarning("Aviso","Selecione a linha a ser apagada")
    else:
        result = tkMessageBox.askquestion('Confirm', 'Are you sure you want to delete this record?',
                                          icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            cursor=conn.execute("DELETE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()

#function to search data
def SearchRecord():
    #open database
    Database()
    #checking search text is empty or not
    if SEARCH.get() != "":
        #clearing current display data
        tree.delete(*tree.get_children())
        #select query with where clause
        cursor=conn.execute("SELECT * FROM REGISTRATION WHERE CODE LIKE ?", ('%' + str(SEARCH.get()) + '%',))
        #fetch all matching records
        fetch = cursor.fetchall()
        #loop for displaying all records into GUI
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
#defining function to access data from SQLite database
def DisplayData():
    #open database
    Database()
    #clear current data
    tree.delete(*tree.get_children())
    #select query
    cursor=conn.execute("SELECT * FROM REGISTRATION")
    #fetch all data from database
    fetch = cursor.fetchall()
    #loop for displaying all data in GUI
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

#calling function
DisplayForm()
if __name__=='__main__':
#Running Application
 mainloop()
