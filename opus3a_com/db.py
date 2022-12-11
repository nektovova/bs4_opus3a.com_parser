import sqlite3
import datetime

# нужна 
# 1) функция добавления новой строки с проверкой на дубликат
# 2) функция которая запускается в конце работы скрипта - если строка не обновилась или она не добавлена сегодня, то мы ее удаляем или ставим статус 0, отстуствует, мы ее на сайт выводить не будем

db_name = 'db_with_images.db'
def create_table():
    # it will create a databse with name sqlite.db
    connection= sqlite3.connect(db_name) 
    cursor= connection.cursor()
    table_query = '''CREATE TABLE IF NOT EXISTS items
                (name text, singer_name text, image text, category text, item_format text, release_year text, barcode text, price int, item_url text, updated_ts text, show int)'''
                
    cursor.execute(table_query)
    # you need to commit changes as well
    connection.commit()
    # you also need to close  the connection
    connection.close()




# сюда надо передать все данные
def add_data(name, singer_name, image, category, item_format, release_year, barcode, price, item_url):
    connection = sqlite3.connect(db_name) 
    # student list 
    cursor= connection.cursor()

    # отправка команд с переменными к sqlite обязательно в таком формате
    cursor.execute("SELECT * FROM items WHERE item_url = ?", [item_url])
    result = cursor.fetchone()
    if result:  # result could be None or tuple (record)
        # print('In base already, price recheck need to code')
        connection.close()
    else:
        # print("Not in base, add it!!!")
        # кавычки экранируются если мы юзаем двойные кавычки
        updated_ts = datetime.datetime.now()
        q = f'INSERT INTO items VALUES ("{name}","{singer_name}","{image}","{category}","{item_format}","{release_year}","{barcode}","{price}","{item_url}","{updated_ts}", 0)'

        # executing the insert queries

        cursor.execute(q)

        # you need to commit changes as well
        connection.commit()
        connection.close()




def get_data():
    connection= sqlite3.connect(db_name) 
    cursor= connection.cursor()
    q="Select * from items"

    students_data = cursor.execute(q)
    for data in students_data:
        print(data)

    # you also need to close  the connection
    connection.close()
    return


def search_in_db(artist_name):
    connection= sqlite3.connect(db_name) 
    cursor= connection.cursor()
    search_query = "%"+artist_name+"%"
    q="Select * from items WHERE singer_name LIKE '%s'" % search_query

    search_results = cursor.execute(q)
    search_results = search_results.fetchall()
    print(search_results)
    return(search_results)