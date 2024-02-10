import requests
import urllib.parse

from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Property


@receiver(post_save, sender=Property)
def calculate_long_lat(sender, instance, created, **kwargs):
    if created:
        address = instance.address
        url = 'https://nominatim.openstreetmap.org/search?q=' + urllib.parse.quote(address) + '&format=json'
        try:
            response = requests.get(url).json()

            if response:
                print(response)
                # Check if response has data
                latitude = response[0]["lat"]
                longitude = response[0]["lon"]

                # Update the instance with the fetched latitude and longitude
                instance.latitude = latitude
                instance.longitude = longitude
                instance.save()

        except requests.RequestException as e:
            # Handle request exception (e.g., connection error, timeout)
            print(f"Error fetching coordinates: {e}")




