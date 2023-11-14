import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.viev_records() # Инициализация основного окна и загрузка записей
    
    def init_main(self):
        toolbar = tk.Frame(bg = '#d7d8e0', bd = 2) # Настройка панели инструментов
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img=tk.PhotoImage(file='./img/add.png')
        btn_open_dialog=tk.Button(toolbar, bg = '#d7d8e0', bd = 0, # Кнопка для открытия диалогового окна добавления новой записи
                                  image=self.add_img, 
                                  command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree= ttk.Treeview(self,  # Настройка Treeview для отображения записей
                                 columns=['ID','fio','tel','email','sal'],
                                 height=45, show='headings')
        self.tree.column('ID', width=30,anchor=tk.CENTER)
        self.tree.column('fio', width=309,anchor=tk.CENTER)
        self.tree.column('tel', width=159,anchor=tk.CENTER)
        self.tree.column('email', width=157,anchor=tk.CENTER)
        self.tree.column('sal', width=157,anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('fio', text='ФИО')
        self.tree.heading('tel', text='Телефонный номер')
        self.tree.heading('email', text='email')
        self.tree.heading('sal', text='Зарплата')

        self.tree.pack(side=tk.LEFT)


        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0',
                                    bd=0,image=self.update_img,
                                    command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)
    
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, 
                               image=self.delete_img,
                               command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)


    def open_dialog(self):
        Child()

    def records(self, fio, tel, email, sal):  # Добавление новой записи в базу данных и обновление отображения
        self.db.insert_data(fio, tel, email, sal)
        self.viev_records()
    
    def viev_records(self): # Просмотр всех записей в Treeview
        self.db.c.execute('''
        SELECT * FROM db''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_update_dialog(self):
        Update()
    
    def update_record(self, fio, tel, email, sal):  # Обновление записи в базе данных и обновление отображения
        self.db.conn.execute('''
    UPDATE db SET fio=?, tel=?, email=? sal=? WHERE ID = ?''', (fio, tel, email,
        self.tree.see(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.viev_records()

    def delete_records(self): # Удаление выбранных записей из базы данных и обновление отображения
        for selection_item in self.tree.selection():
            self.db.c.execute('''
        DELETE FROM db WHERE id = ?''',
        (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.viev_records()

class Child(tk.Toplevel):  
    def __init__(self):
        super().__init__()
        self.init_child()
        self.view=app

    def init_child(self):  # Диалоговое окно для добавления новой записи
        self.title('Добавить')
        self.geometry('400x220')
        root.resizable(False,False)
        self.grab_set()
        self.focus_set()

        label_fio=tk.Label(self, text='ФИО')
        label_fio.place(x=50,y=50)
        label_select=tk.Label(self,text='Телефонный номер')
        label_select.place(x=50,y=80)
        label_sum=tk.Label(self,text='email')
        label_sum.place(x=50,y=110)
        label_sum=tk.Label(self,text='Зарплата')
        label_sum.place(x=50,y=140)

        self.entry_fio=ttk.Entry(self)
        self.entry_fio.place(x=100,y=50)

        self.entry_tel=ttk.Entry(self)
        self.entry_tel.place(x=100,y=80)

        self.entry_email=ttk.Entry(self)
        self.entry_email.place(x=100,y=110)

        self.entry_sal=ttk.Entry(self)
        self.entry_sal.place(x=100,y=140)


        self.button_cancel=ttk.Button(self, text='cancel',
                                      command=self.destroy)
        self.button_cancel.place(x=300,y=170)

        self.btn_ok=ttk.Button(self, text='add')
        self.btn_ok.place(x=220,y=170)
        self.btn_ok.bind('<Button-1>',
                         lambda event: self.view.records(self.entry_fio.get(),
                                                    self.entry_email.get(),
                                                    self.entry_tel.get(),
                                                    self.entry_sal.get()))

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db=db
        self.default_data()
    
    def init_edit(self): # Диалоговое окно для обновления записи
        self.title('Редактировать позицию')
        btn_edit=ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205,y=170)
        btn_edit.bind('<Button-1>',
                      self.view.update_record(self.entry_fio.get(),
                                              self.entry_email.get(),
                                              self.entry_tel.get(),
                                              self.entry_sal.get()))
        btn_edit.bind('<Button-1>', lambda event:
                      self.destroy(), add='+')
        self.btn_ok.destroy()
    
    def default_data(self): # Заполнение диалогового окна данными выбранной записи
        self.db.c.execute('''
        SELECT * FROM db WHERE id=?'''
        (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_fio.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_sal.insert(0, row[3])
        


class DB:
    def __init__(self):  # Инициализация базы данных
        self.conn = sqlite3.connect('db.db')
        self.c=self.conn.cursor()
        self.c.execute('''
    CREATE TABLE IF NOT EXISTS db (id integer key, fio text, tel text, email text, sal text)

''')    
        self.conn.commit()
    
    def insert_data(self, fio, tel, email, sal): # Добавление новой записи в базу данных
        self.c.execute('''
    INSERT INTO db (fio, tel, email, sal) VALUES (?, ?, ?)''',(fio, tel, email, sal))
        self.conn.commit()

if __name__ == '__main__': # Настройка приложения и запуск основного цикла
    root = tk.Tk() 
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Телефонная книга')
    root.geometry('805x450')
    root.resizable(False,False)
    root.mainloop()