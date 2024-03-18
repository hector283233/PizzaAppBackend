from django.db import models
from django.contrib.auth.models import AbstractUser

class Mobile(models.Model):
    mobile = models.CharField(max_length=16)
    is_sms_sent = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    sms_code = models.CharField(max_length=16, default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mobile
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['mobile']),
            models.Index(fields=['created_at']),
        ]

class RefId(models.Model):
    ref_uid = models.IntegerField(default=1000)

class User(AbstractUser):
    ref_id = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.is_superuser or not self.is_staff:
                last_user = RefId.objects.latest('id')
                uid = int(last_user.ref_uid) + 1
                self.ref_id = uid
                last_user.ref_uid = uid
                last_user.save()
            super(User, self).save(*args, **kwargs)
            Profile.objects.create(user=self)
        else:
            super(User, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ('-id', )
        verbose_name = 'Пользователь'
        verbose_name_plural = "Пользователи"
        indexes = [
            models.Index(fields=['ref_id']),
        ]

        

class Profile(models.Model):
    REGIONS = [
        ("Aşgabat", "Aşgabat"),
        ("Mary", "Mary"),
        ("Lebap", "Lebap"),
        ("Daşoguz", "Daşoguz"),
        ("Balkan", "Balkan"),
        ("Ahal", "Ahal"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name='Пользователь', 
                                related_name="user_profile")
    referer = models.ForeignKey(User, verbose_name="Пригласившый", 
                on_delete=models.SET_NULL, null=True, blank=True,
                related_name="referer_profile")
    total_point = models.IntegerField(default=0, 
                                verbose_name="Количество балов")
    full_name = models.CharField(max_length=255, null=True, blank=True, 
                                verbose_name='Имя')
    image = models.ImageField(("Фото"), upload_to='profiles/', null=True, 
                                blank=True)
    region = models.CharField(max_length=16, choices=REGIONS, 
                            default="Mary")
    address = models.CharField(max_length=255, null=True, blank=True, 
                            verbose_name="Адрес")
    email = models.CharField(max_length=128, null=True, blank=True, 
                            verbose_name="Почта")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"