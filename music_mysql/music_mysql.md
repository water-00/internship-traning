# music_mysql说明文档——基础部分

## 系统简介

⼀个简单的个⼈⾳乐收藏数据库，有查询⾳乐、查询作曲家、添加⾳乐、删除⾳乐等功能。

## 功能描述

### CRUD功能描述

#### 1.删除操作

给两个参数str1和str2（其中⼀个可以为空），如果数据库中有该参数的模糊匹配，则找到对应曲⼦

**表连接涉及字段**：where opus like '%" + str1 + "%' and composer like '%" + str2 + "%

##### 代码

``

```
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
```

#### 2.添加操作

添加曲⼦，如果piece.composer不在composer表中，则执⾏触发器

**触发器描述**：如果piece.composer不在composer表中，则执⾏触发器

##### 插⼊操作源码

``

```
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
```

##### 触发器源码

`DELIMITER ;; !50003 CREATE DEFINER=`root`@`localhost`RIGGER `check_insert_piece` BEFORE INSERT ON `piece` FOR EACH ROW begin if new.composer not in (select name from composer) then signal SQLSTATE '45000' set message_text = "composer not exsits."; end if; end */;; DELIMITER ;`

#### 3.更新操作

更改piece中某⾸曲⼦的所属专辑。⽤procedure更改piece.album，要求新的piece.album在album表中。

**表连接涉及字段**：album_name not in (select name from album)

##### 更新代码

``

```
def exec_search_piece(frm, str1, str2):# 曲子查找结果展示以及更新专辑
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
```

##### 创建存储过程源码

```
create procedure update_album(in opus_name varchar(20), in album_name varchar(50))
begin
    if album_name not in (select name from album) then
        signal sqlstate '45000'
        set message_text = 'album not exists.';
    else
        update piece set album = album_name where Opus like CONCAT('%', opus_name, '%');
    end if;
end;
```

##### 存储过程执⾏源码

``

```
def exec_update(frm, opus, new_album):# 更新专辑信息
    sql = "call update_album('" + opus + "', '" + new_album + "');"
    try:
        cursor.execute(sql)
        messagebox.showinfo(message='update successfully.')
    except Exception as m:
        messagebox.showerror('error', m.args)
```

#### 4.查询操作

根据opus, name模糊匹配找到⼀⾸曲⼦。

**表连接字段**：where opus like '%" + str1 + "%' and name like '%" + str2 + "%'

##### 查询代码

``

```
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


def exec_search_piece(frm, str1, str2):# 曲子查找结果展示以及更新专辑
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
```
