from django.db import models
from seller .models import Seller
from django.db.models.signals import post_save
# Create your models here.

class Users(models.Model):
    name= models.CharField(max_length=50)
    email= models.EmailField(unique=True)
    phone= models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.email

class Userprofile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    image =models.ImageField(upload_to='profile', default='avtar.jpg')
    about =models.TextField(default='Please add something about you like which is your favourite blogger, favourite book etc.')
    gender =models.CharField(max_length=100, default='Gender')
    dob = models.DateField(null=True)
    city = models.CharField(max_length=200, default='City')
    state = models.CharField(max_length=200, default='State')
    def __str__(self):
        return self.user.email

class BookDetail(models.Model):
    book_seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=200, unique=True)
    book_author = models.CharField(max_length=200)
    book_language = models.CharField(max_length=200)
    book_pages = models.PositiveIntegerField()
    book_price = models.PositiveIntegerField()
    book_desc = models.TextField()
    book_qty = models.IntegerField()
    book_avail = models.BooleanField(default=True)
    book_img = models.ImageField(upload_to='books', default='mybook.png')
    cdate = models.DateTimeField(auto_now_add=True)
    udate = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.book_name

class Book_sold(models.Model):
    customer = models.ForeignKey(Users, on_delete=models.CASCADE)
    book = models.ForeignKey(BookDetail, on_delete=models.CASCADE)
    solddate = models.DateTimeField(auto_now_add=True)
    udate = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.book

class Cart(models.Model):
    customer = models.ForeignKey(Users, on_delete=models.CASCADE)
    book = models.ForeignKey(BookDetail, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    price= models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

class Orders(models.Model):
    rel_customer = models.ForeignKey(Users, on_delete=models.CASCADE)
    cust_name = models.CharField(max_length=200)
    cust_email = models.EmailField()
    cust_phone = models.CharField(max_length=100)
    cust_state = models.CharField(max_length=100)
    cust_city = models.CharField(max_length=100)
    cust_address = models.TextField()
    rel_book = models.ForeignKey(BookDetail, on_delete=models.CASCADE)
    rel_seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    rel_seller_name = models.CharField(max_length=100)
    book_price = models.PositiveIntegerField()
    book_total_price = models.PositiveIntegerField()
    book_qty = models.PositiveIntegerField()


def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Userprofile.objects.create(user =instance)
post_save.connect(create_user_profile, sender =Users)