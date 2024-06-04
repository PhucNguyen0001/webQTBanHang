from db_connect import myDB
from sanphammoi import SanPhamMoi
from donhang import DonHang
from peewee import *

class ChiTietDonHang(Model):
    iddonhang = ForeignKeyField(DonHang, column_name='iddonhang', field='id')
    idsp = ForeignKeyField(SanPhamMoi, column_name='idsp', field='id')
    soluong = IntegerField()
    gia = IntegerField()

    class Meta:
        database = myDB
        primary_key = CompositeKey('iddonhang', 'idsp')


if __name__ == '__main__':
    record = ChiTietDonHang.select()
    for r in record:
        print(r.iddonhang, r.idsp)