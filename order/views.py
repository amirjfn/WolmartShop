from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from product.models import Product
from .cart_module import Cart
from .models import Order, OrderItem, DiscountCode


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)

        return render(request, 'order/cart.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        color, quantity, back_color = request.POST.get('color'), request.POST.get('quantity'), request.POST.get(
            'back_color')
        print(color, back_color)
        cart = Cart(request)
        cart.add(product, quantity, color, back_color)
        return redirect('order:cart')


class CartEditView(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('order:cart')


class OrderDetailView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        return render(request, 'order/order_detail.html', {'order': order})


class OrderCreationView(View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total_price=cart.total())
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], color=item['color'],
                                     quantity=item['quantity'], price=item['price'])
        cart.remove_cart()
        return redirect('order:order_detail', order.id)


class ApplyDiscountView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        code = request.POST.get('discount_code')
        discount_code = get_object_or_404(DiscountCode, name=code)
        if discount_code.quantity == 0:
            return redirect('order:order_detail', order.id)
        order.total_price -= order.total_price * discount_code.discount/100
        order.save()
        discount_code.quantity -= 1
        discount_code.save()
        return redirect('order:order_detail', order.id)