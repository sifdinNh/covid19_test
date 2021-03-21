from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField




class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def get_profile_image_filepath(self, filename):
    return 'profile_images/' + str(self.pk) + '/profile_image.png'

def get_default_profile_image():
    return "Capture.png"

class Centre(models.Model):
    address = models.CharField(max_length=60)
    name=models.CharField(max_length=40)
    capacity=models.IntegerField(null=True, blank=True)


    def __str__(self):
        return "{}".format(self.name)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    class Types(models.TextChoices):
        CIT = "CIT", "Citoyen"
        C_ADMIN = "C_ADMIN", "Center_admin"
        ADMIN= "ADMIN", "Admin"


    base_type = Types.CIT


    type = models.CharField( max_length=50, choices=Types.choices, default=base_type)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True,
                                      default=get_default_profile_image)
    center=models.ForeignKey(Centre, on_delete=models.CASCADE, null=True, blank=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]
    def get_full_name(self):
        return self.first_name + " " + self.last_name
    def is_Citoyen(self):
        if self.type == UserAccount.Types.CIT:
            return True
        return False
    def is_Administrateur(self):
        if self.type == UserAccount.Types.C_ADMIN:
            return True
        return False

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.email



class Citoyen(models.Model):
    user=models.OneToOneField(UserAccount,on_delete=models.CASCADE)
    CID=models.CharField(max_length=8,unique=True)
    RAMID=models.CharField(max_length=10, unique=True, default=0000000,blank=True, null=True)

    cov_19=models.BooleanField(default=False)
    date_N=models.DateField()
    address=models.CharField(max_length=60)
    phone = PhoneNumberField(null=True,blank=True)
    is_RDV = models.BooleanField(default=False)
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    def get_id(self):
        return self.user.id

    def __str__(self):
        return "{} {}  CID: {}".format(self.user.first_name,self.user.last_name,self.CID)

class RDV(models.Model):
    citoyen=models.OneToOneField(Citoyen,on_delete=models.CASCADE)
    date_RDV = models.DateTimeField(auto_now_add=True)
    is_confirmed=models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    center_id   = models.IntegerField(default=0,blank=True,null=True)
    def __str__(self):
        return self.citoyen.CID











class Administrateur(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    status = models.BooleanField(default=False)
    centre=models.ForeignKey(Centre,on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + "[" + self.centre.name + "]"
