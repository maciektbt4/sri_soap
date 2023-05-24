from django.db import models
import datetime

# Create your models here.
class Person(models.Model):
    sex = models.CharField(max_length=50)
    hight =models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    job = models.CharField(max_length=50)
    email = models.EmailField(verbose_name="Email")
    birth_date = models.DateField(default=datetime.date.today)

    #display the data with first_name
    def __str__(self):
        return self.first_name
