from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.


def index(request):
    request.session.flush()
    return render(request, 'main.html')


def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    the_user = User.objects.filter(id=request.session['user_id'])
    context = {
        'user': User.objects.get(id=request.session['user_id']), 
        'all_messages': Wall.objects.all()
    }
    return render(request, 'homepage.html', context)


def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return  redirect('/')
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['first_name'], 
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw,
        )
        request.session['user_id'] = new_user.id
        return redirect('/success')
    return redirect('/')


def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return  redirect('/login_page')
    if request.method == 'POST':
        the_user = User.objects.filter(email = request.POST['email'])
        if the_user:
            logged_user = the_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                print(request.method)
                request.session['user_id'] = logged_user.id
                return redirect('/success')
        messages.error(request, "Email or Password incorrect")
    return redirect('/')

def login_page(request):
    return render(request, 'login_page.html')

def logout(request):
    request.session.flush()
    return redirect('/')

def post_message(request):
    Wall.objects.create(message=request.POST['message'],poster=User.objects.get(id=request.session['user_id']))
    return redirect('/success')


def post_comment(request, user_id):
    poster = User.objects.get(id=request.session['user_id'])
    message = Wall.objects.get(id=user_id)
    Comment.objects.create(comment=request.POST['comment'], poster=poster, wall_message= message)
    return redirect('/success')


def profile(request, user_id):
    context = {
        'user': User.objects.get(id= user_id)
    }
    return render(request, 'profile.html', context)


def like(request, user_id):
    liked_message = Wall.objects.get(id= user_id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/success')

def delete_post(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    post_to_delete = Wall.objects.get(id=user_id)
    post_to_delete.delete()
    return redirect('/success')

def delete_comment(request, user_id):
    destroyed = Comment.objects.get(id= user_id)
    destroyed.delete()
    return redirect('/success')


def edit(request, user_id):
    edit_user = User.objects.get(id= user_id)
    edit_user.first_name = request.POST['first_name']
    edit_user.last_name = request.POST['last_name']
    edit_user.email = request.POST['email']
    edit_user.save()
    return redirect('/success')