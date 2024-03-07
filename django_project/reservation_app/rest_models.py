from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyCustomerManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Customer model
class Rest_Customer(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_admin = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyCustomerManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

# IHA model
class Rest_IHA(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=3)
    image = models.ImageField(upload_to='iha_images/')

    def __str__(self):
        return f"{self.brand} {self.model}"

# Reservation model
class Rest_Reservation(models.Model):
    customer = models.ForeignKey(Rest_Customer, on_delete=models.CASCADE)
    iha = models.ForeignKey(Rest_IHA, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    number = models.IntegerField()
    start_date = models.DateField()
    finish_date = models.DateField()

    def __str__(self):
        return f"Reservation {self.id} by {self.customer.username}"
