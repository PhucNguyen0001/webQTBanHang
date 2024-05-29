from .donhang import DonHang
from .sanpham import SanPham
from .sanphammoi import SanPhamMoi
from .chitietdonhang import ChiTietDonHang
from .user import User
from peewee import *
from .db_connect import myDB

def get_sanpham():
    query = ((SanPhamMoi
              .select(SanPhamMoi, SanPham)
              .join(SanPham, attr='sanPham')
              .where(SanPhamMoi.loai == SanPham.id)))
    return query

def get_dsdonhang():
    query = DonHang.select()
    result = []
    for record in query:
        result.append({

        })

def get_chitietdonhang(id_donhang):
    query = (ChiTietDonHang
             .select(ChiTietDonHang, SanPhamMoi)
             .join(SanPhamMoi, attr='sanPhamMoi')
             .where((ChiTietDonHang.iddonhang == id_donhang)
                    & (SanPhamMoi.id == ChiTietDonHang.idsp)))
    return query

def get_user():
    query = User.select()
    # result = []
    # for record in query:
    #     result.append({
    #         'Name': record.username,
    #         'Email': record.email,
    #         'Mobile': record.mobile,
    #         'Address': record.diachi,
    #         'Password': record.password
    #     })
    # return result
    return [{
        'Name': record.username,
        'Email': record.email,
        'Mobile': record.mobile,
        'Address': record.diachi,
        'Password': record.password
    } for record in query]


if __name__ == '__main__':
    print(get_user())