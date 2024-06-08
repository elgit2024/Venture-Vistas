from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.models import User
from .models import Tour, OrderTour, Customer, Hotel, OrderHotel, Checkoutenquiry, VendorRequest, Payment, Hotel_Checkoutenquiry
from .forms import TourForm, CustomerForm, HotelForm

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from blog.models import Tour
from django.utils import timezone
# --------- Site Pages ----------------

def payment(request):
    return render(request, 'blog/payment.html')

def save_payment(request):
    if request.method == "POST":
        user = request.user
        pt = Payment(user=user)
        pt.save()
    return redirect('blog:payment')
    
def index(request):
    tours = Tour.objects.all()
    todaysDate = datetime.today()
    print( todaysDate)
    return render(request, 'blog/index.html', {'tours': tours, 'todaysDate': todaysDate})

def search_tours(request):
    tours = Tour.objects.all()
    searched_tours = {}

    if request.method == 'POST':
        tourName = request.POST["tourName"]
        tourDate = request.POST["tourDate"]
        print(tourName)
        print(tourDate)
        if tourName == "none":
            print("with none")
            searched_tours = tours.filter(started__gt=tourDate)  
        else:
            print("without none")
            searched_tours = tours.filter(name__contains=tourName) | tours.filter(started__gt=tourDate)

    return render(request, 'blog/tours.html', {'tours': tours, 'searched_tours': searched_tours})

def services(request):
    hotels = Hotel.objects.all()
    searched_hotels = {}
    if request.method == 'POST':
        cityOrName = request.POST["cityOrName"]
        hotelClass = request.POST["hotelClass"]

        searched_hotels = Hotel.objects.filter(name__contains=cityOrName) | Hotel.objects.filter(city__contains=cityOrName) | Hotel.objects.filter(hotelClass=hotelClass)
    context = {'hotels':hotels, 'searched_hotels': searched_hotels}
    return render(request, 'blog/services.html', context)


def checkout(request):
    return render(request, 'blog/checkout.html')

def save_checkout(request):
    if request.method == "POST":
        user = request.user
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        state = request.POST.get('state')
        district = request.POST.get('district')
        pin = request.POST.get('pin')
        phone = request.POST.get('phone')
        tour_date = request.POST.get('tour_date')
        tour_travellers = request.POST.get('tour_travellers')
        en = Checkoutenquiry(first_name=first_name,second_name=second_name,email=email,address=address,state=state,district=district,pin=pin,phone=phone, user=user,tour_date=tour_date,tour_travellers=tour_travellers)
        en.save()
        messages.success(request, "Checkout information saved successfully.")
    return redirect('blog:tours')

def vendor_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('blog:add_tour')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/vendor_login.html', {'form': form})

def vendor_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Signup successful! Welcome!')
            return redirect('blog:vlogin')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/vendor_signup.html', {'form': form})

# ------------- Tour operations -----------------
@login_required(login_url='blog:login')
def addTour(request):
    # create object of form
    form = TourForm(request.POST or None, request.FILES or None)

    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        form.save()
        messages.info(request, "The tour added successfully!")
        return HttpResponseRedirect("/tours_list")

    return render(request, 'blog/../../templates/admin/add_tour.html', {'form': form})


@login_required(login_url='blog:login')
def tour_edit(request, id):
    tour = Tour.objects.get(id=id)
    form = TourForm(instance=tour)

    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            form.save()
            messages.info(request, "The tour updated successfully!")
            return HttpResponseRedirect("/tours_list")

    return render(request, 'blog/../../templates/admin/tour_edit.html', {'form': form})


def expirytime(request):
    now = timezone.now()
    tours = Tour.objects.filter(approved=True, expiry__lte=now)
    return render(request, 'blog/tours.html', {'expirytime': tours})

def home_page(request):
    now = timezone.now().date()
    tours = Tour.objects.filter(expiry__gte=now)
    return render(request, 'blog/tours.html', {'tours': tours})

def detail_view(request, id):
    tour = Tour.objects.get(id = id)
    return render(request, "blog/detail_view.html", {'tour':tour})


def tour_detail(request, id):
    tour = Tour.objects.get(id = id)
    return render(request, "admin/tour_detail.html", {'tour':tour})


@login_required(login_url='blog:login')
def tour_delete(request, id):
    context = {'id':id}

    # fetch the object related to passed id
    obj = get_object_or_404(Tour, id=id)

    if request.method == "POST":
        if request.POST.get('submit') == 'Yes':
            obj.delete()
            messages.info(request, "The tour Deleted successfully!")
            return HttpResponseRedirect("/tours_list")
        else:
            return HttpResponseRedirect("/tours_list")

    return render(request, "blog/../../templates/admin/tour_delete.html", context)


def tours(request):
    tours = Tour.objects.all()
    # tours.count()
    return render(request, 'blog/tours.html', {'tours': tours})


def tours_list(request):
    context = {'tours': Tour.objects.all()}
    return render(request, 'admin/tours_list.html', context)

# ------------ Login / Sign UP operations -----------------
@login_required(login_url='blog:login')
def vendor_req(request):
    return render(request, 'accounts/vendor_request.html')

def vendor_req_save(request):
    if request.method == "POST":
        vendoruser = request.POST.get('vendoruser')
        db = VendorRequest(vendoruser=vendoruser)
        db.save()
    return render(request, 'blog/index.html')


def signUp_view (request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:tours')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/sign_up.html', {'form':form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('blog:tours')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('blog:index')


@login_required(login_url='blog:login')
def base_admin_view(request):
    return render(request, 'admin/base_admin.html')


@login_required(login_url='blog:login')
def add_to_cart(request, id):
    tour = get_object_or_404(Tour, id=id)
    # tour = Tour.objects.filter(id=id)

    order_item, created = OrderTour.objects.get_or_create(
        tour=tour,
        customer=request.user,
        ordered=True,
    )
    if created:
        messages.info(request, "This item is added to your cart!")
        return redirect("blog:checkout")
    else:
        order_item.save()
        messages.info(request, "This item is added to your cart!")
        return redirect("blog:checkout")


@login_required
def order(request):
    orders = OrderTour.objects.filter(customer=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'admin/user/user_order.html', context)


@login_required
def users_list(request):
    orders = OrderTour.objects.filter(customer=request.user, ordered=True)
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'admin/user/users_list.html', context)


@login_required
def user_detail(request, id):
    user = get_object_or_404(User, id=id)
    user_orders = user.ordertour_set.all()
    checkoutorder = Checkoutenquiry.objects.filter(user=user)
    context = {
        'user': user,
        'user_orders': user_orders,
        'checkoutorder':checkoutorder,
    }
    return render(request, 'admin/user/user_detail.html', context)


@login_required
def order_delete(request, id):
    order = get_object_or_404(OrderTour, id=id)

    if request.method == "POST":
        if request.POST.get('submit') == 'Yes':
            order.delete()
            messages.info(request, "The tour Deleted successfully!")
            return HttpResponseRedirect("/order")
        else:
            return HttpResponseRedirect("/tours_list")

    return render(request, 'admin/user/user_order_delete.html')


# ----------- Hotel views --------------------
@login_required(login_url='blog:login')
def addHotel(request):
    form = HotelForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.info(request, "The Hotel Added Successfully!")
            return HttpResponseRedirect("hotels_list")

    return render(request, 'admin/hotel/add_hotel.html', {'form': form})


@login_required(login_url='blog:login')
def hotel_edit(request, id):
    hotel = Hotel.objects.get(id=id)
    form = HotelForm(instance=hotel)

    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            messages.info(request, "The "+hotel.name+" edited successfully!")
            return HttpResponseRedirect("/hotel/" + id)

    return render(request, 'admin/hotel/hotel_edit.html', {'form': form})


@login_required(login_url='blog:login')
def hotel_delete(request, id):
    context = {'id':id}

    # fetch the object related to passed id
    obj = get_object_or_404(Hotel, id=id)

    if request.method == "POST":
        if request.POST.get('submit') == 'Yes':
            obj.delete()
            messages.info(request, "The Hotel Deleted Successfully!")
            return HttpResponseRedirect("/hotel/hotels_list")
        else:
            return HttpResponseRedirect("/hotel/hotels_list")

    return render(request, "admin/hotel/hotel_delete.html", context)

def hotels_list(request):
    hotels = Hotel.objects.all()
    return render(request, "admin/hotel/hotels_list_admin.html", {'hotels': hotels})


def hotel_detail_admin(request, id):
    hotel = Hotel.objects.get(id=id)
    return render(request, "admin/hotel/hotel_detail_admin.html",{'hotel':hotel})


def hotel_detail(request, id):
    hotel = Hotel.objects.get(id=id)
    return render(request, "admin/hotel/hotel_detail.html",{'hotel': hotel})


# ----------- Hotel Orders -------------
@login_required(login_url='blog:login')
def orderHotel(request, id):
    hotel = get_object_or_404(Hotel, id=id)

    order_item, created = OrderHotel.objects.get_or_create(
        hotel=hotel,
        customer=request.user,
    )
    if created:
        messages.info(request, "This item is added to your cart!")
        return redirect("blog:hotel_checkout")
    else:
        order_item.save()
        messages.info(request, "This item is added to your cart.")
        return redirect("blog:hotel_checkout")

@csrf_protect
def hotel_checkout(request):
    return render(request, 'blog/hotel_checkout.html')

@csrf_protect
def save_hotelcheckout(request):
    if request.method == "POST":
        user = request.user
        full_name = request.POST.get('Full_name')
        aadhar = request.POST.get('Adhar Number')
        email = request.POST.get('Email')
        phone = request.POST.get('Phone Number')
        
        print(f"Received data: user={user}, full_name={full_name}, aadhar={aadhar}, email={email}, phone={phone}")
        
        if not all([full_name, aadhar, email, phone]):
            messages.error(request, "All fields are required.")
            return redirect('blog:hotel_checkout')
        
        ft = Hotel_Checkoutenquiry(user=user, full_name=full_name, email=email, aadhar=aadhar, phone=phone)
        try:
            ft.save()
            print("Data saved successfully.")
            messages.success(request, "Checkout information saved successfully.")
        except Exception as e:
            print(f"Error saving data: {e}")
            messages.error(request, f"An error occurred: {e}")
            return redirect('blog:hotel_checkout')
        
        return redirect('blog:services')
    else:
        print("Request method is not POST.")
        return redirect('blog:hotel_checkout')

@login_required(login_url='blog:login')
def myHotelOrders(request):
    orders = OrderHotel.objects.filter(customer=request.user)
    print("222")
    context = {'orders': orders}
    return render(request, "admin/hotel/hotel_orders_admin.html", context)


@login_required
def orderHotelDelete(request, id):
    order = get_object_or_404(OrderHotel, id=id)

    if request.method == "POST":
        if request.POST.get('submit') == 'Yes':
            order.delete()
            messages.info(request, "The Hotel Deleted From Orders Successfully!")
            return HttpResponseRedirect("/myHotelOrders")
        else:
            return HttpResponseRedirect("/myHotelOrders")

    return render(request, 'admin/hotel/hotel_order_delete.html')