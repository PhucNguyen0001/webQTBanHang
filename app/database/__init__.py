import datetime
import base64

from .donhang import DonHang
from .sanpham import SanPham
from .sanphammoi import SanPhamMoi
from .chitietdonhang import ChiTietDonHang
from .user import User
from peewee import *
from .db_connect import myDB

arr_trangthai = ['Chưa xác nhận', 'Đã xác nhận', 'Đang giao hàng', 'Đã nhận hàng', 'Đã hủy']


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
        "id": record.id,
        "receiver": record.user_dh.username,
        "address": record.diachi,
        "phone_number": record.sodienthoai,
        "order_date": record.ngaydathang.strftime('%Y-%m-%d'),
        "total": record.tongtien,
        "status": arr_trangthai[record.trangthai],
        "status_int": record.trangthai
    } for record in query]
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
        'id': record.id,
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


def get_money_by_month():
    query = (DonHang
             .select(DonHang.ngaydathang, fn.SUM(DonHang.tongtien))
             .group_by(fn.MONTH(DonHang.ngaydathang))
             .dicts())
    # return list(query)
    ar_month = [record['ngaydathang'].strftime('%B') for record in query]
    ar_data = [record['tongtien'] for record in query]
    return ar_month, ar_data


def get_money_by_type():
    query1 = (ChiTietDonHang
              .select(SanPhamMoi.loai.alias('loai'),
                      fn.SUM(ChiTietDonHang.soluong * ChiTietDonHang.gia).alias('tong_tien'))
              .join(SanPhamMoi)
              .group_by(SanPhamMoi.loai))
    query2 = (SanPham
              .select(SanPham.tensanpham, query1.c.tong_tien)
              .join(query1, on=(SanPham.id == query1.c.loai))
              .dicts())
    ar_tensp = []
    ar_tongtien = []
    for record in query2:
        ar_tensp.append(record['tensanpham'])
        ar_tongtien.append(record['tong_tien'])
    return ar_tensp, ar_tongtien


def get_product():
    query = (SanPhamMoi
             # .select(SanPhamMoi.tensp, SanPhamMoi.giasp, SanPhamMoi.mota, SanPhamMoi.hinhanh, SanPham.tensanpham)
             .select(SanPhamMoi.id,
                     SanPhamMoi.tensp,
                     SanPhamMoi.giasp,
                     SanPhamMoi.mota,
                     SanPham.tensanpham)
             .join(SanPham)
             .dicts())
    return list(query)


def select_product(id):
    query = (SanPhamMoi
             # .select(SanPhamMoi.tensp, SanPhamMoi.giasp, SanPhamMoi.mota, SanPhamMoi.hinhanh, SanPham.tensanpham)
             .select(SanPhamMoi.tensp,
                     SanPhamMoi.giasp,
                     SanPhamMoi.mota,
                     SanPhamMoi.hinhanh,
                     SanPham.tensanpham,
                     SanPhamMoi.id,
                     SanPhamMoi.loaianh)
             .join(SanPham)
             .where(SanPhamMoi.id == id)
             .dicts())
    result = list(query)[0]
    if result['loaianh'] != 'link':
        result['hinhanh'] = f"data:image/{result['loaianh']};base64," + result['hinhanh']
    return result


def suaThongTinSanPham(id, tensp, giasp, hinhanh, mota, loai, loaianh):
    if hinhanh is None:
        query = (SanPhamMoi.update(tensp=tensp,
                                   giasp=giasp,
                                   mota=mota,
                                   loai=loai,
                                   loaianh=loaianh)
                 .where(SanPhamMoi.id == id))
    else:
        query = (SanPhamMoi.update(tensp=tensp,
                                   giasp=giasp,
                                   hinhanh=hinhanh,
                                   mota=mota,
                                   loai=loai,
                                   loaianh=loaianh)
                 .where(SanPhamMoi.id == id))

    query.execute()


def get_loai():
    query = SanPham.select(SanPham.id, SanPham.tensanpham).dicts()
    return list(query)


def themSanPhamMoi(tensp, giasp, hinhanh, mota, loai, loaianh):
    if hinhanh is None:
        query = (SanPhamMoi.insert(tensp=tensp,
                                   giasp=giasp,
                                   mota=mota,
                                   hinhanh='',
                                   loai=loai,
                                   loaianh=loaianh))
    else:
        query = (SanPhamMoi.insert(tensp=tensp,
                                   giasp=giasp,
                                   hinhanh=hinhanh,
                                   mota=mota,
                                   loai=loai,
                                   loaianh=loaianh))
    query.execute()


def select_customer(id):
    query = User.select().where(User.id == id).dicts()
    return list(query)[0]


def suaThongTinUser(id, username, mobile, diachi):
    query = User.update(
        username=username,
        mobile=mobile,
        diachi=diachi
    ).where(User.id == id)
    query.execute()


def capNhatDonHang(id, action=True):
    if action:
        query = (DonHang.update(trangthai=DonHang.trangthai + 1)
                 .where(DonHang.id == id))
        query.execute()
    else:
        query = (DonHang.update(trangthai=-1)
                 .where(DonHang.id == id))
        query.execute()


if __name__ == '__main__':
    print(get_product(18))
