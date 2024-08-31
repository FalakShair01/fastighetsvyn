from django_filters import rest_framework as filters
from .models import Property


class PropertyFilter(filters.FilterSet):
    class Meta:
        model = Property
        fields = {
            "byggnad": ["in", "exact"],
            "gatuadress": ["in", "exact"],
            "postnummer": ["in", "exact"],
            "byggår": ["in", "exact"],
            "antal_bostäder": ["in", "exact"],
            "skyddsrum": ["in", "exact"],
            "boarea": ["in", "exact"],
            "snittarea_per_bostad": ["in", "exact"],
            "fjärrvärme": ["in", "exact"],
        }
