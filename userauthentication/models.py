from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string
from django.utils import timezone

class CustomUser(AbstractUser):
    # Ekstra bilgiler
    phone_number = models.CharField(max_length=15)
    email_verified = models.BooleanField(default=False)
    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number']  # Kullanıcı oluşturulurken gerekli alanlar

    def __str__(self):
        return self.username
    
class PreRegisteredUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)  # şifreyi plaintext değil, hash edilmiş şekilde saklamak önemli
    verification_code = models.CharField(max_length=6, unique=True)
    is_verified = models.BooleanField(default=False)  # Doğrulama işlemi tamamlandı mı?
    is_mail_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def generate_verification_code(self):
        # 6 haneli rastgele büyük harflerden oluşan bir kod oluştur
        return ''.join(random.choices(string.ascii_uppercase, k=6))

    def save(self, *args, **kwargs):
        if not self.verification_code:
            self.verification_code = self.generate_verification_code()
        super().save(*args, **kwargs)
    
class PasswordResetUser(models.Model):
    user = models.ForeignKey(CustomUser, related_name="password_reset", on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, unique=True)
    is_verified = models.BooleanField(default=False)  # Doğrulama işlemi tamamlandı mı?
    is_change_password = models.BooleanField(default=False)  # Şifresini değiştirdi mi?
    def generate_verification_code(self):
            # 6 haneli rastgele büyük harflerden oluşan bir kod oluştur
            return ''.join(random.choices(string.ascii_uppercase, k=6))

    def save(self, *args, **kwargs):
        if not self.verification_code:
            self.verification_code = self.generate_verification_code()
        super().save(*args, **kwargs)