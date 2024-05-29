from .db_connect import myDB
from .user import User
from peewee import *

class DonHang(Model):
    id = IntegerField(column_name='id', primary_key=True)
    iduser = ForeignKeyField(User, field='id', column_name='iduser')
    diachi = TextField()
    sodienthoai = TextField()
    email = TextField()
    soluong = IntegerField()
    tongtien = IntegerField()
    trangthai = IntegerField()

    class Meta:
        database = myDB


if __name__ == '__main__':
    record = DonHang.select()
    for r in record:
        print(r.diachi)