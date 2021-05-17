from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.

def index(request):
    return render(request, 'index.html')

def loginuser(request):
    print(request.POST)
    print('**********************************')
    errors = User.objects.loginValidator(request.POST)
    print('************************ERRORS', errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    emailMatch = User.objects.filter(email = request.POST['useremail'])
    request.session['userID'] = emailMatch[0].id
    return redirect('/blog')

def createuser(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    hashpwd = bcrypt.hashpw(request.POST['pwd'].encode(), bcrypt.gensalt()).decode()

    newuser = User.objects.create(first_name = request.POST['fname'], last_name = request.POST['lname'], email = request.POST['useremail'], password = hashpwd)
    request.session['userID'] = newuser.id
    return redirect('/blog')

def logout(request):
    request.session.clear()
    return redirect('/')

def blog(request):
    context = {
        "user": User.objects.get(id= request.session['userID']),
        "entry_db":Entry.objects.all()
    }
    return render(request, 'blog.html', context)

def addentry(request):
    context = {
        "user": User.objects.get(id= request.session['userID']),
    }
    return render(request, 'addentry.html', context)

def asset(request):
    context = {
        "user": User.objects.get(id= request.session['userID']),
    }
    return render(request, 'asset.html', context)