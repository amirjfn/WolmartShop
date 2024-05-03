from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.UserLogin.as_view(), name='login'),
    path('otplogin', views.OtpLoginView.as_view(), name='otplogin'),
    path('checkotp', views.CheckOtpView.as_view(), name='check_otp'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('edit_profile', views.UserEditProfile.as_view(), name='edit_profile'),
    path('add/address', views.AddAddressView.as_view(), name='add_address'),
]