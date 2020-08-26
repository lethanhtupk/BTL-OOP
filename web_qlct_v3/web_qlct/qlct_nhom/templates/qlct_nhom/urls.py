from django.urls import path
from .views import show_qlct_nhom_page, lay_bieu_do_cot, lay_bieu_do, yc_them_nhom, them_nhom, yc_them_nhom_user, yc_them_vi_nhom, them_vi_nhom, yc_them_chi_tieu, them_nhom_user, them_chitieu,lay_ls_chi_tieu, lay_ds_user


urlpatterns = [
    path('', show_qlct_nhom_page, name='qlct_nhom_page'),
    path('themnhom/', yc_them_nhom, name='themnhom'),
    path('themnhom/thuc_hien', them_nhom, name='thuc_hien_them_nhom'),
    path('ds-user/<int:id_nhom>', lay_ds_user, name='ds_user'),
    path('them-nhomuser/', yc_them_nhom_user, name='them_nhom_user'),
    path('them-nhomuser/thuc-hien', them_nhom_user, name='thuc_hien_them_nhom_user'),
    path('themvinhom/', yc_them_vi_nhom, name='them_vinhom'),
    path('themvinhom/thuc_hien', them_vi_nhom, name='thuc_hien_them_vinhom'),
    path('lsct/<int:id_vi>', lay_ls_chi_tieu, name = 'lay_ls_chi_tieu_nhom'),
    path('themchitieu', yc_them_chi_tieu, name='them_chitieu'),
    path('bieudo/<int:id_vi>', lay_bieu_do, name = 'lay_bieu_do_nhom'),
    path('bieudocot/<int:id_vi>', lay_bieu_do_cot, name = 'lay_bieu_do_cot_nhom'),
    path('themchitieu/thuc_hien', them_chitieu, name='thuc_hien_them_chi_tieu_nhom'),
]