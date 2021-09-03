from django.urls import path
from . import views
urlpatterns = [
    path('signin', views.signin, name='seller_signin'),
    path('seller_admin', views.seller_admin, name='seller_admin'),
    path('s_logout', views.s_logout, name='s_logout'),
    path('del_book/<int:id>', views.del_book, name='del_book'),
    path('edit_book/<int:id>', views.edit_book, name='edit_book')
]
