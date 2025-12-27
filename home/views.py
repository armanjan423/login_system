from django.shortcuts import render, redirect
from django.http import HttpResponse
import pymongo
import datetime
import bcrypt
import re
import secrets # To generate a random token
import os

# MongoDB Configuration
MONGO_URL = os.getenv('MONGO_URL')
DB_NAME = "mysite_db"
USER_COLLECTION = "users"

def get_db():
    client = pymongo.MongoClient(MONGO_URL)
    return client[DB_NAME]

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        city = request.POST.get('city')
        password = request.POST.get('password')

        # 1. Email Format Validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return render(request, 'home/signup.html', {'error': 'Invalid email format. Please enter a valid email.'})

        # 2. Username Validation (Length and chars)
        if len(username) < 3 or not re.match("^[a-zA-Z0-9_ ]+$", username):
            return render(request, 'home/signup.html', {'error': 'Username must be at least 3 characters and contain only letters, numbers, and underscores.'})

        # 3. Password Validation (Mix of 7+ chars and letters/numbers)
        if len(password) < 7 or not re.search("[a-zA-Z]", password) or not re.search("[0-9]", password):
            return render(request, 'home/signup.html', {'error': 'Password must be at least 7 characters and contain both letters and numbers.'})

        db = get_db()
        users = db[USER_COLLECTION]

        # 2. Check if user already exists
        if users.find_one({'email': email}):
            return render(request, 'home/signup.html', {'error': 'An account with this email already exists.'})

        # 3. Hash Password for Security
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # 4. Generate Token (Session simulation)
        token = secrets.token_hex(16)

        # 5. Save User
        user_data = {
            'username': username,
            'email': email,
            'city': city,
            'password': hashed_password,
            'token': token,
            'created_at': datetime.datetime.now()
        }
        users.insert_one(user_data)

        # 6. Set Session (Token)
        request.session['auth_token'] = token
        request.session['user_email'] = email

        return redirect('dashboard')

    return render(request, 'home/signup.html')

def login_view(request):
    # If already logged in, go to dashboard
    if 'auth_token' in request.session:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 1. Basic Email Format Validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return render(request, 'home/login.html', {'error': 'Invalid email format.'})

        db = get_db()
        users = db[USER_COLLECTION]

        # 1. Find user by email
        user = users.find_one({'email': email})

        if user:
            # 2. Verify hashed password
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                # Create a new token on every login for security
                new_token = secrets.token_hex(16)
                users.update_one({'email': email}, {'$set': {'token': new_token}})
                
                request.session['auth_token'] = new_token
                request.session['user_email'] = email
                return redirect('dashboard')
            else:
                return render(request, 'home/login.html', {'error': 'Email or password wrong'})
        else:
            return render(request, 'home/login.html', {'error': 'Email or password wrong'})

    return render(request, 'home/login.html')

def dashboard(request):
    # Check if user is logged in
    token = request.session.get('auth_token')
    email = request.session.get('user_email')

    if not token or not email:
        return redirect('login')

    db = get_db()
    user = db[USER_COLLECTION].find_one({'email': email, 'token': token})

    if not user:
        # Invalid token
        return redirect('logout')

    context = {
        'username': user.get('username'),
        'email': user.get('email'),
        'city': user.get('city'),
        'created_at': user.get('created_at').strftime("%B %d, %Y") if user.get('created_at') else "N/A"
    }

    return render(request, 'home/dashboard.html', context)

def logout_view(request):
    # Clear the session
    if 'auth_token' in request.session:
        del request.session['auth_token']
    if 'user_email' in request.session:
        del request.session['user_email']
    
    return redirect('login')

def about(request):
    return HttpResponse('this is about page')

def contact(request):
    return HttpResponse('this is contact page')
