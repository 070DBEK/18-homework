from django.urls import path
from . import views


app_name = 'categories'


urlpatterns = [
    path('list/', views.category_list, name='list'),
    path('create/', views.create_category, name='create'),
    path('update/<int:pk>/', views.update_category, name='update'),
    path('detail/<int:pk>/', views.category_detail, name='detail'),
    path('delete/<int:pk>/', views.delete_category, name='delete'),
]