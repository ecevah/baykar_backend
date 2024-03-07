from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator
from enum import Enum
from datetime import datetime
import pytz

class CategoryChoices(Enum):
    OPTION1 = 'IHA 0'
    OPTION2 = 'IHA 1'
    OPTION3 = 'IHA 2'
    OPTION4 = 'IHA 4'

class IHA(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    weight = models.IntegerField()
    category = models.CharField(
        max_length=50,
        choices=[(tag.name, tag.value) for tag in CategoryChoices]
    )
    price = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='iha_images/', null=True, blank=True)

class Customers(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(6),
        ]
    )

    def clean(self):
        if not any(c.islower() for c in self.password) or not any(c.isupper() for c in self.password):
            raise ValidationError("Password must contain at least one uppercase and one lowercase letter.")
        

class Reservations(models.Model):
    iha = models.ForeignKey(IHA, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    start_date = models.DateTimeField()  
    finish_date = models.DateTimeField() 
    total_price = models.IntegerField(validators=[MinValueValidator(0)])
    number = models.IntegerField(default=1)

    def clean(self):
        now = datetime.now(pytz.timezone('UTC')) 
        if self.start_date < now:
            raise ValidationError("The start date and time cannot be in the past.")
        if self.finish_date < self.start_date:
            raise ValidationError("The finish date and time cannot be earlier than the start date and time.")
