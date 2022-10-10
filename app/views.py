from pickle import FALSE
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate , login as loginUser , logout
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
# Create your views here.
from app.forms import TODOForm
from app.models import TODO

def home(request):
    form = TODOForm()
    return render(request , 'index.html' , context={'form' : form})

def login(request):
    if request.method == 'GET':
        form=AuthenticationForm()
        context={
        "form": form
        }
        return render(request , 'login.html', context=context)
    else:
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
          username = form.cleaned_data.get('username')
          password = form.cleaned_data.get('password')
          user = authenticate(username=username , password= password)
        if user is not None:
          loginUser(request , user)
          return redirect('home')
        else:
          context={
        "form": form
        }
        return render(request , 'login.html', context=context)
          



def signup(request):
    if request.method =='GET':
       form = UserCreationForm()
       context = {
           "form" : form
    }
       return render(request , 'signup.html' , context=context)
    else:
       print(request.POST)
       form = UserCreationForm(request.POST)
       context = {
           "form" : form
    }
    if form.is_valid():
        user = form.save()
        print(user)
        if user is not None:
            return redirect('login')
       
    else:
        return render(request , 'signup.html' , context=context)
        

def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = TODOForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo= form.save(commit=False)
            todo.user = user
            todo.save()
            print(todo)
            return redirect("home")
        else: 
            return render(request , 'index.html' , context={'form' : form})