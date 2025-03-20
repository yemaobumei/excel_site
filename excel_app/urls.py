from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_excel, name='upload'),
    path('view/', views.view_data, name='view_data'),
    path('view_st/', views.view_data_st, name='view_data_st'),
]