from .db_connect import myDB
from peewee import *

class SanPham(Model):
    id = IntegerField(column_name='id', primary_key=True)
    tensanpham = TextField()
    hinhanh = TextField()

    class Meta:
        database = myDB


if __name__ == '__main__':
    record = SanPham.select()
    for r in record:
        print(r.hinhanh)