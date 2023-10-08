from django.shortcuts import render, redirect
from .models import Account, UserProfile, Role, Scheme, Company
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



##  Scheme Manager
def SchemeManager(request):
    message= ""
    mtype=""
    if(request.method == 'POST'):
        try:
            name = request.POST.get("scheme_name")
            type = request.POST.get("scheme_type")
            status = request.POST.get("scheme_status")
            Scheme.objects.create(name=name, type=type, status=status)
            message= "Added Successfully"
            mtype="success"
        except:
            message= "Something went wrong.."
            mtype="failed"
    
    scheme_data = Scheme.objects.all()
    return render(request, "scheme_manager.html", {"data" : scheme_data, "message": message, "mtype":mtype})

# Role Manager
def roleManager(request):
    message= ""
    mtype=""
    if(request.method == 'POST'):
        try:
            name = request.POST.get("role_name")
            Role.objects.create(name=name)
            message= "Added Successfully"
            mtype="success"
        except:
            message= "Something went wrong.."
            mtype="failed"
    role_data = Role.objects.all()
    return render(request, "role.html", {"data" : role_data, "message": message, "mtype":mtype})

def company(request):
    message= ""
    mtype=""
    if(request.method == 'POST'):
        try:
            company_name = request.POST.get("company_name")
            sort_name = request.POST.get("sort_name")
            website = request.POST.get("website")
            logo = request.FILES.get("image")
            status = request.POST.get("status")
            sender_id = request.POST.get("sender_id")
            sms_user_id = request.POST.get("sms_user_id")
            sms_password = request.POST.get("sms_password")
            sms_uti = request.POST.get("sms_uti")
            smtp_url = request.POST.get("smtp_url")
            smtp_user_name = request.POST.get("smtp_user_name")
            smtp_password = request.POST.get("smtp_password")
            smtp_port = request.POST.get("smtp_port")
            Company.objects.create(company_name = company_name, sort_name = sort_name, website = website, logo = logo, status = status, sender_id = sender_id, sms_user_id = sms_user_id, sms_password = sms_password, sms_uti = sms_uti, smtp_url = smtp_url, smtp_user_name = smtp_user_name, smtp_password = smtp_password, smtp_port = smtp_port)
            message= "Added Successfully"
            mtype="success"
        except :
            message= "Something went wrong.."
            mtype="failed"
    company = Company.objects.all()
    return render(request, "company.html", {"data" : company, "message": message, "mtype":mtype})