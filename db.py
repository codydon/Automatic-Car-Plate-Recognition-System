import mysql.connector as mc
conn = mc.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'image' 
)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS my_table(ID INT AUTO_INCREMENT PRIMARY KEY,number VARCHAR(100) NOT NULL,date VARCHAR(100))")
conn.commit()
cursor.close()