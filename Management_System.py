#import libraries
#pip install pandas
#pip install pillow
#pip install tkinter
#pip install openpyxl
#pip install reportlab
import os
import tempfile
import tkinter
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import sqlite3
from PIL import Image, ImageTk
import time
from datetime import timedelta, date
import openpyxl
#libraries to create the pdf file and add text to it
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont

global company_brand
company_brand="Auto Center Oliveira"

#SETTING UP PRINTING DESIGN
#convert the font so it is compatible
pdfmetrics.registerFont(TTFont('Arial','Arial.ttf'))
#import company's logo
im = Image.open('AO.png')
width, height = im.size
ratio = width/height
image_width = 400
image_height = int(image_width / ratio)
#Page information
page_width = 2156
page_height = 3050
#Invoice variables
company_name ='Auto Center Oliveira'
payment_terms = 'x'
contact_info = 'x'
margin = 100
month_year = 'February 2022'

#function to define database
def Database():
    global conn, cursor
    #creating student database
    conn = sqlite3.connect("management.db")
    cursor = conn.cursor()
    #creating STUD_REGISTRATION table
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS REGISTRATION (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, CODE TEXT, DATE TEXT, DATE2 TEXT, MEC TEXT, CONTACT TEXT, PRICE TEXT, SERVICE TEXT)")

#ALTER TABLE, THEN COMMENT THESE COMMANDS:
    try:
        filep='sum.txt'
        with open(filep, 'a') as file_objectp:
            file_objectp.write('')
    except:
        cursor.execute('''ALTER TABLE REGISTRATION ADD COLUMN TRANSACTIONS TEXT''')
        cursor.execute('''ALTER TABLE REGISTRATION ADD COLUMN PAIDWHERE TEXT''')
        file = open("sum.txt", "w") 
        file.write("1") 
        file.close()

#defining function for creating GUI Layout
def DisplayForm():
    #creating window
    display_screen = Tk()
    #setting width and height for window
    display_screen.geometry("1350x715")
    #setting title for window
    display_screen.title("Jesse Leite Softwares                                                      https://jesse-leite-softwares.onrender.com")
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
    global transactions
    transactions = StringVar()
    global paidwhere
    paidwhere = StringVar()

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
    lbl_text = Label(TopViewForm, text=company_brand, font=('verdana', 25), width=600,bg="#1C2833",fg="white")
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
    Label(LFrom, text="Tipo de Transação ", font=("Arial", 13)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=transactions).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Pago Onde ", font=("Arial", 13)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=paidwhere).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Preço Total\na atualizar", font=("Arial", 13)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=price).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Tarefa a\nadicionar", font=("Arial", 13)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=service).pack(side=TOP, padx=10, pady=10, fill=X)
    Label(LFrom, text="Pode-se inserir apenas placa,\ndatas e preço, após placa\nter sido cadastrada.\nDeve-se usar ponto,\n ao invés de vírgula.Pode-se atualizar\npreço e adiconar serviços, para tal clique\nem 'Atualizar'.\nClique em 'ADICIONAR TAREFAS E PRODUTOS' para\nsalvar serviços/produtos\nEm Tipo de Transações, pode-se pôr: Débito, crédito, Dinheiro etc\nEm Pago Onde, pode-se pôr: Oficina, Autopeças etc .", font=("Arial", 7)).pack(side=TOP)

    #creating search label and entry in second frame
    lbl_txtsearch = Label(LeftViewForm, text="Pesquise aqui", font=('verdana', 10),bg="gray")
    lbl_txtsearch.pack()
    #creating search entry
    search = Entry(LeftViewForm, textvariable=SEARCH, font=('verdana', 15), width=10)
    search.pack(side=TOP, padx=10, fill=X)
    #creating search button
    btn_search = Button(LeftViewForm, text="Pesquisar\nPLACA", command=SearchRecord)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    #creating search customer button
    btn_search = Button(LeftViewForm, text="CLIENTE\nUsar Dados", command=SearchCustomer)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    #creating search button
    btn_search2 = Button(LeftViewForm, text="Pesquisar\nNÚMERO", command=SearchRecord2)
    btn_search2.pack(side=TOP, padx=10, pady=10, fill=X)
    #creating view button
    btn_view = Button(LeftViewForm, text="Ver tudo", command=DisplayData)
    btn_view.pack(side=TOP, padx=10, pady=10, fill=X)
    #creating printing button
    btn_print = Button(LeftViewForm, text="Imprimir", command=Print)
    btn_print.pack(side=TOP, padx=10, pady=10, fill=X)
    #creating printing button
    btn_print = Button(LeftViewForm, text="Imprimir Design", command=PrintDesign)
    btn_print.pack(side=TOP, padx=10, pady=10, fill=X)
    #creating delete button
    btn_delete = Button(LeftViewForm, text="Apagar", command=Delete)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
    #creating update button
    btn_update = Button(LeftViewForm, text="Atualizar", command=Update)
    btn_update.pack(side=TOP, padx=10, pady=10, fill=X)

    #creating input_screen button
    btn_inputs = Button(LeftViewForm, text="ADICIONAR\nTAREFAS E/OU\nPRODUTOS", command=input_screenForm)
    btn_inputs.pack(side=TOP, padx=10, pady=10, fill=X)
    #creating read_screen button
    btn_read = Button(LeftViewForm, text="Ver Ordem\nde Serviços", command=read_screenForm)
    btn_read.pack(side=TOP, padx=10, pady=10, fill=X)
    #creating report_screen button
    btn_read = Button(LeftViewForm, text="Relatório", command=report_screenForm)
    btn_read.pack(side=TOP, padx=10, pady=10, fill=X)

   #setting scrollbar
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm,columns=("Id", "Nome", "Placa","Data de Entrada","Data de Saída","Mecânico","Fone", "Preço Total(R$)", "Serviço","Tipo de Transação","Pago Onde"),
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
    tree.heading('Preço Total(R$)', text="Preço Total(R$)", anchor=W)
    tree.heading('Serviço', text="Serviço", anchor=W)
    tree.heading('Tipo de Transação', text="Tipo de Transação", anchor=W)
    tree.heading('Pago Onde', text="Pago Onde", anchor=W)
    #setting width of the columns
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=200)
    tree.column('#2', stretch=NO, minwidth=0, width=60)
    tree.column('#3', stretch=NO, minwidth=0, width=50)
    tree.column('#4', stretch=NO, minwidth=0, width=45)
    tree.column('#5', stretch=NO, minwidth=0, width=45)
    tree.column('#6', stretch=NO, minwidth=0, width=40)
    tree.column('#7', stretch=NO, minwidth=0, width=75)
    tree.column('#8', stretch=NO, minwidth=0, width=40)
    tree.column('#9', stretch=NO, minwidth=0, width=80)
    tree.pack()
    DisplayData()

    #IMAGE
    if company_brand=='Auto Center Oliveira':
        image0 = Image.open("AO.png")
        image1 = image0.resize((43, 43), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image1)
        label1 = tkinter.Label(image=test)
        label1.image = test
        label1.place(x=275, y=0.45)

def SearchCustomer():
#open database
    Database()
    if not tree.selection():
        tkMessageBox.showwarning("Aviso","Selecione uma linha com a placa e dados do cliente")
    else:
        result = tkMessageBox.askquestion('Confirmar', 'Você quer usar estes dados de cliente?',
                                          icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)

            cursor=conn.execute("SELECT NAME FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            bct1=str(fetch).translate({ord(i): None for i in "'"})
            bct2=bct1.translate({ord(i): None for i in "["})
            bct3=bct2.translate({ord(i): None for i in "]"})
            bct4=bct3.translate({ord(i): None for i in "("})
            dct5=bct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT CODE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            cct1=str(fetch).translate({ord(i): None for i in "'"})
            cct2=cct1.translate({ord(i): None for i in "["})
            cct3=cct2.translate({ord(i): None for i in "]"})
            cct4=cct3.translate({ord(i): None for i in "("})
            ect5=cct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT CONTACT FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            ect1=str(fetch).translate({ord(i): None for i in "'"})
            ect2=ect1.translate({ord(i): None for i in "["})
            ect3=ect2.translate({ord(i): None for i in "]"})
            ect4=ect3.translate({ord(i): None for i in "("})
            gct5=ect4.translate({ord(i): None for i in ")"})

            a2=dct5 #name
            a3=ect5 #code
            a5=gct5 #phone
            global customerdata
            content0 = a2 + a3 + a5
            content1=content0.translate({ord(i): '>' for i in ","})
            content=content1.translate({ord(i): '' for i in "'"})
            customerdata = {}
            customerdata = content.split(">")
            print(customerdata)
            global namecopied, codecopied, contactcopied
            namecopied=str(customerdata[0])
            codecopied=str(customerdata[1])
            contactcopied=str(customerdata[2])
        cursor.close()
        conn.close()

global s01
s01=['']
#function to insert data into database
def input_screenForm():
    import tkinter as tk
    import tkinter.ttk as ttk
    global tasks, tasks_prices
    tasks=[]
    tasks_prices=[]
 
    class Application(tk.Frame):
        def __init__(self, root):
            self.root = root
            self.initialize_user_interface()
     
        def initialize_user_interface(self):
            # Configure the root object for the Application
            self.root.title("SERVIÇO(S)")
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            self.root.config(background="black")
     
            # Define the different GUI widgets
            self.name_label = tk.Label(self.root, text="TAREFA:")
            self.entry1 = tk.Entry(self.root)
            self.name_label.grid(row=0, column=0, sticky=tk.W)
            self.entry1.grid(row=0, column=1)
     
            self.idnumber_label = tk.Label(self.root, text="PREÇO(R$)")
            self.entry2 = tk.Entry(self.root)
            self.idnumber_label.grid(row=1, column=0, sticky=tk.W)
            self.entry2.grid(row=1, column=1)
     
            self.submit_button = tk.Button(self.root, text="Inserir", command=self.insert_data)
            self.submit_button.grid(row=2, column=1, sticky=tk.W)
     
            self.exit_button = tk.Button(self.root, text="SALVAR\nTAREFAS", command=input_screen2Form)
            self.exit_button.grid(row=0, column=3)
     
            # Set the treeview
            self.tree = ttk.Treeview(self.root, columns=('Tarefa', 'Preço'))
     
            # Set the heading (Attribute Names)
            self.tree.heading('#0', text='Id')
            self.tree.heading('#1', text='Tarefa')
            self.tree.heading('#2', text='Preço')
     
            # Specify attributes of the columns (We want to stretch it!)
            self.tree.column('#0', stretch=tk.YES)
            self.tree.column('#1', stretch=tk.YES)
            self.tree.column('#2', stretch=tk.YES)
     
            self.tree.grid(row=4, columnspan=4, sticky='nsew')
            self.treeview = self.tree
     
            self.id = 0
            self.iid = 0
     
        def insert_data(self):
            self.treeview.insert('', 'end', iid=self.iid, text=str(self.id),
                                 values=(self.entry1.get(),
                                         self.entry2.get()))
            self.iid = self.iid + 1
            self.id = self.id + 1
            tasks.append(self.entry1.get()+'|')
            tasks_prices.append(float(self.entry2.get()))
    app = Application(tk.Tk())
    app.root.mainloop()

def input_screen2Form():
    import tkinter as tk
    import tkinter.ttk as ttk
    global products_amounts, products, products_prices
    products_amounts=[]
    products=[]
    products_prices=[]
 
    class Application(tk.Frame):
        def __init__(self, root):
            self.root = root
            self.initialize_user_interface()
     
        def initialize_user_interface(self):
            # Configure the root object for the Application
            self.root.title("PRODUTO(S)")
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            self.root.config(background="black")
     
            # Define the different GUI widgets
            self.name_label = tk.Label(self.root, text="QUANTIDADE:")
            self.entry1 = tk.Entry(self.root)
            self.name_label.grid(row=0, column=0, sticky=tk.W)
            self.entry1.grid(row=0, column=1)

            self.name_label = tk.Label(self.root, text="PRODUTO:")
            self.entry2 = tk.Entry(self.root)
            self.name_label.grid(row=1, column=0, sticky=tk.W)
            self.entry2.grid(row=1, column=1)
     
            self.idnumber_label = tk.Label(self.root, text="PREÇO(R$)")
            self.entry3 = tk.Entry(self.root)
            self.idnumber_label.grid(row=2, column=0, sticky=tk.W)
            self.entry3.grid(row=2, column=1)
     
            self.submit_button = tk.Button(self.root, text="Inserir", command=self.insert_data)
            self.submit_button.grid(row=3, column=1, sticky=tk.W)
     
            self.exit_button = tk.Button(self.root, text="SALVAR\nTUDO", command=save_tasks)
            self.exit_button.grid(row=0, column=3)
     
            # Set the treeview
            self.tree = ttk.Treeview(self.root, columns=('Quantidade','Produto', 'Preço'))
     
            # Set the heading (Attribute Names)
            self.tree.heading('#0', text='Id')
            self.tree.heading('#1', text='Quantidade')
            self.tree.heading('#2', text='Produto')
            self.tree.heading('#3', text='Preço')
     
            # Specify attributes of the columns (We want to stretch it!)
            self.tree.column('#0', stretch=tk.YES)
            self.tree.column('#1', stretch=tk.YES)
            self.tree.column('#2', stretch=tk.YES)
            self.tree.column('#3', stretch=tk.YES)
     
            self.tree.grid(row=4, columnspan=4, sticky='nsew')
            self.treeview = self.tree
     
            self.id = 0
            self.iid = 0
     
        def insert_data(self):
            self.treeview.insert('', 'end', iid=self.iid, text=str(self.id),
                                 values=(self.entry1.get(),
                                         self.entry2.get(),
                                         self.entry3.get()))
            self.iid = self.iid + 1
            self.id = self.id + 1
            products_amounts.append(float(self.entry1.get()))
            products.append(self.entry2.get()+'|')
            products_prices.append(float(self.entry3.get()))
    app = Application(tk.Tk())
    app.root.mainloop()

def save_tasks():
    total_price_sum=0
    try:
        for g in range(len(products_prices)):
           products_prices[g] = products_prices[g] * products_amounts[g]
        total_price_sum = sum(tasks_prices)+sum(products_prices)
        tkMessageBox.showwarning("PREÇO TOTAL DE TAREFAS E PRODUTOS É: "+str(total_price_sum)+'                                                                           ')
    except:
        tkMessageBox.showwarning("Em algum campo de preço foi inserido algo que não é número.\nFavor, refazer o preenchimento das tarefas e produtos")
    s01=tasks
    s01.append(products)

    result = tkMessageBox.askquestion('Confirmar', 'Você quer salvar o pedido?\nIsto salvará os nomes, tarefas,\nprodutos, datas, placa etc',
                                      icon="warning")
    if result == 'yes':
        s1=str(s01)
        s2=s1.translate({ord(i): None for i in "["})
        s3=s2.translate({ord(i): None for i in "]"})
        s4=s3.translate({ord(i): None for i in ","})
        services=s4
        Database()
        #getting form data
        name1=name.get()
        if name1=="":
            name1=namecopied
        code1=code.get()
        if code1=="":
            code1=codecopied
        date1=date.get()
        date21=date2.get()
        mec1=mec.get()
        contact1=contact.get()
        if contact1=="":
            contact1=contactcopied
        price1=float(total_price_sum)
        service1=services
        transactions1=transactions.get()
        paidwhere1=paidwhere.get()
        #execute query
        conn.execute('''INSERT INTO REGISTRATION (NAME,CODE,DATE,DATE2,MEC,TRANSACTIONS,PAIDWHERE,CONTACT,PRICE, SERVICE)
        VALUES (?,?,?,?,?,?,?,?,?,?)''',(name1,code1.upper(),date1,date21,mec1,transactions1,paidwhere1,contact1,price1,service1))
        conn.commit()
        tkMessageBox.showinfo("Messagem","Salva com sucesso")
        #refresh table data
        DisplayData()
        conn.close()
def read_screenForm():
    #open database
    Database()
    if not tree.selection():
        tkMessageBox.showwarning("Aviso","Selecione a linha de pedido a ser visualizado")
    else:
        result = tkMessageBox.askquestion('Confirmar', 'Você quer visualizar este pedido?',
                                          icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)

            cursor=conn.execute("SELECT ID FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            ct1=str(fetch).translate({ord(i): None for i in "'"})
            ct2=ct1.translate({ord(i): None for i in "["})
            ct3=ct2.translate({ord(i): None for i in "]"})
            ct4=ct3.translate({ord(i): None for i in "("})
            ct004=ct4.translate({ord(i): None for i in ")"})
            ct5=ct004.translate({ord(i): None for i in ","})

            cursor=conn.execute("SELECT PRICE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            fct1=str(fetch).translate({ord(i): None for i in "'"})
            fct2=fct1.translate({ord(i): None for i in "["})
            fct3=fct2.translate({ord(i): None for i in "]"})
            fct4=fct3.translate({ord(i): None for i in "("})
            wwz=fct4.translate({ord(i): None for i in ")"})
            hct5=wwz.translate({ord(i): None for i in ","})

            cursor=conn.execute("SELECT SERVICE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            gct1=str(fetch).translate({ord(i): None for i in "'"})
            gct2=gct1.translate({ord(i): None for i in "["})
            gct3=gct2.translate({ord(i): None for i in "]"})
            gct4=gct3.translate({ord(i): None for i in "("})
            ictx=gct4.translate({ord(i): None for i in ")"})
            ict5=ictx.translate({ord(i): None for i in '"'})

            cursor=conn.execute("SELECT TRANSACTIONS FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            afct1=str(fetch).translate({ord(i): None for i in "'"})
            afct2=afct1.translate({ord(i): None for i in "["})
            afct3=afct2.translate({ord(i): None for i in "]"})
            afct4=afct3.translate({ord(i): None for i in "("})
            awwz=afct4.translate({ord(i): None for i in ")"})
            ahct5=awwz.translate({ord(i): None for i in ","})

            cursor=conn.execute("SELECT PAIDWHERE    FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            bgct1=str(fetch).translate({ord(i): None for i in "'"})
            bgct2=bgct1.translate({ord(i): None for i in "["})
            bgct3=bgct2.translate({ord(i): None for i in "]"})
            bgct4=bgct3.translate({ord(i): None for i in "("})
            bictx=bgct4.translate({ord(i): None for i in ")"})
            bict5=bictx.translate({ord(i): None for i in '"'})

            cursor.close()
            conn.close()
    
            import tkinter as tk
            import tkinter.ttk as ttk
            class Application(tk.Frame):
                def __init__(self, root):
                    self.root = root
                    self.initialize_user_interface()
                def initialize_user_interface(self):
                    # Configure the root object for the Application
                    self.root.geometry('400x300')
                    self.root.title("ORDEM DE PEDIDO")
                    self.root.grid_rowconfigure(0, weight=1)
                    self.root.grid_columnconfigure(0, weight=1)
                    self.root.config(background="gray")
             
                    self.name_label = tk.Label(self.root, text="PREÇO TOTAL:(R$) "+hct5)
                    self.name_label.grid(row=1, column=0, sticky=tk.W)

                    self.name_label2 = tk.Label(self.root, text="NÚMERO DO PEDIDO:(R$) "+ct5)
                    self.name_label2.grid(row=0, column=0, sticky=tk.W)

                    self.name_label = tk.Label(self.root, text="TIPO DE TRANSAÇÃO:(R$) "+ahct5)
                    self.name_label.grid(row=2, column=0, sticky=tk.W)

                    self.name_label2 = tk.Label(self.root, text="PAGO ONDE:(R$) "+ bict5)
                    self.name_label2.grid(row=3, column=0, sticky=tk.W)
             
                    self.idnumber_label = tk.Label(self.root, text="SERVIÇOS E PRODUTOS DO PEDIDO:")
                    self.label_see_request = tk.Label(self.root, text="")
                    self.idnumber_label.grid(row=4, column=0, sticky=tk.W)
                    self.label_see_request.grid(row=4, column=1)

                 
                    # Set the treeview
                    self.tree = ttk.Treeview(self.root, columns=('Número do Pedido','Serviço/Produto', 'Preço Total'))
             
                    # Set the heading (Attribute Names)
                    self.tree.heading('#0', text='Id')
                    self.tree.heading('#1', text='Serviços/Produtos')
             
                    # Specify attributes of the columns (We want to stretch it!)
                    self.tree.column('#0', stretch=tk.YES)
                    self.tree.column('#1', stretch=tk.YES)
             
                    self.tree.grid(row=5, columnspan=4, sticky='nsew')
                    self.treeview = self.tree
             
                    self.id = 0
                    self.iid = 0

                    serv_prod_list=str(ict5).split('|')
                    listed=[]
                    i=0
                    count=0
                    for j in str(ict5):
                        if str(j) == '|':
                            count+=1
                    z=1+int(count)
                    while i < z:
                        listed.append(serv_prod_list[i])
                        self.treeview.insert('', 'end', iid=self.iid, text=str(self.id),
                                             values=(serv_prod_list[i]))
                        self.iid = self.iid + 1
                        self.id = self.id + 1
                        i=i+1

            app = Application(tk.Tk())
            app.root.mainloop()

global xxy
xxy=[]

def report_screenForm():
    import tkinter as tk
    import tkinter.ttk as ttk
    class Application(tk.Frame):
        def __init__(self, root):
            self.root = root
            self.initialize_user_interface()
        def initialize_user_interface(self):
            # Configure the root object for the Application
            self.root.geometry('550x350')
            self.root.title("RELATÓRIO")
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            self.root.config(background="gray")
            def Print_Report():
                import datetime
                self.treeview.insert('', 'end', iid=self.iid, text=str(self.id),
                     values=(self.entry1.get(),
                             self.entry2.get()))
                self.iid = self.iid + 1
                self.id = self.id + 1
                aaa=[]
                bbb=[]
                aaa.append(self.entry1.get())
                bbb.append(self.entry2.get())
                aai=str(aaa)
                bbi=str(bbb)

                ii=aai.split('/')
                ff=bbi.split('/')

                import pandas as pd
                yeari1=ii[2].translate({ord(i): None for i in '['})
                yeari2=yeari1.translate({ord(i): None for i in ']'})
                yeari=yeari2.translate({ord(i): None for i in "'"})
                yearf1=ff[2].translate({ord(i): None for i in '['})
                yearf2=yearf1.translate({ord(i): None for i in ']'})
                yearf=yearf2.translate({ord(i): None for i in "'"})

                mi1=ii[1].translate({ord(i): None for i in '['})
                mi2=mi1.translate({ord(i): None for i in ']'})
                mi=mi2.translate({ord(i): None for i in "'"})
                mf1=ff[1].translate({ord(i): None for i in '['})
                mf2=mf1.translate({ord(i): None for i in ']'})
                mf=mf2.translate({ord(i): None for i in "'"})

                di1=ii[0].translate({ord(i): None for i in '['})
                di2=di1.translate({ord(i): None for i in ']'})
                di=di2.translate({ord(i): None for i in "'"})
                df1=ff[0].translate({ord(i): None for i in '['})
                df2=df1.translate({ord(i): None for i in ']'})
                df=df2.translate({ord(i): None for i in "'"})

                from datetime import date, timedelta
                sdate = date(int(yeari), int(mi), int(di))   # start date
                q='RELATÓRIO DE FATURAMENTO AUTO CENTER OLIVEIRA\nORDEM DE DADOS:\nPreço|Data de Saída|Tarefas ou Produtos\n'
                filename='journal.txt'
                with open(filename, 'w') as file_object:
                    file_object.write(q)

                filenamen='sum.txt'
                with open(filenamen, 'w') as file_objectz:
                    file_objectz.write('[')

                #SET DATES QUERYING FORMAT     
                edate = date(int(yearf), int(mf), int(df))   # end date
                delta = edate - sdate       # as timedelta

                #Reset sum.txt file
                filenamex0='sum.txt'
                with open(filenamex0, 'w') as file_objectsum0:
                    file_objectsum0.write('')

                for i in range(delta.days + 1):
                    day = sdate + timedelta(days=i)
                    interm=str(day)
                    sep=interm.split('-')
                    date_between=str(sep[2])+'/'+str(sep[1])+'/'+str(sep[0])

                    #REGISTER PRICES
                    Database()
                    cursor=conn.execute("SELECT PRICE FROM REGISTRATION WHERE DATE2 = ?", (date_between,))
                    fetch = cursor.fetchall()
                    ct1=str(fetch).translate({ord(i): None for i in "'"})
                    ct2=ct1.translate({ord(i): None for i in "["})
                    ct3=ct2.translate({ord(i): None for i in "]"})
                    ct4=ct3.translate({ord(i): None for i in "("})
                    ct004=ct4.translate({ord(i): '{' for i in ")"})
                    ct0045=ct004.translate({ord(i): None for i in ","})
                    ct5s=ct0045.translate({ord(i): None for i in '"'})
                    ct5=ct5s.translate({ord(i): None for i in ","})
                    ct6=ct5.translate({ord(i): None for i in ","})
                    filenamex='sum.txt'
                    with open(filenamex, 'a') as file_objectsum:
                        file_objectsum.write(ct6)
                    #GET DATA TO REPORT
                    Database()
                    cursor=conn.execute("SELECT PRICE, DATE2, SERVICE FROM REGISTRATION WHERE DATE2 = ?", (date_between,))
                    fetch = cursor.fetchall()
                    ct1=str(fetch).translate({ord(i): None for i in "'"})
                    ct2=ct1.translate({ord(i): None for i in "["})
                    ct3=ct2.translate({ord(i): None for i in "]"})
                    ct4=ct3.translate({ord(i): None for i in "("})
                    ct004=ct4.translate({ord(i): '{' for i in ")"})
                    ct0045=ct004.translate({ord(i): None for i in ","})
                    ct5s=ct0045.translate({ord(i): None for i in '"'})
                    ct5=ct5s.translate({ord(i): None for i in ","})
                    report_data=ct5.split('{')
                    inte=str(report_data)
                    listfin=[]
                    listfin.append(inte)
                    listfin2=str(listfin).translate({ord(i): None for i in '"'})
                    global result
                    result='0'
                    result1=listfin2.translate({ord(i): None for i in "['']"})
                    result=result1.translate({ord(i): '\n' for i in ","})
                    filename='journal.txt'
                    with open(filename, 'a') as file_object:
                        file_object.write(result)

                #ADD SUM.TXT TO JOURNAL.TXT:
                filesumfin = open("sum.txt")
                prices_data0 = filesumfin.read().replace("\n", " ")
                filesumfin.close()

                prices_data1=prices_data0.split('{')
                yui=0
                prices_data3=[]
                while yui < len(prices_data1):
                    if prices_data1[yui] != '':
                        prices_data2=float(prices_data1[yui])
                        prices_data3.append(prices_data2)
                    yui=yui+1
                prices_data4=sum(prices_data3)
                prices_data5=str(prices_data4)

                prices_data='TOTAL DE FATURAMENTO NO PERÍODO SELECIONADO: '+prices_data5

                filename4='journal.txt'
                with open(filename4, 'a') as file_object4:
                    file_object4.write(prices_data)

                #SEND DATA FROM TXT FILE TO PRINTER:
                if result != '0':
                    os.startfile("journal.txt", "print")

            self.name_label = tk.Label(self.root, text="Data Inicial:dd/mm/aaaa (contando o dia)")
            self.entry1 = tk.Entry(self.root)
            self.name_label.grid(row=1, column=0, sticky=tk.W)
            self.entry1.grid(row=2, column=0)
            
            self.name_label = tk.Label(self.root, text="Data Final:dd/mm/aaaa (não contando o dia)")
            self.entry2 = tk.Entry(self.root)
            self.name_label.grid(row=1, column=1, sticky=tk.W)
            self.entry2.grid(row=2, column=1)

            self.submit_button = tk.Button(self.root, text="Imprimir Relatório", command=Print_Report)
            self.submit_button.grid(row=3, column=1, sticky=tk.W)

            #open database
            Database()
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']

            # Set the treeview
            self.tree = ttk.Treeview(self.root, columns=('Id','Data Inicial','Data Final'))

            # Set the heading (Attribute Names)
            self.tree.heading('#0', text='Data Id')
            self.tree.heading('#1', text='Data Inicial')
            self.tree.heading('#2', text='Data Final')
     
            # Specify attributes of the columns (We want to stretch it!)
            self.tree.column('#0', stretch=tk.YES)
            self.tree.column('#1', stretch=tk.YES)
            self.tree.column('#2', stretch=tk.YES)
     
            self.tree.grid(row=4, columnspan=4, sticky='nsew')
            self.treeview = self.tree
     
            self.id = 0
            self.iid = 0
            cursor.close()
            conn.close()
    app = Application(tk.Tk())
    app.root.mainloop()

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
            ct1=str(fetch).translate({ord(i): None for i in "'"})
            ct2=ct1.translate({ord(i): None for i in "["})
            ct3=ct2.translate({ord(i): None for i in "]"})
            ct4=ct3.translate({ord(i): None for i in "("})
            ct5=ct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT NAME FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            bct1=str(fetch).translate({ord(i): None for i in "'"})
            bct2=bct1.translate({ord(i): None for i in "["})
            bct3=bct2.translate({ord(i): None for i in "]"})
            bct4=bct3.translate({ord(i): None for i in "("})
            dct5=bct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT CODE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            cct1=str(fetch).translate({ord(i): None for i in "'"})
            cct2=cct1.translate({ord(i): None for i in "["})
            cct3=cct2.translate({ord(i): None for i in "]"})
            cct4=cct3.translate({ord(i): None for i in "("})
            ect5=cct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT DATE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            dct1=str(fetch).translate({ord(i): None for i in "'"})
            dct2=dct1.translate({ord(i): None for i in "["})
            dct3=dct2.translate({ord(i): None for i in "]"})
            dct4=dct3.translate({ord(i): None for i in "("})
            fct5=dct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT DATE2 FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            dct12=str(fetch).translate({ord(i): None for i in "'"})
            dct22=dct12.translate({ord(i): None for i in "["})
            dct32=dct22.translate({ord(i): None for i in "]"})
            dct42=dct32.translate({ord(i): None for i in "("})
            fct52=dct42.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT MEC FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            mdct1=str(fetch).translate({ord(i): None for i in "'"})
            mdct2=mdct1.translate({ord(i): None for i in "["})
            mdct3=mdct2.translate({ord(i): None for i in "]"})
            mdct4=mdct3.translate({ord(i): None for i in "("})
            mfct5=mdct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT CONTACT FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            ect1=str(fetch).translate({ord(i): None for i in "'"})
            ect2=ect1.translate({ord(i): None for i in "["})
            ect3=ect2.translate({ord(i): None for i in "]"})
            ect4=ect3.translate({ord(i): None for i in "("})
            gct5=ect4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT PRICE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            fct1=str(fetch).translate({ord(i): None for i in "'"})
            fct2=fct1.translate({ord(i): None for i in "["})
            fct3=fct2.translate({ord(i): None for i in "]"})
            fct4=fct3.translate({ord(i): None for i in "("})
            hct5=fct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT SERVICE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            gct1=str(fetch).translate({ord(i): None for i in "'"})
            gct2=gct1.translate({ord(i): None for i in "["})
            gct3=gct2.translate({ord(i): None for i in "]"})
            gct4=gct3.translate({ord(i): None for i in "("})
            ictx=gct4.translate({ord(i): None for i in ")"})
            ict5=ictx.translate({ord(i): None for i in '"'})

            cursor=conn.execute("SELECT TRANSACTIONS FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            afct1=str(fetch).translate({ord(i): None for i in "'"})
            afct2=afct1.translate({ord(i): None for i in "["})
            afct3=afct2.translate({ord(i): None for i in "]"})
            afct4=afct3.translate({ord(i): None for i in "("})
            awwz=afct4.translate({ord(i): None for i in ")"})
            ahct5=awwz.translate({ord(i): None for i in ","})

            cursor=conn.execute("SELECT PAIDWHERE    FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            bgct1=str(fetch).translate({ord(i): None for i in "'"})
            bgct2=bgct1.translate({ord(i): None for i in "["})
            bgct3=bgct2.translate({ord(i): None for i in "]"})
            bgct4=bgct3.translate({ord(i): None for i in "("})
            bictx=bgct4.translate({ord(i): None for i in ")"})
            bict5=bictx.translate({ord(i): None for i in '"'})

            a1='Número de ordem: '+ct5
            a2='Nome: '+dct5
            a3='Placa: '+ect5
            a4='Data de Entrada: '+fct5
            a42='Data de Saída: '+fct52
            a43='Mecânico: '+mfct5
            a5='Fone: '+gct5
            a6='Preço Total(R$): '+hct5
            a7='Serviço(s): '+ict5
            a8='Tipo de Transação: '+ahct5
            a9='Pago Onde: '+bict5
            global content
            content0=a1+a2+a3+a4+a42+a43+a5+a7+a6+a8+a9
            content=content0.translate({ord(i): '\n' for i in ","})
        cursor.close()
        conn.close()
    #PRINT
    brand=str(company_brand.upper)
    global q
    q='------------------------------------------------------------------\n'+brand+'\n------------------------------------------------------------------\nOrdem de Serviço\n------------------------------------------------------------------\n'+content+'------------------------------------------------------------------'
    filename=tempfile.mktemp(".txt")
    open (filename, "w"). write(q)
    os.startfile(filename, "print")

def PrintDesign():
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
            ct1=str(fetch).translate({ord(i): None for i in "'"})
            ct2=ct1.translate({ord(i): None for i in "["})
            ct3=ct2.translate({ord(i): None for i in "]"})
            ct4=ct3.translate({ord(i): None for i in "("})
            ct5=ct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT NAME FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            bct1=str(fetch).translate({ord(i): None for i in "'"})
            bct2=bct1.translate({ord(i): None for i in "["})
            bct3=bct2.translate({ord(i): None for i in "]"})
            bct4=bct3.translate({ord(i): None for i in "("})
            dct5=bct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT CODE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            cct1=str(fetch).translate({ord(i): None for i in "'"})
            cct2=cct1.translate({ord(i): None for i in "["})
            cct3=cct2.translate({ord(i): None for i in "]"})
            cct4=cct3.translate({ord(i): None for i in "("})
            ect5=cct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT DATE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            dct1=str(fetch).translate({ord(i): None for i in "'"})
            dct2=dct1.translate({ord(i): None for i in "["})
            dct3=dct2.translate({ord(i): None for i in "]"})
            dct4=dct3.translate({ord(i): None for i in "("})
            fct5=dct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT DATE2 FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            dct12=str(fetch).translate({ord(i): None for i in "'"})
            dct22=dct12.translate({ord(i): None for i in "["})
            dct32=dct22.translate({ord(i): None for i in "]"})
            dct42=dct32.translate({ord(i): None for i in "("})
            fct52=dct42.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT MEC FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            mdct1=str(fetch).translate({ord(i): None for i in "'"})
            mdct2=mdct1.translate({ord(i): None for i in "["})
            mdct3=mdct2.translate({ord(i): None for i in "]"})
            mdct4=mdct3.translate({ord(i): None for i in "("})
            mfct5=mdct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT CONTACT FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            ect1=str(fetch).translate({ord(i): None for i in "'"})
            ect2=ect1.translate({ord(i): None for i in "["})
            ect3=ect2.translate({ord(i): None for i in "]"})
            ect4=ect3.translate({ord(i): None for i in "("})
            gct5=ect4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT PRICE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            fct1=str(fetch).translate({ord(i): None for i in "'"})
            fct2=fct1.translate({ord(i): None for i in "["})
            fct3=fct2.translate({ord(i): None for i in "]"})
            fct4=fct3.translate({ord(i): None for i in "("})
            hct5=fct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT SERVICE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            gct1=str(fetch).translate({ord(i): None for i in "'"})
            gct2=gct1.translate({ord(i): None for i in "["})
            gct3=gct2.translate({ord(i): None for i in "]"})
            gct4=gct3.translate({ord(i): None for i in "("})
            ictx=gct4.translate({ord(i): None for i in ")"})
            ict5=ictx.translate({ord(i): None for i in '"'})

            cursor=conn.execute("SELECT TRANSACTIONS FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            afct1=str(fetch).translate({ord(i): None for i in "'"})
            afct2=afct1.translate({ord(i): None for i in "["})
            afct3=afct2.translate({ord(i): None for i in "]"})
            afct4=afct3.translate({ord(i): None for i in "("})
            awwz=afct4.translate({ord(i): None for i in ")"})
            ahct5=awwz.translate({ord(i): None for i in ","})

            cursor=conn.execute("SELECT PAIDWHERE    FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            bgct1=str(fetch).translate({ord(i): None for i in "'"})
            bgct2=bgct1.translate({ord(i): None for i in "["})
            bgct3=bgct2.translate({ord(i): None for i in "]"})
            bgct4=bgct3.translate({ord(i): None for i in "("})
            bictx=bgct4.translate({ord(i): None for i in ")"})
            bict5=bictx.translate({ord(i): None for i in '"'})

            a1='Número de ordem: '+ct5
            a2='Nome: '+dct5
            a3='Placa: '+ect5
            a4='Data de Entrada: '+fct5
            a42='Data de Saída: '+fct52
            a43='Mecânico: '+mfct5
            a5='Fone: '+gct5
            a6='Preço Total(R$): '+hct5
            a7='Serviço(s): '+ict5
            a8='Tipo de Transação: '+ahct5
            a9='Pago Onde: '+bict5
            global content
            content0=a1+a2+a3+a4+a42+a43+a5+a7+a6+a8+a9
            content=content0.translate({ord(i): '\n' for i in ","})

        #Creating a pdf file and setting a naming convention
        c = canvas.Canvas(str(ct5) + '_Servicos_' + str(dct5) +'.pdf')
        c.setPageSize((page_width, page_height))

        #Drawing the image
        c.drawInlineImage("C:\\Users\\macbook\\Desktop\\Management_System\\Orcamentos_E_Servicos\\AO.png", page_width - image_width - margin,
                          page_height - image_height - margin,
                          image_width, image_height)

        #Invoice information
        c.setFont('Arial',80)
        text = 'NOTA DE SERVIÇOS'
        text_width = stringWidth(text,'Arial',80)
        c.drawString((page_width-text_width)/2, page_height - image_height - margin, text)
        y = page_height - image_height - margin*4
        x = 2*margin
        x2 = x + 550
        
        c.setFont('Arial', 45)
        c.drawString(x, y, 'Gerado por: ')
        c.drawString(x2,y, 'Auto Center Oliveira')
        y -= margin
        
        c.drawString(x,y,'Cliente: ')
        c.drawString(x2,y,str(dct5))
        y -= margin
        
        c.drawString(x,y,'Numero do Orçamento: ')
        c.drawString(x2,y, str(ct5))
        y -= margin

        c.drawString(x,y, 'Data Inicial: ')
        c.drawString(x2,y, str(fct5))
        y -= margin
        
        c.drawString(x,y,'Data Final: ')
        c.drawString(x2,y, str(fct52))
        y -= margin *2
        
        c.drawString(x,y, 'Placa: ')
        c.drawString(x2,y, str(ect5))
        y -= margin

        c.drawString(x,y,'Mecânico: ')
        c.drawString(x2,y, str(mfct5))
        y-= margin
        
        c.drawString(x,y, 'Fone: ')
        c.drawString(x2,y, str(gct5))
        y -= margin

        c.drawString(x,y,'Tipo de Transacão: ')
        c.drawString(x2,y, str(ahct5))
        y-= margin
        
        c.drawString(x,y, 'Pago Onde: ')
        c.drawString(x2,y, str(bict5))
        y -= margin

        c.drawString(x,y,'Servico(s): ')
        c.drawString(x2,y, str(ict5))
        y-= margin

        c.drawString(x,y,'Preço Total: ')
        c.drawString(x2,y,'R$ ' + str(hct5) + '0')
        y -= margin*3
               
        c.drawString(x,y,'Obrigado pela escolha!')
        y -= margin
        c.drawString(x,y,'Fone: (11) 1234-5678')
        y -= margin
        c.drawString(x,y,'Sistemas empresariais e comerciais: https://jesse-leite-softwares.onrender.com')    

        #Saving the pdf file
        c.save()
        cursor.close()
        conn.close()

def Delete():
    #open database
    Database()
    result='yes'
    if result == 'yes':
        curItem = tree.focus()
        contents = (tree.item(curItem))
        selecteditem = contents['values']
        tree.delete(curItem)
        cursor=conn.execute("DELETE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
        conn.commit()
    cursor.close()
    conn.close()

def Update():
    #TELL TO SELECT ROW
    if not tree.selection():
        tkMessageBox.showwarning("Aviso","Selecione a linha a ser atualizada")
    else:
        result = tkMessageBox.askquestion('Confirmar', 'Você quer atualizar este pedido?\nO número de pedido será modificado',
                                          icon="warning")
        if result == 'yes':
            #READ DATABASE
            Database()
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)

            cursor=conn.execute("SELECT ID FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            ct1=str(fetch).translate({ord(i): None for i in "'"})
            ct2=ct1.translate({ord(i): None for i in "["})
            ct3=ct2.translate({ord(i): None for i in "]"})
            ct4=ct3.translate({ord(i): None for i in "("})
            ct5=ct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT NAME FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            bct1=str(fetch).translate({ord(i): None for i in "'"})
            bct2=bct1.translate({ord(i): None for i in "["})
            bct3=bct2.translate({ord(i): None for i in "]"})
            bct4=bct3.translate({ord(i): None for i in "("})
            dct5=bct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT CODE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            cct1=str(fetch).translate({ord(i): None for i in "'"})
            cct2=cct1.translate({ord(i): None for i in "["})
            cct3=cct2.translate({ord(i): None for i in "]"})
            cct4=cct3.translate({ord(i): None for i in "("})
            ect5=cct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT DATE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            dct1=str(fetch).translate({ord(i): None for i in "'"})
            dct2=dct1.translate({ord(i): None for i in "["})
            dct3=dct2.translate({ord(i): None for i in "]"})
            dct4=dct3.translate({ord(i): None for i in "("})
            fct5=dct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT DATE2 FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            dct12=str(fetch).translate({ord(i): None for i in "'"})
            dct22=dct12.translate({ord(i): None for i in "["})
            dct32=dct22.translate({ord(i): None for i in "]"})
            dct42=dct32.translate({ord(i): None for i in "("})
            fct52=dct42.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT MEC FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            mdct1=str(fetch).translate({ord(i): None for i in "'"})
            mdct2=mdct1.translate({ord(i): None for i in "["})
            mdct3=mdct2.translate({ord(i): None for i in "]"})
            mdct4=mdct3.translate({ord(i): None for i in "("})
            mfct5=mdct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT CONTACT FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            ect1=str(fetch).translate({ord(i): None for i in "'"})
            ect2=ect1.translate({ord(i): None for i in "["})
            ect3=ect2.translate({ord(i): None for i in "]"})
            ect4=ect3.translate({ord(i): None for i in "("})
            gct5=ect4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT PRICE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            fct1=str(fetch).translate({ord(i): None for i in "'"})
            fct2=fct1.translate({ord(i): None for i in "["})
            fct3=fct2.translate({ord(i): None for i in "]"})
            fct4=fct3.translate({ord(i): None for i in "("})
            hct5=fct4.translate({ord(i): None for i in ")"})

            cursor=conn.execute("SELECT SERVICE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            gct1=str(fetch).translate({ord(i): None for i in "'"})
            gct2=gct1.translate({ord(i): None for i in "["})
            gct3=gct2.translate({ord(i): None for i in "]"})
            gct4=gct3.translate({ord(i): None for i in "("})
            ictx=gct4.translate({ord(i): None for i in ")"})
            ict5=ictx.translate({ord(i): None for i in '"'})

            cursor=conn.execute("SELECT TRANSACTIONS FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            afct1=str(fetch).translate({ord(i): None for i in "'"})
            afct2=afct1.translate({ord(i): None for i in "["})
            afct3=afct2.translate({ord(i): None for i in "]"})
            afct4=afct3.translate({ord(i): None for i in "("})
            awwz=afct4.translate({ord(i): None for i in ")"})
            ahct5=awwz.translate({ord(i): None for i in ","})

            cursor=conn.execute("SELECT PAIDWHERE FROM REGISTRATION WHERE ID = %d" % selecteditem[0])
            fetch = cursor.fetchall()
            bgct1=str(fetch).translate({ord(i): None for i in "'"})
            bgct2=bgct1.translate({ord(i): None for i in "["})
            bgct3=bgct2.translate({ord(i): None for i in "]"})
            bgct4=bgct3.translate({ord(i): None for i in "("})
            bictx=bgct4.translate({ord(i): None for i in ")"})
            bict5=bictx.translate({ord(i): None for i in '"'})
        #remove ','
            ct5=ct5.translate({ord(i): None for i in ','})
            xct5=ct5.translate({ord(i): None for i in ' '})
            global yct5
            yct5=int(xct5)
            dct5=dct5.translate({ord(i): None for i in ','})
            ect5=ect5.translate({ord(i): None for i in ','})
            fct5=fct5.translate({ord(i): None for i in ','})
            fct52=fct52.translate({ord(i): None for i in ','})
            mfct5=mfct5.translate({ord(i): None for i in ','})
            gct5=gct5.translate({ord(i): None for i in ','})
            hct5=hct5.translate({ord(i): None for i in ','})
            ict5=ict5.translate({ord(i): None for i in ','})
            ct5=ct5.translate({ord(i): None for i in ','})
            ahct5=ahct5.translate({ord(i): None for i in ','})
            bict5=bict5.translate({ord(i): None for i in ','})
            cursor.close()
            conn.close()

        #INSERT DATA IN ROW
        global s01
        s01=['']
        global s1
        stxt=service.get()+'|'
        s0=stxt.split()
        s01.append(ict5)
        s01.append(s0)
        s1=str(s01)
        s2=s1.translate({ord(i): None for i in "["})
        s3=s2.translate({ord(i): None for i in "]"})
        s4=s3.translate({ord(i): None for i in ","})
        services=s4
        def fillall():
            tkMessageBox.showinfo("Preencha conforme anterior/a atualizar: Preço total a Atualizar                    ")
            #refresh table data
            DisplayData()
        def fillall2():
            tkMessageBox.showinfo("Preencha conforme anterior/a atualizar: Tipo Transação                    ")
            #refresh table data
            DisplayData()
        def fillall3():
            tkMessageBox.showinfo("Preencha conforme anterior/a atualizar: Pago Onde                    ")
            #refresh table data
            DisplayData()
        def fillall4():
            tkMessageBox.showinfo("Preencha conforme anterior/a atualizar: Data Saída                    ")
            #refresh table data
            DisplayData()
        Database()
    #getting form data
        if price.get() != '':
            price1=price.get()
        else:
            fillall()
        if transactions.get() != '':
            transactions1=transactions.get()
        else:
            fillall2()
        if paidwhere.get() != '':
            paidwhere1=paidwhere.get()
        else:
            fillall3()
        if date2.get() != '':
            date21=date2.get()
        else:
            fillall4()
        service1=service.get()
        #execute query
        conn.execute('''INSERT INTO REGISTRATION (NAME,CODE,DATE,DATE2,MEC,TRANSACTIONS,PAIDWHERE,CONTACT,PRICE,SERVICE)
        VALUES (?,?,?,?,?,?,?,?,?,?)''',(dct5,ect5.upper(),fct5,date21,mfct5,transactions1,paidwhere1,gct5,price1,service1))
        conn.commit()
        tkMessageBox.showinfo("Messagem","Salva com sucesso\ncom novo Número de Pedido")
        #refresh table data
        DisplayData()

        #DELETE OLD ROW
        result = tkMessageBox.askquestion('Confirmar', 'Concluir atualização?',
                                          icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            # tree.delete(curItem)
            Database()
            cursor=conn.execute("DELETE FROM REGISTRATION WHERE ID = %d" % yct5)
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
