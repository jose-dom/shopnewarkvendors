from django.db import models
from django.urls import reverse
from django.conf import settings
from users.models import User
from PIL import Image

OPTIONS = (
    ('None','None'),
    ('Sale','Sale'),
    ('Return','Return'),
)

class Transaction(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    customer = models.CharField(max_length=12, null=False, default='', verbose_name="Customer Phone Number")
    date_time = models.CharField(max_length=50, default='')
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    options = models.CharField(max_length=12, null=False, default='Other', verbose_name="Options", choices=OPTIONS)



