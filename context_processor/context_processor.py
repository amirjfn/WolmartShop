from product.models import Product


def products(request):
    product = Product.objects.all()

    return {'product': product}