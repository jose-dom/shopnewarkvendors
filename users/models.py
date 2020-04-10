from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from PIL import Image
from django.urls import reverse
from phone_field import PhoneField
from multiselectfield import MultiSelectField

BANNER_CHOICES = (
    ("Please create my banners. I understand there is a cost of $25","Please create my banners. I understand there is a cost of $25"),
    ("No, thank you. I will email you my banners (No Cost). If I do not email you my banners within 5 business days, I authorize you to create the banners for us at the above cost of $25 for both banners.","No, thank you. I will email you my banners (No Cost). If I do not email you my banners within 5 business days, I authorize you to create the banners for us at the above cost of $25 for both banners.")
)

BUSINESS_STRUCTURE_CHOICES = (
    ("Sole Proprietorship","Sole Proprietorship"),
    ("Limited Liability Corporation","Limited Liability Corporation"),
    ("S Corp","S Corp"),
    ("Other","Other")
)

LOCATION_TYPE = (
    ("Physical Location","Physical Location"),
    ("Home-based","Home-based"),
    ("Online","Online")
)

SPECIAL_BUSINESS = (
    ("Minority Owned","Minority Owned"),
    ("Woman Owned","Woman Owned"),
    ("MWBE Certified","MWBE Certified")
)

TAX_CREDIT_OPTIONS = (
    ("On line, manually (Free)","On line, manually (Free)"),
    ("Downloading the application onto my own Android (Free)","Downloading the application onto my own Android (Free)"),
    ("Fincredit’s Dedicated Device and Stand ($90)","Fincredit’s Dedicated Device and Stand ($90)")
)

TAX_CREDITS_RATES = (
    ("Cost to me: 10%, Net Reward to Customer: 7.0%","Cost to me: 10%, Net Reward to Customer: 7.0%"),
    ("Cost to me: 14.3%, Net Reward to Customer: 10%","Cost to me: 14.3%, Net Reward to Customer: 10%"),
    ("Cost to me: 17.1%, Net Reward to Customer: 12%","Cost to me: 17.1%, Net Reward to Customer: 12%"),
    ("Other","Other")
)

TERMS_CONDITIONS = (
    ("AGREE", "Agree"),
    ("DISAGREE", "Disagree")
)

APPROVED_OPTIONS = (
    ("YES", "YES"),
    ("NO", "NO")
)

class Manager(BaseUserManager):
    def create_user(self, email, company_name, legal_name, address, business_type, contact_name, phone_number, website, banner, business_structure, length_of_operation, number_of_employees, location_type, speical_business, terms_conditions, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not company_name:
            raise ValueError("Users must have an company name")
        if not legal_name:
            raise ValueError("Users must have an legal name")
        if not address:
            raise ValueError("Users must have an address")
        if not business_type:
            raise ValueError("Users must have an business type")
        if not contact_name:
            raise ValueError("Users must have an contact name")
        if not phone_number:
            raise ValueError("Users must have an phone number")
        if not website:
            raise ValueError("Users must have an website")
        if not banner:
            raise ValueError("Users must have an banner")
        if not business_structure:
            raise ValueError("Users must have an business structure")
        if not length_of_operation:
            raise ValueError("Users must have an length of operation")
        if not number_of_employees:
            raise ValueError("Users must have an number of employees")
        if not location_type:
            raise ValueError("Users must have an location type")
        if not speical_business:
            raise ValueError("Users must have an special business")
        if not terms_conditions:
            raise ValueError("Users must have an terms and conditions")

        user = self.model(
            email=self.normalize_email(email),
            password=password,
            company_name=company_name,
            legal_name=legal_name,
            address=address,
            business_type=business_type,
            contact_name=contact_name,
            phone_number=phone_number,
            website=website,
            banner=banner,
            business_structure=business_structure,
            length_of_operation=length_of_operation,
            number_of_employees=number_of_employees,
            location_type=location_type,
            speical_business=speical_business,
            terms_conditions=terms_conditions
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, company_name, legal_name, address, business_type, contact_name, phone_number, website, banner, business_structure, length_of_operation, number_of_employees, location_type, speical_business, terms_conditions, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            company_name=company_name,
            legal_name=legal_name,
            address=address,
            business_type=business_type,
            contact_name=contact_name,
            phone_number=phone_number,
            website=website,
            banner=banner,
            business_structure=business_structure,
            length_of_operation=length_of_operation,
            number_of_employees=number_of_employees,
            location_type=location_type,
            speical_business=speical_business,
            terms_conditions=terms_conditions
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email Address", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name="Date Joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last Login", auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    ##company info
    company_name = models.CharField(max_length=100, unique=False, verbose_name="Name of Business")
    legal_name = models.CharField(max_length=100, unique=False, verbose_name="Legal Name")
    address = models.CharField(max_length=100, unique=False, verbose_name="Address")
    business_type = models.CharField(max_length=100, unique=False, verbose_name="Type of Business")
    contact_name = models.CharField(max_length=100, unique=False, verbose_name="Contact Name")
    phone_number = models.CharField(max_length=12, blank=False, help_text="Contact Phone Number")
    website = models.CharField(max_length=30, unique=False, verbose_name="Website", help_text="Ex: www.example.com")

    ##banking info
    bank_name = models.CharField(max_length=100, unique=False, verbose_name="Bank Name", default="", blank=True)
    branch_location = models.CharField(max_length=100, unique=False, verbose_name="Branch Location", default="", blank=True)
    aba_number = models.CharField(max_length=100, unique=False, verbose_name="ABA Number", default="", blank=True)
    account_number = models.CharField(max_length=100, unique=False, verbose_name="Account Number", default="", blank=True)

    ##banner info
    banner = models.CharField(verbose_name="Options", max_length=1000, choices=BANNER_CHOICES)

    ##speical business info
    business_structure = models.CharField(max_length=1000, choices=BUSINESS_STRUCTURE_CHOICES)
    length_of_operation = models.CharField(max_length=100, unique=False, verbose_name="Length of Operation", help_text="Ex: 10 months")
    number_of_employees = models.CharField(max_length=100, unique=False, verbose_name="Number of Employees", help_text="Ex: 12 employees")
    location_type = MultiSelectField(choices=LOCATION_TYPE, unique=False, verbose_name="Does your business have a physical location? (Check all that apply)")
    speical_business = MultiSelectField(choices=SPECIAL_BUSINESS, unique=False, verbose_name="Is your business: (Check all that apply)")

    ##tax credits
    tax_credits = models.CharField(max_length=1000, choices=TAX_CREDIT_OPTIONS)
    rate = models.CharField(choices=TAX_CREDITS_RATES, max_length=50, verbose_name="Percentage", default='', null=False)

    ##terms and conditions
    terms_conditions = models.CharField(choices=TERMS_CONDITIONS, blank=False, verbose_name="Terms & Coniditons", default='Agree', max_length=8)

    ##approved
    approved = models.CharField(choices=APPROVED_OPTIONS, default="NO", verbose_name="Application Approved", max_length=3)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'company_name','legal_name', 'address', 'business_type', 'contact_name', 'phone_number', 'website',
        'banner',
        'business_structure', 'length_of_operation', 'number_of_employees', 'location_type', 'speical_business',
        'terms_conditions'
    ]

    objects = Manager()

    def __str__(self):
        return self.email + ", " + self.company_name

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def get_absolute_url(self):
        return reverse("user-detail", kwargs={'email': self.email})


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics', verbose_name="Profile Image")

    def __str__(self):
        return f'{self.user.email} Profile'
