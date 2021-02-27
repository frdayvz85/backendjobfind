import django_filters
from django_filters import BooleanFilter
from .models import *
from django.forms import CheckboxInput

TYPE_CHOICES = (
    (0, 'Online'),
    (1, 'Physical'),
)

class JobFilter(django_filters.FilterSet):
    new_type = BooleanFilter(field_name="type")
    class Meta:
        model = Job
        fields = ('type', 'level', 'experience')
        exclude = ['type']




# , widget=CheckboxInput(attrs={'class': 'form-control'})