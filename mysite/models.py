from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Hotel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    class Meta:
      app_label = 'mysite'

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)
    count = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    date_from = models.DateField()
    date_to = models.DateField()
    room_price = models.IntegerField()

    @property
    def total_price(self):
        return self.room_price * (self.date_to - self.date_from).days

    @property
    def total_days(self):
        return (self.date_to - self.date_from).days

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username} - {self.room.name}"
