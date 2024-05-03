from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('cart', views.CartDetailView.as_view(), name='cart'),
    path('add/<int:pk>', views.CartAddView.as_view(), name='cart_add'),
    path('delete/<str:id>', views.CartEditView.as_view(), name='cart_delete'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/add', views.OrderCreationView.as_view(), name='order_create'),
    path('applydiscount/<int:pk>', views.ApplyDiscountView.as_view(), name='apply_discount'),
]