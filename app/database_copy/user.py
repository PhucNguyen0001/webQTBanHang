from db_connect import myDB
from peewee import *

class User(Model):
    id = IntegerField(column_name='id', primary_key=True)
    email = IntegerField()
    password = IntegerField(column_name='pass')
    username = TextField()
    mobile = TextField()
    uid = TextField()
    diachi = TextField()

    class Meta:
        database = myDB



if __name__ == '__main__':
    record = User.select()
    for r in record:
        print(r.id, r.username)