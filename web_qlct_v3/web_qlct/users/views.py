from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def home(request):
    return render(request, 'users/home.html')


def about(request):
    return render(request, 'users/about.html', {'title': 'About'})


@login_required
def profile(request):
    current_user = request.user
    # email = current_user.email
    contex = {
        # 'email': email,
        'email': current_user.email,
        'username': current_user.username,
        'firstname': current_user.first_name,
        'lastname': current_user.last_name,
    }
    return render(request, 'users/profile.html', contex)


def yc_capnhap_taikhoan(request):
    current_user = request.user
    context = {
        'username': current_user.username,
        'email': current_user.email,
    }    
    return render(request, 'users/capnhap_taikhoan.html', context=context)


def capnhap_taikhoan (request):
    current_user = request.user
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    # date_of_birth = request.POST['date_of_birth']
    # image = request.POST['fileupload']
    email = request.POST['email']

    current_user.first_name = first_name
    current_user.last_name = last_name
    current_user.email = email
    current_user.save()
    return redirect('thongtin_taikhoan')


def thongtin_taikhoan(request):
    current_user = request.user
    context = {
        'username': current_user.username,
        'firstname': current_user.first_name,
        'lastname': current_user.last_name,
        'email': current_user.email,
    }
    return render(request, 'users/thongtin_taikhoan.html', context=context)

