import psycopg2

dataBase = psycopg2.connect(
    host="localhost",
    user='postgres',
    password='admin',
)
dataBase.set_session(autocommit=True)

cursorObject = dataBase.cursor()
cursorObject.execute("CREATE DATABASE demo_crm")
print("Database created")

dataBase.close()