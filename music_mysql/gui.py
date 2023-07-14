from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql
import csv
import random




def search_piece():# 曲子查找界面
    frm = Toplevel()
    frm.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], minsize=50)
    frm.columnconfigure(0, minsize=50)
    Label(master=frm, text='Opus:', font=('Arial', 18)).grid(row=0, column=0)
    e1 = Entry(master=frm, font=('Arial', 18), width=20)
    e1.grid(row=1, column=0)
    Label(master=frm, text='name:', font=('Arial', 18)).grid(row=2, column=0)
    e2 = Entry(master=frm, font=('Arial', 18), width=20)# e1、e2输入
    e2.grid(row=3, column=0)
    click = lambda:exec_search_piece(frm, e1.get(), e2.get())
    Button(master=frm, text='search', command=click).grid(row=4, column=0)


def exec_search_piece(frm, str1, str2):# 曲子查找结果展示以及更新专辑  # 多表查询
    tree = ttk.Treeview(master=frm)
    ls = ['Opus', 'name', 'composer', 'album', 'birthplace']
    tree['columns'] = ('Opus', 'name', 'composer', 'album', 'birthplace')
    for i in ls:
        tree.column(i, anchor='center')
        tree.heading(i, text=i)
    # sql = "select * from info "
    # sql = "select opus opus, piece.name name, piece.composer composer, piece.album album, composer.birthplace birthplace from piece, composer where piece.composer = composer.name"
    # if str1 != '' and str2 != '':
    #     sql = sql + "and opus like '%" + str1 + "%' and piece.name like '%" + str2 + "%';"
    # elif str1 != '':
    #     sql = sql + "and opus like '%" + str1 + "%';"
    # elif str2 != '':
    #     sql = sql + "and piece.name like '%" + str2 + "%';"
    # else:
    #     Label(master=frm, text='input valid', font=('Arial', 18)).grid(row=5, column=0)
    #     return
    sql = "SELECT opus, piece.name, piece.composer, piece.album, composer.birthplace FROM piece, composer WHERE piece.composer = composer.name "

    if str1 != '' and str2 != '':
        sql += "AND opus LIKE '%" + str1 + "%' AND piece.name LIKE '%" + str2 + "%'"
    elif str1 != '':
        sql += "AND opus LIKE '%" + str1 + "%'"
    elif str2 != '':
        sql += "AND piece.name LIKE '%" + str2 + "%'"
    else:
        Label(master=frm, text='input valid', font=('Arial', 18)).grid(row=5, column=0)
        return

    sql += ";"  # 添加分号表示 SQL 查询的结束

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

def exec_update(frm, opus, new_album):# 更新专辑信息
    sql = "call update_album('" + opus + "', '" + new_album + "');"
    try:
        cursor.execute(sql)
        messagebox.showinfo(message='update successfully.')
    except Exception as m:
        messagebox.showerror('error', m.args)

def search_composer():# 查找作曲家界面
    frm = Toplevel()
    frm.rowconfigure([0, 1, 2, 3, 4], minsize=50)
    frm.columnconfigure(0, minsize=50)
    Label(master=frm, text='name:', font=('Arial', 18)).grid(row=0, column=0)
    e1 = Entry(master=frm, font=('Arial', 18), width=20)
    e1.grid(row=1, column=0)
    click = lambda:exec_search_composer(frm, e1.get())
    Button(master=frm, text='search', command=click).grid(row=3, column=0)

def exec_search_composer(frm, str1):# 查找作曲家
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

def add_piece():# 添加曲子界面
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


def exec_add_piece(frm, opus, name, composer, album):# 添加曲子
    sql = "insert into piece values('" + opus + "', '" + name + "', '" + composer + "', '" + album + "');"
    try:
        cursor.execute(sql)
        messagebox.showinfo(message="Successful!")
    except Exception as m:
        messagebox.showerror("error", m.args)

def add_composer():# 添加编曲者界面
    frm = Toplevel()
    frm.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], minsize=50)
    frm.columnconfigure(0, minsize=50)

    Label(master=frm, text='name:', font=('Arial', 18)).grid(row=0, column=0)
    e1 = Entry(master=frm, font=('Arial', 18), width=20)
    e1.grid(row=1, column=0)
    Label(master=frm, text='birth_date:', font=('Arial', 18)).grid(row=2, column=0)
    e2 = Entry(master=frm, font=('Arial', 18), width=20)
    e2.grid(row=3, column=0)
    Label(master=frm, text='death_date:', font=('Arial', 18)).grid(row=4, column=0)
    e3 = Entry(master=frm, font=('Arial', 18), width=20)
    e3.grid(row=5, column=0)
    Label(master=frm, text='country:', font=('Arial', 18)).grid(row=6, column=0)
    e4 = Entry(master=frm, font=('Arial', 18), width=20)
    e4.grid(row=7, column=0)

    click = lambda: exec_add_composer(frm, e1.get(), e2.get(), e3.get(), e4.get())
    Button(master=frm, text='add', command=click).grid(row=8, column=0)

def exec_add_composer(frm, name, birth_time='', death_time='', country=''):# 添加编曲者
    sql = "insert into composer values('" + name + "', '" + birth_time + "', '" + death_time + "', '" + country + "');"
    try:
        cursor.execute(sql)
        messagebox.showinfo(message="Successful!")
    except Exception as m:
        messagebox.showerror("error", m.args)

def add_album():
    frm = Toplevel()
    frm.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], minsize=50)
    frm.columnconfigure(0, minsize=50)

    Label(master=frm, text='name:', font=('Arial', 18)).grid(row=0, column=0)
    e1 = Entry(master=frm, font=('Arial', 18), width=20)
    e1.grid(row=1, column=0)
    Label(master=frm, text='pulish_date:', font=('Arial', 18)).grid(row=2, column=0)
    e2 = Entry(master=frm, font=('Arial', 18), width=20)
    e2.grid(row=3, column=0)
    Label(master=frm, text='company:', font=('Arial', 18)).grid(row=4, column=0)
    e3 = Entry(master=frm, font=('Arial', 18), width=20)
    e3.grid(row=5, column=0)
    Label(master=frm, text='performer:', font=('Arial', 18)).grid(row=6, column=0)
    e4 = Entry(master=frm, font=('Arial', 18), width=20)
    e4.grid(row=7, column=0)

    click = lambda: exec_add_album(frm, e1.get(), e2.get(), e3.get(), e4.get())
    Button(master=frm, text='add', command=click).grid(row=8, column=0)

def exec_add_album(frm, name, publish_time='', company='', performer=''):
    sql = "insert into album values('" + name + "', '" + publish_time + "', '" + company + "', '" + performer + "');"
    try:
        cursor.execute(sql)
        messagebox.showinfo(message="Successful!")
    except Exception as m:
        messagebox.showerror("error", m.args)


def delete_piece():# 删除曲子界面
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


def exec_delete_piece(frm, opus, composer):# 删除曲子
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
    
def confirm(frm, del_sql):# 确认执行commit
    cursor.execute("START TRANSACTION")
    cursor.execute(del_sql)
    cursor.execute("COMMIT")
    messagebox.showinfo(message='Delete successfully.')
    
def cancel(frm, del_sql):# 取消执行rollback
    cursor.execute("START TRANSACTION")
    cursor.execute(del_sql)
    cursor.execute("ROLLBACK")
    messagebox.showinfo(message='Deletion canceled.')

def onCloseOtherFrame(otherFrame):
    otherFrame.destroy()
    window.update()
    window.deiconify() # 将主窗口恢复显示

def db_init():
    # 连接数据库
    cnx = pymysql.connect(
        host="localhost",
        user="root",
        password="111111",
    )

    # 创建数据库
    cursor = cnx.cursor()
    # 删除已存在的数据库（music）
    cursor.execute("DROP DATABASE IF EXISTS music")

    # 创建新的数据库（music）
    cursor.execute("CREATE DATABASE music CHARACTER SET utf8mb4")
    cursor.close()


    # 切换到创建的数据库
    # cnx.database = "music"
    cursor = cnx.cursor()
    cursor.execute("USE music")
    cursor.close()

    # 创建表
    cursor = cnx.cursor()
    create_album_table_query = """
    CREATE TABLE album (
      name VARCHAR(100) NOT NULL,
      publish_time DATE DEFAULT NULL,
      company VARCHAR(100) DEFAULT NULL,
      performer VARCHAR(100) DEFAULT NULL,
      PRIMARY KEY (name)
    )
    """
    cursor.execute(create_album_table_query)
    cnx.commit()
    cursor.close()

    # 插入数据
    cursor = cnx.cursor()
    insert_album_data_query = """
    INSERT INTO album (name, publish_time, company, performer)
    VALUES
      ('album1', '2002-05-28', 'company1', 'A'),
      ('album2', '1990-11-12', 'company1', 'B'),
      ('album3', '2012-07-09', 'company2', 'C'),
      ('album4', '2018-08-12', 'company2', 'D')
    """
    cursor.execute(insert_album_data_query)
    cnx.commit()
    cursor.close()

    # 创建composer表
    cursor = cnx.cursor()
    create_composer_table_query = """
    CREATE TABLE composer (
      name VARCHAR(100) NOT NULL,
      birth_time VARCHAR(100) DEFAULT NULL,
      death_time VARCHAR(100) DEFAULT NULL,
      birthplace VARCHAR(100) DEFAULT NULL,
      PRIMARY KEY (name)
    )
    """
    cursor.execute(create_composer_table_query)
    cnx.commit()
    cursor.close()

    cursor = cnx.cursor()
    create_piece_table_query = """
    CREATE TABLE piece (
      opus VARCHAR(100) NOT NULL,
      name VARCHAR(100) DEFAULT NULL,
      composer VARCHAR(100) NOT NULL,
      album VARCHAR(100) DEFAULT NULL,
      PRIMARY KEY (Opus, composer),
      FOREIGN KEY (composer) REFERENCES composer (name),
      FOREIGN KEY (album) REFERENCES album (name)
    )
    """
    cursor.execute(create_piece_table_query)
    cnx.commit()
    cursor.close()



    # 创建触发器
    cursor = cnx.cursor()
    create_trigger_query = """
    CREATE TRIGGER check_insert_piece BEFORE INSERT ON piece FOR EACH ROW
    BEGIN
        DECLARE composer_count INT;
        SELECT COUNT(*) INTO composer_count FROM composer WHERE name = NEW.composer;
        IF composer_count = 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Composer does not exist.';
        END IF;
    END
    """
    cursor.execute(create_trigger_query)
    cnx.commit()
    cursor.close()

    # 创建存储过程
    cursor = cnx.cursor()
    create_procedure_query = """
    CREATE PROCEDURE update_album(IN opus_name VARCHAR(50), IN album_name VARCHAR(50))
    BEGIN
        DECLARE album_count INT;
        SELECT COUNT(*) INTO album_count FROM album WHERE name = album_name;
        IF album_count = 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Album does not exist.';
        ELSE
            UPDATE piece SET album = album_name WHERE Opus LIKE CONCAT('%', opus_name, '%');
        END IF;
    END
    """
    cursor.execute(create_procedure_query)
    cnx.commit()
    cursor.close()

    # 关闭数据库连接
    cnx.close()


#
db_init()

db = pymysql.connect(host="localhost", user="root", password="111111", database="music", port=3306, autocommit=True, charset="utf8mb4")
# 创建游标对象
cursor = db.cursor()

#存composer
with open('composer.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 跳过标题行

    # 逐行读取CSV文件数据并插入到数据库
    for row in csv_reader:
        name, birth_time, death_time, birthplace = row

        # 检查每一项是否为空，如果为空则设为字符串 'NULL'
        if not name:
            name = 'NULL'
        if not birth_time:
            birth_time = 'NULL'
        if not death_time:
            death_time = 'NULL'
        if not birthplace:
            birthplace = 'NULL'

        # 构建SQL插入语句
        sql = "INSERT INTO composer (name, birth_time, death_time, birthplace) VALUES ('{}', '{}', '{}', '{}');".format(name, birth_time, death_time, birthplace)

        print(sql)
        # 执行SQL插入语句
        try:
            cursor.execute(sql)
        except:
            continue




#存piece
with open('data/piece.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 跳过标题行

    # 逐行读取CSV文件数据并插入到数据库
    for row in csv_reader:
        opus, name, composer, album = row



        # 检查每一项是否为空，如果为空则设为字符串 'NULL'
        if not opus:
            opus = 'NULL'
        if not name:
            name = 'NULL'
        if not composer:
            composer = 'NULL'
        if not album:
            album = 'NULL'

        # 构建SQL插入语句
        sql = "INSERT INTO piece (opus, name, composer, album) VALUES ('{}', '{}', '{}', '{}');".format(opus, name, composer, album)

        print(sql)
        # 执行SQL插入语句
        cursor.execute(sql)

window = Tk()
window.title('数据库系统作业')
window.rowconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50)
window.columnconfigure(0, minsize=50)
#初始化主界面
l = Label(master=window, text="my favorite pieces", font = ('Arial', 30), width = 20).grid(row=0, column=0)
btn_search_piece = Button(master=window, text="search piece", command=search_piece).grid(row=1, column=0)
btn_search_composer = Button(master=window, text="search composer", command=search_composer).grid(row=2, column=0)
btn_add_piece = Button(master=window, text="add piece", command=add_piece).grid(row=3, column=0)
btn_add_composer = Button(master=window, text="add composer", command=add_composer).grid(row=4, column=0)
btn_add_album = Button(master=window, text="add album", command=add_album).grid(row=5, column=0)
btn_delete_piece = Button(master=window, text="delete piece", command=delete_piece).grid(row=6, column=0)

window.mainloop()