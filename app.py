import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'tourism_secret_2024')
app.config['SESSION_PERMANENT'] = False

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = '1234'

translations = {
    'ar': {
        'home': 'الرئيسية', 'admin': 'الإدارة',
        'search_placeholder': 'ابحث عن مدينة...', 'search_btn': 'استكشف',
        'hero_subtitle': 'اكتشف أجمل المدن المغربية', 'see_details': 'عرض التفاصيل',
        'destinations_title': 'الوجهات السياحية', 'type': 'النوع', 'distance': 'المسافة',
        'bus': 'الحافلة', 'taxi': 'التاكسي', 'reserve': 'احجز الآن',
        'reserve_title': 'حجز', 'your_name': 'اسمك', 'departure_date': 'تاريخ المغادرة',
        'confirm': 'تأكيد الحجز', 'dashboard': 'لوحة التحكم',
        'total_destinations': 'الوجهات', 'total_reservations': 'الحجوزات',
        'active_cities': 'المدن النشطة', 'total_persons': 'إجمالي الأشخاص',
        'reservations_list': 'قائمة الحجوزات', 'client_name': 'اسم العميل',
        'city': 'المدينة', 'departure': 'تاريخ المغادرة', 'persons': 'الأشخاص',
        'action': 'الإجراء', 'delete': 'حذف', 'add_city': 'إضافة مدينة',
        'logout': 'خروج', 'login_title': 'تسجيل الدخول', 'username': 'اسم المستخدم',
        'password': 'كلمة السر', 'login_btn': 'دخول',
        'login_error': 'اسم المستخدم أو كلمة السر خاطئة',
        'add_city_title': 'إضافة مدينة جديدة', 'city_name': 'اسم المدينة',
        'description': 'الوصف', 'city_type': 'النوع', 'image_url': 'رابط الصورة',
        'add_btn': 'إضافة المدينة', 'dir': 'rtl', 'explore': 'استكشف المدينة',
        'all': 'الكل', 'restaurants': 'مطاعم', 'hotels': 'فنادق',
        'museums': 'متاحف', 'pharmacies': 'صيدليات', 'places': 'أماكن سياحية',
        'address': 'العنوان', 'price': 'السعر', 'rating': 'التقييم',
        'back': 'رجوع',
        'total_attractions': 'المعالم السياحية', 'top_ville': 'أكثر وجهة حجزاً',
        'avg_personnes': 'متوسط الأشخاص', 'today_reservations': 'حجوزات اليوم',
        'type_ville': 'مدينة', 'type_plage': 'شاطئ', 'type_montagne': 'جبل',
        'type_desert': 'صحراء', 'type_histoire': 'تاريخ',
        'email': 'البريد الإلكتروني', 'telephone': 'رقم الهاتف',
        'card_info': 'معلومات البطاقة البنكية', 'download_pdf': 'تحميل PDF',
        'attraction_reservations': 'حجوزات المعالم',
        'attraction_name': 'اسم المعلم', 'client': 'العميل',
        'menu_title': 'قائمة الطعام', 'dish': 'الطبق',
        'select_dish': 'اختر الأطباق المطلوبة',
        'rooms_title': 'الغرف المتاحة', 'room_type': 'نوع الغرفة',
        'persons_capacity': 'أشخاص', 'select_room': 'اختر الغرفة',
        'location': 'الموقع على الخريطة', 'details': 'التفاصيل',
        'success': 'تم بنجاح', 'error': 'خطأ حاول مرة أخرى',
        'booking_success': '✅ تم الحجز بنجاح',
        'booking_processing': '⏳ جاري الحجز...',
        'booking_error': 'خطأ في الحجز، حاول مرة أخرى',
        'placeholder_name': 'أدخل الاسم...',
        'placeholder_email': 'أدخل البريد الإلكتروني...',
        'placeholder_phone': 'أدخل رقم الهاتف...',
        'city_added_success': '✅ تمت إضافة المدينة بنجاح',
        'details_col': 'التفاصيل',
        'pdf_title': 'تأكيد الحجز',
        'pdf_city': 'المدينة', 'pdf_client': 'العميل',
        'pdf_date': 'التاريخ', 'pdf_persons': 'الأشخاص',
        'pdf_items': 'المواد', 'pdf_status': 'الحالة',
        'pdf_confirmed': '✅ مؤكد',
        'pdf_thank_you': 'شكرا لحجزك مع توريسم دينر!',
        'pdf_attraction': 'المعلم السياحي',
        'departure_city': 'مدينة الانطلاق', 'no_guide': 'بدون مرشد',
        'voir_tous': 'الكل', 'favorites': 'المفضلة', 'guide': 'مرشد',
        'guides': 'مرشدون', 'mad': 'درهم', 'export_json': 'تصدير JSON',
        'search_results': 'نتائج البحث', 'filter_type': 'نوع الرحلة',
        'filter_guide': 'اختر مرشداً', 'no_results': 'لا توجد نتائج',
        'guides_title': 'مرشدونا السياحيون', 'guide_specialty': 'الاختصاص',
        'guide_price': 'السعر', 'guide_phone': 'الهاتف', 'book_guide': 'احجز مرشداً',
        'itinerary_title': 'برنامج الرحلة المقترح - 3 أيام',
        'day_one': 'اليوم الأول', 'day_two': 'اليوم الثاني', 'day_three': 'اليوم الثالث',
        'day1_activity': 'الوصول والتجول في المدينة',
        'day2_activity': 'زيارة المعالم الرئيسية',
        'day3_activity': 'استكشاف الأسواق والمغادرة',
        'day1_time1': '09:00 - الوصول إلى المدينة', 'day1_time2': '11:00 - التجول في الأسواق',
        'day1_time3': '13:00 - الغداء في مطعم تقليدي', 'day1_time4': '15:00 - زيارة المعالم القريبة',
        'day2_time1': '09:00 - الإفطار', 'day2_time2': '10:30 - زيارة المتاحف',
        'day2_time3': '13:00 - الغداء', 'day2_time4': '15:00 - جولة في المدينة القديمة',
        'day3_time1': '09:00 - الإفطار', 'day3_time2': '10:30 - التسوق',
        'day3_time3': '12:00 - الغداء', 'day3_time4': '14:00 - المغادرة',
        'atmosphere': 'الأجواء',
        'risks': 'تنبيهات', 'activities': 'الأنشطة', 'useful_info': 'معلومات مفيدة',
        'rating_label': 'التقييم', 'share': 'مشاركة', 'explore_attractions': 'المعالم السياحية', 'add_favori': 'أضف إلى المفضلة',
        'remove_favori': 'أزل من المفضلة', 'our_guides': 'مرشدونا',
        'guide_specialty_label': 'الاختصاص', 'guide_price_label': 'السعر',
        'guide_phone_label': 'الهاتف', 'price_estimate': 'تقدير التكلفة',
        'transport_cost': 'النقل', 'accommodation_cost': 'الإقامة',
        'guide_cost': 'المرشد', 'total_estimated': 'المجموع التقديري',
        'hero_tagline': '"اكتشف العالم معنا"', 'hero_subtitle2': 'تجارب لا تنسى في انتظارك',
        'pop_destinations': 'الوجهات الشعبية', 'best_guides': 'أفضل المرشدين', 'affordable_prices': 'أسعار مناسبة',
        'pop_destinations_desc': 'أجمل المدن المغربية في انتظارك', 'best_guides_desc': 'مرشدون محترفون بخبرة عالية',
        'affordable_prices_desc': 'عروض تناسب جميع الميزانيات',
        'search_results_title': 'نتائج البحث', 'voir_details': 'عرض التفاصيل',
        'reviews': 'تقييم', 'avis_count': 'تقييم', 'localisation': 'الموقع',
        'bus_duration': 'مدة الحافلة', 'taxi_duration': 'مدة التاكسي', 'voiture_duration': 'مدة السيارة',
        'plats_typiques': 'الأطباق النمطية', 'transport': 'النقل',
        'departure_date': 'تاريخ المغادرة', 'return_date': 'تاريخ العودة',
        'accommodation_type': 'نوع الإقامة', 'hotel': 'فندق', 'riad': 'رياض', 'auberge': 'نزل', 'camp': 'مخيم',
        'check_availability': 'تحقق من التوفر', 'confirm_reservation': 'تأكيد الحجز',
        'recap_title': 'ملخص الحجز', 'days_nights': 'أيام/ليالي',
        'total_estimate': 'المجموع التقديري', 'transport_cost_label': 'النقل',
        'accommodation_cost_label': 'الإقامة', 'guide_cost_label': 'المرشد',
        'best_period': 'أفضل فترة', 'languages': 'اللغات', 'currency': 'العملة',
        'population': 'السكان',
        'plan_title': 'خطط رحلتك',
        'num_days': 'عدد الأيام',
        'generate_btn': 'توليد البرنامج',
        'days_label': 'أيام',
        'day': 'اليوم',
        'morning': 'صباحاً',
        'afternoon': 'ظهراً',
        'evening': 'مساءً',
        'day_activity': 'نشاط اليوم',
        'no_attractions_for_itinerary': 'لا توجد معالم كافية لتوليد برنامج رحلة',
    
    },
    'fr': {
        'home': 'Accueil', 'admin': 'Admin',
        'search_placeholder': 'Rechercher une ville...', 'search_btn': 'Explorer',
        'hero_subtitle': 'Decouvrez les plus belles villes du Maroc', 'see_details': 'Voir details',
        'destinations_title': 'Destinations', 'type': 'Type', 'distance': 'Distance',
        'bus': 'Bus', 'taxi': 'Taxi', 'reserve': 'Reserver maintenant',
        'reserve_title': 'Reserver', 'your_name': 'Votre nom', 'departure_date': 'Date de depart',
        'confirm': 'Confirmer', 'dashboard': 'Dashboard',
        'total_destinations': 'Destinations', 'total_reservations': 'Reservations',
        'active_cities': 'Villes actives', 'total_persons': 'Personnes totales',
        'reservations_list': 'Liste des reservations', 'client_name': 'Nom client',
        'city': 'Ville', 'departure': 'Date depart', 'persons': 'Personnes',
        'action': 'Action', 'delete': 'Supprimer', 'add_city': 'Ajouter ville',
        'logout': 'Deconnexion', 'login_title': 'Connexion Admin',
        'username': "Nom d'utilisateur", 'password': 'Mot de passe', 'login_btn': 'Connecter',
        'login_error': 'Nom ou mot de passe incorrect',
        'add_city_title': 'Ajouter une ville', 'city_name': 'Nom de la ville',
        'description': 'Description', 'city_type': 'Type', 'image_url': "URL de l'image",
        'add_btn': 'Ajouter', 'dir': 'ltr', 'explore': 'Explorer la ville',
        'all': 'Tout', 'restaurants': 'Restaurants', 'hotels': 'Hotels',
        'museums': 'Musees', 'pharmacies': 'Pharmacies', 'places': 'Lieux',
        'address': 'Adresse', 'price': 'Prix', 'rating': 'Note',
        'back': 'Retour',
        'total_attractions': 'Attractions', 'top_ville': 'Ville plus reservee',
        'avg_personnes': 'Moyenne personnes', 'today_reservations': "Reservations aujourd'hui",
        'type_ville': 'Ville', 'type_plage': 'Plage', 'type_montagne': 'Montagne',
        'type_desert': 'Desert', 'type_histoire': 'Histoire',
        'email': 'Email', 'telephone': 'Telephone',
        'card_info': 'Informations carte', 'download_pdf': 'Telecharger PDF',
        'attraction_reservations': "Reservations d'attractions",
        'attraction_name': 'Nom attraction', 'client': 'Client',
        'menu_title': 'Menu', 'dish': 'Plat',
        'select_dish': 'Selectionnez les plats',
        'rooms_title': 'Chambres disponibles', 'room_type': 'Type de chambre',
        'persons_capacity': 'personnes', 'select_room': 'Choisir',
        'location': 'Localisation', 'details': 'Details',
        'success': 'Succes', 'error': 'Erreur reessayez',
        'booking_success': '✅ Reservation reussie',
        'booking_processing': '⏳ Reservation en cours...',
        'booking_error': 'Erreur lors de la reservation, reessayez',
        'placeholder_name': 'Entrer le nom...',
        'placeholder_email': 'Entrer votre email...',
        'placeholder_phone': 'Entrer votre telephone...',
        'city_added_success': '✅ Ville ajoutee avec succes',
        'details_col': 'Details',
        'pdf_title': 'Confirmation de reservation',
        'pdf_city': 'Ville', 'pdf_client': 'Client',
        'pdf_date': 'Date', 'pdf_persons': 'Personnes',
        'pdf_items': 'Articles', 'pdf_status': 'Statut',
        'pdf_confirmed': '✅ Confirme',
        'pdf_thank_you': 'Merci d\'avoir reserve avec Tourism Dinner!',
        'pdf_attraction': 'Attraction',
        'departure_city': 'Ville de depart', 'no_guide': 'Sans guide',
        'voir_tous': 'Tous', 'favorites': 'Favoris', 'guide': 'Guide',
        'guides': 'Guides', 'mad': 'DH', 'export_json': 'Exporter JSON',
        'search_results': 'Resultats de recherche', 'filter_type': 'Type de voyage',
        'filter_guide': 'Choisir un guide', 'no_results': 'Aucun resultat',
        'guides_title': 'Nos guides touristiques', 'guide_specialty': 'Specialite',
        'guide_price': 'Prix', 'guide_phone': 'Telephone', 'book_guide': 'Reserver un guide',
        'itinerary_title': 'Itineraire suggere - 3 jours',
        'day_one': 'Jour 1', 'day_two': 'Jour 2', 'day_three': 'Jour 3',
        'day1_activity': 'Arrivee et balade en ville',
        'day2_activity': 'Visite des principaux sites',
        'day3_activity': 'Exploration des souks et depart',
        'day1_time1': '09:00 - Arrivee en ville', 'day1_time2': '11:00 - Balade dans les souks',
        'day1_time3': '13:00 - Dejeuner restaurant traditionnel', 'day1_time4': '15:00 - Visite des sites proches',
        'day2_time1': '09:00 - Petit dejeuner', 'day2_time2': '10:30 - Visite des musees',
        'day2_time3': '13:00 - Dejeuner', 'day2_time4': '15:00 - Tour dans la medina',
        'day3_time1': '09:00 - Petit dejeuner', 'day3_time2': '10:30 - Shopping',
        'day3_time3': '12:00 - Dejeuner', 'day3_time4': '14:00 - Depart',
        'atmosphere': 'Ambiance',
        'risks': 'Avertissements', 'activities': 'Activites', 'useful_info': 'Infos utiles',
        'rating_label': 'Note', 'share': 'Partager', 'explore_attractions': 'Attractions', 'add_favori': 'Ajouter aux favoris',
        'remove_favori': 'Retirer des favoris', 'our_guides': 'Nos guides',
        'guide_specialty_label': 'Specialite', 'guide_price_label': 'Prix',
        'guide_phone_label': 'Telephone', 'price_estimate': 'Estimation du prix',
        'transport_cost': 'Transport', 'accommodation_cost': 'Hebergement',
        'guide_cost': 'Guide', 'total_estimated': 'Total estime',
        'hero_tagline': '"Decouvrez le monde avec nous"', 'hero_subtitle2': 'Des experiences inoubliables vous attendent',
        'pop_destinations': 'Destinations Populaires', 'best_guides': 'Meilleurs Guides', 'affordable_prices': 'Prix Abordables',
        'pop_destinations_desc': 'Les plus belles villes du Maroc vous attendent', 'best_guides_desc': 'Des guides professionnels hautement qualifies',
        'affordable_prices_desc': 'Des offres pour tous les budgets',
        'search_results_title': 'Resultats de recherche', 'voir_details': 'Voir details',
        'reviews': 'Avis', 'avis_count': 'avis', 'localisation': 'Localisation',
        'bus_duration': 'Duree bus', 'taxi_duration': 'Duree taxi', 'voiture_duration': 'Duree voiture',
        'plats_typiques': 'Plats typiques', 'transport': 'Transport',
        'departure_date': 'Date de depart', 'return_date': 'Date de retour',
        'accommodation_type': "Type d'hebergement", 'hotel': 'Hotel', 'riad': 'Riad', 'auberge': 'Auberge', 'camp': 'Camp',
        'check_availability': 'Verifier la disponibilite', 'confirm_reservation': 'Confirmer la reservation',
        'recap_title': 'Recapitulatif', 'days_nights': 'jours/nuits',
        'total_estimate': 'Estimation totale', 'transport_cost_label': 'Transport',
        'accommodation_cost_label': 'Hebergement', 'guide_cost_label': 'Guide',
        'best_period': 'Meilleure periode', 'languages': 'Langues', 'currency': 'Monnaie',
        'population': 'Population',
        'plan_title': 'Planifiez votre itineraire',
        'num_days': 'Nombre de jours',
        'generate_btn': 'Generer le programme',
        'days_label': 'jours',
        'day': 'Jour',
        'morning': 'Matin',
        'afternoon': 'Apres-midi',
        'evening': 'Soir',
        'day_activity': 'Activite du jour',
        'no_attractions_for_itinerary': 'Pas assez d\'attractions pour generer un itineraire',
    },
    'en': {
        'home': 'Home', 'admin': 'Admin',
        'search_placeholder': 'Search for a city...', 'search_btn': 'Explore',
        'hero_subtitle': 'Discover the most beautiful cities of Morocco', 'see_details': 'See details',
        'destinations_title': 'Destinations', 'type': 'Type', 'distance': 'Distance',
        'bus': 'Bus', 'taxi': 'Taxi', 'reserve': 'Book now',
        'reserve_title': 'Book', 'your_name': 'Your name', 'departure_date': 'Departure date',
        'confirm': 'Confirm', 'dashboard': 'Dashboard',
        'total_destinations': 'Destinations', 'total_reservations': 'Reservations',
        'active_cities': 'Active cities', 'total_persons': 'Total persons',
        'reservations_list': 'Reservations list', 'client_name': 'Client name',
        'city': 'City', 'departure': 'Departure date', 'persons': 'Persons',
        'action': 'Action', 'delete': 'Delete', 'add_city': 'Add city',
        'logout': 'Logout', 'login_title': 'Admin Login', 'username': 'Username',
        'password': 'Password', 'login_btn': 'Login',
        'login_error': 'Invalid username or password',
        'add_city_title': 'Add a city', 'city_name': 'City name',
        'description': 'Description', 'city_type': 'Type', 'image_url': 'Image URL',
        'add_btn': 'Add city', 'dir': 'ltr', 'explore': 'Explore the city',
        'all': 'All', 'restaurants': 'Restaurants', 'hotels': 'Hotels',
        'museums': 'Museums', 'pharmacies': 'Pharmacies', 'places': 'Places',
        'address': 'Address', 'price': 'Price', 'rating': 'Rating',
        'back': 'Back',
        'total_attractions': 'Attractions', 'top_ville': 'Top City',
        'avg_personnes': 'Avg Persons', 'today_reservations': "Today's Reservations",
        'type_ville': 'City', 'type_plage': 'Beach', 'type_montagne': 'Mountain',
        'type_desert': 'Desert', 'type_histoire': 'History',
        'email': 'Email', 'telephone': 'Phone',
        'card_info': 'Card Info', 'download_pdf': 'Download PDF',
        'attraction_reservations': 'Attraction Reservations',
        'attraction_name': 'Attraction Name', 'client': 'Client',
        'menu_title': 'Menu', 'dish': 'Dish',
        'select_dish': 'Select dishes',
        'rooms_title': 'Available Rooms', 'room_type': 'Room Type',
        'persons_capacity': 'persons', 'select_room': 'Select Room',
        'location': 'Location', 'details': 'Details',
        'success': 'Success', 'error': 'Error try again',
        'booking_success': '✅ Booking successful',
        'booking_processing': '⏳ Processing booking...',
        'booking_error': 'Error during booking, try again',
        'placeholder_name': 'Enter your name...',
        'placeholder_email': 'Enter your email...',
        'placeholder_phone': 'Enter your phone number...',
        'city_added_success': '✅ City added successfully',
        'details_col': 'Details',
        'pdf_title': 'Booking Confirmation',
        'pdf_city': 'City', 'pdf_client': 'Client',
        'pdf_date': 'Date', 'pdf_persons': 'Persons',
        'pdf_items': 'Items', 'pdf_status': 'Status',
        'pdf_confirmed': '✅ Confirmed',
        'pdf_thank_you': 'Thank you for booking with Tourism Dinner!',
        'pdf_attraction': 'Attraction',
        'departure_city': 'Departure City', 'no_guide': 'No Guide',
        'voir_tous': 'All', 'favorites': 'Favorites', 'guide': 'Guide',
        'guides': 'Guides', 'mad': 'MAD', 'export_json': 'Export JSON',
        'search_results': 'Search Results', 'filter_type': 'Trip Type',
        'filter_guide': 'Choose a guide', 'no_results': 'No results found',
        'guides_title': 'Our Tour Guides', 'guide_specialty': 'Specialty',
        'guide_price': 'Price', 'guide_phone': 'Phone', 'book_guide': 'Book a Guide',
        'itinerary_title': 'Suggested 3-Day Itinerary',
        'day_one': 'Day 1', 'day_two': 'Day 2', 'day_three': 'Day 3',
        'day1_activity': 'Arrival and city walk',
        'day2_activity': 'Visit main attractions',
        'day3_activity': 'Explore souks and departure',
        'day1_time1': '09:00 - Arrival in city', 'day1_time2': '11:00 - Stroll through souks',
        'day1_time3': '13:00 - Lunch at traditional restaurant', 'day1_time4': '15:00 - Visit nearby sites',
        'day2_time1': '09:00 - Breakfast', 'day2_time2': '10:30 - Visit museums',
        'day2_time3': '13:00 - Lunch', 'day2_time4': '15:00 - Old city tour',
        'day3_time1': '09:00 - Breakfast', 'day3_time2': '10:30 - Shopping',
        'day3_time3': '12:00 - Lunch', 'day3_time4': '14:00 - Departure',
        'atmosphere': 'Atmosphere',
        'risks': 'Warnings', 'activities': 'Activities', 'useful_info': 'Useful Info',
        'rating_label': 'Rating', 'share': 'Share', 'explore_attractions': 'Attractions', 'add_favori': 'Add to favorites',
        'remove_favori': 'Remove from favorites', 'our_guides': 'Our Guides',
        'guide_specialty_label': 'Specialty', 'guide_price_label': 'Price',
        'guide_phone_label': 'Phone', 'price_estimate': 'Price Estimate',
        'transport_cost': 'Transport', 'accommodation_cost': 'Accommodation',
        'guide_cost': 'Guide', 'total_estimated': 'Total Estimated',
        'hero_tagline': '"Discover the world with us"', 'hero_subtitle2': 'Unforgettable experiences await you',
        'pop_destinations': 'Popular Destinations', 'best_guides': 'Best Guides', 'affordable_prices': 'Affordable Prices',
        'pop_destinations_desc': 'The most beautiful Moroccan cities await you', 'best_guides_desc': 'Professional highly qualified guides',
        'affordable_prices_desc': 'Offers for all budgets',
        'search_results_title': 'Search Results', 'voir_details': 'View Details',
        'reviews': 'Reviews', 'avis_count': 'reviews', 'localisation': 'Location',
        'bus_duration': 'Bus duration', 'taxi_duration': 'Taxi duration', 'voiture_duration': 'Car duration',
        'plats_typiques': 'Typical dishes', 'transport': 'Transport',
        'departure_date': 'Departure date', 'return_date': 'Return date',
        'accommodation_type': 'Accommodation type', 'hotel': 'Hotel', 'riad': 'Riad', 'auberge': 'Hostel', 'camp': 'Camp',
        'check_availability': 'Check availability', 'confirm_reservation': 'Confirm reservation',
        'recap_title': 'Summary', 'days_nights': 'days/nights',
        'total_estimate': 'Total Estimate', 'transport_cost_label': 'Transport',
        'accommodation_cost_label': 'Accommodation', 'guide_cost_label': 'Guide',
        'best_period': 'Best period', 'languages': 'Languages', 'currency': 'Currency',
        'population': 'Population',
        'plan_title': 'Plan Your Itinerary',
        'num_days': 'Number of Days',
        'generate_btn': 'Generate Itinerary',
        'days_label': 'days',
        'day': 'Day',
        'morning': 'Morning',
        'afternoon': 'Afternoon',
        'evening': 'Evening',
        'day_activity': "Today's Activity",
        'no_attractions_for_itinerary': 'Not enough attractions to generate an itinerary',
        
    }
}

_APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get('DB_PATH', os.path.join(_APP_DIR, 'database.db'))

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT count(*) FROM villes")
        c.close(); conn.close()
        return
    except:
        try: conn.close()
        except: pass
    import setup_db

init_db()

def get_lang():
    return session.get('lang', 'ar')

def t():
    return translations[get_lang()]

@app.before_request
def ensure_session():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

@app.context_processor
def inject_helpers():
    return dict(t=t(), lang=get_lang())

@app.route('/set_lang/<lang>')
def set_lang(lang):
    if lang in ['ar', 'fr', 'en']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('home'))

def qry_villes(cursor, s, extra_cols='', where='', params=()):
    cols = f"id, nom, description{s} as description, type, distance, prix_bus, prix_taxi, image, note"
    if extra_cols:
        cols += ', ' + extra_cols
    try:
        sql = f"SELECT {cols} FROM villes"
        if where:
            sql += f" WHERE {where}"
        sql += " ORDER BY CAST(note AS REAL) DESC"
        cursor.execute(sql, params)
        return cursor.fetchall()
    except sqlite3.OperationalError:
        base = f"id, nom, description{s} as description, type, distance, prix_bus, prix_taxi, image, note"
        if extra_cols:
            base += ', ' + extra_cols
        sql = f"SELECT {base} FROM villes"
        if where:
            sql += f" WHERE {where}"
        sql += " ORDER BY CAST(note AS REAL) DESC"
        cursor.execute(sql, params)
        return cursor.fetchall()

@app.route('/')
def home():
    db = get_db()
    cursor = db.cursor()
    lang = get_lang()
    s = '' if lang == 'ar' else f'_{lang}'
    type_filter = request.args.get('type')
    extra = "lat, lng, review_count, bus_duration, taxi_duration, voiture_duration"
    if type_filter:
        villes = qry_villes(cursor, s, extra, "type=?", (type_filter,))
    else:
        villes = qry_villes(cursor, s, extra)
    types_list = ['Ville', 'Plage', 'Montagne', 'Desert', 'Histoire']
    gs = '' if lang == 'fr' else f'_{lang}'
    cursor.execute(f"SELECT id, nom{gs} as nom, specialite{gs} as specialite, prix, telephone, image FROM guides ORDER BY id")
    guides = cursor.fetchall()
    top_cities = villes[:3] if villes else []
    cursor.execute("SELECT COUNT(*) as cnt FROM villes")
    total_villes = cursor.fetchone()['cnt']
    sid = session.get('session_id', '')
    cursor.execute("SELECT ville_id FROM favoris WHERE session_id=?", (sid,))
    fav_ids = [r['ville_id'] for r in cursor.fetchall()]
    cursor.close()
    db.close()
    return render_template("index.html", villes=villes, types=types_list, guides=guides, fav_ids=fav_ids, top_cities=top_cities, total_villes=total_villes)

@app.route('/results')
def results():
    db = get_db()
    cursor = db.cursor()
    lang = get_lang()
    s = '' if lang == 'ar' else f'_{lang}'
    q = request.args.get('q', '').strip()
    type_filter = request.args.get('type', '')
    guide_filter = request.args.get('guide', '')
    conditions = []
    params = []
    if q:
        conditions.append(f"(nom LIKE ? OR description{s} LIKE ?)")
        params.extend([f'%{q}%', f'%{q}%'])
    if type_filter:
        conditions.append("type=?")
        params.append(type_filter)
    where = ' AND '.join(conditions) if conditions else '1=1'
    villes = qry_villes(cursor, s, 'lat, lng, review_count, bus_duration, taxi_duration, voiture_duration', where, tuple(params))
    if guide_filter:
        cursor.execute(f"SELECT ville_id FROM guides WHERE id=?", (guide_filter,))
        g = cursor.fetchone()
        if g:
            villes = [v for v in villes if v['id'] == g['ville_id']]
        else:
            villes = []
    gs = '' if lang == 'fr' else f'_{lang}'
    cursor.execute(f"SELECT id, nom{gs} as nom FROM guides ORDER BY id")
    all_guides = cursor.fetchall()
    cursor.close()
    db.close()
    types_list = ['Ville', 'Plage', 'Montagne', 'Desert', 'Histoire']
    return render_template("search_results.html", villes=villes, types=types_list, q=q, type_filter=type_filter, guide_filter=guide_filter, all_guides=all_guides)

@app.route('/details/<int:id>')
def details(id):
    db = get_db()
    cursor = db.cursor()
    lang = get_lang()
    s = '' if lang == 'ar' else f'_{lang}'
    try:
        cursor.execute(f"SELECT id, nom, description{s} as description, type, distance, prix_bus, prix_taxi, image, note, rating{s} as rating, atmosphere{s} as atmosphere, risques{s} as risques, activites{s} as activites, infos_utiles{s} as infos_utiles, galerie1, galerie2, galerie3, lat, lng, review_count, bus_duration, taxi_duration, voiture_duration, plats_typiques{s} as plats_typiques, population, monnaie, langues, meilleure_periode{s} as meilleure_periode FROM villes WHERE id=?", (id,))
    except sqlite3.OperationalError:
        cursor.execute(f"SELECT id, nom, description{s} as description, type, distance, prix_bus, prix_taxi, image, note, rating{s} as rating, atmosphere{s} as atmosphere, risques{s} as risques, activites{s} as activites, infos_utiles{s} as infos_utiles, galerie1, galerie2, galerie3 FROM villes WHERE id=?", (id,))
    ville = cursor.fetchone()
    if not ville:
        cursor.close(); db.close()
        return '<h1>404 - Ville non trouvée</h1>', 404
    attractions = []
    guides = []
    avis_list = []
    prix_hebergement = []
    cursor.execute(f"SELECT id, nom{s} as nom, categorie, description{s} as description, adresse{s} as adresse, prix, image, note FROM attractions WHERE ville_id=? ORDER BY id", (id,))
    attractions = cursor.fetchall()
    gs = '' if lang == 'fr' else f'_{lang}'
    cursor.execute(f"SELECT id, nom{gs} as nom, specialite{gs} as specialite, prix, telephone, image FROM guides WHERE ville_id=?", (id,))
    guides = cursor.fetchall()
    try:
        cursor.execute("SELECT id, auteur, note, commentaire, date_post FROM avis WHERE ville_id=? ORDER BY date_post DESC", (id,))
        avis_list = cursor.fetchall()
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("SELECT type_hebergement, prix_par_nuit FROM ville_prix_hebergement WHERE ville_id=? ORDER BY prix_par_nuit ASC", (id,))
        prix_hebergement = cursor.fetchall()
    except sqlite3.OperationalError:
        pass
    sid = session.get('session_id', '')
    cursor.execute("SELECT ville_id FROM favoris WHERE session_id=? AND ville_id=?", (sid, id))
    is_fav = cursor.fetchone() is not None
    cursor.close()
    db.close()
    return render_template("details.html", ville=ville, attractions=attractions, guides=guides, is_fav=is_fav, avis_list=avis_list, prix_hebergement=prix_hebergement)

@app.route('/api/generate_itinerary/<int:ville_id>')
def generate_itinerary(ville_id):
    db = get_db()
    cursor = db.cursor()
    lang = get_lang()
    s = '' if lang == 'ar' else f'_{lang}'
    days = request.args.get('days', 3, type=int)
    days = max(1, min(days, 30))
    cursor.execute(f"SELECT id, nom{s} as nom, categorie, description{s} as description, adresse{s} as adresse, prix, image, note FROM attractions WHERE ville_id=? AND categorie NOT IN ('hotel','pharmacie')", (ville_id,))
    all_attractions = cursor.fetchall()
    cursor.close()
    db.close()
    if not all_attractions:
        return {'itinerary': [], 'error': 'no_attractions'}
    meals = {'ar': {'breakfast': 'إفطار', 'lunch': 'غداء', 'dinner': 'عشاء'},
             'fr': {'breakfast': 'Petit dejeuner', 'lunch': 'Dejeuner', 'dinner': 'Diner'},
             'en': {'breakfast': 'Breakfast', 'lunch': 'Lunch', 'dinner': 'Dinner'}}
    m = meals.get(lang, meals['en'])
    restaurants = [a for a in all_attractions if a['categorie'] == 'restaurant']
    sights = [a for a in all_attractions if a['categorie'] != 'restaurant']
    import random
    random.shuffle(sights)
    random.shuffle(restaurants)
    itinerary = []
    if days == 1:
        day_restaurants = restaurants[:2] if len(restaurants) >= 2 else (restaurants[:1] if restaurants else [])
        day_sights = sights[:2] if len(sights) >= 2 else sights[:1]
        slots = []
        slots.append({'time': '09:00', 'icon': '🥐', 'label': m['breakfast'], 'type': 'meal'})
        if len(day_sights) > 0:
            s2 = day_sights[0]
            slots.append({'time': '10:00', 'icon': '📍', 'label': s2['nom'], 'desc': s2['description'] or '', 'prix': s2['prix'] or '', 'type': 'attraction', 'id': s2['id']})
        lunch_place = day_restaurants[0] if len(day_restaurants) > 0 else None
        if lunch_place:
            slots.append({'time': '13:00', 'icon': '🍽️', 'label': m['lunch'] + ' - ' + lunch_place['nom'], 'prix': lunch_place['prix'] or '', 'type': 'attraction', 'id': lunch_place['id']})
        else:
            slots.append({'time': '13:00', 'icon': '🍽️', 'label': m['lunch'], 'type': 'meal'})
        if len(day_sights) > 1:
            s3 = day_sights[1]
            slots.append({'time': '15:00', 'icon': '📍', 'label': s3['nom'], 'desc': s3['description'] or '', 'prix': s3['prix'] or '', 'type': 'attraction', 'id': s3['id']})
        if lang == 'ar':
            day_summary_lbl = 'استكشاف المدينة'
        elif lang == 'fr':
            day_summary_lbl = 'Exploration de la ville'
        else:
            day_summary_lbl = 'City exploration'
        itinerary.append({'day': 1, 'title': day_summary_lbl, 'activities': slots})
    else:
        sights_per_day = max(1, len(sights) // days) if sights else 0
        rest_per_day = max(1, len(restaurants) // days) if restaurants else 0
        for d in range(days):
            slots = []
            slots.append({'time': '09:00', 'icon': '🥐', 'label': m['breakfast'], 'type': 'meal'})
            si = d * sights_per_day
            si = min(si, len(sights) - 1) if sights else 0
            if sights and si < len(sights):
                s2 = sights[si]
                slots.append({'time': '10:00', 'icon': '📍', 'label': s2['nom'], 'desc': s2['description'] or '', 'prix': s2['prix'] or '', 'type': 'attraction', 'id': s2['id']})
            ri = d * rest_per_day
            ri = min(ri, len(restaurants) - 1) if restaurants else 0
            if restaurants and ri < len(restaurants):
                lunch_place = restaurants[ri]
                slots.append({'time': '13:00', 'icon': '🍽️', 'label': m['lunch'] + ' - ' + lunch_place['nom'], 'prix': lunch_place['prix'] or '', 'type': 'attraction', 'id': lunch_place['id']})
            else:
                slots.append({'time': '13:00', 'icon': '🍽️', 'label': m['lunch'], 'type': 'meal'})
            si2 = si + 1
            if sights and si2 < len(sights):
                s3 = sights[si2]
                slots.append({'time': '15:00', 'icon': '📍', 'label': s3['nom'], 'desc': s3['description'] or '', 'prix': s3['prix'] or '', 'type': 'attraction', 'id': s3['id']})
            ri2 = ri + 1
            if restaurants and ri2 < len(restaurants):
                dinner_place = restaurants[ri2]
                slots.append({'time': '20:00', 'icon': '🌙', 'label': m['dinner'] + ' - ' + dinner_place['nom'], 'prix': dinner_place['prix'] or '', 'type': 'attraction', 'id': dinner_place['id']})
            else:
                slots.append({'time': '20:00', 'icon': '🌙', 'label': m['dinner'], 'type': 'meal'})
            if lang == 'ar':
                titles = ['استكشاف المدينة', 'زيارة المعالم', 'جولة ثقافية', 'مغامرة جديدة', 'اكتشاف الأسواق', 'رحلة استرخاء', 'استكشاف الطبيعة']
            elif lang == 'fr':
                titles = ['Exploration ville', 'Visite des sites', 'Tour culturel', 'Nouvelle aventure', 'Decouverte des souks', 'Journee detente', 'Exploration nature']
            else:
                titles = ['City exploration', 'Site visits', 'Cultural tour', 'New adventure', 'Souk discovery', 'Relaxation day', 'Nature exploration']
            itinerary.append({'day': d + 1, 'title': titles[d % len(titles)], 'activities': slots})
    return {'itinerary': itinerary}

@app.route('/explore/<int:id>')
def explore(id):
    db = get_db()
    cursor = db.cursor()
    lang = get_lang()
    s = '' if lang == 'ar' else f'_{lang}'
    cursor.execute(f"SELECT id, nom, description{s} as description, type, distance, prix_bus, prix_taxi, image FROM villes WHERE id=?", (id,))
    ville = cursor.fetchone()
    if not ville:
        cursor.close(); db.close()
        return '<h1>404 - Ville non trouvée</h1>', 404
    cursor.execute(f"SELECT id, ville_id, nom{s} as nom, categorie, description{s} as description, adresse{s} as adresse, prix, image, note FROM attractions WHERE ville_id=? ORDER BY categorie", (id,))
    attractions = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("explore.html", ville=ville, attractions=attractions)

@app.route('/attraction/<int:id>')
def attraction_detail(id):
    db = get_db()
    cursor = db.cursor()
    lang = get_lang()
    s = '' if lang == 'ar' else f'_{lang}'
    if lang == 'ar': ms = '_ar'
    elif lang == 'en': ms = '_en'
    else: ms = ''
    cursor.execute(f"SELECT a.id, a.ville_id, a.nom{s} as nom, a.categorie, a.description{s} as description, a.adresse{s} as adresse, a.prix, a.image, a.note, v.nom as ville_nom FROM attractions a JOIN villes v ON a.ville_id = v.id WHERE a.id=?", (id,))
    a = cursor.fetchone()
    menu_items = []
    hotel_rooms = []
    if not a:
        cursor.close(); db.close()
        return '<h1>404 - Attraction non trouvée</h1>', 404
    if a['categorie'] == 'restaurant':
        cursor.execute(f"SELECT id, attraction_id, nom_item{ms} as nom_item, prix, description{ms} as description FROM menu_items WHERE attraction_id=? ORDER BY id", (id,))
        menu_items = cursor.fetchall()
    elif a['categorie'] == 'hotel':
        cursor.execute(f"SELECT id, attraction_id, type_chambre{ms} as type_chambre, prix, description{ms} as description, capacite FROM hotel_rooms WHERE attraction_id=? ORDER BY id", (id,))
        hotel_rooms = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("attraction_detail.html", a=a, menu_items=menu_items, hotel_rooms=hotel_rooms)

@app.route('/reserver_attraction/<int:id>', methods=['GET', 'POST'])
def reserver_attraction(id):
    db = get_db()
    cursor = db.cursor()
    lang = get_lang()
    s = '' if lang == 'ar' else f'_{lang}'
    if lang == 'ar': ms = '_ar'
    elif lang == 'en': ms = '_en'
    else: ms = ''
    cursor.execute(f"SELECT a.id, a.ville_id, a.nom{s} as nom, a.categorie, a.description{s} as description, a.adresse{s} as adresse, a.prix, a.image, a.note, v.nom as ville_nom FROM attractions a JOIN villes v ON a.ville_id = v.id WHERE a.id=?", (id,))
    a = cursor.fetchone()
    if not a:
        cursor.close(); db.close()
        return '<h1>404 - Attraction non trouvée</h1>', 404
    menu_items = []
    hotel_rooms = []
    if a['categorie'] == 'restaurant':
        cursor.execute(f"SELECT id, nom_item{ms} as nom_item, prix, description{ms} as description FROM menu_items WHERE attraction_id=? ORDER BY id", (id,))
        menu_items = cursor.fetchall()
    elif a['categorie'] == 'hotel':
        cursor.execute(f"SELECT id, type_chambre{ms} as type_chambre, prix, description{ms} as description, capacite FROM hotel_rooms WHERE attraction_id=? ORDER BY id", (id,))
        hotel_rooms = cursor.fetchall()
    if request.method == 'POST':
        nom = request.form.get('nom', '')
        email = request.form.get('email', '')
        telephone = request.form.get('telephone', '')
        date_depart = request.form.get('date_depart', '')
        personnes = request.form.get('personnes', '1')
        card_number = request.form.get('card_number', '')
        card_last4 = card_number[-4:] if len(card_number) >= 4 else ''
        selected_items = request.form.get('selected_items', '')
        details = selected_items if selected_items else None
        cursor.execute(
            "INSERT INTO attraction_reservations (attraction_id, attraction_nom, ville_nom, nom_client, email, telephone, card_last4, date_depart, personnes, details) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (id, a['nom'], a['ville_nom'], nom, email, telephone, card_last4, date_depart, personnes, details)
        )
        db.commit()
        res_id = cursor.lastrowid
        cursor.close()
        db.close()
        return {'success': True, 'attraction_nom': a['nom'], 'nom': nom, 'email': email, 'date_depart': date_depart, 'personnes': personnes, 'details': details, 'res_id': res_id}
    cursor.close()
    db.close()
    return render_template("reserver_attraction.html", a=a, menu_items=menu_items, hotel_rooms=hotel_rooms)

@app.route('/reservation/<int:id>', methods=['GET', 'POST'])
def reservation(id):
    db = get_db()
    cursor = db.cursor()
    lang = get_lang()
    s = '' if lang == 'ar' else f'_{lang}'
    cursor.execute(f"SELECT id, nom, description{s} as description, type, distance, prix_bus, prix_taxi, image, note FROM villes WHERE id=?", (id,))
    ville = cursor.fetchone()
    if not ville:
        cursor.close(); db.close()
        return '<h1>404 - Ville non trouvée</h1>', 404
    if request.method == 'POST':
        nom = request.form.get('nom', '')
        email = request.form.get('email', '')
        telephone = request.form.get('telephone', '')
        date_depart = request.form.get('date_depart', '')
        date_retour = request.form.get('date_retour', '')
        personnes = request.form.get('personnes', '1')
        accommodation_type = request.form.get('accommodation_type', 'hotel')
        card_number = request.form.get('card_number', '')
        card_last4 = card_number[-4:] if len(card_number) >= 4 else ''
        cursor.execute(
            "INSERT INTO reservations (nom_client, ville, email, telephone, card_last4, date_depart, personnes) VALUES (?,?,?,?,?,?,?)",
            (nom, ville['nom'], email, telephone, card_last4, date_depart, personnes)
        )
        db.commit()
        cursor.close()
        db.close()
        return {'success': True, 'ville': ville['nom'], 'nom': nom, 'email': email, 'date_depart': date_depart, 'personnes': personnes}
    prix_hebergement = []
    try:
        cursor.execute("SELECT type_hebergement, prix_par_nuit FROM ville_prix_hebergement WHERE ville_id=? ORDER BY prix_par_nuit ASC", (id,))
        prix_hebergement = cursor.fetchall()
    except sqlite3.OperationalError:
        pass
    gs = '' if lang == 'fr' else f'_{lang}'
    cursor.execute(f"SELECT id, nom, nom_fr, nom_en FROM villes ORDER BY id")
    all_villes = cursor.fetchall()
    cursor.execute(f"SELECT id, nom{gs} as nom, specialite{gs} as specialite, prix, telephone, image FROM guides WHERE ville_id=?", (id,))
    guides = cursor.fetchall()
    cursor.close()
    db.close()
    import re
    price_estimates = {}
    for ph in prix_hebergement:
        bus_match = re.search(r'(\d+)\s*DH', ville['prix_bus']) if ville['prix_bus'] else None
        transport_bus = int(bus_match.group(1)) if bus_match else 0
        taxi_match = re.search(r'(\d+)\s*DH', ville['prix_taxi']) if ville['prix_taxi'] else None
        transport_taxi = int(taxi_match.group(1)) if taxi_match else 0
        accom = int(ph['prix_par_nuit']) if ph['prix_par_nuit'] else 0
        price_estimates[ph['type_hebergement']] = {
            'bus_1j': transport_bus + accom,
            'taxi_1j': transport_taxi + accom,
            'bus_3j': transport_bus + accom * 3,
            'taxi_3j': transport_taxi + accom * 3,
        }
    return render_template("reservation.html", ville=ville, prix_hebergement=prix_hebergement, price_estimates=price_estimates, all_villes=all_villes, guides=guides)

@app.route('/search')
def search():
    db = get_db()
    cursor = db.cursor()
    lang = get_lang()
    s = '' if lang == 'ar' else f'_{lang}'
    q = request.args.get('q', '').strip()
    type_filter = request.args.get('type', '')
    guide_filter = request.args.get('guide', '')
    conditions = []
    params = []
    if q:
        conditions.append(f"(nom LIKE ? OR description{s} LIKE ?)")
        params.extend([f'%{q}%', f'%{q}%'])
    if type_filter:
        conditions.append("type=?")
        params.append(type_filter)
    where = ' AND '.join(conditions) if conditions else '1=1'
    villes = qry_villes(cursor, s, 'lat, lng, review_count, bus_duration, taxi_duration, voiture_duration', where, tuple(params))
    if guide_filter:
        cursor.execute(f"SELECT ville_id FROM guides WHERE id=?", (guide_filter,))
        g = cursor.fetchone()
        if g:
            villes = [v for v in villes if v['id'] == g['ville_id']]
        else:
            villes = []
    gs = '' if lang == 'fr' else f'_{lang}'
    cursor.execute(f"SELECT id, nom{gs} as nom FROM guides ORDER BY id")
    all_guides = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("search_results.html", villes=villes, q=q, type_filter=type_filter, guide_filter=guide_filter, all_guides=all_guides)

@app.route('/api/villes')
def api_villes():
    db = get_db()
    cursor = db.cursor()
    lang = get_lang()
    s = '' if lang == 'ar' else f'_{lang}'
    villes = qry_villes(cursor, s, 'lat, lng, population, monnaie, langues')
    cursor.close()
    db.close()
    return jsonify([dict(v) for v in villes])

@app.route('/api/prix-estimation', methods=['POST'])
def api_prix_estimation():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'invalid request'}), 400
    import re
    ville_id = data.get('ville_id')
    nb_personnes = int(data.get('nb_personnes', 1))
    nb_jours = int(data.get('nb_jours', 1))
    transport_type = data.get('transport_type', 'bus')
    accommodation_type = data.get('accommodation_type', 'hotel')
    guide_id = data.get('guide_id')
    depart_ville_id = data.get('depart_ville_id')
    db = get_db()
    cursor = db.cursor()
    if depart_ville_id and int(depart_ville_id) == int(ville_id):
        transport_price = 0
    else:
        cursor.execute("SELECT prix_bus, prix_taxi FROM villes WHERE id=?", (ville_id,))
        v = cursor.fetchone()
        if not v:
            cursor.close(); db.close()
            return jsonify({'transport':0,'accommodation':0,'guide':0,'total':0})
        bus_m = re.search(r'(\d+)\s*DH', v['prix_bus']) if v['prix_bus'] else None
        bus_val = int(bus_m.group(1)) if bus_m else 0
        taxi_m = re.search(r'(\d+)\s*DH', v['prix_taxi']) if v['prix_taxi'] else None
        taxi_val = int(taxi_m.group(1)) if taxi_m else 0
        transport_price = (bus_val if transport_type == 'bus' else taxi_val) * nb_personnes
    accom_price = 0
    try:
        cursor.execute("SELECT prix_par_nuit FROM ville_prix_hebergement WHERE ville_id=? AND type_hebergement=?", (ville_id, accommodation_type))
        ph = cursor.fetchone()
        accom_price = float(ph['prix_par_nuit']) * nb_personnes * nb_jours if ph else 0
    except sqlite3.OperationalError:
        pass
    guide_price = 0
    if guide_id:
        cursor.execute("SELECT prix FROM guides WHERE id=?", (guide_id,))
        g = cursor.fetchone()
        if g:
            gm = re.search(r'(\d+(?:\.\d+)?)', g['prix'])
            guide_price = float(gm.group(1)) * nb_jours if gm else 0
    cursor.close()
    db.close()
    total = float(transport_price + accom_price + guide_price)
    return jsonify({'transport': transport_price, 'accommodation': accom_price, 'guide': guide_price, 'total': total})

@app.route('/favori/toggle/<int:ville_id>')
def toggle_favori(ville_id):
    sid = session.get('session_id', '')
    if not sid:
        return jsonify({'error': 'no session'})
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM favoris WHERE session_id=? AND ville_id=?", (sid, ville_id))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("DELETE FROM favoris WHERE id=?", (existing[0],))
        is_fav = False
    else:
        cursor.execute("INSERT INTO favoris (session_id, ville_id) VALUES (?, ?)", (sid, ville_id))
        is_fav = True
    db.commit()
    cursor.close()
    db.close()
    return jsonify({'is_fav': is_fav})

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USERNAME and request.form.get('password') == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            error = t()['login_error']
    return render_template("login.html", error=error)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM villes")
    total_villes = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM reservations")
    total_reservations = cursor.fetchone()['total']
    cursor.execute("SELECT SUM(personnes) as total FROM reservations")
    total_personnes = cursor.fetchone()['total'] or 0
    cursor.execute("SELECT COUNT(DISTINCT ville) as total FROM reservations")
    villes_actives = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM attractions")
    total_attractions = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM attraction_reservations")
    total_attraction_reservations = cursor.fetchone()['total']
    cursor.execute("SELECT v.nom, COUNT(*) as cnt FROM reservations r JOIN villes v ON r.ville = v.nom GROUP BY v.nom ORDER BY cnt DESC LIMIT 1")
    top_row = cursor.fetchone()
    top_ville = top_row['nom'] if top_row else '—'
    cursor.execute("SELECT AVG(personnes) as avg FROM reservations")
    avg_personnes = round(cursor.fetchone()['avg'] or 0, 1)
    cursor.execute("SELECT COUNT(*) as total FROM reservations WHERE DATE(date_depart) = DATE('now')")
    today_reservations = cursor.fetchone()['total']
    cursor.execute("SELECT id, nom, type, image FROM villes ORDER BY id ASC")
    villes = cursor.fetchall()
    cursor.execute("SELECT r.id, r.nom_client, r.ville, r.date_depart, r.personnes, v.type FROM reservations r LEFT JOIN villes v ON r.ville = v.nom ORDER BY r.id DESC")
    reservations = cursor.fetchall()
    cursor.execute("SELECT ar.id, ar.attraction_nom, ar.ville_nom, ar.nom_client, ar.email, ar.telephone, ar.date_depart, ar.personnes, ar.details, a.categorie FROM attraction_reservations ar LEFT JOIN attractions a ON ar.attraction_id = a.id ORDER BY ar.id DESC")
    attraction_reservations = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('admin.html',
        total_villes=total_villes, total_reservations=total_reservations,
        total_personnes=total_personnes, villes_actives=villes_actives,
        total_attractions=total_attractions, total_attraction_reservations=total_attraction_reservations,
        top_ville=top_ville, avg_personnes=avg_personnes, today_reservations=today_reservations,
        villes=villes, reservations=reservations, attraction_reservations=attraction_reservations,
        added=request.args.get('added')
    )

@app.route('/admin/delete/<int:id>')
def delete_reservation(id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM reservations WHERE id=?", (id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('admin'))

@app.route('/admin/delete_ville/<int:id>')
def delete_ville(id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM reservations WHERE ville=(SELECT nom FROM villes WHERE id=?)", (id,))
    cursor.execute("DELETE FROM attractions WHERE ville_id=?", (id,))
    cursor.execute("DELETE FROM villes WHERE id=?", (id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('admin'))

@app.route('/admin/add_ville', methods=['GET', 'POST'])
def add_ville():
    if not session.get('admin'):
        return redirect(url_for('login'))
    msg = None
    if request.method == 'POST':
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO villes (nom, description, description_fr, description_en, type, distance, prix_bus, prix_taxi, image) VALUES (?,?,?,?,?,?,?,?,?)",
                (request.form['nom'], request.form['description'], request.form.get('description_fr', ''), request.form.get('description_en', ''), request.form['type'],
                 request.form['distance'], request.form['prix_bus'], request.form['prix_taxi'], request.form['image'])
            )
            db.commit()
            cursor.close()
            db.close()
            return redirect(url_for('admin', added='1'))
        except Exception as e:
            msg = 'Error: ' + str(e)
    return render_template("add_ville.html", msg=msg)

if __name__ == '__main__':
    app.run(debug=True)
