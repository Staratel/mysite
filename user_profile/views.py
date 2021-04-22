from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .serializer import UserSerializer, UserSerializeDetails
from rest_framework import generics
from .forms import UserForm


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializeDetails


def index(request):
    user = User.objects.filter(id=request.user.id)
    if request.method == "POST":
        return render(request, 'index.html', {'form':user[0]})
    else:
        return redirect('login')

def user_login(request):
    user_form = UserForm()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html', {'user':user})
        else:
            return render(request, 'login.html', {'invalid':True, 'form': user_form})
    else:
        return render(request, 'login.html', {'invalid':False, 'form': user_form})


def user_logout(request):
    logout(request)
    return redirect('login')


def user_registration(request):
    user_form = UserForm()
    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            username = request.POST.get('username')
            existing_user = User.objects.filter(username=username)
        else:
            return render(request, 'registration.html', {'invalid_input': True, 'form':user_form})

        if len(existing_user) == 0:
            password = request.POST.get('password')
            user = User.objects.create_user(username, '', password)
            user.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return render(request, 'index.html', {'user':user})
        else:
            return render(request, 'registration.html', {'invalid':True, 'form': user_form})
    else:
        return render(request, 'registration.html', {'invalid':False, 'form': user_form})
