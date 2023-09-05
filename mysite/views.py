from rest_framework import generics
from .models import Hotel, Room, Booking
from .serializers import HotelSerializer, RoomSerializer, BookingSerializer
from django.contrib.auth.models import User
from datetime import date, timedelta
from faker import Faker

class HotelListView(generics.ListAPIView):
    serializer_class = HotelSerializer

    def get_queryset(self):
        date = self.request.query_params.get('date')
        return Hotel.objects.filter(rooms__count__gt=0, rooms__bookings__isnull=False, rooms__bookings__date_from__lte=date, rooms__bookings__date_to__gte=date).distinct()

class RoomListView(generics.ListAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        return Room.objects.filter(hotel_id=hotel_id, count__gt=0)

class UserBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(user=user)


def create_test_data():
  fake = Faker()

  for _ in range(5):
    username = fake.user_name()
    User.objects.create(username=username)

  for _ in range(10):
    hotel = Hotel.objects.create(name=fake.company())

    for _ in range(5):
      room = Room.objects.create(hotel=hotel, name=fake.color_name(), count=fake.random_int(min=1, max=10),
                                 price=fake.random_int(min=50, max=200))

      for _ in range(3):
        user = User.objects.order_by('?').first()
        date_from = fake.date_between(start_date='-30d', end_date='today')
        date_to = date_from + timedelta(days=fake.random_int(min=1, max=7))
        room_price = room.price * (date_to - date_from).days

        Booking.objects.create(user=user, room=room, date_from=date_from, date_to=date_to, room_price=room_price)

  print("База данных заполнена тестовыми данными.")
