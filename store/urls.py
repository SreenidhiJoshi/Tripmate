from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),
    path('product/<int:pk>/', views.product, name='product'),
    path('cart/', views.generate_map, name="cart"),
    path('travel-route/', views.travel_route, name='travel_route'),
]