from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    byggnad = serializers.ReadOnlyField(source="building.byggnad")

    class Meta:
        model = Expense
        fields = "__all__"
        extra_kwargs = {"attachment": {"required": False}}

    def validate_attachment(self, value):
        if value in [None, ""]:
            return None
        return value
