from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.item_create, name='create_item'),
    path('update/<int:id>/', views.item_edit, name='update_item'),
    path('delete/<int:id>/', views.item_delete, name='delete_item'),
]