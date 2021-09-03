from django.shortcuts import render, redirect
from .models import Seller
from bookstore .models import Orders, BookDetail
# Create your views here.
def signin(request):
    if request.session.get('email2'):
        return redirect('seller_admin')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        if email == "":
            dict = {
                'msg': 'Please enter email address',
            }
            return render(request, 'seller_login.html', dict)

        ps = Seller.objects.filter(email=email, password=password)
        if ps:
            request.session['email2'] = email
            return redirect('seller_admin')
        else:
            dict = {
                'msg': 'Email or Password not match',
            }
            return render(request, 'seller_login.html', dict)

    return render(request, 'seller_login.html')

def seller_admin(request):
    if not request.session.get('email2'):
        return redirect('seller_login')
    slr= request.session.get('email2')
    seller = Seller.objects.get(email=slr)
    sold= Orders.objects.filter(rel_seller=seller)
    books = BookDetail.objects.filter(book_seller=seller)
    if 'save' in request.POST:
        book_name = request.POST.get('book_name')
        chk_book = BookDetail.objects.filter(book_name=book_name)
        if chk_book:
            dict = {
                'seller': seller,
                'sold': sold,
                'books': books,
                'msg':'Book already exists!'
            }
            return render(request, 'seller_admin.html', dict)
        book_author = request.POST.get('book_author')
        book_language = request.POST.get('book_language')
        book_pages = request.POST.get('book_pages')
        book_price = request.POST.get('book_price')
        book_desc = request.POST.get('book_desc')
        book_qty = request.POST.get('book_qty')
        book_avail = request.POST.get('book_avail')
        book_img = request.FILES.get('book_img')
        print(book_name)
        add_book= BookDetail.objects.create(book_seller= seller, book_name=book_name, book_author=book_author, book_language=book_language, book_pages=book_pages, book_price=book_price, book_desc=book_desc, book_qty=book_qty, book_avail=book_avail, book_img=book_img, status=True)
        if add_book:
            print('book added successfully')
            return redirect('seller_admin')
        else:
            print('not added')
            return redirect('seller_admin')
    dict={
        'seller':seller,
        'sold':sold,
        'books':books
    }
    return render(request, 'seller_admin.html', dict)

def s_logout(request):
    if not request.session.get('email2'):
        return redirect('seller_login')
    del request.session['email2']
    return redirect('seller_signin')

def del_book(request, id=None):
    if not request.session.get('email2'):
        return redirect('seller_login')
    m1 = BookDetail.objects.filter(id=id)
    m1.delete()
    return redirect('seller_admin')

def edit_book(request, id=None):
    if not request.session.get('email2'):
        return redirect('seller_login')
    slr = request.session.get('email2')
    seller = Seller.objects.get(email=slr)
    m1 = BookDetail.objects.get(id=id)
    if 'save' in request.POST:
        book_name = request.POST.get('book_name')
        book_author = request.POST.get('book_author')
        book_language = request.POST.get('book_language')
        book_pages = request.POST.get('book_pages')
        book_price = request.POST.get('book_price')
        book_desc = request.POST.get('book_desc')
        book_qty = request.POST.get('book_qty')
        book_avail = request.POST.get('book_avail')
        # book_img = request.FILES.get('book_img')
        # print(book_img)
        update_book = BookDetail.objects.filter(book_name=book_name).update(book_seller=seller, book_name=book_name, book_author=book_author,
                                             book_language=book_language, book_pages=book_pages, book_price=book_price,
                                             book_desc=book_desc, book_qty=book_qty, book_avail=book_avail,
                                              status=True)
        if update_book:
            print('book Updated successfully')
            return redirect('seller_admin')
        else:
            print('not Update')
            return redirect('seller_admin')
    dict={
        'bk':m1,
        'seller': seller,
    }
    return render(request, 'edit_book.html',dict)