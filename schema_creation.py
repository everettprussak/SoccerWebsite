import mysql.connector

#change password for your personal password!
conn = mysql.connector.connect(host="localhost",
                                user = "root",
                                password = "Clippers47!",
                                auth_plugin = 'mysql_native_password')


cursor = conn.cursor()


# creating the schema called application
def first_run():
    cursor.execute('''
    CREATE SCHEMA application
    ''')


first_run()

print(conn)
conn.close()
