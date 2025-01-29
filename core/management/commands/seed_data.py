import os
import json
from django.core.management.base import BaseCommand
from django.core.files import File
from django.contrib.auth import get_user_model
from core.models import GeneralSetting, SectionSetting  # Modellerin bulunduğu app'i uygun şekilde değiştirin
from tour.models import TourInfo


class Command(BaseCommand):
    help = "Seed initial data for the application"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        # Süper kullanıcı oluştur
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                phone_number="587",
                password="1"
            )
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' created successfully"))
        else:
            self.stdout.write(self.style.WARNING("Superuser 'admin' already exists"))

        # GeneralSetting oluştur veya güncelle
        site_settings, created = GeneralSetting.objects.get_or_create(id=1)
        site_settings.site_title = "Sea & Land Travel Agency"
        
        # Favicon ve logo dosyalarını static dizininden al ve kaydet
        favicon_path = os.path.join("static", "image/cropped-icon-1-32x32.png")
        logo_path = os.path.join("static", "image/sealand-logo-w.svg")
        banner_path = os.path.join("static", "image/photo-1516483638261-f4dbaf036963.png")
        
        if os.path.exists(favicon_path):
            with open(favicon_path, "rb") as f:
                site_settings.favicon.save("cropped-icon-1-32x32.png", File(f), save=False)
        else:
            self.stdout.write(self.style.ERROR("Favicon file not found"))
        
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                site_settings.logo.save("sealand-logo-w.svg", File(f), save=False)
        else:
            self.stdout.write(self.style.ERROR("Logo file not found"))
        
        site_settings.save()
        self.stdout.write(self.style.SUCCESS("General settings updated successfully"))
        
        self.seed_tour_data(banner_path)
        
    def seed_tour_data(self, banner_path):
        data_folder = os.path.join("data")  # JSON dosyalarının bulunduğu klasör
        tour_files = ["2_hour.json", "3_hour.json"]

        for file_name in tour_files:
            file_path = os.path.join(data_folder, file_name)
            
            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR(f"File not found: {file_name}"))
                continue
            
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # JSON dosyasına göre tur tipini belirle
            if "2_hour" in file_name:
                tour_type = "twohour"
            elif "3_hour" in file_name:
                tour_type = "threehour"
            else:
                self.stdout.write(self.style.ERROR(f"Unknown tour type in file: {file_name}"))
                continue
            
            # SectionSetting oluştur veya güncelle
            section, created = SectionSetting.objects.get_or_create(tour_type=tour_type)
            section.title_start = data["title_start"]
            section.description_start = data["description_start"]
            if os.path.exists(banner_path):
                with open(banner_path, "rb") as f:
                    section.banner_img_start.save("banner.png", File(f), save=False)
                    section.banner_img_end.save("banner.png", File(f), save=False)
            section.title_map = data["title_tour"]
            section.title_end = data["title_end"]
            section.description_end = data["description_end"]
            section.save()
            self.stdout.write(self.style.SUCCESS(f"SectionSetting created/updated for {tour_type}"))

            # TourInfo kayıtlarını temizleyip tekrar ekleyelim (Önceden var olan verileri sıfırla)
            TourInfo.objects.filter(tour_type=tour_type).delete()

            for tour in data.get("tour_infos", []):
                TourInfo.objects.create(
                    tour_type=tour_type,
                    order=tour["order"],
                    place_name=tour["place_name_EN"],
                    description=tour["description_EN"],
                    google_maps_url=tour["google_maps_url"],
                    info_url=tour["info_url"]
                )

            self.stdout.write(self.style.SUCCESS(f"TourInfo records created for {tour_type}"))
        
        