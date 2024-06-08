from django.urls import path

from . import views
from django.contrib import admin


app_name = 'blog'
urlpatterns = [

    path('', views.index, name='index'),
    path('services', views.services, name='services'),
    path('checkout', views.checkout, name='checkout'),
    path('hotel_checkout', views.hotel_checkout, name='hotel_checkout'),

    # Tours Page
    path('tours', views.tours, name='tours'),
    path('tour/<id>', views.detail_view, name='detail_view'),
    # Search Tour
    path('search_tours', views.search_tours, name='search_tours'),

    # Login / Sign Up / Logout / Admin
    path('admin', admin.site.urls),
    path('vendorsignup/', views.vendor_signup, name='vsignup'),
    path('vendorlogin/', views.vendor_login, name='vlogin'),
    path('vendor_req', views.vendor_req, name='vendor_req'),
    path('vendor_req_save', views.vendor_req_save, name='vendor_req_save'),
    path('signup', views.signUp_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),

    path('base_admin', views.base_admin_view, name='base_admin'),

    # CRUD
    path('add_tour', views.addTour, name='add_tour'),
    path('tours_list', views.tours_list, name='tours_list'),
    path('tour/<id>/edit', views.tour_edit, name='tour_edit'),
    path('tour/<id>/delete', views.tour_delete, name='tour_delete'),
    path('tour/detail/<id>', views.tour_detail, name='tour_detail'),
    path('tour/admin/users_list', views.users_list, name='users_list'),
    path('tour/admin/user_detail/<id>', views.user_detail, name='user_detail'),

# ------- Order Tour urls -------
    path('payment', views.payment, name='payment'),
    path('tour/add_to_cart/<id>', views.add_to_cart, name='add_to_cart'),
    path('order', views.order, name='order'),
    path('savecheckout/',views.save_checkout, name='savecheckout'),
    path('savepayment',views.save_payment, name='savepayment'),
    path('order_delete/<id>', views.order_delete, name='order_delete'),

# ------- Hotel urls -------
    path('hotel/add', views.addHotel, name='hotel_add'),
    path('hotel/hotels_list', views.hotels_list, name = 'hotels_list'),
    path('hotel/<id>', views.hotel_detail, name='hotel_detail'),
    path('save_hotelcheckout/',views.save_hotelcheckout, name='save_hotelcheckout'),
    path('hotel/<id>/admin', views.hotel_detail_admin, name = 'hotel_detail_admin'),
    path('hotel/<id>/edit', views.hotel_edit, name='hotel_edit'),
    path('hotel/<id>/delete', views.hotel_delete, name='hotel_delete'),

    path('hotel/<id>/orderHotel', views.orderHotel, name='orderHotel'),
    path('myHotelOrders', views.myHotelOrders, name='myHotelOrders'),
    path('hotel/<id>/orderHotelDelete', views.orderHotelDelete, name='orderHotelDelete'),

]
