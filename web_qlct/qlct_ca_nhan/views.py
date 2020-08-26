from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import LinhVuc, ViCaNhan
from hoadon.views import lay_ds_hoa_don, them_hoa_don
from hoadon.models import HoaDon
from django.db.models import Sum
import datetime

def show_qlct_ca_nhan_page(request):
    current_user = request.user
    ds_vi = current_user.vicanhan_set.filter(is_deleted=0)
    context = {
        'ds_vi': ds_vi,
        'email': current_user.email,
    }
    return render(request, 'qlct_ca_nhan/intro.html', context=context)


def yc_them_vi(request):
    current_user = request.user
    ds_vi = current_user.vicanhan_set.filter(is_deleted=0)
    context = {
        'ds_vi': ds_vi,
        'email': current_user.email,
    }
    return render(request, 'qlct_ca_nhan/themvi.html', context)


def them_vi(request):
    current_user = request.user
    ten = request.POST['ten']
    dinh_muc = request.POST['dinh_muc']
    sodu = request.POST['so_du']

    current_user = request.user
    ds_vi = current_user.vicanhan_set.filter(is_deleted=0)
    context = {
        'ds_vi': ds_vi,
        'email': current_user.email,
    }
    if current_user.is_authenticated:
        current_user.vicanhan_set.create(
            ten=ten, dinh_muc=dinh_muc, so_du=sodu, is_deleted=0)
        return render(request, 'qlct_ca_nhan/themvi_thuchien.html', context)
    else:
        print('user invalid')
        return redirect('login')


def yc_them_linhvuc(request):
    current_user = request.user
    ds_linhvuc = current_user.linhvuc_set.all()
    ds_vi = current_user.vicanhan_set.filter(is_deleted=0)
    context = {
        'email': current_user.email,
        'ds_linhvuc': ds_linhvuc,
        'ds_vi': ds_vi,
    }
    return render(request, 'qlct_ca_nhan/themlinhvuc.html', context=context)


def them_linhvuc(request):
    current_user = request.user
    print(request.POST)
    ten = request.POST['ten']
    loai = request.POST['loai']
    
    if str(loai) == "Chi tiêu":
        loai = 1
    else: 
        loai = 0
    id_linhvuc_cha = -1
    # print(id_linhvuc_cha)
    current_user = request.user
    ds_vi = current_user.vicanhan_set.filter(is_deleted=0)
    context = {
        'ds_vi': ds_vi,
        'email': current_user.email,
    }

    linh_vuc_cha = None

    if current_user.is_authenticated:
        linhvuc = current_user.linhvuc_set.create(ten=ten, loai=loai)
        if int(id_linhvuc_cha) != -1:
            linh_vuc_cha = LinhVuc.objects.get(pk=id_linhvuc_cha)
            linhvuc.linh_vuc = linh_vuc_cha
            linhvuc.save()

        return render(request, 'qlct_ca_nhan/themvi_thuchien.html', context)
    else:
        print('user invalid')
        return redirect('login')


def lay_ls_chi_tieu(request, id_vi):
    ds_hoa_don = lay_ds_hoa_don(id_vi_ca_nhan = id_vi)
    current_user = request.user
    ds_vi = current_user.vicanhan_set.filter(is_deleted=0)
    vi = ViCaNhan.objects.get(pk=id_vi)
    so_du = vi.so_du
    context = {
        'ds_chitieu': ds_hoa_don,
        'ds_vi': ds_vi,
        'email': current_user.email,
        'so_du': so_du,
    } 
    return render(request, 'qlct_ca_nhan/lsct.html', context)


def yc_them_chi_tieu(request):
    current_user = request.user
    ds_linhvuc = current_user.linhvuc_set.all()
    ds_vi = current_user.vicanhan_set.filter(is_deleted=0)
    context = {
        'ds_vi': ds_vi,
        'email': current_user.email,
        'ds_linhvuc': ds_linhvuc,
    }
    return render(request, 'qlct_ca_nhan/themchitieu.html', context)


def them_chitieu(request):
    current_user = request.user
    ten_hoa_don = request.POST["ten_hoa_don"]
    so_tien = request.POST["so_tien"]
    ghi_chu = request.POST["ghi_chu"]   
    id_linhvuc = request.POST["linh_vuc"]
    id_vi = request.POST["vi_ca_nhan"]

    current_user = request.user
    ds_vi = current_user.vicanhan_set.filter(is_deleted=0)
    context = {
        'ds_vi': ds_vi,
        'email': current_user.email,
    }
    print(ghi_chu)

    if not current_user.is_authenticated:
        print('permission deni')
        return redirect('login')

    date_time = datetime.datetime.now()
    result = them_hoa_don(
        current_user=current_user,
        ten_hoa_don=ten_hoa_don,
        so_tien=so_tien,
        thoi_gian_giao_dich=date_time,
        id_linh_vuc=id_linhvuc,
        ghichu=ghi_chu,
        id_vi_ca_nhan=id_vi,
    )

    return render(request, 'qlct_ca_nhan/themvi_thuchien.html', context)


def lay_bieu_do(request, id_vi):
    # ds_hoa_don = lay_ds_hoa_don(id_vi_ca_nhan = id_vi)
    ds_linh_vuc = HoaDon.objects.filter(vi_ca_nhan = id_vi).values('linh_vuc__ten').annotate(Sum('so_tien'))
    current_user = request.user
    ds_vi = current_user.vicanhan_set.filter(is_deleted=0)
    ds_ten = []
    ds_tien = []
    total = 0
    for i in ds_linh_vuc:
        ds_ten.append(i['linh_vuc__ten'])
        ds_tien.append(i['so_tien__sum'])
        total += int(i['so_tien__sum'])
    context = {
        'ds_vi': ds_vi,
        'email': current_user.email,
        'ds_ten': ds_ten,
        'ds_tien': ds_tien,
        'total': total
    }

    return render(request, 'qlct_ca_nhan/bieudotron.html', context)

from django.db.models.functions import Extract
def lay_bieu_do_cot(request, id_vi):

    current_user = request.user
    ds_vi = current_user.vicanhan_set.filter(is_deleted=0)

    ds_linh_vuc = HoaDon.objects.filter(vi_ca_nhan = id_vi).values('linh_vuc__ten').annotate(Sum('so_tien'))

    so1= ds_linh_vuc[0]['so_tien__sum']

    so2= ds_linh_vuc[1]['so_tien__sum']

    so3= ds_linh_vuc[2]['so_tien__sum']

    so4= ds_linh_vuc[3]['so_tien__sum']

    so5= ds_linh_vuc[4]['so_tien__sum']

    so6= ds_linh_vuc[5]['so_tien__sum']

    so7= ds_linh_vuc[6]['so_tien__sum']

    so8= ds_linh_vuc[7]['so_tien__sum']

    so9= ds_linh_vuc[8]['so_tien__sum']

    so10= ds_linh_vuc[9]['so_tien__sum']


    context = {
        'ds_vi': ds_vi,
        'email': current_user.email,
        'so1': so1,
        'so2': so2,
        'so3': so3,
        'so4': so4,
        'so5': so5,
        'so6': so6,
        'so7': so7,
        'so8': so8,
        'so9': so9,
        'so10': so10,
    }

    print(ds_linh_vuc)
    return render(request, 'qlct_ca_nhan/bieudocot.html', context)
