from django.urls import path
from sazgaryab import views

urlpatterns = [
    path('products/', views.get_all_products, name="all_products"),
    path('find_compatibles/', views.find_compatibles, name="find_compatibles")
]