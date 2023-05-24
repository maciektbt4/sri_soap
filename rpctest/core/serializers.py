from rest_framework import serializers
from .models import Person
from datetime import date

class PersonSerializer(serializers.ModelSerializer):

	class Meta:
		model = Person
		fields = ['id', 'sex', 'hight', 'first_name', 'last_name', 'job', 'email', 'birth_date']

