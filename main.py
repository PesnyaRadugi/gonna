import sqlite3

try:
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()
    print('Файл создан/открыт')
    
    #cursor.execute("""create table test(
    #id INTEGER PRIMARY KEY,
    #text TEXT NOT NULL);""")

    cursor.execute("""
    UPDATE test SET text = 'first object' WHERE id = 1
    ;""")

    cursor.execute("""
    SELECT * FROM test
    """)
    objects = cursor.fetchall()
    for object in objects:
        for value in object:
            print(value)

    connection.commit()

    cursor.close()
except sqlite3.Error as error:
    print(error) 
finally: 
    if connection:
        connection.close()