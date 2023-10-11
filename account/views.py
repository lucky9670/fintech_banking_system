from django.shortcuts import render, redirect
from .models import Account, UserProfile, Role, Scheme, Company
from .models import Account, UserProfile, Role, Scheme, APIManager, Provider, Commission, CommissionType
from django.contrib import auth
from lib.settings import password_check
from django.http import JsonResponse
import uuid
import requests

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

def WhiteLabelManager(request):
    wdata = Account.objects.all()
    return render(request, 'whitelabel.html', {"data":wdata})   

def SuperDistributor(request):
    wdata = Account.objects.all()
    return render(request, 'whitelabel.html', {"data":wdata})   

def Distributor(request):
    wdata = Account.objects.all()
    return render(request, 'whitelabel.html', {"data":wdata})   

def Retailer(request):
    wdata = Account.objects.all()
    return render(request, 'whitelabel.html', {"data":wdata})   

##  Scheme Manager
def SchemeManager(request):
    message= ""
    mtype=""
    scheme_data = Scheme.objects.all()
    
    com_data = CommissionType.objects.all()
    return render(request, "scheme_manager.html", {"data" : scheme_data, "pdata":com_data, "message": message, "mtype":mtype})


def GetProviderDataBYID(request):
    data = []
    if(request.method == "POST"):
        com_id = request.POST.get("com_id")
        commission = CommissionType.objects.get(id=com_id)
        print(commission)
    provider_data = Provider.objects.filter(com_type= commission)
    
    
    for state in provider_data:
        commission = Commission.objects.filter(operator_id= state.id)
        if commission.count() >= 1:
            for cdata in commission:
                my_data = {"name":state.name, "id":state.id, "whitelabel":cdata.white_label, "super_dist":cdata.super_distributor, "distributor":cdata.distributor, "retailer":cdata.retailer, "type":cdata.type}
        else:
            my_data = {"name":state.name, "id":state.id, "whitelabel":0.0, "super_dist":0.0, "distributor":0.0, "retailer":0.0, "type":0.0}   
        data.append(my_data)
    return JsonResponse({"pdata":data})
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
    
    scheme_data = APIManager.objects.all()
    return render(request, "api.html", {"data" : scheme_data, "message": message, "mtype":mtype})

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
        com_type = request.POST.get("com_type")
        commission = CommissionType.objects.get(id=com_type)
        api = APIManager.objects.get(id=api_id)
        is_mandatory = True
        Provider.objects.create(name=name, type=type,com_type=commission, status=status, logo=file_url, is_mandatory=is_mandatory, api_id=api,re_1=re_1, re_2=re_2, re_3=re_3, re_4=re_4)
        message= "Added Successfully"
        mtype="success"
        # except:
        #     message= "Something went wrong.."
        #     mtype="failed"
    api_data = APIManager.objects.all()
    com_data = CommissionType.objects.all()

    scheme_data = Provider.objects.all()
    return render(request, "provider.html", {"data" : scheme_data,"apidata":api_data,"com_data":com_data, "message": message, "mtype":mtype})


def AddCommission(request):
    mtype = ""
    message = ""
    if(request.method == 'POST'):
        com_type_id = request.POST.get("com_id")
        scheme_id = request.POST.get("scheme_id")
        ids = request.POST.get("ids")
        types = request.POST.get("type")
        whitelabel = request.POST.get("whitelabel")
        super_dist = request.POST.get("super_dist")
        distributor = request.POST.get("distributor")
        retailer = request.POST.get("retailer")
        commission = CommissionType.objects.get(id=com_type_id)
        scheme = Scheme.objects.get(id=scheme_id)
        
        for id, type, wl, sd, dn, rt in zip(ids.split(','), types.split(','), whitelabel.split(','), super_dist.split(','), distributor.split(','), retailer.split(',')):
            print(id, type, wl, sd, dn, rt)
            operator = Provider.objects.get(id=id)
            Commission.objects.create(com_type_id=commission,operator_id=operator, scheme_id=scheme, type=type,  white_label=wl, super_distributor=sd, distributor=dn, retailer=rt)
            message= "Added Successfully"
            mtype="success"
            # pass
        # data = parse_qs(form_data, output)
        print(ids, types, whitelabel, super_dist, distributor, retailer)        
    return JsonResponse({'mtype':mtype, 'message':message})

def GetCommissionBySchemeAndCType(request):
    if(request.method == "POST"):
        com_type_id = request.POST.get('com_id')
        # scheme_id = request.POST.get('scheme_id')
        comm_data = Commission.objects.all()
        print(comm_data)
        cdata =[]
        for data in comm_data:
            com_data = { "com_type_id":data.com_type_id,  "type":data.type, "white_label":data.white_label, "super_distributor":data.super_distributor, "distributor":data.distributor, "retailer":data.retailer }
            cdata.append(com_data)
    return JsonResponse({"data":cdata})           


def ProfileManager(request):
    user = Account.objects.get(id= 2)
    # user_profile = UserProfile.objects.get(user=user)
    return render(request, 'profile.html', {"data":user}) 




## change password 

def ChangePassword(request):
    mtype =""
    message=""
    try:
        if(request.method == "POST"):
            password = request.POST.get("password")
            user = Account.objects.get(id=2)
            user.password = password
            user.save()
            mtype="success"
            message="Password Changes Successfully"
    except:
        mtype="failed"
        message="Something went wrong!...."
    return JsonResponse({"mtype":mtype, "message":message})




## mobile recharge process
def MobileRecharge(request):
    
    return render(request, "recharge.html")

def MobileRechargeRequest(request):
    if(request.method == "POST"):
        # import pdb; pdb.set_trace()
        operator = request.POST.get("operator")
        number = request.POST.get("number")
        amount = request.POST.get("amount")
        pin = request.POST.get("pin")
        user = request.POST.get("pin")
        pdata = Provider.objects.get(name=operator)
        api_data = APIManager.objects.get(id=1)
        arguments = {"username": api_data.username,"token": api_data.password, "api_code":api_data.type, "api_url":api_data.url, "number":number, "amount":amount, "opcode":pdata.re_1 }
    RechargeServiceType(arguments)
    return JsonResponse({"message":"request submitted successfully"})


def RechargeServiceType(argument):
    match argument["api_code"]:
        case "recharge1":
            transection_number = uuid.uuid4()
            api_url = "{}/recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argument["api_url"],argument["username"],argument["token"], argument["opcode"], argument["number"], argument["amount"], transection_number )
            response = requests.get(f"{api_url}")
            print(api_url)
            if(response.status_code == 200):
                print(response.json())
                return response
            else:
                return 400
            # return api_url
        case "recharge2":
            transection_number = uuid.uuid4()
            api_url = "/recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argument["username"],argument["token"], argument["opcode"], argument["number"], argument["amount"], transection_number )
            return api_url
        case "recharge3":
            transection_number = uuid.uuid4()
            api_url = "/recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argument["username"],argument["token"], argument["opcode"], argument["number"], argument["amount"], transection_number )
            return api_url
        case "recharge4":
            transection_number = uuid.uuid4()
            api_url = "/recharge/api?username={}&token={}&opcode={}&number={}&amount={}&orderid={}&format=json".format(argument["username"],argument["token"], argument["opcode"], argument["number"], argument["amount"], transection_number )
            return api_url
        case default:
            return "something went wrong"
  
 
# head = RechargeServiceType(2)
# print(head) 