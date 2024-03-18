from django.db import models
from user.models import User, Profile

class Category(models.Model):
    title_tm = models.CharField(max_length=32, 
                                verbose_name="Название (tm)")
    title_ru = models.CharField(max_length=32, 
                                verbose_name="Название (ru)")
    is_set = models.BooleanField(default=False, 
                                verbose_name="Комплект?")
    icon = models.ImageField(upload_to='icons/')
    order = models.IntegerField(default=1, verbose_name="Порядок")

    def __str__(self):
        return self.title_tm
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['order']

class Product(models.Model):
    is_active = models.BooleanField(default=True, 
                                verbose_name="Активен?")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                related_name='category_product', verbose_name='Категория')
    title_tm = models.CharField(max_length=32, verbose_name="Название (tm)")
    title_ru = models.CharField(max_length=32, null=True, blank=True, 
                                verbose_name="Название (ru)")
    description_tm = models.TextField(null=True, blank=True, 
                                verbose_name="Описание (tm)")
    description_ru = models.TextField(null=True, blank=True, 
                                verbose_name="Описание (ru)")
    is_new = models.BooleanField(default=False, verbose_name="Новый?")
    is_special = models.BooleanField(default=False, verbose_name="Специальный?")
    is_cheap = models.BooleanField(default=False, verbose_name="Дешевый?")
    image1 = models.ImageField(upload_to='product/', blank=True, null=True,
                                verbose_name='Фото 1')
    image2 = models.ImageField(upload_to='product/', blank=True, null=True,
                                verbose_name='Фото 2')
    image3 = models.ImageField(upload_to='product/', blank=True, null=True,
                                verbose_name='Фото 3')
    image4 = models.ImageField(upload_to='product/', blank=True, null=True,
                                verbose_name='Фото 4')
    image5 = models.ImageField(upload_to='product/', blank=True, null=True,
                                verbose_name='Фото 5')
    image6 = models.ImageField(upload_to='product/', blank=True, null=True,
                                verbose_name='Фото 6')
    like_count = models.IntegerField(default=0, 
                                verbose_name='Количество лайков')
    purchase_count = models.IntegerField(default=0, 
                                verbose_name='Количество покупок')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_tm
    
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['updated_at']),
        ]

class ProductSizePrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name="Продукт", 
                                related_name="product_psp")
    price = models.FloatField(default=0, verbose_name="Цена")
    size_tm = models.CharField(max_length=32, verbose_name='Размер (tm)',
                            null=True, blank=True)
    size_ru = models.CharField(max_length=32, verbose_name='Размер (ru)',
                            null=True, blank=True)
    purchase_count = models.IntegerField(default=0, 
                                verbose_name='Количество покупок')
    purchase_point = models.IntegerField(default=0,
                                verbose_name='Балл на покупку')
    referer_point = models.IntegerField(default=0,
                                verbose_name="Балл для реферала")
    point_equivalent = models.IntegerField(default=0,
                                         verbose_name="Эквалент баллами")

    def __str__(self):
        return str(self.product.title_tm) + ' - ' + str(self.price)
    
    class Meta:
        verbose_name = "Продукт Цена"
        verbose_name_plural = "Продукты Цены"

class Group(models.Model):
    product = models.ManyToManyField(Product,
                                verbose_name="Продукт", 
                                related_name="product_group")
    image = models.ImageField(upload_to='groups/', blank=True, null=True,
                              verbose_name='Фото')
    title_tm = models.CharField(max_length=32, verbose_name="Название (tm)")
    title_ru = models.CharField(max_length=32, null=True, blank=True, 
                                verbose_name="Название (ru)")
    description_tm = models.TextField(null=True, blank=True, 
                                verbose_name="Описание (tm)")
    description_ru = models.TextField(null=True, blank=True, 
                                verbose_name="Описание (ru)")
    purchase_count = models.IntegerField(default=0, 
                                verbose_name='Количество покупок')
    purchase_point = models.IntegerField(default=0,
                                verbose_name='Балл на покупку')
    referer_point = models.IntegerField(default=0,
                                verbose_name="Балл для реферала")
    total_price = models.FloatField(default=0, verbose_name="Цена")
    point_equivalent = models.IntegerField(default=0,
                                         verbose_name="Эквалент баллами")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title_tm
    
    class Meta:
        verbose_name = "Комбо"
        verbose_name_plural = "Комбо"
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=['updated_at']),
        ]

class Order(models.Model):
    ORDER_STATUS = [
        ("ORDERPLACED", "ORDERPLACED"),
        ("ACCEPTED", "ACCEPTED"),
        ("DELIVERED", "DELIVERED"),
        ("PAID", "PAID"),
        ("NOTPAID", "NOTPAID"),
    ]
    user = models.ForeignKey(User, verbose_name="Пользователь", 
                             on_delete=models.CASCADE,
                             related_name="user_order")
    status = models.CharField(max_length=16, choices=ORDER_STATUS,
                              verbose_name="Статус заказа")
    purchase_point = models.IntegerField(default=0,
                                verbose_name='Балл на покупку')
    referer_point = models.IntegerField(default=0,
                                verbose_name="Балл для реферала")
    total_price = models.FloatField(default=0, verbose_name="Цена")
    delivery_price = models.FloatField(default=0, verbose_name="Цена доставки")
    with_point = models.BooleanField(default=False, verbose_name="Оплата баллами?")
    point_equivalent = models.IntegerField(default=-1,
                                         verbose_name="Эквалент баллами")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.user.username) + " - " + str(self.created_at)
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['created_at']),
        ]
    # TODO: Check all possible combinations
    def save(self, *args, **kwargs):
        if not self.pk:
            profile = Profile.objects.filter(user=self.user).first()
            if not self.with_point:
                if profile:
                    profile.total_point += self.purchase_point
                    profile.save()
                if profile.referer:
                    referer = profile.referer
                    ref_profile = Profile.objects.filter(user=referer).first()
                    ref_profile.total_point += self.referer_point
                    ref_profile.save()
            if self.with_point:
                if self.point_equivalent != -1:
                    if profile.total_point > self.point_equivalent:
                        profile.total_point -= self.point_equivalent
            super(Order, self).save(*args, **kwargs)
        else:
            super(Order, self).save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name="Заказ",
                              on_delete=models.CASCADE,
                              related_name="order_orderitem")
    product = models.ForeignKey(Product, verbose_name="Продукт",
                                on_delete=models.CASCADE,
                                related_name="product_orderitem")
    qty = models.IntegerField(default=1, verbose_name="Количество")
    purchase_point = models.IntegerField(default=0,
                                verbose_name='Балл на покупку')
    referer_point = models.IntegerField(default=0,
                                verbose_name="Балл для реферала")
    price = models.FloatField(default=0, verbose_name="Цена")
    point_equivalent = models.IntegerField(default=-1,
                                         verbose_name="Эквалент баллами")
    
    def __str__(self):
        return str(self.product.title_tm)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.product.purchase_count += 1
            self.product.save()
        super(OrderItem, self).save(*args, **kwargs)
            
    
    class Meta:
        verbose_name = "Продукт Заказа"
        verbose_name_plural = "Прдукты Заказов"
        
class Info(models.Model):
    title = models.CharField(max_length=128, verbose_name="Название")
    mobile = models.CharField(max_length=16, verbose_name="Мобильный")
    email = models.CharField(max_length=64, verbose_name="Почта")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Инфо"
        verbose_name_plural = "Инфо"
        ordering =["-id"]

class Banner(models.Model):
    TYPE = [
        ("MAIN", "MAIN"),
        ("SECONDARY", "SECONDARY"),
        ("OTHER", "OTHER"),
    ]
    title = models.CharField(max_length=128, verbose_name="Название")
    image = models.ImageField(upload_to="banners/", verbose_name="Фото")
    banner_type = models.CharField(max_length=16, choices=TYPE, default="MAIN")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"
        ordering = ["-id"]
        
class Settings(models.Model):
    delivery_price = models.FloatField(default=0, verbose_name="Цена доставки")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"
        ordering = ["-id"]
    
    def __str__(self):
        return str(self.created_at)
    
class PushImage(models.Model):
    image = models.ImageField("Фото", upload_to='banners/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Фото Пуш"
        verbose_name_plural = "Фото Пуш"
    
    def __str__(self):
        return str(self.created_at)