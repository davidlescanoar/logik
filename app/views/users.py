from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app.forms import *
from logik.tasks import sendEmail
from rest_framework import viewsets
from rest_framework import permissions
from app.serializers import UserSerializer

# Create your views here.

class welcome(View):
    def get(self, request, *args, **kwargs):
        contactForm=ContactForm()
        return render(request, 'welcome.html', {'form':contactForm})
    def post(self, request, *args, **kwargs):
        form=ContactForm(request.POST)
        if form.is_valid():
            sendEmail.delay(form.cleaned_data['text'])
        return redirect('/')


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            user = form.save()

            if user is not None:
                do_login(request, user)

                #De momento, arrancamos en home
                return redirect('/')

    return render(request, "register.html", {'form': form, 'no_logik_form':1})

def login(request):
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                do_login(request, user)
                #De momento, arrancamos en home
                return redirect('/')

    return render(request, "login.html", {'form': form, 'no_logik_form':1})

def logout(request):
    do_logout(request)

    return redirect('/')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]