import datetime

from donhang import DonHang
from sanpham import SanPham
from sanphammoi import SanPhamMoi
from chitietdonhang import ChiTietDonHang
from user import User
from peewee import *
from db_connect import myDB

arr_trangthai = ['Chưa xác nhận', 'Đã xác nhận', 'Đang giao hàng', 'Đã nhận hàng']
def get_sanpham():
    query = ((SanPhamMoi
              .select(SanPhamMoi, SanPham)
              .join(SanPham, attr='sanPham')
              .where(SanPhamMoi.loai == SanPham.id)))
    return query

def get_dsdonhang():
    query = (DonHang
             .select(DonHang, User.username)
             .join(User, attr='user_dh')
             .where(DonHang.iduser == User.id))
    return [{
        "receiver": record.user_dh.username,
        "address": record.diachi,
        "phone_number": record.sodienthoai,
        "order_date": record.ngaydathang.strftime('%Y-%m-%d'),
        "total": record.tongtien,
        "status": arr_trangthai[record.trangthai]
    }for record in query]
    # return query

def get_ctdonhang(id_donhang):
    query = (ChiTietDonHang
             .select(ChiTietDonHang, SanPhamMoi)
             .join(SanPhamMoi, attr='sanPhamMoi')
             .where((ChiTietDonHang.iddonhang == id_donhang)
                    & (SanPhamMoi.id == ChiTietDonHang.idsp)))
    return query


def get_user():
    # query = User.select()
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
    } for record in User.select()]


def get_tongtien():
    return DonHang.select(fn.SUM(DonHang.tongtien)).scalar()


def get_tongtientheothang():
    year, month = datetime.date.today().year, datetime.date.today().month
    total_amount = (DonHang
                    .select(fn.SUM(DonHang.tongtien))
                    .where((fn.YEAR(DonHang.ngaydathang) == year) &
                           (fn.MONTH(DonHang.ngaydathang) == month))
                    .scalar())
    return total_amount


def get_demdonht():
    return (DonHang
            .select(fn.COUNT(DonHang.id))
            .where(DonHang.trangthai == 3)
            .scalar())


def get_donchuaht():
    return (DonHang
            .select(fn.COUNT(DonHang.id))
            .where(DonHang.trangthai != 3)
            .scalar())


if __name__ == '__main__':
    print(get_donchuaht())
