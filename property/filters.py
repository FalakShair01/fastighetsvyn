from django_filters import rest_framework as filters
from .models import Property


class PropertyFilter(filters.FilterSet):
    class Meta:
        model = Property
        fields = {
            "byggnad": ["icontains"],
            "byggår": ["icontains"],
            "boarea": ["icontains"],
            "fastighetsbeteckning": ["icontains"],
            "hiss": ["exact"],
            "skyddsrum": ["exact"],
            "antal_våningar": ["icontains"],
            "antal_bostäder": ["icontains"],
            "fjärrvärme": ["exact"],
            "solpaneler": ["exact"],
            "ventilationssystem": ["icontains"],
            "uppvärmningssystem": ["icontains"],
            "postnummer": ["icontains"],
            "gatuadress": ["icontains"],
        }
