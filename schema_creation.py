import mysql.connector
conn = mysql.connector.connect(host="localhost",
                                user = "root",
                                password = "Clippers47!",
                                auth_plugin = 'mysql_native_password')


cursor = conn.cursor()

def first_run():
    cursor.execute('''
    CREATE SCHEMA application
    ''')


first_run()
