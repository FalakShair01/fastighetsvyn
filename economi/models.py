from django.db import models

# Create your models here.
class Account(models.Model):
    pass

class Expense(models.Model):
    TYPES_OF_EXPEBDITURE = (
    ("Energi", "Energi"),
    ("Vatten", "Vatten"),
    )
    type_of_expenditure = models.CharField(max_length=6, choices=TYPES_OF_EXPEBDITURE)

