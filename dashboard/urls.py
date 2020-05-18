from django.urls import path

from dashboard import views

app_name = 'dashboard'
urlpatterns = [
    path('order', views.add_order, name='order'),
]
