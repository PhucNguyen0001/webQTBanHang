import peewee as pw

myDB = pw.MySQLDatabase(
    "dataonline",
    host="localhost",
    port=3306,
    user="root",
    passwd=""
)

if __name__ == '__main__':
    myDB.connect()
    print('success')
    myDB.close()

