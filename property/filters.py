from django_filters import rest_framework as filters
from .models import Property


class PropertyFilter(filters.FilterSet):
    class Meta:
        model = Property
        fields = {
            "byggnad": ["in"],
            "byggår": ["in"],
            "boarea": ["in"],
            "fastighetsbeteckning": ["in"],
            "hiss": ["exact"],
            "skyddsrum": ["exact"],
            "antal_våningar": ["in"],
            "antal_bostäder": ["in"],
            "fjärrvärme": ["exact"],
            "solpaneler": ["exact"],
            "ventilationssystem": ["in"],
            "uppvärmningssystem": ["in"],
            "postnummer": ["in"],
            "gatuadress": ["in"],
        }
