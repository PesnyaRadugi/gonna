import sqlite3


class DataBase:
    def __init__(self, name):
        self.test = 'test'
        self.tables = []
        self.connection = sqlite3.connect(f'{name}.db')
        self.cursor = self.connection.cursor()

    def try_add_table(self, name):
        try:
            self.cursor.execute(f"""
            CREATE TABLE {name} (
            id INTEGER PRIMARY KEY);
            """)
        except:
            pass

    def __delete__(self, instance):
        self.connection.close()
        super().__delete__(self, instance)

    def try_add_columns(self, table, **kwargs):
            for name_of_column, type_of_column, in kwargs.items():
                try:
                    self.cursor.execute(f"""ALTER TABLE {table.name} ADD COLUMN {name_of_column} {type_of_column};""")
                    self.connection.commit()
                except:
                    pass

    def get_table_objects(self, table):
        self.cursor.execute(f"""SELECT * FROM {table.name};""")
        return self.cursor.fetchall()

    def get_table_object(self, table, name_of_column, value_of_column):
        self.cursor.execute(f"""
        SELECT * FROM {table.name}
        WHERE {name_of_column} = {value_of_column};
        """)
        return self.cursor.fetchall()

    def create_table_object(self, table, *args):
        try: #боже, как ты заебал, держи свой трай, харе засирать теминал, что объект уже существует
            parameters = ""
            for ele in args:
                if isinstance(ele, str):
                    parameters += "'" + str(ele) + "'" + ','
                else:
                    parameters += str(ele) + ','
            parameters = parameters[:-1]
            self.cursor.execute(f"""
                INSERT INTO {table.name}({','.join(table.colums.keys())})
                VALUES ({parameters});
                """)
        except:
            pass

        self.connection.commit()

    def update_table_object(self, table, name_of_column, value_of_column, *args):
        try:
            for index, column in enumerate(list(table.colums.keys())[1:]):
                self.cursor.execute(f"""
                    UPDATE {table.name} SET {column} = {args[index] if isinstance(args[index], int) else "'" + args[index] + "'"}
                    WHERE {name_of_column} = {value_of_column};
                    """)
                self.connection.commit()
        except: 
            pass

    def delete_table_object(self, table, name_of_columnm, value_ofcolumn):
        self.cursor.execute(f"""
            DELETE FROM {table.name}
            WHERE {name_of_columnm} = {value_ofcolumn}
        """)
        self.connection.commit()

    def get_info(self, table):
        self.cursor.execute(f"""PRAGMA table_info({table.name});""")
        return self.cursor.fetchall()

class Table:
    def __init__(self, name, database):
        self.colums = {}
        self.database = database
        self.name = name
        self.database.try_add_table(name)
        for column in self.database.get_info(self):
            self.colums[column[1]] = column[2]

    def add_columns(self, **kwargs):
        for name_of_column, type_of_column in kwargs.items():
            self.colums[name_of_column] = type_of_column
        self.database.try_add_columns(self, **kwargs)

    def get_objects(self):
        return self.database.get_table_objects(self)

    def get_object(self, name_of_column, value_of_column):
        return self.database.get_table_object(self, name_of_column, value_of_column)
    
    def create_object(self, *args):
        self.database.create_table_object(self, *args)
    
    def update_object(self, name_of_column, value_of_column, *args):
        self.database.update_table_object(self, name_of_column, value_of_column, *args)
    
    def delete_object(self, name_of_column, value_of_column):
        self.database.delete_table_object(self, name_of_column, value_of_column)

#Новые экземпляры класса
db = DataBase('test')
pets = Table('pets', db)


# Манипуляции со столбцами
columns = {'name': 'TEXT'}
pets.add_columns(**columns)
print(pets.colums)


# Добавление строк
pets.create_object(1, 'ALice')
print(pets.colums.keys())
print(pets.update_object('id', 1, 'Ben'))
print(pets.get_object('id', 1))
pets.delete_object('id', 1)
print(pets.get_object('id', 1))
