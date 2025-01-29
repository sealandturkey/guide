from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from .models import PreRegisteredUser, PasswordResetUser
import traceback

@receiver(post_save, sender=PreRegisteredUser)
def send_verification_email(sender, instance, created, **kwargs):
    if created and instance.verification_code and not instance.is_verified and not instance.is_mail_sent:
        # Mail gönderme işlemi
        subject = 'Please Verify Your Email Address'
        
        # E-posta içeriği (HTML ve düz metin)
        html_message = render_to_string('emails/verification_email.html', {
            'first_name': instance.first_name,
            'verification_code': instance.verification_code,
        })
        plain_message = strip_tags(html_message)

        try:
            print("Send Mail'e geldik")
            # E-posta gönderimi
            msg = EmailMultiAlternatives(
                subject,
                plain_message,
                None,
                [instance.email],
                # headers={"List-Unsubscribe": "<mailto:unsub@example.com>"},
            )
            msg.attach_alternative(html_message, "text/html")
            msg.send()

            # Mail gönderildikten sonra 'is_mail_sent' alanını True yap
            instance.is_mail_sent = True
            instance.save()

        except Exception as e:
            # Hata mesajını logla veya yazdır
            print("E-posta gönderimi sırasında bir hata meydana geldi:")
            print(traceback.format_exc())
            
@receiver(post_save, sender=PasswordResetUser)
def send_verification_email_for_reset_pass(sender, instance, created, **kwargs):
    if created and not instance.is_verified:
        subject = 'Password Reset Verification Code'
        html_message = render_to_string('emails/reset_password_email.html', {
            'verification_code': instance.verification_code,
            'first_name': instance.user.first_name
        })
        plain_message = strip_tags(html_message)

        try:
            # E-posta gönderimi
            msg = EmailMultiAlternatives(
                subject,
                plain_message,
                None,
                [instance.user.email],
            )
            msg.attach_alternative(html_message, "text/html")
            msg.send(fail_silently=False)
            print("BURDAYIZ")
        except Exception as e:
            print("E-posta gönderimi sırasında bir hata meydana geldi:")
            print(traceback.format_exc())