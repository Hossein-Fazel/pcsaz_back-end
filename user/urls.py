from django.urls import path
from .views import *

urlpatterns = [
    path("login/", login, name="login"),
    path('personal_data/', get_personal, name='get_peersonal'),
    path('vip_detail/', get_vip_detail, name='vip_detail'),
    path('discount_detail/', get_discount_detail, name='discount_detail'),
    path('carts_detail/', get_carts_detail, name='carts_status')
]