JAZZMIN_SETTINGS = {
    "site_title": "SLTA - Panel",
    "site_header": "SLTA - Panel",
    "site_brand": "SLTA Panel",
    "site_logo": "image/cropped-icon-1-32x32.png",
    "welcome_sign": "Welcome to SLTA Admin Panel",
    "show_sidebar": True,
    "navigation_expanded": True,
    "copyright": "SLTA",
    "search_model": ["tour.TourInfo"],
    "show_ui_builder": True,
    # "language_chooser": True, #TODO: Activate when added i18n
    "icons": {
        # App İkonları
        "core": "fas fa-cogs",  # Core app'i için dişli çarklar ikonu
        "tour": "fas fa-map-signs",  # Tour app'i için yön işaretleri ikonu
        "userauthentication": "fas fa-users-cog",  # Kullanıcı yönetimi için kullanıcı ve ayarlar ikonu

        # Core Modelleri
        "core.GeneralSetting": "fas fa-sliders-h",  # Genel ayarlar için yatay kaydırıcı ikonu
        "core.LanguageSetting": "fas fa-language",  # Dil ayarları için dil ikonu
        "core.SectionSetting": "fas fa-puzzle-piece",  # Bölüm ayarları için yapboz parçası ikonu

        # Tour Modelleri
        "tour.TourInfo": "fas fa-info-circle",  # Tur bilgisi için bilgi simgesi

        # UserAuthentication Modelleri
        "userauthentication.CustomUser": "fas fa-user-circle",  # Kullanıcı profili için kullanıcı dairesi ikonu
    }
}

# JAZZMIN_UI_TWEAKS = {
#     "navbar_small_text": False,
#     "footer_small_text": False,
#     "body_small_text": False,
#     "brand_small_text": False,
#     "brand_colour": False,
#     "accent": "accent-primary",
#     "navbar": "navbar-warning navbar-light",
#     "no_navbar_border": False,
#     "navbar_fixed": True,
#     "layout_boxed": False,
#     "footer_fixed": False,
#     "sidebar_fixed": False,
#     "sidebar": "sidebar-light-indigo",
#     "sidebar_nav_small_text": False,
#     "sidebar_disable_expand": False,
#     "sidebar_nav_child_indent": False,
#     "sidebar_nav_compact_style": False,
#     "sidebar_nav_legacy_style": False,
#     "sidebar_nav_flat_style": True,
#     "theme": "default",
#     "dark_mode_theme": None,
#     "button_classes": {
#         "primary": "btn-primary",
#         "secondary": "btn-secondary",
#         "info": "btn-info",
#         "warning": "btn-warning",
#         "danger": "btn-danger",
#         "success": "btn-success"
#     },
#     "actions_sticky_top": True
# }