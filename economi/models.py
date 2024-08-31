from django.db import models
from property.models import Property
from users.models import User


# Create your models here.
def expense_file_upload(instance, filename):
    return "/".join(["expense", str(instance.user.username), filename])


class Expense(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_expenses"
    )
    type_of_transaction = models.CharField(max_length=255)
    type_of_cost_or_revenue = models.CharField(max_length=255)
    date_of_transaction = models.DateField(null=True)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    value_added_tax = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    account = models.TextField(null=True)
    building = models.ForeignKey(
        Property, on_delete=models.SET_NULL, related_name="building_expenses", null=True
    )
    comment = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to=expense_file_upload, blank=True, null=True)

    def __str__(self):
        return f"{self.type_of_transaction} - {self.user.username}"
