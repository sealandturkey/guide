from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from userauthentication.models import CustomUser, PreRegisteredUser, PasswordResetUser
from django.urls import reverse
import base64
import json
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

# TODO: Verification code ekle mail doğrulması yap
def login_view(request):
    next_param = request.GET.get('next')
    if request.method == 'POST' and next_param:
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)  # Email üzerinden authenticate
        if user:
            login(request, user)
            return redirect(f"{next_param}?success=true")
        else:
            error_message = base64.urlsafe_b64encode(
                json.dumps({'error_login': 'Your password or username is incorrect, please try again.'}).encode()
            ).decode()
            return redirect(f"{next_param}?error={error_message}")
    return redirect('/')


def register_view(request):
    next_param = request.GET.get('next')
    if request.method == 'POST' and next_param:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        verification_code = request.POST.get('verification_code')  # Gelen doğrulama kodu

        if verification_code:  # Eğer doğrulama kodu gönderildiyse
            # Doğrulama kodunu veritabanında sorgula
            try:
                pre_registered_user = PreRegisteredUser.objects.get(verification_code=verification_code, is_verified=False)
                # Veritabanındaki bilgileri CustomUser'a aktar
                user = CustomUser.objects.create_user(
                    username=pre_registered_user.email,
                    email=pre_registered_user.email,
                    password=pre_registered_user.password,
                    first_name=pre_registered_user.first_name,
                    last_name=pre_registered_user.last_name,
                    phone_number=pre_registered_user.phone_number
                )
                # Doğrulama işlemini tamamla
                pre_registered_user.is_verified = True
                pre_registered_user.save()
                login(request, user)  # Kayıt sonrası otomatik giriş
                next_url = next_param or '/'
                return redirect(f"{next_url}?success=true")
            except PreRegisteredUser.DoesNotExist:
                # Doğrulama kodu bulunamazsa hata mesajı döndür
                error_message = base64.urlsafe_b64encode(
                    json.dumps({'error_verify': 'Invalid verification code.'}).encode()
                ).decode()
                return redirect(f"{next_param}?error={error_message}")
        else:  # Doğrulama kodu yoksa, bilgileri PreRegisteredUser olarak kaydet
            if CustomUser.objects.filter(email=email).exists():
                error_message = base64.urlsafe_b64encode(
                    json.dumps({'error_register': 'This email is already registered. Please use a different email.'}).encode()
                ).decode()
                return redirect(f"{next_param}?error={error_message}")

            if CustomUser.objects.filter(phone_number=phone_number).exists():
                error_message = base64.urlsafe_b64encode(
                    json.dumps({'error_register': 'This phone number is already registered. Please use a different phone number.'}).encode()
                ).decode()
                return redirect(f"{next_param}?error={error_message}")

            # Yeni kullanıcı bilgilerini PreRegisteredUser olarak kaydet
            pre_registered_user = PreRegisteredUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                password=password
            )
            pre_registered_user.save()  # Kaydet ve doğrulama kodunu oluştur
            return redirect(f"{next_param}?step=verification")
    return redirect('/')

def reset_password_view(request):
    if request.method == "POST":
        print("request.POST: ", request.POST)
        email = request.POST.get("email_reset")
        verification_code = request.POST.get("verification_code")
        password = request.POST.get("password")
        password_again = request.POST.get("password_again")
        next_param = request.GET.get("next", "/")
        print("email: ", email)
        print("verification_code: ", verification_code)
        print("password: ", password)
        
        
        data = base64.urlsafe_b64encode(
            json.dumps({
                'email': email,
                'verification_code': verification_code,
            }).encode()
        ).decode()

        if not next_param:
            return redirect('/')

        # 1. Adım: Sadece email gönderilmişse
        if email and not verification_code and not password:
            try:
                user = CustomUser.objects.get(email=email)
                reset_user = PasswordResetUser.objects.filter(user=user).first()

                if reset_user:
                    # Eğer reset_user mevcutsa, sil
                    reset_user.delete()
                    
                reset_user = PasswordResetUser.objects.create(user=user)
                return redirect(f"{next_param}?resetdata={data}")
            except CustomUser.DoesNotExist:
                return redirect(f"{next_param}?resetdata={data}")

        # 2. Adım: Email ve verification_code gönderilmişse
        if email and verification_code and not password:
            try:
                reset_user = PasswordResetUser.objects.get(user__email=email, verification_code=verification_code)
                if not reset_user.is_verified and not reset_user.is_change_password:
                    reset_user.is_verified = True
                    reset_user.save()
                    return redirect(f"{next_param}?resetdata={data}")
                else:
                    error_message = base64.urlsafe_b64encode(
                        json.dumps({'error_verify': 'Verification code invalid or already used.'}).encode()
                    ).decode()
                    return redirect(f"{next_param}?error={error_message}")
            except PasswordResetUser.DoesNotExist:
                error_message = base64.urlsafe_b64encode(
                    json.dumps({'error_verify': 'Invalid verification code.'}).encode()
                ).decode()
                return redirect(f"{next_param}?error={error_message}")

        # 3. Adım: Email, verification_code ve password gönderilmişse
        if email and verification_code and password and password_again:
            if password != password_again:
                error_message = base64.urlsafe_b64encode(
                    json.dumps({'error_verify': 'Passwords do not match.'}).encode()
                ).decode()
                return redirect(f"{next_param}?error={error_message}")

            try:
                reset_user = PasswordResetUser.objects.get(user__email=email, verification_code=verification_code)
                if reset_user.is_verified and not reset_user.is_change_password:
                    reset_user.user.set_password(password)
                    reset_user.user.save()
                    reset_user.is_change_password = True
                    reset_user.save()
                    login(request, reset_user.user)  # Kullanıcıyı otomatik olarak giriş yaptır
                    return redirect(f"{next_param}?success=true")
                else:
                    error_message = base64.urlsafe_b64encode(
                        json.dumps({'error_verify': 'Verification code invalid or already used.'}).encode()
                    ).decode()
                    return redirect(f"{next_param}?error={error_message}")
            except PasswordResetUser.DoesNotExist:
                error_message = base64.urlsafe_b64encode(
                    json.dumps({'error_verify': 'Invalid verification code.'}).encode()
                ).decode()
                return redirect(f"{next_param}?error={error_message}")

        # Hatalı istek
        return redirect('/')