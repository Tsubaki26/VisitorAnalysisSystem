import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='mysqlkeito1340@',
    db='visitor_analysis_system'
)

cursor = conn.cursor()

# cursor.execute('SHOW TABLES FROM test_db')
cursor.execute('select * from number_plate')
# cursor.execute('insert test_table(id, name) value(2, "Bob")')


for row in cursor.fetchall():
    print(row)

# cursor.close()
# conn.commit()
conn.close()