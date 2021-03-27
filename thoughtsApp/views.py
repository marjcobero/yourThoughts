from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.

def index(request):
    return render(request, 'register.html')

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
        return redirect('/thoughts')
    return redirect('/')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return  redirect('/')
    if request.method == 'POST':
        the_user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), the_user.password.encode()):
            print(request.method)
            request.session['user_id'] = the_user.id
            request.session['greeting'] = the_user.first_name
            return redirect('/thoughts')
        messages.error(request, "Email or Password incorrect")
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def show_all(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'all_thoughts': Thought.objects.all(),
            'the_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'allthoughts.html', context)

def create_thoughts(request):
    errors = Thought.objects.thought_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/thoughts')
    else:
        user = User.objects.get(id=request.session['user_id'])
        thought = Thought.objects.create(
            thought=request.POST['thought'],
            user=User.objects.get(id=request.session['user_id'])
        )
        return redirect('/thoughts')

def show_one(request):
    context = {
        'thought': Thought.objects.get(id=request.session['user_id']),
        'the_user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, "thought.html", context)

def like(request, user_id):
    liked_posts = Thought.objects.get(id=user_id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_posts.user_likes.add(user_liking)
    return redirect('/thoughts')

def delete(request, user_id):
    remove = Thought.objects.get(id=user_id)
    remove.delete()
    return redirect('/thoughts')