from django.shortcuts import render, redirect
from .models import Account, UserProfile, Role, Scheme, Company
from .models import Account, UserProfile, Role, Scheme, APIManager, Provider, Commission, CommissionType
from django.contrib import auth
from lib.settings import password_check
from django.http import JsonResponse

from django.core.files.storage import FileSystemStorage
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
    scheme_data = Scheme.objects.all()
    provider_data = CommissionType.objects.all()
    return render(request, "scheme_manager.html", {"data" : scheme_data,"pdata":provider_data, "message": message, "mtype":mtype})
def AddScheme(request):
    message= ""
    mtype=""
    if(request.method == 'POST'):
        id = request.POST.get("sid")
        print(id, type(id))
        if(id == ''):
            try:
                print("Inside post")
                name = request.POST.get("name")
                type1 = request.POST.get("type")
                status = request.POST.get("status")
                Scheme.objects.create(name=name, type=type1, status=status)
                message= "Added Successfully"
                mtype="success"
            except:
                message= "Something went wrong.."
                mtype="failed"
        else:
            try:
                print("Inside edit")
                name = request.POST.get("name")
                type1 = request.POST.get("type")
                status = request.POST.get("status")
                scheme = Scheme.objects.get(id = id)
                scheme.name = name
                scheme.type = type1
                scheme.status = status
                scheme.save()
                message= "Updated Successfully"
                mtype="success"
            except:
                message= "Something went wrong.."
                mtype="failed"
    return JsonResponse({'mtype':mtype, 'message':message})
def DeleteScheme(request):
    message= ""
    mtype=""
    if(request.method == "POST"):
        try:
            id = request.POST.get('sid')
            data = Scheme.objects.get(pk=id)
            data.delete()
            message= "Deleted Successfully"
            mtype="success"
        except:
            message= "Something went wrong.."
            mtype="failed"
    return JsonResponse({'mtype':mtype, 'message':message})
        # scheme_data = Scheme.objects.all()
        # return render(request, "scheme_manager.html", {"data" : scheme_data, "message": message, "mtype":mtype})
def editScheme(request):
    message= ""
    mtype=""
    if(request.method == "POST"):
        try:
            id = request.POST.get('sid')
            data = Scheme.objects.get(pk=id)
            scheme_data = {"id":data.id, "name":data.name, "type":data.type, "status":data.status }
            message= "Deleted Successfully"
            mtype="success"
        except:
            message= "Something went wrong.."
            mtype="failed"
    return JsonResponse({'mtype':mtype, 'message':message, 'data':scheme_data})    


## Commission type 

def CommissionTypeManager(request):
    message= ""
    mtype=""
    scheme_data = CommissionType.objects.all()
    return render(request, "commission_type_manager.html", {"data" : scheme_data, "message": message, "mtype":mtype})
def AddCommissionType(request):
    message= ""
    mtype=""
    if(request.method == 'POST'):
        id = request.POST.get("sid")
        print(id, type(id))
        if(id == ''):
            try:
                print("Inside post")
                name = request.POST.get("name")
                type1 = request.POST.get("type")
                status = request.POST.get("status")
                CommissionType.objects.create(name=name, type=type1, status=status)
                message= "Added Successfully"
                mtype="success"
            except:
                message= "Something went wrong.."
                mtype="failed"
        else:
            try:
                print("Inside edit")
                name = request.POST.get("name")
                type1 = request.POST.get("type")
                status = request.POST.get("status")
                scheme = CommissionType.objects.get(id = id)
                scheme.name = name
                scheme.type = type1
                scheme.status = status
                scheme.save()
                message= "Updated Successfully"
                mtype="success"
            except:
                message= "Something went wrong.."
                mtype="failed"
    return JsonResponse({'mtype':mtype, 'message':message})
def DeleteCommssionType(request):
    message= ""
    mtype=""
    if(request.method == "POST"):
        try:
            id = request.POST.get('sid')
            data = CommissionType.objects.get(pk=id)
            data.delete()
            message= "Deleted Successfully"
            mtype="success"
        except:
            message= "Something went wrong.."
            mtype="failed"
    return JsonResponse({'mtype':mtype, 'message':message})
        # scheme_data = Scheme.objects.all()
        # return render(request, "scheme_manager.html", {"data" : scheme_data, "message": message, "mtype":mtype})
def editCommissionType(request):
    message= ""
    mtype=""
    if(request.method == "POST"):
        try:
            id = request.POST.get('sid')
            data = Scheme.objects.get(pk=id)
            scheme_data = {"id":data.id, "name":data.name, "type":data.type, "status":data.status }
            message= "Deleted Successfully"
            mtype="success"
        except:
            message= "Something went wrong.."
            mtype="failed"
    return JsonResponse({'mtype':mtype, 'message':message, 'data':scheme_data})    



## API Manager

def apiManager(request):
    message= ""
    mtype=""
    if(request.method == 'POST'):
        try:
            name = request.POST.get("product_name")
            sort_name = request.POST.get("sort_name")
            url = request.POST.get("url")
            status = request.POST.get("status")
            api_key = request.POST.get("api_key")
            username = request.POST.get("username")
            password = request.POST.get("password")
            optional = request.POST.get("optional")
            code = request.POST.get("code")
            type = request.POST.get("type")
            APIManager.objects.create(product_name=name, sort_name=sort_name, url=url, status=status, api_key=api_key, username=username, password=password, optional=optional, code=code, type=type)
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
    api_data = APIManager.objects.all()
    return render(request, "api.html", {"data" : api_data, "message": message, "mtype":mtype})


def ProviderManager(request):
    message= ""
    mtype=""
    if(request.method == 'POST') and request.FILES['logo']:
        # try:
        name = request.POST.get("name")
        re_1 = request.POST.get("re_1")
        re_2 = request.POST.get("re_2")
        re_3 = request.POST.get("re_3")
        re_4 = request.POST.get("re_4")
        api_id = request.POST.get("api_id")
        type = request.POST.get("type")
        status = request.POST.get("status")
        logo = request.FILES['logo']
        fss = FileSystemStorage()
        file = fss.save(logo.name, logo)
        file_url = fss.url(file)
        is_mandatory = request.POST.get("is_mandatory")
        Provider.objects.create(name=name, type=type, status=status, logo=file_url, is_mandatory=is_mandatory, api_id=api_id,re_1=re_1, re_2=re_2, re_3=re_3, re_4=re_4)
        message= "Added Successfully"
        mtype="success"
        # except:
        #     message= "Something went wrong.."
        #     mtype="failed"
    api_data = APIManager.objects.all()
    scheme_data = Provider.objects.all()
    return render(request, "provider.html", {"data" : scheme_data,"apidata":api_data, "message": message, "mtype":mtype})

def whitelabel(request):
    role = Role.objects.get(name="White Label")
    data = Account.objects.filter(role = role)
    return render(request, "whitelabel.html", {"data" : data, "name" : "White Label"})

def superDistributer(request):
    role = Role.objects.get(name="Super Distributer")
    data = Account.objects.filter(role = role)
    return render(request, "whitelabel.html", {"data" : data, "name" : "Super Distributer"})

def Distributer(request):
    role = Role.objects.get(name="Distributer")
    data = Account.objects.filter(role = role)
    return render(request, "whitelabel.html", {"data" : data, "name" : "Distributer"})

def Retailer(request):
    role = Role.objects.get(name="Retailer")
    data = Account.objects.filter(role = role)
    return render(request, 'whitelabel.html', {"data":data, "name" : "Retailer"}) 


def Dashboard(request):
    return render(request,'dashboard.html')