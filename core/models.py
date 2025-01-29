from django.db import models
from django.utils.translation import gettext_lazy as _


class GeneralSetting(models.Model):
    site_title = models.CharField(max_length=255, verbose_name=_("Site Title"))
    favicon = models.FileField(upload_to="logos/favicon/", verbose_name=_("Favicon"))
    logo = models.FileField(upload_to="logos/", verbose_name=_("Logo"))

class LanguageSetting(models.Model):
    short_language_name = models.CharField(max_length=2, verbose_name=_("Language (Short Name TR, EN etc.)"))
    language_name = models.CharField(max_length=255, verbose_name=_("Language Name"))
    
    def __str__(self):
        return f"{self.language_name} ({self.short_language_name})"
    
TOUR_CHOICES = [
    ('twohour', _("Two Hour Tour")),
    ('threehour', _("Three Hour Tour")),
]

class SectionSetting(models.Model):
    tour_type = models.CharField(max_length=15, choices=TOUR_CHOICES, verbose_name=_("Tour Type"), default="twohour")
    title_start = models.CharField(max_length=255, verbose_name=_("Title Start Section (English)"))
    description_start = models.TextField(verbose_name=_("Description Start Section (English)"))
    banner_img_start = models.FileField(upload_to="banners/", verbose_name=_("Banner Image URL Start Section"), blank=True, null=True)
    
    title_map = models.CharField(max_length=255, verbose_name=_("Map Title (Tour Type) (English)"))
    
    title_end = models.CharField(max_length=255, verbose_name=_("Title End Section (English)"))
    description_end = models.TextField(verbose_name=_("Description End Section (English)"))
    banner_img_end = models.FileField(upload_to="banners/", verbose_name=_("Banner Image URL End Section"), blank=True, null=True)

    class Meta:
        verbose_name = _("Section Settings")
        verbose_name_plural = _("Section Settings")
        
class SectionSettingTranslation(models.Model):
    section_setting = models.ForeignKey(SectionSetting, related_name="translations", on_delete=models.CASCADE, verbose_name=_("Site Settings"))
    language = models.ForeignKey(LanguageSetting, verbose_name=_("Language"), on_delete=models.SET_NULL, null=True)
    
    title_start = models.CharField(max_length=255, verbose_name=_("Title Start Section"))
    description_start = models.TextField(verbose_name=_("Description Start Section"))
    
    title_map = models.CharField(max_length=255, verbose_name=_("Map Title (Tour Type)"))
    
    title_end = models.CharField(max_length=255, verbose_name=_("Title End Section"))
    description_end = models.TextField(verbose_name=_("Description End Section"))

    def __str__(self):
        return f"{self.language.language_name} - {self.id}"

    class Meta:
        verbose_name = _("Section Settings Translation")
        verbose_name_plural = _("Section Settings Translations")
        unique_together = ('section_setting', 'language')  # Aynı dil bir kez eklenebilir