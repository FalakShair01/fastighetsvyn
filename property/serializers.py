from rest_framework import serializers
from .models import Property, Document


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('id', 'byggand', 'fond', 'ansvarig_AM', 'yta', 'loa', 'bta', 'lokal_elproduktion',
                  'installered_effekt', 'geo_energi', 'epc_tal', 'address', 'picture')
        
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'file',)
