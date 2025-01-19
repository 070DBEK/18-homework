from django.urls import path
from . import views


app_name = 'products'


urlpatterns = [
    path('list/', views.product_list, name='list'),
    path('create/', views.create_products, name='create'),
    path('update/<int:pk>/', views.update_products, name='update'),
    path('detail/<int:pk>/', views.product_detail, name='detail'),
    path('delete/<int:pk>/', views.product_delete, name='delete'),
]