from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from core.models import GeneralSetting, SectionSetting, LanguageSetting, TOUR_CHOICES, LanguageSetting, SectionSettingTranslation
from .models import TourInfo, TourInfoTranslation
from base64 import urlsafe_b64decode
import json

def show_page(request, parameter, language):
    # Kullanıcı giriş yapmamışsa login sayfasına yönlendirme yap
    # if not request.user.is_authenticated:
        # # Mevcut URL'yi `next` parametresine ekleyerek yönlendir
        # login_url = f"{reverse('login')}?next={request.path}"
        # return redirect(login_url)
    # LANGUAGE parametresini doğrula
    valid_languages = LanguageSetting.objects.values_list('short_language_name', flat=True)
    valid_languages = [lang.lower() for lang in valid_languages]
    # Geçerli dil eşleştiyse logla
    matched_language = LanguageSetting.objects.filter(short_language_name__iexact=language).first()
    
    success_data = False
    success = request.GET.get('success')
    if success:
        success_data = success
    error_param = request.GET.get('error')
    step_param = request.GET.get('step')
    reset_param = request.GET.get('resetdata')
    decoded_message = None
    reset_data = None
    if error_param:
        # Şifreli mesajı çöz
        decoded_message = json.loads(urlsafe_b64decode(error_param).decode())
    
    if reset_param:
        reset_data = json.loads(urlsafe_b64decode(reset_param).decode())
    
    if not matched_language:
        valid_tour_types = [choice[0] for choice in TOUR_CHOICES]
        if parameter not in valid_tour_types:
            # Eğer parametre geçersizse 404 döndür
            raise Http404("Invalid tour type")
        # GeneralSetting'den ilk kaydı al
        general_setting = GeneralSetting.objects.first()
        langage_setting = LanguageSetting.objects.all()
        section_setting = SectionSetting.objects.filter(tour_type=parameter).first()
        tour_data = TourInfo.objects.filter(tour_type=parameter)
        tour_data_json = json.dumps(list(tour_data.values()))
        selected_language = {
            'short_name': "us",
            'name': "English"
        }
    else:
        general_setting = GeneralSetting.objects.first()
        langage_setting = LanguageSetting.objects.all()
        section_setting = SectionSetting.objects.filter(tour_type=parameter).first()
        section_setting_translation = SectionSettingTranslation.objects.filter(section_setting=section_setting, language=matched_language).first()
        # Geçici JSON yapısını oluştur
        if section_setting_translation:
            section_setting.title_start = section_setting_translation.title_start
            section_setting.description_start = section_setting_translation.description_start
            section_setting.title_end = section_setting_translation.title_end
            section_setting.description_end = section_setting_translation.description_end
            section_setting.title_map = section_setting_translation.title_map
            
        tour_datas = TourInfo.objects.filter(tour_type=parameter)

        tour_data_list = []
        
        for tour in tour_datas:
            # TourInfoTranslation ile çeviriyi kontrol et
            translation = TourInfoTranslation.objects.filter(tour_info=tour, language=matched_language).first()

            if translation:
                # Çeviri varsa, çeviri verilerini kullan
                tour_data = {
                    "place_name": translation.place_name,
                    "description": translation.description,
                    "voice_path": translation.voice_path.url if translation.voice_path else None,
                    "google_maps_url": tour.google_maps_url,  # Google Maps URL ve order her zaman aynı kalacak
                    "info_url": translation.info_url,
                    "order": tour.order
                }
            else:
                # Çeviri yoksa, genel TourInfo verilerini kullan
                tour_data = {
                    "place_name": tour.place_name,
                    "description": tour.description,
                    "voice_path": tour.voice_path.url if tour.voice_path else None,
                    "google_maps_url": tour.google_maps_url,
                    "info_url": tour.info_url,
                    "order": tour.order
                }

            tour_data_list.append(tour_data)

        # JSON formatında veriyi oluştur
        tour_data_json = json.dumps(tour_data_list)
        selected_language = {
            'short_name': language.lower(),
            'name': matched_language.language_name
        }
        
    data = {
        'general_setting': general_setting, 
        'language_setting': langage_setting, 
        'section_setting': section_setting,
        'tour_data': tour_data_json,
        'selected_language': selected_language,
        'is_user_authenticated': request.user.is_authenticated,
        'error_message': decoded_message,
        'step_param': step_param,
        'reset_data': json.dumps(reset_data),
        'success_data': success_data,
    }
    return render(request, 'tour/2_hour_tour.html', data)