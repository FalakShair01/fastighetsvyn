from django_filters import rest_framework as filters
from .models import Property


class PropertyFilter(filters.FilterSet):
    class Meta:
        model = Property
        fields = {
            "byggnad": ["in", "exact", "icontains"],
            "byggår": ["in", "exact", "icontains"],
            "boarea": ["in", "exact", "icontains"],
            "fastighetsbeteckning": ["in", "exact", "icontains"],
            "hiss": ["exact"],
            "skyddsrum": ["exact"],
            "antal_våningar": ["in", "exact", "icontains"],
            "antal_bostäder": ["in", "exact", "icontains"],
            "fjärrvärme": ["exact"],
            "solpaneler": ["exact"],
            "ventilationssystem": ["in", "exact", "icontains"],
            "uppvärmningssystem": ["in", "exact", "icontains"],
            "postnummer": ["in", "exact", "icontains"],
            "gatuadress": ["in", "exact", "icontains"],
        }
