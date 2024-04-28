# basic URL Configurations
from django.urls import path
from apis import views

# specify URL Path for rest_framework
urlpatterns = [
    path('<pk>', views.get_user),
    path('add/', views.add_user),
    path('login/<pk>', views.user_login),
    path('emergency/<pk>/<lon>/<lat>/', views.emergency_contact),
    path('fare-pay/<pk>/<phone>/<int:amount>', views.fare_payment),
]
