import  psycopg2
from config import host, user, password, bd_name

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS username (
                id SERIAL PRIMARY KEY,
                name VARCHAR(25) UNIQUE,
                surname varchar(25) NOT NULL,
                email varchar(30) NOT NULL
            );""")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone (
                id SERIAL PRIMARY KEY,
                phon INTEGER,
                fk_phone INTEGER NOT NULL REFERENCES username(id)
            );""")
    conn.commit()    
    return cur.fetchone()[0]
#Функция, создающая структуру БД (таблицы).

def add_client(conn, name, surname, email):
    with conn.cursor() as cur:
        cur.execute(f"INSERT INTO username (name, surname, email) VALUES ('{name}', '{surname}', '{email}');")
        
    conn.commit()
#Функция, позволяющая добавить нового клиента.
 
def add_phone(conn, fk_phone, phone):
    with conn.cursor() as cur:
        cur.execute("""
                 SELECT id FROM username WHERE surname=%s;
                 """, (surname,))
        fk_phone = cur.fetchone()
        cur.execute("""
                INSERT INTO phone(phon, fk_phone) VALUES(%s, %s);
                """, (phone, fk_phone))
        conn.commit() 
#Функция, позволяющая добавить телефон для существующего клиента.

def change_client(conn, client_id, first_name, last_name, email, phones, newname):
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT id FROM username WHERE surname=%s;
                    """, (last_name,))
        def get_newname_id(cur, last_name: str) -> int:
            cur.execute("""
            SELECT id FROM username WHERE name=%s;
            """, (last_name,))
            return cur.fetchone()[0]
        lastname_id = get_newname_id(cur, last_name)
        cur.execute("""
        UPDATE username SET name=%s, surname=%s, email=%s WHERE id=%s;
        """, (first_name, newname, email, lastname_id))
        cur.execute("""
        UPDATE phone SET phon=%s WHERE fk_phone=%s;
        """, (phones, lastname_id))
        
        conn.commit()
#Функция, позволяющая изменить данные о клиенте.

def delete_phone(conn, phones):
    with conn.cursor() as cur:
        cur.execute("""
                 SELECT id FROM phone WHERE phon=%s;
                 """, (phones,))
        fk_phone = cur.fetchone()
        cur.execute("""
                DELETE FROM phone WHERE id=%s;
                """, (fk_phone))
        conn.commit() 
#Функция, позволяющая удалить телефон для существующего клиента.

def delete_client(conn, last_name):
    with conn.cursor() as cur:
        cur.execute("""
                 SELECT id FROM username WHERE surname=%s;
                 """, (last_name,))
        client_id = cur.fetchone()
        cur.execute("""
                DELETE FROM phone WHERE fk_phone=%s;
                """, (client_id))
        
        cur.execute("""
                DELETE FROM username WHERE id=%s;
                """, (client_id))
        conn.commit() 
#Функция, позволяющая удалить существующего клиента.

def find_client(conn, first_name, last_name, email, phone):
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT id FROM username WHERE surname=%s;
                    """, (last_name,))
        def get_newname_id(cur, last_name: str) -> int:
            cur.execute("""
            SELECT id FROM username WHERE name=%s;
            """, (last_name,))
            return cur.fetchone()[0]
        lastname_id = get_newname_id(cur, last_name)
        cur.execute("""
        UPDATE username SET name=%s, surname=%s, email=%s WHERE id=%s;
        """, (first_name, newname, email, lastname_id))
        cur.execute("""
        UPDATE phone SET phon=%s WHERE fk_phone=%s;
        """, (phones, lastname_id))
        
        conn.commit()
        cur.execute("""
        SELECT * FROM course;
        """)
        print('fetchall', cur.fetchall())
#Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону. 


with psycopg2.connect(host=host, database=bd_name, user=user, password=password)  as conn:
    #print('Возможные команды: 1, 2, 3, 4, 5, 6, 7')
    comand = input('Введите название команды ')
 
    if comand == '1':
        create_db(conn)
    
    elif comand == '2':
        name = input("Введите имя: ")
        surname = input("Введите фамилию: ")
        email = input("Введите email: ")
        
        add_client(conn, name, surname, email)
    
    elif comand == '3':
        phone = int(input("Введите телефон: "))
        surname = input("Введите фамилию: ")
        fk_phone = int()
        add_phone(conn, fk_phone, phone)
            
    elif comand == '4':
        client_id = int()
        last_name = input("Введите фамилию пользователя данные которого необходимо заменить: ")
        first_name = input("Введите имя: ")
        newname = input("Введите фамилию: ")
        email = input("Введите email: ")
        phones = int(input("Введите телефон: "))
        change_client(conn, client_id, first_name, last_name, email, phones, newname)

    elif comand == '5':
        phones = int(input("Введите телефон для удаления: "))

        delete_phone(conn, phones)

    elif comand == '6':
        last_name = input("Введите фамилию пользователя данные которого необходимо удалить: ")

        delete_client(conn, last_name)

    elif comand == '7':
        first_name = input("Введите имя: ")
        last_name = input("Введите фамилию: ")
        email = input("Введите email: ")
        phone = int(input("Введите телефон: "))

        print(find_client(conn, first_name, last_name, email, phone))

                                                                                                                                                                
    
        

conn.close()

   