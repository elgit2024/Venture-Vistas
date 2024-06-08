from django.contrib import admin
from .models import Tour, Hotel, OrderHotel, Checkoutenquiry, Payment, Hotel_Checkoutenquiry
from .models import OrderTour, Customer, VendorRequest

# Register your models here.
admin.site.register(Tour)
admin.site.register(Customer)
admin.site.register(OrderTour)
admin.site.register(Hotel)
admin.site.register(OrderHotel)
admin.site.register(Checkoutenquiry)
admin.site.register(VendorRequest)
admin.site.register(Payment)
admin.site.register(Hotel_Checkoutenquiry)
