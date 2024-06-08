from django.conf import settings
from django.db import models
from django.utils import timezone

class VendorRequest(models.Model):
    vendoruser = models.CharField(null=True,max_length=20)

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

class Checkoutenquiry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20,null=True)
    second_name = models.CharField(max_length=20,null=True)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=50,null=True)
    district = models.CharField(max_length=50,null=True)
    pin = models.IntegerField(null=True)
    phone = models.CharField(null=True, max_length=10)
    tour_date = models.DateField(null=True)
    tour_travellers = models.IntegerField(null=True)

class Hotel_Checkoutenquiry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    full_name = models.CharField(null=True,max_length=100)
    email = models.EmailField(null=True)
    aadhar = models.CharField(null=True,max_length=12)
    phone = models.CharField(null=True,max_length=10)

    def __str__(self):
        return self.full_name
    
class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    place = models.CharField(max_length=50)


class Tour(models.Model):
    name = models.CharField('Tour name', max_length=60)
    description = models.TextField('Tour description')
    started = models.DateTimeField('Started date')
    expiry = models.DateField('Expiry date', null=True)
    duration = models.IntegerField('Tour duration')
    price = models.IntegerField('Tour price')
    image = models.ImageField('Tour image', upload_to='tours/')
    approved = models.BooleanField('Approved', default=False)

    def is_expired(self):
        return timezone.now() > self.expiry

    def __str__(self):
        return self.name
    # customer = models.ManyToManyField(Customer)


class OrderTour(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    # orders =

    def __str__(self):
        return self.tour.name


class Hotel(models.Model):
    name = models.CharField('Hotel name', max_length=60)
    city = models.CharField('Hotel city', max_length=60)
    price = models.IntegerField('Price for one person')
    hotelClass = models.IntegerField('Class of the hotel')
    image = models.ImageField('Tour image', upload_to='hotels/')

    def __str__(self):
        return self.name


class OrderHotel(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    def __str__(self):
        return self.hotel.name


# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     start_date = models.DateTimeField(auto_now_add=True)
#     ordered = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.user.name