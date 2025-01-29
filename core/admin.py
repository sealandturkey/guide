from django.contrib import admin
from .models import GeneralSetting, SectionSetting, SectionSettingTranslation, LanguageSetting
from django.contrib.auth.models import Group

# Kullanıcı ve grup modellerini admin panelinden kaldır
admin.site.unregister(Group)

# SectionSettingTranslation Inline
class SectionSettingTranslationInline(admin.TabularInline):
    model = SectionSettingTranslation
    extra = 0  # Yeni çeviri eklemek için bir boş alan sağlar

# GeneralSetting Admin
@admin.register(GeneralSetting)
class GeneralSettingAdmin(admin.ModelAdmin):
    list_display = ('site_title', 'favicon', 'logo')
    
    # `search_fields` özelliğini kaldırarak arama alanını devre dışı bırak
    search_fields = ()
    
    # Yeni bir obje ekleme butonunu devre dışı bırak
    def has_add_permission(self, request):
        return False

    # Toplu silme dropdown'ını devre dışı bırak
    actions = None
    
    def has_delete_permission(self, request, obj=None):
        return False

# SectionSetting Admin
@admin.register(SectionSetting)
class SectionSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'tour_type', 'title_start', 'title_end')
    search_fields = ('title_start', 'title_end')
    inlines = [SectionSettingTranslationInline]
    
@admin.register(LanguageSetting)
class LanguageSettingAdmin(admin.ModelAdmin):
    list_display = ('short_language_name', 'language_name')
    search_fields = ('short_language_name','language_name')