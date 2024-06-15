from .db_connect import myDB
from .sanpham import SanPham
from peewee import *

class SanPhamMoi(Model):
    id = IntegerField(column_name='id', primary_key=True)
    tensp = TextField()
    giasp = IntegerField()
    hinhanh = TextField()
    mota = TextField()
    loai = ForeignKeyField(SanPham, backref='type', field='id', column_name='loai')
    loaianh = TextField()

    class Meta:
        database = myDB


if __name__ == '__main__':
    record = SanPhamMoi.select()
    for r in record:
        print(r.hinhanh)