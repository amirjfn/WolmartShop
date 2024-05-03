from django.db import models




class BackGroundColor(models.Model):
    background_color = models.CharField(max_length=35, null=True, blank=True, verbose_name='رنگ بک گراند')
    color_name = models.CharField(max_length=30, null=True, verbose_name='رنگ محصول')

    class Meta:
        verbose_name = 'رنگ بک گراند'
        verbose_name_plural = 'رنگ بک گراند ها'

    def __str__(self):
        return f'{self.background_color}-{self.color_name}'


class Product(models.Model):
    title = models.CharField(max_length=80, verbose_name='نام محصول')
    description = models.TextField(verbose_name='توضیحات')
    price = models.IntegerField(verbose_name='قیمت')
    discount = models.SmallIntegerField(verbose_name='تخفیف')
    image = models.ImageField(upload_to='products', verbose_name='تصویر')
    color_back = models.ManyToManyField(BackGroundColor, related_name='productss', verbose_name='رنگ بک گراند محصول')


    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return f'{self.title}'

class Information(models.Model):
    product = models.ForeignKey(Product, null=True , on_delete=models.CASCADE, related_name='informations', verbose_name='اطلاعات محصول')
    text = models.TextField(verbose_name='متن محصول')

    def __str__(self):
        return self.text[:30]