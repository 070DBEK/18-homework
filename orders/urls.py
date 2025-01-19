from django.urls import path
from . import views


app_name = 'orders'


urlpatterns = [
    path('list/', views.order_list, name='list'),
    path('create/', views.create_order, name='create'),
    path('update/<int:pk>/', views.update_order, name='update'),
    path('detail/<int:pk>/', views.order_detail, name='detail'),
]
