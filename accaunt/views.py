from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm
from .forms import UserCreateForm, LoginForm
from django.contrib.auth import login, logout, get_user_model, update_session_auth_hash

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreateForm()
    return render(request, 'registration/register.html', {'form': form})



# def login_user(request):
#     if request.method == 'POST':
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect("profile")
#     else:
#         form = LoginForm()
#     return render(request, "registration/login.html", {'form': form})
from django.contrib.auth import authenticate, login


from django.contrib.auth import authenticate, login

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("profile")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {'form': form})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')