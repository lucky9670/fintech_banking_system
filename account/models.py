from django.db import models
from django.contrib.auth.models import AbstractUser
from lib.models import BaseModel

# Create your models here.
class Role(BaseModel):
    name = models.CharField(max_length=250)

class Company(BaseModel):
    company_name = models.CharField(max_length=250)
    sort_name = models.CharField(max_length=20)
    website = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='media/company/')
    status = models.BooleanField()
    sender_id = models.CharField(max_length=200)
    sms_user_id = models.CharField(max_length=200)
    sms_password = models.CharField(max_length=200)
    sms_uti = models.CharField(max_length=200)
    smtp_url = models.CharField(max_length=200)
    smtp_user_name = models.CharField(max_length=200)
    smtp_password = models.CharField(max_length=200)
    smtp_port = models.CharField(max_length=200)

class Scheme(BaseModel):
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    
class Account(AbstractUser):
    """
        Inherits from default User of Django and extends the fields.
        The following fields are part of Django User Model:
        | id
        | password
        | last_login
        | is_superuser
        | username
        | first_name
        | last_name
        | email
        | is_staff
        | is_active
        | date_joined
        """
    name = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(max_length=50,blank=True,null=True)
    password = models.CharField(max_length=500)
    phone = models.CharField(max_length=50,blank=True,null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    modified_at = models.DateTimeField(editable=False, auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone"]

class UserProfile(models.Model):
    otp = models.CharField(max_length=50, blank=True, null=True)
    otp_resend = models.IntegerField(blank=True, null=True)
    wallet_ammount = models.FloatField(blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=50, default='Pending')
    shop_name = models.CharField(max_length=250, blank=True, null=True)
    gstin = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=7, blank=True, null=True)
    pan_card = models.CharField(max_length=50, blank=True, null=True)
    aadhar_card = models.CharField(max_length=50, blank=True, null=True)
    aadhar_card_front = models.ImageField(upload_to ='media/member/', blank=True, null=True)
    aadhar_card_front = models.ImageField(upload_to ='media/member/', blank=True, null=True)
    pan_card_pic = models.ImageField(upload_to='media/member/', blank=True, null=True)
    gstin_pic = models.ImageField(upload_to='media/member/', blank=True, null=True)
    profile_pic = models.ImageField(upload_to='media/member/', blank=True, null=True)
    kyc = models.CharField(max_length=50, blank=True, null=True)
    callback_url = models.CharField(max_length=250, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    reset_password = models.BooleanField(default=False)
    bank_holder_name = models.CharField(max_length=50, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    bank_ifsc = models.CharField(max_length=50, blank=True, null=True)
    app_token = models.CharField(max_length=2000, blank=True, null=True)
    old_password = models.CharField(max_length=250, blank=True, null=True)
    scheme = models.ForeignKey(Account, on_delete=models.CASCADE)
    scheme = models.ForeignKey(Scheme, blank=True, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)
