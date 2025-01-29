from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import LanguageSetting, TOUR_CHOICES

class TourInfo(models.Model):
    tour_type = models.CharField(max_length=15, choices=TOUR_CHOICES, verbose_name=_("Tour Type"))
    order = models.PositiveIntegerField(verbose_name=_("Order"))
    place_name = models.CharField(max_length=255, verbose_name=_("Place Name (English)"))
    description = models.TextField(verbose_name=_("Description (English)"))
    voice_path = models.FileField(upload_to='voices/en/', verbose_name=_("Voice Path (English)"), blank=True, null=True)
    google_maps_url = models.URLField(max_length=5000, verbose_name=_("Google Maps URL"))
    info_url = models.URLField(verbose_name=_("Info URL"))

    def __str__(self):
        return self.place_name

    class Meta:
        verbose_name = _("Tour Info")
        verbose_name_plural = _("Tour Infos")
        ordering = ["order"]
        
class TourInfoTranslation(models.Model):
    tour_info = models.ForeignKey(TourInfo, related_name="translations", on_delete=models.CASCADE, verbose_name=_("Tour Info"))
    language = models.ForeignKey(LanguageSetting, verbose_name=_("Language"), on_delete=models.SET_NULL, null=True)
    place_name = models.CharField(max_length=255, verbose_name=_("Place Name"))
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    voice_path = models.FileField(upload_to='voices/', verbose_name=_("Voice Path"), blank=True, null=True)
    info_url = models.URLField(verbose_name=_("Info URL"))
    
    def __str__(self):
        return f"{self.language.language_name} - {self.place_name}"

    class Meta:
        verbose_name = _("Tour Info Translation")
        verbose_name_plural = _("Tour Info Translations")
        unique_together = ('tour_info', 'language')  # Her dil bir kez eklenebilir