#import libraries
import os
import tempfile
import tkinter
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import sqlite3
from PIL import Image, ImageTk

#function to define database
def Database():
    global conn, cursor
    #creating student database
    conn = sqlite3.connect("management.db")
    cursor = conn.cursor()
    #creating STUD_REGISTRATION table
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS REGISTRATION (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, CODE TEXT, DATE TEXT, DATE2 TEXT, MEC TEXT, CONTACT TEXT, PRICE TEXT, SERVICE TEXT)")

#defining function for creating GUI Layout
def DisplayForm():
    #creating window
    display_screen = Tk()
    #setting width and height for window
    display_screen.geometry("1350x715")
    #setting title for window
    display_screen.title("Jesse Leite Softwares                                                      https://relaxed-dijkstra-f2b25b.netlify.app")
    global tree
    global SEARCH
    global name,code,date,date2,mec,contact,price,service
    SEARCH = StringVar()
    name = StringVar()
    code = StringVar()
    date = StringVar()
    date2 = StringVar()
    mec = StringVar()
    contact = StringVar()
    price = StringVar()
    service = StringVar()

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
    lbl_text = Label(TopViewForm, text="Auto Center Oliveira", font=('verdana', 25), width=600,bg="#1C2833",fg="white")
    lbl_text.pack(fill=X)
    #creating registration form in first left frame
    Label(LFrom, text="Nome  ", font=("Arial", 13)).pack(side=TOP)
    Entry(LFrom,font=("Arial",10,"bold"),textvariable=name).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Placa(sem traço) ", font=("Arial", 13)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=code).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Data de Entrada ", font=("Arial", 13)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=date).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Data de Saída ", font=("Arial", 13)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=date2).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Mecânico ", font=("Arial", 13)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=mec).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Fone ", font=("Arial", 13)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=contact).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Preço(R$) ", font=("Arial", 13)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=price).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Serviço ", font=("Arial", 13)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=service).pack(side=TOP, padx=10, pady=10, fill=X)
    Button(LFrom,text="Salvar tarefa",font=("Arial", 12, "bold"),command=enter).pack(side=TOP, padx=10,pady=5, fill=X)
    Button(LFrom,text="Salvar",font=("Arial", 12, "bold"),command=register).pack(side=TOP, padx=10,pady=5, fill=X)
    Button(LFrom,text="Finalizar pedido",font=("Arial", 12, "bold"),command=reset).pack(side=TOP, padx=10,pady=5, fill=X)
    Label(LFrom, text="Pode-se inserir apenas placa,\ndatas e preço, após placa\nter sido cadastrada.\n\nDeve-se usar ponto,\n ao invés de vírgula.\nClique em 'Salvar Tarefa' e 'Salvar'.\npara salvar e para pular de linha\nna nota a ser impressa.", font=("Arial", 7)).pack(side=TOP)

    #creating search label and entry in second frame
    lbl_txtsearch = Label(LeftViewForm, text="Pesquise aqui", font=('verdana', 10),bg="gray")
    lbl_txtsearch.pack()
    #creating search entry
    search = Entry(LeftViewForm, textvariable=SEARCH, font=('verdana', 15), width=10)
    search.pack(side=TOP, padx=10, fill=X)
    #creating search button
    btn_search = Button(LeftViewForm, text="Pesquisar\nPLACA", command=SearchRecord)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    #creating search button
    btn_search = Button(LeftViewForm, text="Pesquisar\nNÚMERO", command=SearchRecord2)
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
    tree = ttk.Treeview(MidViewForm,columns=("Id", "Nome", "Placa","Data de Entrada","Data de Saída","Mecânico","Fone", "Preço(R$)", "Serviço"),
                        selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    #setting headings for the columns
    tree.heading('Id', text="Número de Pedido", anchor=W)
    tree.heading('Nome', text="Nome", anchor=W)
    tree.heading('Placa', text="Placa", anchor=W)
    tree.heading('Data de Entrada', text="Data de Entrada", anchor=W)
    tree.heading('Data de Saída', text="Data de Saída", anchor=W)
    tree.heading('Mecânico', text="Mecânico", anchor=W)
    tree.heading('Fone', text="Fone", anchor=W)
    tree.heading('Preço(R$)', text="Preço(R$)", anchor=W)
    tree.heading('Serviço', text="Serviço", anchor=W)
    #setting width of the columns
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=200)
    tree.column('#2', stretch=NO, minwidth=0, width=70)
    tree.column('#3', stretch=NO, minwidth=0, width=80)
    tree.column('#4', stretch=NO, minwidth=0, width=80)
    tree.column('#5', stretch=NO, minwidth=0, width=70)
    tree.column('#6', stretch=NO, minwidth=0, width=70)
    tree.column('#7', stretch=NO, minwidth=0, width=70)
    tree.pack()
    DisplayData()

#IMAGE
    image0 = Image.open("AO.png")
    image1 = image0.resize((43, 43), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(image1)
    label1 = tkinter.Label(image=test)
    label1.image = test
    label1.place(x=275, y=0.45)

global s01
s01=['']
#function to insert data into database
def enter():
    global s1
    stxt=service.get()
    s0=stxt.split()
    s01.append(s0)
    s1=str(s01)+'\n'
def register():
    s2=s1.translate({ord(i): None for i in "["})
    s3=s2.translate({ord(i): None for i in "]"})
    s4=s3.translate({ord(i): None for i in ","})
    services=s4
    Database()
    #getting form data
    name1=name.get()
    code1=code.get()
    date1=date.get()
    date21=date2.get()
    mec1=mec.get()
    contact1=contact.get()
    price1=price.get()
    service1=services
    #execute query
    conn.execute('''INSERT INTO REGISTRATION (NAME,CODE,DATE,DATE2,MEC,CONTACT,PRICE, SERVICE)
    VALUES (?,?,?,?,?,?,?,?)''',(name1,code1.upper(),date1,date21,mec1,contact1,price1,service1))
    conn.commit()
    tkMessageBox.showinfo("Messagem","Salva com sucesso")
    #refresh table data
    DisplayData()
    conn.close()
def reset():
    l=len(s01)
    del s01[0:l]
def Print():
        #open database
    Database()
    if not tree.selection():
        tkMessageBox.showwarning("Aviso","Selecione a linha a ser impressa")
    else:
        result = tkMessageBox.askquestion('Confirmar', 'Você quer imprimir este pedido?',
                                          icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)

            cursor=conn.execute("SELECT ID FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            ct1=str(fetch).translate({ord(i): '\n' for i in "'"})
            ct2=ct1.translate({ord(i): None for i in "["})
            ct3=ct2.translate({ord(i): None for i in "]"})
            ct4=ct3.translate({ord(i): None for i in "("})
            ct5=ct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT NAME FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            bct1=str(fetch).translate({ord(i): '\n' for i in "'"})
            bct2=bct1.translate({ord(i): None for i in "["})
            bct3=bct2.translate({ord(i): None for i in "]"})
            bct4=bct3.translate({ord(i): None for i in "("})
            dct5=bct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT CODE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            cct1=str(fetch).translate({ord(i): '\n' for i in "'"})
            cct2=cct1.translate({ord(i): None for i in "["})
            cct3=cct2.translate({ord(i): None for i in "]"})
            cct4=cct3.translate({ord(i): None for i in "("})
            ect5=cct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT DATE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            dct1=str(fetch).translate({ord(i): '\n' for i in "'"})
            dct2=dct1.translate({ord(i): None for i in "["})
            dct3=dct2.translate({ord(i): None for i in "]"})
            dct4=dct3.translate({ord(i): None for i in "("})
            fct5=dct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT DATE2 FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            dct12=str(fetch).translate({ord(i): '\n' for i in "'"})
            dct22=dct12.translate({ord(i): None for i in "["})
            dct32=dct22.translate({ord(i): None for i in "]"})
            dct42=dct32.translate({ord(i): None for i in "("})
            fct52=dct42.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT MEC FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            mdct1=str(fetch).translate({ord(i): '\n' for i in "'"})
            mdct2=mdct1.translate({ord(i): None for i in "["})
            mdct3=mdct2.translate({ord(i): None for i in "]"})
            mdct4=mdct3.translate({ord(i): None for i in "("})
            mfct5=mdct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT CONTACT FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            ect1=str(fetch).translate({ord(i): '\n' for i in "'"})
            ect2=ect1.translate({ord(i): None for i in "["})
            ect3=ect2.translate({ord(i): None for i in "]"})
            ect4=ect3.translate({ord(i): None for i in "("})
            gct5=ect4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT PRICE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            fct1=str(fetch).translate({ord(i): '\n' for i in "'"})
            fct2=fct1.translate({ord(i): None for i in "["})
            fct3=fct2.translate({ord(i): None for i in "]"})
            fct4=fct3.translate({ord(i): None for i in "("})
            hct5=fct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT SERVICE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            gct1=str(fetch).translate({ord(i): '\n' for i in "'"})
            gct2=gct1.translate({ord(i): None for i in "["})
            gct3=gct2.translate({ord(i): None for i in "]"})
            gct4=gct3.translate({ord(i): None for i in "("})
            ict5=gct4.translate({ord(i): None for i in ")"})

            a1='Número de ordem: '+ct5
            a2='Nome: '+dct5
            a3='Placa: '+ect5
            a4='Data de Entrada: '+fct5
            a42='Data de Saída: '+fct52
            a43='Mecânico: '+mfct5
            a5='Fone: '+gct5
            a6='Preço: '+hct5
            a7='Serviço: '+ict5
            content0=a1+a2+a3+a4+a42+a43+a5+a7+a6
            content=content0.translate({ord(i): '\n' for i in ","})
            cursor.close()
            conn.close()
    #PRINT
    global q
    q='------------------------------------------------------------------\nAUTO CENTER OLIVEIRA\n------------------------------------------------------------------\n\nOrdem de Serviço\n------------------------------------------------------------------\n'+content+'\n------------------------------------------------------------------'
    filename=tempfile.mktemp(".txt")
    open (filename, "w"). write(q)
    os.startfile(filename, "print")
def Delete():
    #open database
    Database()
    if not tree.selection():
        tkMessageBox.showwarning("Aviso","Selecione a linha a ser apagada")
    else:
        result = tkMessageBox.askquestion('Confirmar', 'Você quer apagar este pedido?',
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
        cursor=conn.execute("SELECT * FROM REGISTRATION WHERE CODE LIKE ?", ('%' + str(SEARCH.get().upper()) + '%',))
        #fetch all matching records
        fetch = cursor.fetchall()
        #loop for displaying all records into GUI
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
#function to search data
def SearchRecord2():
    #open database
    Database()
    #checking search text is empty or not
    if SEARCH.get() != "":
        #clearing current display data
        tree.delete(*tree.get_children())
        #select query with where clause
        cursor=conn.execute("SELECT * FROM REGISTRATION WHERE ID LIKE ?", ('%' + str(SEARCH.get().upper()) + '%',))
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
