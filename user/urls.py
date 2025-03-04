from django.urls import path
from user import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path('personal_data/', views.get_personal, name='get_personal'),
    path('vip_detail/', views.get_vip_detail, name='vip_detail'),
    path('discount_detail/', views.get_discount_detail, name='discount_detail'),
    path('carts_detail/', views.get_carts_detail, name='carts_status'),
    path('signup/', views.signup, name='signup'),
    path('add_addresses/', views.add_address, name="add_address")
]