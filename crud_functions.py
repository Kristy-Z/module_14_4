import sqlite3

def initiate_db():
     connection = sqlite3.connect("base_module.db")
     cursor = connection.cursor()

     cursor.execute("DROP TABLE IF EXISTS Products")

     cursor.execute('''
     CREATE TABLE IF NOT EXISTS Products(
     id INTEGER PRIMARY KEY,
     title TEXT NOT NULL,
     description TEXT,
     price INTEGER NOT NULL
     )
     ''')

     cursor.execute("CREATE INDEX IF NOT EXISTS idx_id ON Products(id)")

     for i in range(1, 5):
          cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                         (f"Турбослим {i}", f"Минус калории {i} ", f"{i*1000}"))

     connection.commit()
     connection.close()


#get_all_products возвращает все записи из таблицы Products
def get_all_products():
     connection = sqlite3.connect("base_module.db")
     cursor = connection.cursor()
     products = cursor.execute('SELECT * FROM Products').fetchall()
     connection.close()
     return products
