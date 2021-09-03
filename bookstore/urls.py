from django.urls import path
from . import views
urlpatterns = [
    path('', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
    # path('order_done', views.order_done, name='order_done'),
    path('cart_to_buy', views.cart_to_buy, name='cart_to_buy'),
    path('view_book/<int:id>/', views.view_book, name='view_book'),
    path('buy_now/<int:id>/', views.buy_now, name='buy_now'),
    path('del_cart/<int:id>/', views.del_cart, name='del_cart')
]
