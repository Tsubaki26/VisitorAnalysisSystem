import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='mysqlkeito1340@',
    db='test_db'
)

cursor = conn.cursor()

# cursor.execute('SHOW TABLES FROM test_db')
cursor.execute('select * from test_table')
# cursor.execute('insert test_table(id, name) value(2, "Bob")')


# for row in cursor.fetchall():
#     print(row)

# cursor.close()
conn.commit()
conn.close()