from django.shortcuts import render, redirect, HttpResponse
from .models import Users, Userprofile, BookDetail, Cart, Orders
from seller . models import Seller
from django.core.mail import send_mail
import random
from django.contrib import messages
from socket import gaierror
from opskube_task import settings
# Create your views here.
def signup(request):
    if request.session.get('email1'):
        return redirect('dashboard')

    if 'verify' in request.POST:
        otp_val= request.POST.get('otp_val')
        if otp_val=='':
            messages.success(request, 'Blank Fields Are Not Allowed!')
            return render(request, 'verification.html')
        # print(otp_val)
        # print(type(otp_val))
        name2 = request.session.get('name1')
        email1 = request.session.get('email01')
        phone2 = request.session.get('phone1')
        password2 = request.session.get('password1')
        otp2 = request.session.get('otp1')
        print(name2, email1,phone2,password2, otp_val, otp2)

        if int(otp2)==int(otp_val):
            Users.objects.create(name=name2, email=email1,password=password2, phone=phone2)
            print('data save')
            del request.session['name1']
            del request.session['email01']
            del request.session['otp1']
            del request.session['phone1']
            del request.session['password1']
            return redirect('signin')


        else:
            messages.success(request, 'OTP not match!')
            return render(request,'verification.html')


    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('pass')
        phone=request.POST.get('contact')
        otp=random.randrange(111111,999999)
        dict={
            'name':name,
            'email':email,
            'phone':phone,
            'otp':otp
        }
        allmatch = Users.objects.filter(email=email, phone=phone)
        if allmatch:
            message = 'Email & Contact already exists'
            dict = {
                'msg': message
            }
            return render(request, 'signup.html', dict)

        match = Users.objects.filter(email=email)
        if match:
            message = 'Email already exists'
            dict = {
                'msg': message
            }
            return render(request, 'signup.html', dict)

        if match:
            message='Email already exists'
            dict={
                'msg':message
            }
            return render(request, 'signup.html',dict)
        match2= Users.objects.filter(phone=phone)
        if match2:
            message='Contact number already exists'
            dict={
                'msg':message
            }
            return render(request, 'signup.html',dict)

        try:
            send_mail('Online Bookstore email verification', f'Hello {name}!, Thanks for regiser in online bookstore. Your one time password is {otp}', settings.EMAIL_HOST_USER, [email])
            request.session['otp1'] = otp
            request.session['name1'] = name
            request.session['email01'] = email
            request.session['phone1'] = phone
            request.session['password1'] = password
            return render(request, 'verification.html')



        except gaierror:
            message='🌐 Please check your internet connection'
            dict={
                'msg':message
            }
            return render(request, 'signup.html',dict)
        except:
            message='Please Try Again'
            dict={
                'msg':message
            }
            return render(request, 'signup.html',dict)
    return render(request, 'signup.html')


def signin(request):
    if request.session.get('email1'):
        return redirect('signup')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        if email == "":
            dict = {
                'msg': 'Please enter email address',
            }
            return render(request, 'login.html', dict)

        ps = Users.objects.filter(email=email, password=password)
        if ps:
            request.session['email1'] = email
            return redirect('dashboard')
        else:
            dict = {
                'msg': 'Email or Password not match',
            }
            return render(request, 'signin.html', dict)

    return render(request, 'signin.html')

def dashboard(request):
    if not request.session.get('email1'):
        return redirect('signup')

    umail=request.session.get('email1')
    user = Users.objects.get(email=umail)
    upro =Userprofile.objects.get(user=user)
    books = BookDetail.objects.filter(status=True)
    cart_items = Cart.objects.filter(customer=user).count()
    cart = Cart.objects.filter(customer=user)
    order = Orders.objects.filter(rel_customer=user)
    total=0;
    for i in cart:
        total = total+int(i.subtotal)
    print(total)
    if 'addtocart' in request.POST:
        bookname = request.POST.get('bookname')
        book = BookDetail.objects.get(book_name=bookname)
        if book:
            added = Cart.objects.create(customer=user, book=book, seller=book.book_seller, qty=1, price=book.book_price, subtotal=book.book_price )
            if added:
                print('added successfully!')
                return redirect('dashboard')
        else:
            return redirect('dashboard')
        return redirect('dashboard')
    dict={
        'user':user,
        'upro':upro,
        'books':books,
        'cart_items':cart_items,
        'cart':cart,
        'total':total,
        'order':order
    }
    return render(request, 'dashboard.html', dict)

def logout(request):
    del request.session['email1']
    return redirect('signin')

def view_book(request, id=None):
    if not request.session.get('email1'):
        return redirect('signup')
    umail = request.session.get('email1')
    user = Users.objects.get(email=umail)
    upro =Userprofile.objects.get(user=user)
    book = BookDetail.objects.filter(id=id)
    cart_items = Cart.objects.filter(customer=user).count()
    cart = Cart.objects.filter(customer=user)
    order = Orders.objects.filter(rel_customer=user)
    total = 0;
    for i in cart:
        total = total + int(i.subtotal)
    print(total)
    dict = {
        'user': user,
        'books': book,
        'upro':upro,
        'cart_items': cart_items,
        'cart': cart,
        'total': total,
        'order': order
    }
    return render(request, 'view_book.html', dict)

def del_cart(request, id=None):
    m1 = Cart.objects.get(id=id)
    m1.delete()
    return redirect('dashboard')

def buy_now(request, id=None):
    if not request.session.get('email1'):
        return redirect('signup')
    umail = request.session.get('email1')
    user = Users.objects.get(email=umail)
    upro=Userprofile.objects.get(user=user)
    cart_items = Cart.objects.filter(customer=user).count()
    cart = Cart.objects.filter(customer=user)
    book =BookDetail.objects.get(id=id)
    total = 0;
    for i in cart:
        total = total + int(i.subtotal)
    print(total)

    if request.method=="POST":
        cust_name= request.POST.get('full_name')
        cust_email= request.POST.get('email')
        cust_phone= request.POST.get('phone')
        cust_state= request.POST.get('state')
        cust_city= request.POST.get('City')
        cust_add= request.POST.get('cust_add')
        # book_seller= request.POST.get('book_seller')
        book_seller_name= request.POST.get('book_seller_name')
        book_price= request.POST.get('book_price')
        book_qty= request.POST.get('book_qty')
        total_price= request.POST.get('total_price')
        order_done= Orders.objects.create(rel_customer=user, cust_name=cust_name, cust_email=cust_email, cust_phone=cust_phone, cust_state=cust_state, cust_city=cust_city, cust_address=cust_add, rel_book=book, rel_seller= book.book_seller, rel_seller_name=book_seller_name, book_price= book_price, book_total_price= total_price, book_qty=book_qty)
        if order_done:
            return HttpResponse('Order Done')
        else:
            return redirect('dashboard')
    dict={
        'user':user,
        'cart_items': cart_items,
        'cart': cart,
        'total': total,
        'upro':upro,
        'book':book
    }
    return render(request, 'buy_now.html',dict)


def cart_to_buy(request):
    if not request.session.get('email1'):
        return redirect('signup')
    umail = request.session.get('email1')
    user = Users.objects.get(email=umail)
    upro = Userprofile.objects.get(user=user)
    cart_items = Cart.objects.filter(customer=user).count()
    cart = Cart.objects.filter(customer=user)

    total=0
    for i in cart:
        total = total + int(i.subtotal)
    dict = {
        'user': user,
        'cart_items': cart_items,
        'cart': cart,
        'upro': upro,
        'total':total
    }
    if request.method == 'POST':
        cust_name = request.POST.get('full_name')
        cust_email = request.POST.get('email')
        cust_phone = request.POST.get('phone')
        cust_state = request.POST.get('state')
        cust_city = request.POST.get('City')
        cust_add = request.POST.get('cust_add')
        for i in cart:
            # print(i.book.book_name)
            book_name= BookDetail.objects.get(book_name=i.book.book_name)
            seller = Seller.objects.get(email=i.seller.email)
            order_done= Orders.objects.create(rel_customer=user, cust_name=cust_name, cust_email=cust_email, cust_phone=cust_phone, cust_state=cust_state, cust_city=cust_city, cust_address=cust_add, rel_book=book_name, rel_seller= seller, rel_seller_name=seller.name, book_price= i.book.book_price, book_total_price= i.book.book_price, book_qty=1)
            if order_done:
                m1 = Cart.objects.get(customer=user, book=book_name, seller=seller)
                m1.delete()
                print('order done')
        cart1 = Cart.objects.filter(customer=user)
        print(cart1)
        if not cart1:
            return render(request, 'order_done.html')
    return render(request, 'cart_to_buy.html', dict)