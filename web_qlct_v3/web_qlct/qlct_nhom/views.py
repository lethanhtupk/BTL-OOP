from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render

from hoadon.views import lay_ds_hoa_don, them_hoa_don
from hoadon.models import HoaDon
from django.db.models import Sum

from .models import Nhom, NhomUser, ViNhom


def show_qlct_nhom_page(request):
    current_user = request.user
    ds_nhom = current_user.nhom_set.filter(is_deleted=0)
    ds_vi = []
    for nhom in ds_nhom:
        vis = nhom.vinhom_set.all()
        ds_vi += vis
    
    print(ds_vi)
    context = {
        'ds_nhom': ds_nhom,
        'email': current_user.email,
        'ds_vi': ds_vi,
    }
    return render(request, 'qlct_nhom/intro.html', context=context)


def yc_them_nhom(request):
    current_user = request.user
    ds_nhom = current_user.nhom_set.filter(is_deleted=0)
    ds_vi = []
    for nhom in ds_nhom:
        vis = nhom.vinhom_set.all()
        ds_vi += vis

    context = {
        'ds_nhom': ds_nhom,
        'email': current_user.email,
        'ds_vi': ds_vi,
    }
    return render(request, 'qlct_nhom/themnhom.html', context)


def them_nhom(request):
    current_user = request.user
    ds_nhom = current_user.nhom_set.filter(is_deleted=0)
    ds_vi = []
    for nhom in ds_nhom:
        vis = nhom.vinhom_set.all()
        ds_vi += vis

    context = {
        'ds_nhom': ds_nhom,
        'email': current_user.email,
        'ds_vi': ds_vi,
    }
    current_user = request.user
    ten = request.POST['ten']
    dinh_muc = request.POST['dinh_muc']

    nhom = Nhom(ten=ten, dinh_muc=dinh_muc)
    nhom.save()
    nhom_user = NhomUser(auth_user=current_user, nhom=nhom, is_leader=1)
    nhom_user.save()
  

    return render(request, 'qlct_nhom/themnhom_thuchien.html', context=context)


def lay_ds_user(request, id_nhom):
    current_user = request.user
    ds_nhom = current_user.nhom_set.filter(is_deleted=0)
    ds_vi = []
    for nhom in ds_nhom:
        vis = nhom.vinhom_set.all()
        ds_vi += vis
    id_user = NhomUser.objects.filter(nhom_id=id_nhom).values('auth_user_id')
    ds_dinhmuc = NhomUser.objects.filter(nhom_id=id_nhom).values('dinh_muc')
    ds_user = User.objects.filter(id__in=id_user)
    data = []
    print("số lượng: {} - {}".format(len(ds_dinhmuc), len(ds_user)))
    for i in range(0, len(id_user)):
        print(ds_user[i])
        print(ds_dinhmuc[i]['dinh_muc'])
        x = {'user': ds_user[i],
             'dinh_muc': ds_dinhmuc[i]['dinh_muc']}
        # x['user']: ds_user[i]
        # x['dinh_muc']: ds_dinhmuc[i]
        data.append(x)

    print(data)
    context = {
        'ds_user': data,
        'ds_nhom': ds_nhom,
        'email': current_user.email,
        'ds_vi': ds_vi,
    }
    return render(request, "qlct_nhom/ds_nhomuser.html", context=context)


def yc_them_nhom_user(request):
    current_user = request.user
    ds_nhom = current_user.nhom_set.filter(is_deleted=0)
    ds_vi = []
    for nhom in ds_nhom:
        vis = nhom.vinhom_set.all()
        ds_vi += vis
    current_user = request.user
    ds_nhom = current_user.nhom_set.filter(is_deleted=0)
    ds_user = User.objects.all()
    context = {
        'ds_nhom': ds_nhom,
        'ds_user':ds_user,
        'email': request.user.email,
        'ds_vi': ds_vi,
    }
    return render(request, 'qlct_nhom/them_nhomuser.html', context=context)


def them_nhom_user(request):
    id_nhom = request.POST['nhom']
    id_user = request.POST['user']
    dinh_muc = request.POST['dinh_muc']

    current_user = request.user
    ds_nhom = current_user.nhom_set.filter(is_deleted=0)
    ds_vi = []
    for nhom in ds_nhom:
        vis = nhom.vinhom_set.all()
        ds_vi += vis

    id_users = NhomUser.objects.filter(nhom_id=id_nhom).values('auth_user_id')
    if id_user in id_users:
        return Http404('user đã ở trong nhóm')
    nhom = Nhom.objects.get(pk=id_nhom)
    user = User.objects.get(pk=id_user)
    nhom_user = NhomUser(auth_user=user, nhom=nhom, dinh_muc=dinh_muc)
    nhom_user.save()
    context = {
        'ds_nhom': ds_nhom,
        'email': current_user.email,
        'ds_vi': ds_vi,
    }
    return render(request, 'qlct_nhom/them_nhomuser_thuchien.html', context=context)



def yc_them_vi_nhom(request):
    current_user = request.user
    ds_nhom = current_user.nhom_set.filter(is_deleted=0)
    ds_vi = []
    for nhom in ds_nhom:
        vis = nhom.vinhom_set.all()
        ds_vi += vis
    context = {
        'ds_nhom': ds_nhom,
        'email': current_user.email,
        'ds_vi': ds_vi,
    }

    return render(request, 'qlct_nhom/themvinhom.html', context=context)


def them_vi_nhom(request):

    current_user = request.user
    ds_nhom = current_user.nhom_set.filter(is_deleted=0)
    ds_vi = []
    for nhom in ds_nhom:
        vis = nhom.vinhom_set.all()
        ds_vi += vis
    context = {
        'ds_nhom': ds_nhom,
        'email': current_user.email,
        'ds_vi': ds_vi,
    }

    ten = request.POST['ten']
    dinh_muc = request.POST['dinh_muc']
    so_du = request.POST['so_du']
    id_nhom = request.POST["auth_group"]

    nhom = Nhom.objects.get(pk=id_nhom)
    nhom.vinhom_set.create(ten=ten, dinh_muc=dinh_muc, so_du=so_du)

    return render(request, 'qlct_nhom/themvinhom_thuchien.html', context)


def yc_them_chi_tieu(request):
    current_user = request.user
    ds_linhvuc = current_user.linhvuc_set.all()
    ds_vi = []
    ds_nhom = current_user.nhom_set.filter(is_deleted=0)
    for nhom in ds_nhom:
        ds_vi_nhom = nhom.vinhom_set.all()
        ds_vi.extend(ds_vi_nhom)
    context = {
        'ds_vi': ds_vi,
        'email': current_user.email,
        'ds_linhvuc': ds_linhvuc,
        'ds_nhom': ds_nhom,
    }
    return render(request, 'qlct_nhom/themchitieu.html', context)


def them_chitieu(request):
    current_user = request.user
    ten_hoa_don = request.POST["ten_hoa_don"]
    so_tien = request.POST["so_tien"]
    ghi_chu = request.POST["ghi_chu"]
    date = request.POST["thoi_gian_giao_dich_0"]
    time = request.POST["thoi_gian_giao_dich_1"]
    id_linhvuc = request.POST["linh_vuc"]
    id_vi = request.POST["vi_nhom"]

    current_user = request.user
    ds_nhom = current_user.nhom_set.filter(is_deleted=0)
    ds_vi = []
    for nhom in ds_nhom:
        vis = nhom.vinhom_set.all()
        ds_vi += vis

    context = {
        'ds_nhom': ds_nhom,
        'email': current_user.email,
        'ds_vi': ds_vi,
    }
    print(ghi_chu)

    if not current_user.is_authenticated:
        print('permission deni')
        return redirect('login')

    date_time = date + ' ' + time
    result = them_hoa_don(
        current_user=current_user,
        ten_hoa_don=ten_hoa_don,
        so_tien=so_tien,
        thoi_gian_giao_dich=date_time,
        id_linh_vuc=id_linhvuc,
        ghichu=ghi_chu,
        id_vi_nhom=id_vi,
    )

    return render(request, 'qlct_nhom/themchitieu_thuchien.html', context)


def lay_bieu_do(request, id_vi):
    # ds_hoa_don = lay_ds_hoa_don(id_vi_ca_nhan = id_vi)
    ds_linh_vuc = HoaDon.objects.filter(vi_nhom = id_vi).values('linh_vuc__ten').annotate(Sum('so_tien'))
    current_user = request.user
    ds_nhom = current_user.nhom_set.filter(is_deleted=0)
    ds_vi = []
    for nhom in ds_nhom:
        vis = nhom.vinhom_set.all()
        ds_vi += vis

    lv1 = ds_linh_vuc[0]['linh_vuc__ten']
    so1= ds_linh_vuc[0]['so_tien__sum']

    lv2 = ds_linh_vuc[1]['linh_vuc__ten']
    so2= ds_linh_vuc[1]['so_tien__sum']

    lv3 = ds_linh_vuc[2]['linh_vuc__ten']
    so3= ds_linh_vuc[2]['so_tien__sum']

    lv4 = ds_linh_vuc[3]['linh_vuc__ten']
    so4= ds_linh_vuc[3]['so_tien__sum']

    lv5 = ds_linh_vuc[4]['linh_vuc__ten']
    so5= ds_linh_vuc[4]['so_tien__sum']

    lv6 = ds_linh_vuc[5]['linh_vuc__ten']
    so6= ds_linh_vuc[5]['so_tien__sum']

    lv7 = ds_linh_vuc[6]['linh_vuc__ten']
    so7= ds_linh_vuc[6]['so_tien__sum']

    lv8 = ds_linh_vuc[7]['linh_vuc__ten']
    so8= ds_linh_vuc[7]['so_tien__sum']

    lv9 = ds_linh_vuc[8]['linh_vuc__ten']
    so9= ds_linh_vuc[8]['so_tien__sum']

    lv10 = ds_linh_vuc[9]['linh_vuc__ten']
    so10= ds_linh_vuc[9]['so_tien__sum']


    context = {
        'ds_nhom': ds_nhom,
        'email': current_user.email,
        'ds_vi': ds_vi,
        'lv1': lv1,
        'lv2': lv2,
        'lv3': lv3,
        'lv4': lv4,
        'lv5': lv5,
        'lv6': lv6,
        'lv7': lv7,
        'lv8': lv9,
        'lv9': lv9,
        'lv10': lv10,

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
    return render(request, 'qlct_nhom/bieudotron.html', context)

from django.db.models.functions import Extract
def lay_bieu_do_cot(request, id_vi):

    ds_linh_vuc = HoaDon.objects.filter(vi_nhom = id_vi).values('linh_vuc__ten').annotate(Sum('so_tien'))
    current_user = request.user
    ds_nhom = current_user.nhom_set.filter(is_deleted=0)
    ds_vi = []
    for nhom in ds_nhom:
        vis = nhom.vinhom_set.all()
        ds_vi += vis


    ds_linh_vuc = HoaDon.objects.filter(vi_nhom = id_vi).values('linh_vuc__ten').annotate(Sum('so_tien'))

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
        'ds_nhom': ds_nhom,
        'email': current_user.email,
        'ds_vi': ds_vi,

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
    return render(request, 'qlct_nhom/bieudocot.html', context)


def lay_ls_chi_tieu(request, id_vi):
    current_user = request.user
    ds_nhom = current_user.nhom_set.filter(is_deleted=0)
    ds_hoa_don = lay_ds_hoa_don(id_vi_nhom = id_vi)
    current_user = request.user
    ds_vi = []
    for nhom in ds_nhom:
        vis = nhom.vinhom_set.all()
        ds_vi += vis
    vi = ViNhom.objects.get(pk=id_vi)
    so_du = vi.so_du
    context = {
        'ds_chitieu': ds_hoa_don,
        'ds_vi': ds_vi,
        'email': current_user.email,
        'so_du': so_du,
    } 
    return render(request, 'qlct_nhom/lsct.html', context)
