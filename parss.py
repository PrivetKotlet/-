import sqlite3
from colorama import Fore




class sq:
    list_for_rep= ["ID: ","ФИО: ","КОФЕЙНЯ: ","ДОЛЖНОСТЬ: ","СТАТУС: ","КОНТАКТ: ","ВРЕМЯ: ","ДАТА: ","Комментарий: "]
    list_for_dem_rep = ["ID: ",'Дата: ', 'Должность: ','Временной промеуток: ','Кофейня: ']

    def open_bd():
        try:
            global sqlite_connection 
            global cursor
            sqlite_connection = sqlite3.connect('h.db')
            cursor = sqlite_connection.cursor()
        except sqlite3.Error as error:
            print( Fore.RED + "Ошибка при подключении к sqlite", error)
            
    def parss_YK_pass(a):
        mass = []
        s = 0
        for i in a:
            mass  += a[s]
            s += 1
        mass = list(map(str, mass))
        return mass

    def parss(a):
        mass = []
        s = 0
        for i in a:
            mass  += a[s]
            s += 1
        return mass
    
    def parss_2(replacement,ind):
        p = 0 
        res = ''''''
        for i in replacement:
            a = list(replacement[p]) 
            p2 = 0
            for it in a:
                res += ind[p2] + str(it) + '\n'
                p2 += 1
            res += '\n'    
            p+=1
        return res
 
    class select():

        def get_admin_login():
            sq.open_bd()
            admin_login = cursor.execute('SELECT "логин" FROM админка;').fetchall()
            return sq.parss(admin_login)

        def get_admin_password():
            sq.open_bd()
            admin_password = cursor.execute('SELECT "пароль" FROM админка;').fetchall()
            return sq.parss(admin_password)
        
        def get_yk_password():
            sq.open_bd()
            password = cursor.execute('SELECT "Пароль" FROM кафейни;').fetchall()
            return sq.parss_YK_pass(password)

        def chek(login,password):
            if login in sq.select.get_admin_login() and password in str(sq.select.get_admin_password()):
                return True
            else:
                return False

        def get_workers(coffee_house):
            sq.open_bd()
            a = cursor.execute(f'SELECT "Ф.И.О" FROM user Where каф = "{coffee_house}";').fetchall()
            return sq.parss(a)

        def get_coffee_house(password_yk):
            sq.open_bd()
            coffee_house = str(cursor.execute(f"SELECT кофейня FROM кафейни where Пароль = '{password_yk}';").fetchall()).replace("'","").replace("[(","").replace(")]","").replace(",","")
            return coffee_house

        def select_replacement_post(Coffee_house,name):
            sq.open_bd()
            fio = str(cursor.execute(f'''SELECT Должность FROM user where каф = '{Coffee_house}' and "Ф.И.О" = '{name}';''').fetchall()).replace("'","").replace("[(","").replace(")]","").replace(",","")
            return fio   

        def select_replacement_contact(Coffee_house,name):
            sq.open_bd()
            fio = str(cursor.execute(f'''SELECT контакт FROM user where каф = '{Coffee_house}' and "Ф.И.О" = '{name}';''').fetchall()).replace("'","").replace("[(","").replace(")]","").replace(",","")
            return fio   

        def select_replacement():
            sq.open_bd()
            replacement =cursor.execute(f'''SELECT ID, "Ф.И.О",каф, Должность,статус,контакт,"Временные возможности",День, комментарий FROM замены Where статус = 'Свободный' 
            ''').fetchall()
            return sq.parss_2(replacement,sq.list_for_rep)

        def select_choosed_replacement(coffe_house):
            sq.open_bd()
            replacement =cursor.execute(f'''SELECT ID, "Ф.И.О",каф, Должность,статус,контакт,"Временные возможности",День FROM замены Where статус = '{coffe_house}' 
            ''').fetchall()
            return sq.parss_2(replacement,sq.list_for_rep)

        def select_my_replacement(coffe_house):
            sq.open_bd()
            replacement =cursor.execute(f'''SELECT ID, "Ф.И.О",каф, Должность,статус,контакт,"Временные возможности",День FROM замены Where статус = 'Свободный' And каф = '{coffe_house}' 
            ''').fetchall()
            return sq.parss_2(replacement,sq.list_for_rep)


        def select_demanding_replacement():
            sq.open_bd()
            replacement =cursor.execute(f'''SELECT ID, Дата,Должность,"Временной промежуток",Кофейня FROM [Требуемые замены]; ''').fetchall()
            return sq.parss_2(replacement,sq.list_for_dem_rep)

        def select_replacementByID(id):
            sq.open_bd()
            replacement =cursor.execute(f'''SELECT ID, "Ф.И.О",каф, Должность,статус,контакт,"Временные возможности",День FROM замены Where ID = '{id}' 
            ''').fetchall()
            return sq.parss_2(replacement,sq.list_for_rep)

        def select_coffee_house_for_chek(id):
            sq.open_bd()
            coffe_house_name = cursor.execute(f'''SELECT каф from замены where ID == '{id}' And статус == 'Свободный' ''').fetchone()
            coffe_house_name = str(coffe_house_name).replace("'","").replace("(","").replace(")","").replace(",","")
            return coffe_house_name

        def select_coffee_houseByID(id):
            sq.open_bd()
            coffe_house_name = cursor.execute(f'''SELECT каф from замены where ID = '{id}' ''').fetchone()
            coffe_house_name = str(coffe_house_name).replace("'","").replace("(","").replace(")","").replace(",","")
            return coffe_house_name

        def select_coffee_houseByID_dm(id):
            sq.open_bd()
            coffe_house_name = cursor.execute(f'''SELECT Кофейня from [Требуемые замены] where ID = '{id}' ''').fetchone()
            coffe_house_name = str(coffe_house_name).replace("'","").replace("(","").replace(")","").replace(",","")
            return coffe_house_name

        def select_id():
            sq.open_bd()
            id = cursor.execute(f'''SELECT ID from замены''').fetchall()
            return sq.parss(id)

        def select_iddm():
            sq.open_bd()
            id = cursor.execute(f'''SELECT ID from [Требуемые замены] ''').fetchall()
            return sq.parss(id)

        def select_id_for_my_replacement(coffe_house):
            sq.open_bd()
            id = cursor.execute(f'''SELECT ID from замены Where статус = 'Свободный' And каф = '{coffe_house}' ''').fetchall()
            return sq.parss(id)
            
        def select_user_id(coffe_house):
            sq.open_bd()
            id = cursor.execute(f'''SELECT chat_id FROM кафейни Where кофейня = '{coffe_house}'  ''').fetchone()
            id = str(id).replace("'","").replace("(","").replace(")","").replace(",","")
            if id == 'None':
                return None
            else:
                return int(id)

    class insert():

        def insert_worker(FIO,COFFE_HOUSE,post,CONTACT_WORKERS ):
            sq.open_bd()
            cursor.execute(f'''INSERT INTO user ([Ф.И.О], каф, Должность, контакт) VALUES  ('{FIO}','{COFFE_HOUSE}','{post}','{CONTACT_WORKERS}');''')
            sqlite_connection.commit()

        def insert_coffee_house(COFFE_HOUSE,YK,password_YK):
            sq.open_bd()
            cursor.execute(f'''INSERT INTO кафейни (кофейня,УК,Пароль) VALUES ( '{COFFE_HOUSE}', '{YK}', '{password_YK}')''')
            sqlite_connection.commit()

        def insert_replacement(FIO_rep,Coffe_House,post,contact,time_l,day,comment):
            sq.open_bd()
            cursor.execute(f'''INSERT INTO замены ([Ф.И.О],каф,Должность,статус,контакт,[Временные возможности],День,комментарий)VALUES ('{FIO_rep}','{Coffe_House}','{post}','Свободный','{contact}','{time_l}','{day}','{comment }');''')
            sqlite_connection.commit()

        def insert_demanding_replacement(date,Coffe_House,post,time_l):
            sq.open_bd()
            cursor.execute(f'''INSERT INTO [Требуемые замены] ( Дата,Должность,[Временной промежуток],Кофейня)VALUES ('{date}','{post}','{time_l}','{Coffe_House}' ) ''')
            sqlite_connection.commit()


    class update():

        def update_replacement(id,status):
            sq.open_bd()
            cursor.execute(f'''UPDATE замены SET статус = '{status}' WHERE ID = '{id}' ''')
            sqlite_connection.commit()
        
        def update_time_replacement(id,time):
            sq.open_bd()
            cursor.execute(f'''UPDATE замены SET [Временные возможности] = '{time}' WHERE ID = '{id}' ''')
            sqlite_connection.commit()

        def update_date_replacement(id,day):
            sq.open_bd()
            cursor.execute(f'''UPDATE замены SET  День = '{day}' WHERE ID = '{id}' ''')
            sqlite_connection.commit()

        def update_choosed_replacement(status,id):
            sq.open_bd()
            cursor.execute(f'''UPDATE замены SET  статус = 'Свободный' WHERE статус = '{status}' AND ID = '{id}' ''')
            sqlite_connection.commit()
         
        def update_user_id(id,coffe_house):
            sq.open_bd()
            cursor.execute(f'''UPDATE кафейни SET  chat_id = '{id}' WHERE кофейня = '{coffe_house}' ''')
            sqlite_connection.commit()

    class delete():

        def delete_replacment(id,coffe_house):
            sq.open_bd()
            cursor.execute(f'''DELETE FROM замены WHERE ID = '{id}' AND каф = '{coffe_house}' AND статус == 'Свободный'  ''')
            sqlite_connection.commit()

        def delete_coffe_house(coffe_house):
            sq.open_bd()
            cursor.execute(f'''DELETE FROM кафейни  WHERE кофейня = '{coffe_house}'   ''')
            sqlite_connection.commit()

        def delete_workers(coffe_house,FIO):
            sq.open_bd()
            cursor.execute(f'''DELETE FROM user WHERE "Ф.И.О" = '{FIO}' AND каф = '{coffe_house}'    ''')
            sqlite_connection.commit()
            
        def delete_demanding_replacment(ID):
            sq.open_bd()
            cursor.execute(f'''DELETE FROM [Требуемые замены] WHERE ID = '{ID}' ''')
            sqlite_connection.commit()
        