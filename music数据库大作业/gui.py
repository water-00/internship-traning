from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql

db = pymysql.connect(host = "localhost", user = "root", 
                     password = "wang250188", database = "music", port = 3306, autocommit = True)

# 创建游标对象
cursor = db.cursor()

def search_piece():
    frm = Toplevel()
    frm.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], minsize=50)
    frm.columnconfigure(0, minsize=50)
    Label(master=frm, text='Opus:', font=('Arial', 18)).grid(row=0, column=0)
    e1 = Entry(master=frm, font=('Arial', 18), width=20)
    e1.grid(row=1, column=0)
    Label(master=frm, text='name:', font=('Arial', 18)).grid(row=2, column=0)
    e2 = Entry(master=frm, font=('Arial', 18), width=20)
    e2.grid(row=3, column=0)
    click = lambda:exec_search_piece(frm, e1.get(), e2.get())
    Button(master=frm, text='search', command=click).grid(row=4, column=0)


def exec_search_piece(frm, str1, str2):
    tree = ttk.Treeview(master=frm)
    ls = ['Opus', 'name', 'composer', 'album', 'country']
    tree['columns'] = ('Opus', 'name', 'composer', 'album', 'country')
    for i in ls:
        tree.column(i, anchor='center')
        tree.heading(i, text=i)
    sql = "select * from info "
    if str1 != '' and str2 != '':
        sql = sql + "where opus like '%" + str1 + "%' and name like '%" + str2 + "%';"
    elif str1 != '':
        sql = sql + "where opus like '%" + str1 + "%';"
    elif str2 != '':
        sql = sql + "where name like '%" + str2 + "%';"
    else:
        Label(master=frm, text='input valid', font=('Arial', 18)).grid(row=5, column=0)
        return
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in range(len(result)):
        tree.insert('', i, values=result[i])
    tree['show'] = 'headings'
    tree.grid(row=5, column=0)

    # update album
    if (len(result) == 1 and str1 != ''):
        Label(master=frm, text='new album:', font=('Arial', 18)).grid(row=6, column=0)
        e3 = Entry(master=frm, font=('Arial', 18), width=20)
        e3.grid(row=7, column=0)
        click = lambda:exec_update(frm, str1, e3.get())
        Button(master=frm, text="update", command=click).grid(row=8, column=0)

def exec_update(frm, opus, new_album):
    sql = "call update_album('" + opus + "', '" + new_album + "');"
    try:
        cursor.execute(sql)
        messagebox.showinfo(message='update successfully.')
    except Exception as m:
        messagebox.showerror('error', m.args)

def search_composer():
    frm = Toplevel()
    frm.rowconfigure([0, 1, 2, 3, 4], minsize=50)
    frm.columnconfigure(0, minsize=50)
    Label(master=frm, text='name:', font=('Arial', 18)).grid(row=0, column=0)
    e1 = Entry(master=frm, font=('Arial', 18), width=20)
    e1.grid(row=1, column=0)
    click = lambda:exec_search_composer(frm, e1.get())
    Button(master=frm, text='search', command=click).grid(row=3, column=0)

def exec_search_composer(frm, str1):
    tree = ttk.Treeview(master=frm)
    ls = ['name', 'birth', 'death', 'country']
    tree['columns'] = ('name', 'birth', 'death', 'country')
    for i in ls:
        tree.column(i, anchor='center')
        tree.heading(i, text=i)
    sql = "select * from composer "
    if str1 != '':
        sql = sql + "where name like '%" + str1 + "%';"
    else:
        Label(master=frm, text='input valid', font=('Arial', 18)).grid(row=4, column=0)
        return
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in range(len(result)):
        tree.insert('', i, values=result[i])
    tree['show'] = 'headings'
    tree.grid(row=4, column=0)

def add_piece():
    frm = Toplevel()
    frm.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], minsize=50)
    frm.columnconfigure(0, minsize=50)
    
    Label(master=frm, text='Opus:', font=('Arial', 18)).grid(row=0, column=0)
    e1 = Entry(master=frm, font=('Arial', 18), width=20)
    e1.grid(row=1, column=0)
    Label(master=frm, text='name:', font=('Arial', 18)).grid(row=2, column=0)
    e2 = Entry(master=frm, font=('Arial', 18), width=20)
    e2.grid(row=3, column=0)
    Label(master=frm, text='composer:', font=('Arial', 18)).grid(row=4, column=0)
    e3 = Entry(master=frm, font=('Arial', 18), width=20)
    e3.grid(row=5, column=0)
    Label(master=frm, text='album:', font=('Arial', 18)).grid(row=6, column=0)
    e4 = Entry(master=frm, font=('Arial', 18), width=20)
    e4.grid(row=7, column=0)
    
    
    click = lambda:exec_add_piece(frm, e1.get(), e2.get(), e3.get(), e4.get())
    Button(master=frm, text='add', command=click).grid(row=8, column=0)


def exec_add_piece(frm, opus, name, composer, album):
    sql = "insert into piece values('" + opus + "', '" + name + "', '" + composer + "', '" + album + "');"
    try:
        cursor.execute(sql)
        messagebox.showinfo(message="Successful!")
    except Exception as m:
        messagebox.showerror("error", m.args)

def add_composer():
    4

def exec_add_composer(frm, name, birth_time='', death_time='', country=''):
    4

def add_album():
    4

def exec_add_album(frm, name, publish_time='', company='', performer=''):
    4

def delete_piece():
    frm = Toplevel()
    frm.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7], minsize=50)
    frm.columnconfigure(0, minsize=50)
    
    Label(master=frm, text='Opus:', font=('Arial', 18)).grid(row=0, column=0)
    e1 = Entry(master=frm, font=('Arial', 18), width=20)
    e1.grid(row=1, column=0)
    Label(master=frm, text='composer:', font=('Arial', 18)).grid(row=2, column=0)
    e2 = Entry(master=frm, font=('Arial', 18), width=20)
    e2.grid(row=3, column=0)
    
    click = lambda:exec_delete_piece(frm, e1.get(), e2.get())
    Button(master=frm, text='search', command=click).grid(row=4, column=0)


def exec_delete_piece(frm, opus, composer):
    tree = ttk.Treeview(master=frm)
    ls = ['Opus', 'name', 'composer', 'album']
    tree['columns'] = ('Opus', 'name', 'composer', 'album')
    for i in ls:
        tree.column(i, anchor='center')
        tree.heading(i, text=i)
        
    show_sql = "select * from piece where opus like '%" + opus + "%' and composer like '%" + composer + "%';"
    cursor.execute(show_sql)
    result = cursor.fetchall()
    for i in range(len(result)):
        tree.insert("", i, values=result[i])
    tree['show'] = 'headings'
    tree.grid(row=7, column=0)
    
    del_sql = "delete from piece where opus like '%" + opus + "%' and composer like '%" + composer + "%';"
    click = lambda:confirm(frm, del_sql)
    Button(frm, text='delete all', command=click).grid(row=5, column=0)
    click = lambda:cancel(frm, del_sql)
    Button(frm, text='cancel', command=click).grid(row=6, column=0)
    
def confirm(frm, del_sql):
    cursor.execute("START TRANSACTION")
    cursor.execute(del_sql)
    cursor.execute("COMMIT")
    messagebox.showinfo(message='Delete successfully.')
    
def cancel(frm, del_sql):
    cursor.execute("START TRANSACTION")
    cursor.execute(del_sql)
    cursor.execute("ROLLBACK")
    messagebox.showinfo(message='Deletion canceled.')

def onCloseOtherFrame(otherFrame):
    otherFrame.destroy()
    window.update()
    window.deiconify() # 将主窗口恢复显示
    

window = Tk()
window.title('数据库系统作业')
window.rowconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50)
window.columnconfigure(0, minsize=50)

l = Label(master=window, text="my favorite pieces", font = ('Arial', 30), width = 20).grid(row=0, column=0)
btn_search_piece = Button(master=window, text="search piece", command=search_piece).grid(row=1, column=0)
btn_search_composer = Button(master=window, text="search composer", command=search_composer).grid(row=2, column=0)
btn_add_piece = Button(master=window, text="add piece", command=add_piece).grid(row=3, column=0)
btn_add_composer = Button(master=window, text="add composer", command=add_composer).grid(row=4, column=0)
btn_add_album = Button(master=window, text="add album", command=add_album).grid(row=5, column=0)
btn_delete_piece = Button(master=window, text="delete piece", command=delete_piece).grid(row=6, column=0)

window.mainloop()