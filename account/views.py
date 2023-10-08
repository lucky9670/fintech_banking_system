from django.shortcuts import render, redirect
from .models import Account, UserProfile, Role
from django.contrib import auth
from lib.settings import password_check
# Create your views here.

# Create your views here.
def index(request):
    return render(request,'index.html')

def superDistibuter(request):
    return render(request,'super_distibuter.html')

def registration(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")
        print(name, email, phone, password, confirm_password, role)
        checkpoint = password_check(password)
        if checkpoint == 1:
            return render(request,"register.html", {"message":"Password must contain atleast one capital alphbat"})
        if checkpoint == 2:
            return render(request,"register.html", {"message":"Password must contain atleast one digit"})
        if checkpoint == 3:
            return render(request,"register.html", {"message":"Password must contains one special character like @, $,#,&"})
        user_check_obj = Account.objects.filter(email=email).count()
        if user_check_obj != 0:
            return render(request,"register.html", {"message":'User Already Exists!'})

        if password == confirm_password:
            role = Role.objects.get(id = role)
            user = Account.objects.create_user(username=phone, name=name, email=email, phone=phone, password=password, role=role)
            UserProfile.objects.create(user=user)
            auth.login(request, user)
            return redirect(index)
        else:
            return render(request,"register.html", {"message":"Password and confirm password Does not match"})
    return render(request,"register.html")

def login(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        usercheck = Account.objects.filter(phone__iexact=phone).count()
        if usercheck == 0:
            return render(request,"register.html", {"message":"Please enter valid email or password!"})
        user = auth.authenticate(request, username=phone, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(index)  # Redirect to the user's profile page or any other desired page
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})
    return render(request,"login.html")

def logout(request):
    auth.logout(request)
    return redirect(index)

def changePassword(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_new_password")
        email = request.user.email
        if len(new_password) < 4:
            return render(request, 'login.html', {'error_message': 'enter password of minimun 4 digits'})

        checkpoint = password_check(new_password)
        if checkpoint == 1:
            return render(request,"register.html", {"message":"Password must contain atleast one capital alphbat"})
        if checkpoint == 2:
            return render(request,"register.html", {"message":"Password must contain atleast one digit"})
        if checkpoint == 3:
            return render(request,"register.html", {"message":"Password must contains one special character like @, $,#,&"})
        
        if new_password != confirm_new_password:
            return render(request,"register.html", {"message":"password and confirmpassword doesnot match"})
        userdata = Account.objects.get(email=email)
        if userdata.check_password(new_password):
            return render(request,"register.html", {"message":"new password already exists"})
        if userdata.check_password(old_password):
            userdata.set_password(new_password)
            userdata.save()
            return redirect(index)
        else:
            return render(request,"register.html", {"message":"wrong current password"})
    return render(request,"login.html")