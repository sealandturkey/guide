from django.contrib import admin
from .models import TourInfo, TourInfoTranslation
from core.models import TOUR_CHOICES
class TourInfoTranslationInline(admin.TabularInline):
    model = TourInfoTranslation
    extra = 0

def duplicate_tour_info(modeladmin, request, queryset):
    """
    Admin action to duplicate TourInfo objects with reversed `tour_type`.
    """
    for obj in queryset:
        # `tour_type` alanını tersine çevir (örneğin, "onehour" -> "threehour")
        new_tour_type = next(
            (choice[0] for choice in TOUR_CHOICES if choice[0] != obj.tour_type),
            obj.tour_type
        )
        
        # Yeni TourInfo nesnesi oluştur
        new_tour_info = TourInfo.objects.create(
            tour_type=new_tour_type,
            order=obj.order,
            place_name=obj.place_name,
            description=obj.description,
            voice_path=obj.voice_path,
            google_maps_url=obj.google_maps_url,
            info_url=obj.info_url,
        )

        # İlgili çevirileri (TourInfoTranslation) de kopyala
        translations = obj.translations.all()
        for translation in translations:
            TourInfoTranslation.objects.create(
                tour_info=new_tour_info,
                language=translation.language,
                place_name=translation.place_name,
                description=translation.description,
                voice_path=translation.voice_path,
                info_url=translation.info_url,
            )

duplicate_tour_info.short_description = "Duplicate selected items with reversed tour type"

@admin.register(TourInfo)
class TourInfoAdmin(admin.ModelAdmin):
    list_display = ("order", "place_name", "google_maps_url", "info_url")
    list_filter = ["tour_type"]
    search_fields = ("place_name",)
    inlines = [TourInfoTranslationInline]
    actions = [duplicate_tour_info]  # Action'ı ekledik