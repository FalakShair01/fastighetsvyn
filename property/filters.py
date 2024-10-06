from django_filters import rest_framework as filters
from .models import Property


class PropertyFilter(filters.FilterSet):
    class Meta:
        model = Property
        fields = {
            "byggnad": ["in"],
            "byggår": ["in", "exact"],
            "boarea": ["in", "exact"],
            "fastighetsbeteckning": ["in", "exact"],
            "hiss": ["exact"],
            "skyddsrum": ["exact"],
            "antal_våningar": ["in", "exact"],
            "antal_bostäder": ["in", "exact"],
            "fjärrvärme": ["exact"],
            "solpaneler": ["exact"],
            "ventilationssystem": ["in", "exact"],
            "uppvärmningssystem": ["in", "exact"],
            "postnummer": ["in", "exact"],
            "gatuadress": ["in", "exact"],
        }