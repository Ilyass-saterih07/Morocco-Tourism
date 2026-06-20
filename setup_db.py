import os
import sqlite3

_APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get('DB_PATH', os.path.join(_APP_DIR, 'database.db'))

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

db = sqlite3.connect(DB_PATH)
c = db.cursor()
c.execute("PRAGMA foreign_keys=ON")

c.execute("""CREATE TABLE villes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    nom_fr TEXT,
    nom_en TEXT,
    description TEXT,
    description_fr TEXT,
    description_en TEXT,
    type TEXT,
    distance TEXT,
    prix_bus TEXT,
    prix_taxi TEXT,
    image TEXT,
    note REAL DEFAULT 0,
    note_fr TEXT DEFAULT '',
    note_en TEXT DEFAULT '',
    rating TEXT DEFAULT '',
    rating_fr TEXT DEFAULT '',
    rating_en TEXT DEFAULT '',
    atmosphere TEXT,
    atmosphere_fr TEXT,
    atmosphere_en TEXT,
    risques TEXT,
    risques_fr TEXT,
    risques_en TEXT,
    activites TEXT,
    activites_fr TEXT,
    activites_en TEXT,
    infos_utiles TEXT,
    infos_utiles_fr TEXT,
    infos_utiles_en TEXT,
    galerie1 TEXT,
    galerie2 TEXT,
    galerie3 TEXT,
    lat REAL DEFAULT 0,
    lng REAL DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    bus_duration TEXT DEFAULT '',
    taxi_duration TEXT DEFAULT '',
    voiture_duration TEXT DEFAULT '',
    plats_typiques TEXT,
    plats_typiques_fr TEXT,
    plats_typiques_en TEXT,
    population TEXT DEFAULT '',
    monnaie TEXT DEFAULT '',
    langues TEXT DEFAULT '',
    meilleure_periode TEXT,
    meilleure_periode_fr TEXT,
    meilleure_periode_en TEXT
)""")

c.execute("""CREATE TABLE reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_client TEXT NOT NULL,
    ville TEXT NOT NULL,
    date_depart TEXT NOT NULL,
    personnes INTEGER NOT NULL,
    email TEXT NOT NULL DEFAULT '',
    telephone TEXT NOT NULL DEFAULT '',
    card_last4 TEXT DEFAULT ''
)""")

c.execute("""CREATE TABLE attractions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ville_id INTEGER NOT NULL,
    nom TEXT NOT NULL,
    nom_fr TEXT,
    nom_en TEXT,
    categorie TEXT NOT NULL,
    description TEXT,
    description_fr TEXT,
    description_en TEXT,
    adresse TEXT,
    adresse_fr TEXT,
    adresse_en TEXT,
    prix TEXT,
    image TEXT,
    note REAL DEFAULT 4.0,
    FOREIGN KEY (ville_id) REFERENCES villes(id) ON DELETE CASCADE
)""")

c.execute("""CREATE TABLE attraction_reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attraction_id INTEGER NOT NULL,
    attraction_nom TEXT NOT NULL,
    ville_nom TEXT NOT NULL,
    nom_client TEXT NOT NULL,
    email TEXT NOT NULL,
    telephone TEXT NOT NULL,
    card_last4 TEXT DEFAULT '',
    date_depart TEXT NOT NULL,
    personnes INTEGER NOT NULL,
    details TEXT,
    FOREIGN KEY (attraction_id) REFERENCES attractions(id) ON DELETE CASCADE
)""")

c.execute("""CREATE TABLE menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attraction_id INTEGER NOT NULL,
    nom_item TEXT NOT NULL,
    nom_item_ar TEXT,
    nom_item_en TEXT,
    prix TEXT NOT NULL,
    description TEXT,
    description_ar TEXT,
    description_en TEXT,
    FOREIGN KEY (attraction_id) REFERENCES attractions(id) ON DELETE CASCADE
)""")

c.execute("""CREATE TABLE hotel_rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attraction_id INTEGER NOT NULL,
    type_chambre TEXT NOT NULL,
    type_chambre_ar TEXT,
    type_chambre_en TEXT,
    prix TEXT NOT NULL,
    description TEXT,
    description_ar TEXT,
    description_en TEXT,
    capacite INTEGER DEFAULT 2,
    FOREIGN KEY (attraction_id) REFERENCES attractions(id) ON DELETE CASCADE
)""")

c.execute("""CREATE TABLE guides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    nom_ar TEXT,
    nom_en TEXT,
    ville_id INTEGER NOT NULL,
    specialite TEXT,
    specialite_ar TEXT,
    specialite_en TEXT,
    prix TEXT,
    telephone TEXT,
    image TEXT,
    FOREIGN KEY (ville_id) REFERENCES villes(id) ON DELETE CASCADE
)""")

c.execute("""CREATE TABLE favoris (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    ville_id INTEGER NOT NULL,
    created_at TEXT DEFAULT (datetime('now','localtime')),
    UNIQUE(session_id, ville_id)
)""")

c.execute("""CREATE TABLE ville_prix_hebergement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ville_id INTEGER NOT NULL,
    type_hebergement TEXT NOT NULL,
    prix_par_nuit REAL NOT NULL,
    FOREIGN KEY (ville_id) REFERENCES villes(id) ON DELETE CASCADE
)""")

c.execute("""CREATE TABLE avis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ville_id INTEGER NOT NULL,
    auteur TEXT NOT NULL,
    note REAL NOT NULL,
    commentaire TEXT,
    date_post TEXT DEFAULT (datetime('now','localtime')),
    FOREIGN KEY (ville_id) REFERENCES villes(id) ON DELETE CASCADE
)""")

villes = [
    ('Marrakech','مراكش مدينة حمراء رائعة تجمع بين الأسواق العتيقة والقصور التاريخية.','Marrakech est une ville rouge magnifique qui allie souks ancestraux et palais historiques.','Marrakech is a magnificent red city combining ancient souks and historic palaces.','Ville','Casablanca → Marrakech: 580 km','Casablanca → Marrakech: 120 DH','Casablanca → Marrakech: 350 DH','https://upload.wikimedia.org/wikipedia/commons/d/d2/Jemaa_el-Fnaa_at_night.jpg'),
    ('Chefchaouen','شفشاون المدينة الزرقاء الساحرة في شمال المغرب.','Chefchaouen la ville bleue enchanteresse dans le nord du Maroc.','Chefchaouen the enchanting blue city in northern Morocco.','Montagne','Casablanca → Chefchaouen: 620 km','Casablanca → Chefchaouen: 110 DH','Casablanca → Chefchaouen: 320 DH','https://upload.wikimedia.org/wikipedia/commons/7/70/Chefchaouen_the_blue_pearl_kd.jpg'),
    ('Fes','فاس عاصمة الثقافة والتاريخ في المغرب.','Fes capitale de la culture et de l histoire au Maroc.','Fes capital of culture and history in Morocco.','Histoire','Casablanca → Fes: 300 km','Casablanca → Fes: 80 DH','Casablanca → Fes: 250 DH','https://upload.wikimedia.org/wikipedia/commons/8/8b/Fes_-_Tanneries_-_6.jpg'),
    ('Merzouga','مرزوكة بوابة الصحراء الكبرى في المغرب.','Merzouga la porte du grand desert du Maroc.','Merzouga gateway to the great desert of Morocco.','Desert','Casablanca → Merzouga: 900 km','Casablanca → Merzouga: 180 DH','Casablanca → Merzouga: 500 DH','https://upload.wikimedia.org/wikipedia/commons/4/4c/Dunes-Merzouga-Erg_Chebi.JPG'),
    ('Essaouira','الصويرة مدينة الرياح والفن على ساحل المحيط الأطلسي.','Essaouira la ville du vent et de l art sur la cote atlantique.','Essaouira the city of wind and art on the Atlantic coast.','Plage','Casablanca → Essaouira: 480 km','Casablanca → Essaouira: 100 DH','Casablanca → Essaouira: 300 DH','https://upload.wikimedia.org/wikipedia/commons/b/b4/Sqallla_of_Essaouira_%28ancienne_Mogador%29_20.jpg'),
    ('Agadir','أكادير مدينة الشمس والبحر في جنوب المغرب.','Agadir la ville du soleil et de la mer dans le sud du Maroc.','Agadir the city of sun and sea in southern Morocco.','Plage','Casablanca → Agadir: 580 km','Casablanca → Agadir: 120 DH','Casablanca → Agadir: 350 DH','https://upload.wikimedia.org/wikipedia/commons/e/e8/Agadir_bay.jpg'),
    ('Ifrane','إفران المدينة الأوروبية في قلب المغرب.','Ifrane la ville europeenne au coeur du Maroc.','Ifrane the European city in the heart of Morocco.','Montagne','Casablanca → Ifrane: 350 km','Casablanca → Ifrane: 90 DH','Casablanca → Ifrane: 270 DH','https://upload.wikimedia.org/wikipedia/commons/d/d1/IFRANE_SNOW_MOROCCO.jpg'),
    ('Ouarzazate','ورزازات بوابة الصحراء وعاصمة السينما في المغرب.','Ouarzazate la porte du desert et capitale du cinema au Maroc.','Ouarzazate gateway to the desert and film capital of Morocco.','Histoire','Casablanca → Ouarzazate: 700 km','Casablanca → Ouarzazate: 140 DH','Casablanca → Ouarzazate: 400 DH','https://upload.wikimedia.org/wikipedia/commons/4/4a/Ait_Benhaddou_Pano.jpg'),
    ('Casablanca','الدار البيضاء العاصمة الاقتصادية للمغرب، مدينة الأعمال والثقافة والمعمار العصري.','Casablanca la capitale economique du Maroc, ville d affaires de culture et d architecture moderne.','Casablanca the economic capital of Morocco, city of business culture and modern architecture.','Ville','Casablanca (Centre)','0 DH','0 DH','https://upload.wikimedia.org/wikipedia/commons/e/ec/Sunrise_in_Casablanca_with_Hassan_II_Mosque.jpg'),
    ('El Jadida','الجديدة مدينة ساحلية تاريخية تجمع بين الإرث البرتغالي وجمال المحيط الأطلسي.','El Jadida historic coastal city blending Portuguese heritage and Atlantic beauty.','El Jadida ville cotiere historique alliant heritage portugais et beauté de l Atlantique.','Plage','Casablanca → El Jadida: 96 km','Casablanca → El Jadida: 35 DH','Casablanca → El Jadida: 120 DH','https://upload.wikimedia.org/wikipedia/commons/3/34/Portuguese_Cistern_of_El_Jadida%2C_Morocco.jpg'),
]

c.executemany("INSERT INTO villes (nom, nom_fr, nom_en, description, description_fr, description_en, type, distance, prix_bus, prix_taxi, image) VALUES (?,?,?,?,?,?,?,?,?,?,?)", [(v[0], v[0], v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8]) for v in villes])

c.executemany("INSERT INTO ville_prix_hebergement (ville_id, type_hebergement, prix_par_nuit) VALUES (?,?,?)", [
    (1,'hotel',600),(1,'riad',800),(1,'auberge',300),(1,'camp',200),
    (2,'hotel',450),(2,'riad',550),(2,'auberge',200),(2,'camp',150),
    (3,'hotel',500),(3,'riad',700),(3,'auberge',250),(3,'camp',180),
    (4,'hotel',350),(4,'riad',500),(4,'auberge',150),(4,'camp',500),
    (5,'hotel',550),(5,'riad',650),(5,'auberge',280),(5,'camp',160),
    (6,'hotel',700),(6,'riad',900),(6,'auberge',350),(6,'camp',200),
    (7,'hotel',400),(7,'riad',500),(7,'auberge',200),(7,'camp',300),
    (8,'hotel',380),(8,'riad',500),(8,'auberge',180),(8,'camp',250),
    (9,'hotel',800),(9,'riad',1000),(9,'auberge',400),(9,'camp',250),
    (10,'hotel',500),(10,'riad',600),(10,'auberge',250),(10,'camp',120),
])

c.executemany("INSERT INTO avis (ville_id, auteur, note, commentaire) VALUES (?,?,?,?)", [
    (1,'Sophie M.',5.0,'Magnifique ville, les souks sont incroyables !'),
    (1,'Ahmed R.',4.5,'Superbe séjour, je recommande.'),
    (1,'John D.',4.8,'Un voyage inoubliable.'),
    (2,'Marie L.',5.0,'La ville bleue est un rêve !'),
    (2,'Hassan T.',4.7,'Endroit paisible et magnifique.'),
    (3,'Fatima Z.',4.9,'Fes est un musée à ciel ouvert.'),
    (3,'Pierre A.',4.6,'Histoire et culture exceptionnelles.'),
    (4,'Youssef K.',5.0,'Le désert est magique, surtout au coucher du soleil.'),
    (5,'Leila B.',4.8,'Essaouira, ville du vent et de l art.'),
    (6,'Karim S.',4.7,'Plage magnifique, soleil garanti.'),
    (7,'Nadia A.',4.5,'Ifrane, la petite Suisse du Maroc.'),
    (8,'Omar J.',4.6,'Les studios de cinéma valent le détour.'),
    (9,'Hind M.',4.9,'Casablanca une ville moderne et accueillante.'),
    (10,'Samir D.',4.7,'El Jadida, un joyau portugais au Maroc.'),
])

c.executemany("INSERT INTO guides (nom, nom_ar, nom_en, ville_id, specialite, specialite_ar, specialite_en, prix, telephone, image) VALUES (?,?,?,?,?,?,?,?,?,?)", [
    ('Hassan','حسن','Hassan',1,'Guide historique','مرشد تاريخي','Historical guide','300 DH','+212612345678','https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80'),
    ('Fatima','فاطمة','Fatima',1,'ثقافة ومأكولات','ثقافة ومأكولات','Culture & Cuisine','250 DH','+212612345679','https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&q=80'),
    ('Ahmed','أحمد','Ahmed',2,'جولات المدينة','جولات المدينة','City tours','200 DH','+212612345680','https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80'),
    ('Youssef','يوسف','Youssef',3,'تاريخ فاس','تاريخ فاس','Fes history','250 DH','+212612345681','https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&q=80'),
    ('Karima','كريمة','Karima',3,'حرف يدوية','حرف يدوية','Handicrafts','200 DH','+212612345682','https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&q=80'),
    ('Mohamed','محمد','Mohamed',4,'صحراء وكثبان','صحراء وكثبان','Desert & Dunes','400 DH','+212612345683','https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80'),
    ('Leila','ليلى','Leila',5,'فنون وثقافة','فنون وثقافة','Arts & Culture','250 DH','+212612345684','https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&q=80'),
    ('Omar','عمر','Omar',6,'شاطئ وأمواج','شاطئ وأمواج','Beach & Surf','200 DH','+212612345685','https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80'),
    ('Nadia','نادية','Nadia',7,'طبيعة وغابات','طبيعة وغابات','Nature & Forests','250 DH','+212612345686','https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=400&q=80'),
    ('Rachid','رشيد','Rachid',8,'سينما وصحراء','سينما وصحراء','Cinema & Desert','300 DH','+212612345687','https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80'),
    ('Samira','سميرة','Samira',9,'جولات حضرية','جولات حضرية','Urban tours','250 DH','+212612345688','https://images.unsplash.com/photo-1489424731084-a5d8b219a5bb?w=400&q=80'),
    ('Driss','إدريس','Driss',10,'تاريخ برتغالي','تاريخ برتغالي','Portuguese history','200 DH','+212612345689','https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80'),
])

attractions = [
    (1,'مطعم نوماد','Restaurant Nomad','Restaurant Nomad','restaurant','مطعم عصري يقدم أحسن الأطباق المغربية','Restaurant moderne proposant les meilleurs plats marocains','Modern restaurant serving the best Moroccan dishes','درب عتيق، مراكش','Derb Atiq, Marrakech','Derb Atiq, Marrakech','150-300 DH','https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80',4.8),
    (1,'لو جاردان','Le Jardin','Le Jardin','restaurant','مطعم في حديقة خضراء مع أطباق مغربية وعالمية','Restaurant dans un jardin verdoyant avec plats marocains et internationaux','Restaurant in a green garden with Moroccan and international dishes','زنقة المجلس، مراكش','Rue du Conseil, Marrakech','Rue du Conseil, Marrakech','200-400 DH','https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&q=80',4.7),
    (1,'لامامونيا','La Mamounia','La Mamounia','hotel','أفخم فندق في مراكش والمغرب كله','Le plus luxueux hotel de Marrakech et du Maroc','The most luxurious hotel in Marrakech and all of Morocco','شارع الحرية، مراكش','Avenue de la Liberte, Marrakech','Avenue de la Liberte, Marrakech','3000-15000 DH/ليلة','https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80',4.9),
    (1,'رياض ياسمين','Riad Yasmine','Riad Yasmine','hotel','رياض أصيل في قلب المدينة العتيقة','Riad authentique au coeur de la vieille ville','Authentic riad in the heart of the old city','المدينة القديمة، مراكش','Medina, Marrakech','Medina, Marrakech','800-2000 DH/ليلة','https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&q=80',4.6),
    (1,'متحف مراكش','Musee de Marrakech','Marrakech Museum','musee','متحف يضم أروع التحف الأمازيغية والإسلامية','Musee abritant les plus belles collections amazighes et islamiques','Museum housing the finest Amazigh and Islamic artifacts','ساحة بن يوسف، مراكش','Place Ben Youssef, Marrakech','Place Ben Youssef, Marrakech','70 DH','https://upload.wikimedia.org/wikipedia/commons/1/13/Museum_of_Marrakech.JPG',4.5),
    (1,'متحف إيف سان لوران','Musee Yves Saint Laurent','Yves Saint Laurent Museum','musee','متحف مخصص لأعمال المصمم الشهير','Musee dedie aux oeuvres du celebre createur','Museum dedicated to the works of the famous designer','حديقة المجورلة، مراكش','Jardin Majorelle, Marrakech','Jardin Majorelle, Marrakech','100 DH','https://upload.wikimedia.org/wikipedia/commons/5/52/Architetti_studio_ko%2C_museo_YSL_a_Marrakech.jpg',4.7),
    (1,'صيدلية الحمراء','Pharmacie Al Hambra','Al Hambra Pharmacy','pharmacie','صيدلية مركزية مفتوحة 24 ساعة','Pharmacie centrale ouverte 24h/24','Central pharmacy open 24 hours','شارع محمد الخامس، مراكش','Avenue Mohammed V, Marrakech','Avenue Mohammed V, Marrakech','-','https://images.unsplash.com/photo-1631549916768-4119b2e5f926?w=800&q=80',4.2),
    (1,'ساحة جامع الفنا','Place Jemaa el-Fna','Jemaa el-Fna Square','lieu','أشهر ساحة في المغرب مليئة بالحياة والفرجة','La plus celebre place du Maroc animee et pittoresque','The most famous square in Morocco full of life and entertainment','مراكش المدينة القديمة','Medina, Marrakech','Medina, Marrakech','مجاني','https://upload.wikimedia.org/wikipedia/commons/d/d2/Jemaa_el-Fnaa_at_night.jpg',5.0),
    (1,'جامع الكتبية','Mosquee Koutoubia','Koutoubia Mosque','lieu','أيقونة مراكش والمسجد الأكبر في المدينة','L icone de Marrakech et la plus grande mosquee de la ville','The icon of Marrakech and the largest mosque in the city','ساحة جامع الفنا، مراكش','Place Jemaa el-Fna, Marrakech','Place Jemaa el-Fna, Marrakech','مجاني','https://upload.wikimedia.org/wikipedia/commons/e/e8/Koutoubia_minaret_in_Marrakech%2C_Morocco.jpg',4.9),
    (2,'مطعم باب الصور','Restaurant Bab Ssour','Restaurant Bab Ssour','restaurant','مطعم بإطلالة خلابة على المدينة الزرقاء','Restaurant avec une vue imprenable sur la ville bleue','Restaurant with a breathtaking view of the blue city','باب السوق، شفشاون','Bab Souk, Chefchaouen','Bab Souk, Chefchaouen','80-200 DH','https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&q=80',4.6),
    (2,'كازا بيرليتا','Casa Perleta','Casa Perleta','hotel','فندق أنيق بإطلالة على أزقة المدينة الزرقاء','Hotel elegant avec vue sur les ruelles de la ville bleue','Elegant hotel overlooking the alleys of the blue city','شفشاون المدينة القديمة','Medina, Chefchaouen','Medina, Chefchaouen','600-1500 DH/ليلة','https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=800&q=80',4.7),
    (2,'قصبة شفشاون','Kasbah de Chefchaouen','Chefchaouen Kasbah','musee','قصبة تاريخية تضم متحف الإثنوغرافيا وحديقة جميلة','Kasbah historique abritant un musee d ethnographie et un joli jardin','Historic kasbah housing an ethnography museum and a beautiful garden','المدينة القديمة، شفشاون','Medina, Chefchaouen','Medina, Chefchaouen','20 DH','https://upload.wikimedia.org/wikipedia/commons/7/73/Kasbah_Museum_%2839014311340%29.jpg',4.7),
    (2,'صيدلية الريف','Pharmacie du Rif','Rif Pharmacy','pharmacie','صيدلية في قلب المدينة','Pharmacie au coeur de la ville','Pharmacy in the heart of the city','الساحة الرئيسية، شفشاون','Place Principale, Chefchaouen','Main Square, Chefchaouen','-','https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=800&q=80',4.1),
    (2,'الأزقة الزرقاء','Ruelles Bleues','Blue Alleys','lieu','أجمل أزقة المدينة الزرقاء المزينة بالأبيض والأزرق','Les plus belles ruelles de la ville bleue ornees de blanc et de bleu','The most beautiful alleys of the blue city adorned in white and blue','المدينة القديمة، شفشاون','Medina, Chefchaouen','Medina, Chefchaouen','مجاني','https://upload.wikimedia.org/wikipedia/commons/7/70/Chefchaouen_the_blue_pearl_kd.jpg',5.0),
    (2,'شلال راس الماء','Cascade Ras El Ma','Ras El Ma Waterfall','lieu','شلال طبيعي خلاب عند مدخل شفشاون','Cascade naturelle magnifique a l entree de Chefchaouen','Beautiful natural waterfall at the entrance of Chefchaouen','شمال شفشاون','Nord de Chefchaouen','North of Chefchaouen','مجاني','https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=800&q=80',4.8),
    (2,'جبل كلاع','Mont Kalaa','Mount Kalaa','lieu','قمة جبلية بانوراما استثنائية على المدينة الزرقاء','Sommet montagneux avec panorama exceptionnel sur la ville bleue','Mountain summit with exceptional panorama of the blue city','فوق شفشاون','Au-dessus de Chefchaouen','Above Chefchaouen','مجاني','https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=80',4.9),
    (3,'مطعم دار الطاجين','Restaurant Dar Tajine','Restaurant Dar Tajine','restaurant','أفضل الأطباق الفاسية الأصيلة في قلب المدينة العتيقة','Les meilleurs plats fassis authentiques au coeur de la vieille ville','The best authentic Fassi dishes in the heart of the old city','طلعة كبيرة، فاس','Talaa Kebira, Fes','Talaa Kebira, Fes','100-250 DH','https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80',4.7),
    (3,'رياض فاس','Riad Fes','Riad Fes','hotel','رياض فاخر في قلب فاس البالي بتصميم مغربي أصيل','Riad de luxe au coeur du Fes el-Bali au design marocain authentique','Luxury riad in the heart of Fes el-Bali with authentic Moroccan design','فاس البالي','Fes el-Bali','Fes el-Bali','1500-4000 DH/ليلة','https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80',4.8),
    (3,'متحف البطحاء','Musee Al Batha','Al Batha Museum','musee','متحف الفنون والحرف المغربية في قصر تاريخي','Musee des arts et artisanats marocains dans un palais historique','Museum of Moroccan arts and crafts in a historic palace','فاس البالي','Fes el-Bali','Fes el-Bali','30 DH','https://upload.wikimedia.org/wikipedia/commons/6/6c/Dar_Batha_Museum%2C_Fes_%288958246898%29.jpg',4.6),
    (3,'صيدلية المدينة','Pharmacie de la Medina','Medina Pharmacy','pharmacie','صيدلية مركزية قرب باب بوجلود','Pharmacie centrale pres de Bab Boujloud','Central pharmacy near Bab Boujloud','باب بوجلود، فاس','Bab Boujloud, Fes','Bab Boujloud, Fes','-','https://images.unsplash.com/photo-1563213126-a4273aed2016?w=800&q=80',4.0),
    (3,'المدابغ الملكية','Tanneries Royales','Royal Tanneries','lieu','أشهر مدابغ الجلود في العالم بألوانها الزاهية','Les plus celebres tanneries du monde aux couleurs vives','The most famous tanneries in the world with vibrant colors','فاس البالي','Fes el-Bali','Fes el-Bali','مجاني','https://upload.wikimedia.org/wikipedia/commons/8/8b/Fes_-_Tanneries_-_6.jpg',4.9),
    (3,'جامعة القرويين','Universite Al Quaraouiyine','Al Quaraouiyine University','lieu','أقدم جامعة في العالم تأسست عام 859م','La plus ancienne universite du monde fondee en 859','The oldest university in the world founded in 859','فاس البالي','Fes el-Bali','Fes el-Bali','مجاني','https://upload.wikimedia.org/wikipedia/commons/8/8a/Al_Quaraouiyine.jpg',5.0),
    (3,'حديقة جنان السبيل','Jardin Jnan Sbil','Jnan Sbil Garden','lieu','أقدم حديقة في فاس تعود للعصر المريني','Le plus ancien jardin de Fes datant de l epoque merinide','The oldest garden in Fes dating from the Marinid era','فاس البالي','Fes el-Bali','Fes el-Bali','مجاني','https://upload.wikimedia.org/wikipedia/commons/e/e1/Garden_jnan_sebil_fes.jpg',4.5),
    (4,'مقهى الجنوب','Cafe du Sud','Cafe du Sud','restaurant','مطعم صحراوي يقدم أطباق تقليدية بأجواء صحراوية فريدة','Restaurant saharien proposant des plats traditionnels dans une ambiance unique','Desert restaurant serving traditional dishes in a unique desert atmosphere','مرزوكة المركز','Centre de Merzouga','Center of Merzouga','80-180 DH','https://images.unsplash.com/photo-1529543544282-ea669407fca3?w=800&q=80',4.5),
    (4,'قصبة تمبكتو','Kasbah Tombouctou','Kasbah Tombouctou','hotel','فندق فاخر وسط الكثبان الرملية بإطلالة على الصحراء','Hotel de luxe au milieu des dunes avec vue sur le desert','Luxury hotel in the middle of the dunes with desert view','مرزوكة الكثبان','Dunes de Merzouga','Merzouga Dunes','2000-6000 DH/ليلة','https://upload.wikimedia.org/wikipedia/commons/8/8a/Adobe_towers_of_the_Kasbah_Tombouctou_%28Timbuktu%29_in_the_village_of_Mhamid_El_Ghezlane%2C_Morocco.jpg',4.9),
    (4,'صيدلية الواحة','Pharmacie de l Oasis','Oasis Pharmacy','pharmacie','الصيدلية الرئيسية في مرزوكة','La pharmacie principale de Merzouga','The main pharmacy in Merzouga','مرزوكة المركز','Centre de Merzouga','Center of Merzouga','-','https://images.unsplash.com/photo-1576602976047-174e57a47881?w=800&q=80',4.0),
    (4,'كثبان عرق الشبي','Dunes Erg Chebbi','Erg Chebbi Dunes','lieu','أضخم كثبان رملية في المغرب ارتفاعها 150 متر','Les plus grandes dunes de sable du Maroc hautes de 150 metres','The largest sand dunes in Morocco rising 150 meters','مرزوكة','Merzouga','Merzouga','150 DH جمل','https://upload.wikimedia.org/wikipedia/commons/4/4c/Dunes-Merzouga-Erg_Chebi.JPG',5.0),
    (4,'ليلة في الصحراء','Nuit dans le Desert','Night in the Desert','lieu','تجربة المبيت في خيمة صحراوية تحت النجوم','Experience de nuit sous les etoiles dans une tente saharienne','Overnight experience in a desert tent under the stars','مرزوكة الصحراء','Desert de Merzouga','Merzouga Desert','500-1500 DH','https://images.unsplash.com/photo-1518684079-3c830dcef090?w=800&q=80',5.0),
    (5,'مطعم طاروس','Restaurant Taros','Restaurant Taros','restaurant','مطعم على السطح بإطلالة على المدينة والمحيط','Restaurant sur le toit avec vue sur la ville et l ocean','Rooftop restaurant with view of the city and the ocean','ساحة مولاي الحسن، الصويرة','Place Moulay Hassan, Essaouira','Place Moulay Hassan, Essaouira','150-350 DH','https://images.unsplash.com/photo-1600891964599-f61ba0e24092?w=800&q=80',4.7),
    (5,'فندق سوفيتيل','Hotel Sofitel','Hotel Sofitel','hotel','فندق 5 نجوم بإطلالة مباشرة على المحيط الأطلسي','Hotel 5 etoiles avec vue directe sur l ocean Atlantique','5-star hotel with direct view of the Atlantic Ocean','شاطئ الصويرة','Plage d Essaouira','Essaouira Beach','2000-5000 DH/ليلة','https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80',4.8),
    (5,'متحف سيدي محمد بن عبد الله','Musee Sidi Mohammed ben Abdallah','Sidi Mohammed ben Abdallah Museum','musee','متحف الفنون التقليدية والموسيقى الغناوية','Musee des arts traditionnels et de la musique gnaouie','Museum of traditional arts and Gnaoua music','الصويرة المدينة','Medina d Essaouira','Essaouira Medina','20 DH','https://upload.wikimedia.org/wikipedia/commons/a/a3/Essaouira_le_matin_-_panoramio_%2845%29.jpg',4.4),
    (5,'صيدلية الأطلسي','Pharmacie Atlantique','Atlantic Pharmacy','pharmacie','صيدلية مركزية في الصويرة','Pharmacie centrale a Essaouira','Central pharmacy in Essaouira','شارع محمد الخامس، الصويرة','Avenue Mohammed V, Essaouira','Avenue Mohammed V, Essaouira','-','https://images.unsplash.com/photo-1471864190281-a93a3070b6de?w=800&q=80',4.1),
    (5,'أسوار الصويرة','Remparts d Essaouira','Essaouira Ramparts','lieu','أسوار تاريخية مطلة على المحيط الأطلسي من القرن 18','Remparts historiques surplombant l Atlantique datant du 18e siecle','Historic ramparts overlooking the Atlantic from the 18th century','الصويرة الميناء','Port d Essaouira','Essaouira Port','مجاني','https://upload.wikimedia.org/wikipedia/commons/b/b4/Sqallla_of_Essaouira_%28ancienne_Mogador%29_20.jpg',4.9),
    (6,'مطعم لا سكالا','Restaurant La Scala','Restaurant La Scala','restaurant','مطعم راقي يقدم المأكولات المغربية والمتوسطية','Restaurant elegant proposant cuisine marocaine et mediterraneenne','Elegant restaurant offering Moroccan and Mediterranean cuisine','شاطئ أكادير','Plage d Agadir','Agadir Beach','200-450 DH','https://images.unsplash.com/photo-1544148103-0773bf10d330?w=800&q=80',4.6),
    (6,'ريو تيكيدا بيتش','Riu Tikida Beach','Riu Tikida Beach','hotel','منتجع 5 نجوم مباشرة على شاطئ أكادير الذهبي','Complexe 5 etoiles directement sur la plage d or d Agadir','5-star resort directly on the golden beach of Agadir','شاطئ أكادير','Plage d Agadir','Agadir Beach','2500-7000 DH/ليلة','https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80',4.8),
    (6,'متحف أمازيغ','Musee Amazigh','Amazigh Museum','musee','يضم أكبر مجموعة من التحف الأمازيغية في المغرب','Abrite la plus grande collection d artefacts amazighs du Maroc','Houses the largest collection of Amazigh artifacts in Morocco','أكادير المدينة','Ville d Agadir','Agadir City','30 DH','https://images.unsplash.com/photo-1762893134376-6b6397886866?w=800&q=80',4.5),
    (6,'صيدلية الشمس','Pharmacie du Soleil','Sun Pharmacy','pharmacie','صيدلية مركزية مفتوحة 24 ساعة في أكادير','Pharmacie centrale ouverte 24h/24 a Agadir','Central pharmacy open 24 hours in Agadir','أكادير المركز','Centre d Agadir','Agadir Center','-','https://images.unsplash.com/photo-1516549655169-df83a0774514?w=800&q=80',4.2),
    (6,'شاطئ أكادير','Plage d Agadir','Agadir Beach','lieu','شاطئ ذهبي يمتد 10 كيلومترات مع مياه دافئة','Plage doree s etendant sur 10 km avec eaux chaudes','Golden beach stretching 10 km with warm waters','أكادير','Agadir','Agadir','مجاني','https://upload.wikimedia.org/wikipedia/commons/e/e8/Agadir_bay.jpg',5.0),
    (7,'مطعم بين زوت','Restaurant Pin Zut','Restaurant Pin Zut','restaurant','مطعم وسط غابة الأرز بأطباق مغربية دافئة','Restaurant au milieu de la foret de cedres aux plats marocains chaleureux','Restaurant in the middle of the cedar forest with warm Moroccan dishes','إفران المركز','Centre d Ifrane','Center of Ifrane','100-250 DH','https://images.unsplash.com/photo-1466978913421-dad2ebd01d17?w=800&q=80',4.5),
    (7,'فندق مشليفن','Hotel Michlifen','Hotel Michlifen','hotel','أفخم فندق في إفران بإطلالة على الغابة والجبال','Le plus luxueux hotel d Ifrane avec vue sur la foret et les montagnes','The most luxurious hotel in Ifrane with forest and mountain views','إفران','Ifrane','Ifrane','3000-8000 DH/ليلة','https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80',4.9),
    (7,'صيدلية الأطلس','Pharmacie de l Atlas','Atlas Pharmacy','pharmacie','صيدلية في مركز إفران','Pharmacie au centre d Ifrane','Pharmacy in central Ifrane','إفران المركز','Centre d Ifrane','Center of Ifrane','-','https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800&q=80',4.0),
    (7,'غابة الأرز','Foret de Cedres','Cedar Forest','lieu','غابة الأرز الشهيرة موطن القردة البربرية','La celebre foret de cedres habitat des singes magots','The famous cedar forest home to Barbary macaques','إفران المحيط','Environs d Ifrane','Ifrane Surroundings','مجاني','https://images.unsplash.com/photo-1448375240586-882707db888b?w=800&q=80',4.8),
    (7,'بحيرة دايت عوا','Lac Dayet Aoua','Lake Dayet Aoua','lieu','بحيرة طبيعية خلابة محاطة بالغابات','Lac naturel magnifique entoure de forets','Beautiful natural lake surrounded by forests','خارج إفران','Pres d Ifrane','Near Ifrane','مجاني','https://images.unsplash.com/photo-1439405326854-014607f694d7?w=800&q=80',4.7),
    (8,'مطعم دويرية','Restaurant Douyria','Restaurant Douyria','restaurant','مطعم تقليدي يقدم أطباق ورزازات الأصيلة','Restaurant traditionnel proposant les plats authentiques de Ouarzazate','Traditional restaurant serving authentic Ouarzazate dishes','ورزازات المركز','Centre de Ouarzazate','Center of Ouarzazate','80-200 DH','https://images.unsplash.com/photo-1530554764233-e79e16c91d08?w=800&q=80',4.5),
    (8,'دار قمر','Dar Kamar','Dar Kamar','hotel','رياض فاخر في قلب ورزازات بتصميم قصباوي','Riad de luxe au coeur de Ouarzazate au design kasbaoui','Luxury riad in the heart of Ouarzazate with kasbah design','ورزازات المدينة','Ville de Ouarzazate','Ouarzazate City','1000-3000 DH/ليلة','https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80',4.7),
    (8,'متحف السينما','Musee du Cinema','Cinema Museum','musee','متحف يحكي تاريخ أشهر أفلام صورت في ورزازات','Musee racontant l histoire des plus celebres films tournes a Ouarzazate','Museum telling the story of famous films shot in Ouarzazate','ورزازات المركز','Centre de Ouarzazate','Center of Ouarzazate','50 DH','https://upload.wikimedia.org/wikipedia/commons/9/98/Pathe_Projector_Ouarzazate.jpg',4.6),
    (8,'صيدلية الواحة','Pharmacie de l Oasis','Oasis Pharmacy','pharmacie','صيدلية مركزية في ورزازات','Pharmacie centrale a Ouarzazate','Central pharmacy in Ouarzazate','ورزازات المركز','Centre de Ouarzazate','Center of Ouarzazate','-','https://images.unsplash.com/photo-1550572017-edd951b55104?w=800&q=80',4.0),
    (8,'قصبة أيت بنحدو','Kasbah Ait Ben Haddou','Ait Ben Haddou Kasbah','lieu','أجمل قصبة في المغرب مدرجة في التراث العالمي لليونسكو','La plus belle kasbah du Maroc classee a l UNESCO','The most beautiful kasbah in Morocco listed as UNESCO heritage','30 كم من ورزازات','A 30 km de Ouarzazate','30 km from Ouarzazate','30 DH','https://upload.wikimedia.org/wikipedia/commons/4/4a/Ait_Benhaddou_Pano.jpg',5.0),
    (8,'استوديوهات CLA','Studios CLA','CLA Studios','lieu','أكبر استوديوهات السينما في أفريقيا','Les plus grands studios de cinema en Afrique','The largest film studios in Africa','ورزازات','Ouarzazate','Ouarzazate','60 DH','https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=800&q=80',4.7),
    (9,'ريكس كافيه',"Rick's Cafe","Rick's Cafe",'restaurant','مطعم راق مستوحى من فيلم كازابلانكا الشهير بأجواء كلاسيكية',"Restaurant elegant inspire du celebre film Casablanca dans une ambiance classique","Elegant restaurant inspired by the famous film Casablanca in a classic atmosphere",'شارع سيدي بليوط، الدار البيضاء','Rue Sidi Belyout, Casablanca','Rue Sidi Belyout, Casablanca','300-600 DH','https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80',4.8),
    (9,'لا سقالة','La Sqala','La Sqala','restaurant','مطعم داخل قلعة تاريخية يقدم المأكولات المغربية الأصيلة','Restaurant dans une forteresse historique proposant la cuisine marocaine authentique','Restaurant in a historic fortress serving authentic Moroccan cuisine','بولفار الحانات، الدار البيضاء','Boulevard des Hana, Casablanca','Boulevard des Hana, Casablanca','200-450 DH','https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&q=80',4.7),
    (9,'حياة ريجنسي','Hyatt Regency Casablanca','Hyatt Regency Casablanca','hotel','فندق فاخر 5 نجوم في قلب الدار البيضاء','Hotel de luxe 5 etoiles au coeur de Casablanca','Luxury 5-star hotel in the heart of Casablanca','ساحة محمد الخامس، الدار البيضاء','Place Mohammed V, Casablanca','Place Mohammed V, Casablanca','2500-8000 DH/ليلة','https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80',4.8),
    (9,'فندق كينزي تاور','Hotel Kenzi Tower','Hotel Kenzi Tower','hotel','برج فندقي عصري بإطلالة بانورامية على المدينة والمحيط','Tour hotel moderne avec vue panoramique sur la ville et l ocean','Modern hotel tower with panoramic view of the city and the ocean','مركز التجارة العالمي، الدار البيضاء','World Trade Center, Casablanca','World Trade Center, Casablanca','1800-5000 DH/ليلة','https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80',4.7),
    (9,'متحف الدار البيضاء','Musee de Casablanca','Casablanca Museum','musee','متحف يوثق تاريخ الدار البيضاء من قرية صغيرة إلى مدينة دولية','Musee documentant l histoire de Casablanca de village a ville internationale','Museum documenting Casablancas history from village to international city','حي الأحباس، الدار البيضاء','Quartier des Habous, Casablanca','Habous District, Casablanca','30 DH','https://images.unsplash.com/photo-1606761568499-6d2451b23c66?w=800&q=80',4.5),
    (9,'مسجد الحسن الثاني','Mosquee Hassan II','Hassan II Mosque','lieu','ثاني أكبر مسجد في العالم وأيقونة الدار البيضاء','Deuxieme plus grande mosquee du monde et icone de Casablanca','Second largest mosque in the world and icon of Casablanca','شاطئ الدار البيضاء','Corniche, Casablanca','Corniche, Casablanca','130 DH جولة','https://upload.wikimedia.org/wikipedia/commons/e/ec/Sunrise_in_Casablanca_with_Hassan_II_Mosque.jpg',5.0),
    (9,'صيدلية المركز','Pharmacie du Centre','Central Pharmacy','pharmacie','صيدلية رئيسية في وسط الدار البيضاء','Pharmacie principale au centre de Casablanca','Main pharmacy in central Casablanca','شارع محمد الخامس، الدار البيضاء','Avenue Mohammed V, Casablanca','Avenue Mohammed V, Casablanca','-','https://images.unsplash.com/photo-1550572017-edd951b55104?w=800&q=80',4.3),
    (10,'مطعم السفينة','Restaurant Al Safina','Restaurant Al Safina','restaurant','مطعم على شاطئ الجديدة يقدم أشهى المأكولات البحرية','Restaurant sur la plage d El Jadida proposant les meilleurs fruits de mer','Restaurant on El Jadida beach serving the best seafood','كورنيش الجديدة','Corniche d El Jadida','El Jadida Corniche','150-350 DH','https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&q=80',4.6),
    (10,'فندق لا كاسا','Hotel La Casa','Hotel La Casa','hotel','فندق جميل في قلب الجديدة بالقرب من الشاطئ','Bel hotel au coeur d El Jadida pres de la plage','Beautiful hotel in the heart of El Jadida near the beach','الجديدة المركز','Centre d El Jadida','El Jadida Center','700-2000 DH/ليلة','https://images.unsplash.com/photo-1540541338287-41700207dee6?w=800&q=80',4.5),
    (10,'الصهريج البرتغالي','Citerne Portugaise','Portuguese Cistern','musee','صهريج مائي برتغالي يعود للقرن 16 بأقواسه المذهلة','Citerne portugaise du 16e siecle avec ses arcades epoustouflantes','Portuguese water cistern from the 16th century with stunning arches','الجديدة المدينة','Medina d El Jadida','El Jadida Medina','10 DH','https://upload.wikimedia.org/wikipedia/commons/3/34/Portuguese_Cistern_of_El_Jadida%2C_Morocco.jpg',4.8),
    (10,'صيدلية الشاطئ','Pharmacie de la Plage','Beach Pharmacy','pharmacie','صيدلية قرب شاطئ الجديدة','Pharmacie pres de la plage d El Jadida','Pharmacy near El Jadida beach','كورنيش الجديدة','Corniche d El Jadida','El Jadida Corniche','-','https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=800&q=80',4.1),
    (10,'شاطئ الجديدة','Plage d El Jadida','El Jadida Beach','lieu','شاطئ رملي جميل يمتد على طول الساحل','Belle plage de sable s etendant le long de la cote','Beautiful sandy beach stretching along the coast','الجديدة','El Jadida','El Jadida','مجاني','https://upload.wikimedia.org/wikipedia/commons/3/34/Portuguese_Cistern_of_El_Jadida%2C_Morocco.jpg',4.7),
    (10,'ميناء الجديدة','Port d El Jadida','El Jadida Port','lieu','ميناء تاريخي بناه البرتغاليون في القرن 16','Port historique construit par les Portugais au 16e siecle','Historic port built by the Portuguese in the 16th century','الميناء، الجديدة','Port, El Jadida','Port, El Jadida','مجاني','https://images.unsplash.com/photo-1505228395891-9a51e7e86bf6?w=800&q=80',4.6),
]

c.executemany("INSERT INTO attractions (ville_id, nom, nom_fr, nom_en, categorie, description, description_fr, description_en, adresse, adresse_fr, adresse_en, prix, image, note) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", attractions)

insert_menu_items = [
    (1,'طاجين الدجاج بالليمون','Tajine au citron','Chicken lemon tajine','120 DH','طاجين تقليدي بنكهة الحامض','Tagine traditionnel au citron','Traditional lemon tajine'),
    (1,'كسكس بالخضار','Couscous legumes','Vegetable couscous','90 DH','كسكس مغربي بالخضروات الطازجة','Couscous marocain aux legumes frais','Moroccan couscous with fresh vegetables'),
    (1,'بسطيلة','Pastilla','Pastilla','150 DH','بسطيلة مغربية بالدجاج واللوز','Pastilla marocaine au poulet et amandes','Moroccan pastilla with chicken and almonds'),
    (2,'لحم بالخوخ Pruneaux','Agneau aux pruneaux','Lamb with prunes','140 DH','لحم غنم بالخوخ','Agneau aux pruneaux et amandes','Lamb with prunes and almonds'),
    (2,'حريرة','Harira','Harira','60 DH','حساء مغربي تقليدي','Soupe marocaine traditionnelle','Traditional Moroccan soup'),
    (3,'بسطيلة','Pastilla','Pastilla','180 DH','بسطيلة فاسية بالحمام','Pastilla fassie au pigeon','Fassi pastilla with pigeon'),
    (3,'طاجين فاسي','Tajine fassi','Fassi tajine','130 DH','طاجين فاسي بالبرقوق واللوز','Tajine fassi aux pruneaux et amandes','Fassi tajine with prunes and almonds'),
    (4,'طاجين الصحراء','Tajine du desert','Desert tajine','100 DH','طاجين صحراوي باللحم','Tajine saharien a la viande','Desert meat tajine'),
    (5,'طاجين البحر','Tajine de la mer','Seafood tajine','130 DH','طاجين بالمأكولات البحرية','Tajine aux fruits de mer','Seafood tajine'),
    (5,'مشوي','Grillade','Grill','110 DH','تشكيلة مشاوي','Assortiment de grillades','Grill assortment'),
    (6,'طاجين أكادير','Tajine d Agadir','Agadir tajine','120 DH','طاجين خاص بمنطقة أكادير','Tajine special d Agadir','Special Agadir tajine'),
    (7,'طاجين إفران','Tajine d Ifrane','Ifrane tajine','110 DH','طاجين بجو الغابة','Tajine dans l ambiance forestiere','Tajine in forest ambiance'),
    (8,'كسكس ورزازات','Couscous Ouarzazate','Ouarzazate couscous','100 DH','كسكس على طريقة ورزازات','Couscous a la facon de Ouarzazate','Ouarzazate style couscous'),
    (9,'طاجين الدار البيضاء','Tajine Casablanca','Casablanca tajine','120 DH','طاجين حضري بطابع مديني','Tajine urbain style citadin','Urban city-style tajine'),
    (9,'كوزينة مغربية','Cuisine marocaine','Moroccan cuisine','200 DH','تشكيلة من الأطباق المغربية','Assortiment de plats marocains','Assortment of Moroccan dishes'),
    (10,'طاجين الجديدة','Tajine El Jadida','El Jadida tajine','110 DH','طاجين بلمسة بحرية','Tajine avec une touche marine','Tajine with a marine touch'),
]

c.executemany("INSERT INTO menu_items (attraction_id, nom_item_ar, nom_item, nom_item_en, prix, description_ar, description, description_en) VALUES (?,?,?,?,?,?,?,?)", insert_menu_items)

insert_hotel_rooms = [
    (3,'غرفة كلاسيك','Classique','Classic',1500,'غرفة مريحة بتصميم مغربي','Chambre confortable design marocain','Comfortable room Moroccan design',2),
    (3,'جناح ملكي','Suite royale','Royal Suite',5000,'جناح فخم مع إطلالة على المدينة','Suite luxueuse vue sur la ville','Luxury suite with city view',4),
    (4,'غرفة قياسية','Standard','Standard',800,'غرفة مكيفة مع حمام خاص','Chambre climatisee salle de bain privee','Air-conditioned room private bathroom',2),
    (4,'جناح','Suite','Suite',1500,'جناح عائلي','Suite familiale','Family suite',4),
    (16,'غرفة عادية','Chambre simple','Standard room',300,'غرفة مريحة','Chambre confortable','Comfortable room',2),
    (16,'غرفة مكيفة','Chambre climatisee','Air-conditioned room',450,'غرفة مع تكييف','Chambre avec clim','Room with AC',2),
    (18,'غرفة فاس','Chambre Fes','Fes room',1500,'غرفة بزخرفة مغربية','Chambre a la deco marocaine','Moroccan decor room',2),
    (18,'جناح فاس','Suite Fes','Fes suite',3000,'جناح مطلة على البالي','Suite vue sur Fes el-Bali','Suite overlooking Fes el-Bali',4),
    (25,'خيمة ملكية','Tente royale','Royal tent',2500,'خيمة فاخرة في الكثبان','Tente de luxe dans les dunes','Luxury tent in the dunes',4),
    (31,'غرفة محيط','Chambre ocean','Ocean room',2000,'غرفة مع شرفة على المحيط','Chambre balcon sur l ocean','Room with ocean balcony',2),
    (31,'جناح Atlantique','Suite Atlantique','Atlantic Suite',4000,'جناح على المحيط','Suite sur l ocean','Ocean suite',3),
    (37,'غرفة Riu','Chambre Riu','Riu room',2500,'غرفة منتجع كلاسيكية','Chambre de resort classique','Classic resort room',2),
    (43,'غرفة مشليفن','Chambre Michlifen','Michlifen room',3000,'غرفة مع منظر غابة','Chambre vue foret','Room with forest view',2),
    (45,'غرفة دار قمر','Chambre Dar Kamar','Dar Kamar room',1000,'غرفة بتصميم قصباوي','Chambre design kasbah','Kasbah design room',2),
    (48,'غرفة كينزي','Chambre Kenzi','Kenzi room',1800,'غرفة عصرية مع إطلالة','Chambre moderne avec vue','Modern room with view',2),
    (48,'جناح كينزي','Suite Kenzi','Kenzi suite',4000,'جناح فاخر بإطلالة بانورامية','Suite luxueuse vue panoramique','Luxury suite panoramic view',4),
    (55,'غرفة الجديدة','Chambre El Jadida','El Jadida room',800,'غرفة مريحة','Chambre confortable','Comfortable room',2),
]

c.executemany("INSERT INTO hotel_rooms (attraction_id, type_chambre_ar, type_chambre, type_chambre_en, prix, description_ar, description, description_en, capacite) VALUES (?,?,?,?,?,?,?,?,?)", insert_hotel_rooms)

# Update extra columns for cities
updates = [
    (31.6295, -7.9811, 125, '6h', '3h', '2h30', 'طاجين, كسكس, pastilla, أطباق اللوز', 'Tajine, Couscous, Pastilla, Plats aux amandes', 'Tajine, Couscous, Pastilla, Almond dishes', '~928,000', 'Dirham (MAD)', 'Arabe, Français, Anglais', 'الربيع والخريف', 'Printemps et automne', 'Spring and autumn', 1),
    (35.1688, -5.2636, 98, '6h', '3h30', '2h30', 'طاجين, كسكس, جبن الماعز', 'Tajine, Couscous, Fromage de chèvre', 'Tajine, Couscous, Goat cheese', '~43,000', 'Dirham (MAD)', 'Arabe, Français, Anglais, Espagnol', 'مارس-يونيو', 'Mars-Juin', 'March-June', 2),
    (34.0181, -5.0078, 112, '3h30', '2h', '1h30', 'طاجين فاسي, كسكس, البسطيلة, الحلويات الفاسية', 'Tajine fassi, Couscous, Pastilla, Pâtisseries fassies', 'Fassi tajine, Couscous, Pastilla, Fassi pastries', '~1,112,000', 'Dirham (MAD)', 'Arabe, Français, Anglais', 'الربيع', 'Printemps', 'Spring', 3),
    (31.0444, -4.0033, 87, '10h', '6h', '4h30', 'طاجين, كسكس, الشاي الصحراوي', 'Tajine, Couscous, Thé saharien', 'Tajine, Couscous, Desert tea', '~3,000', 'Dirham (MAD)', 'Arabe, Français, Amazigh', 'الخريف والربيع', 'Automne et printemps', 'Autumn and spring', 4),
    (31.5085, -9.7595, 93, '5h', '2h30', '2h', 'مأكولات بحرية, طاجين, كسكس', 'Fruits de mer, Tajine, Couscous', 'Seafood, Tajine, Couscous', '~77,000', 'Dirham (MAD)', 'Arabe, Français, Anglais', 'الربيع والصيف', 'Printemps et été', 'Spring and summer', 5),
    (30.4278, -9.5981, 105, '6h', '3h', '2h30', 'طاجين, كسكس, مأكولات بحرية', 'Tajine, Couscous, Fruits de mer', 'Tajine, Couscous, Seafood', '~924,000', 'Dirham (MAD)', 'Arabe, Français, Anglais, Allemand', 'طوال السنة', 'Toute l année', 'All year round', 6),
    (33.5217, -5.1122, 76, '4h', '2h', '1h45', 'طاجين, كسكس, جبن, لحوم', 'Tajine, Couscous, Fromage, Viandes', 'Tajine, Couscous, Cheese, Meats', '~14,000', 'Dirham (MAD)', 'Arabe, Français, Amazigh', 'الربيع والصيف', 'Printemps et été', 'Spring and summer', 7),
    (30.9203, -6.8934, 82, '8h', '4h', '3h', 'طاجين, كسكس, أطباق صحراوية', 'Tajine, Couscous, Plats sahariens', 'Tajine, Couscous, Desert dishes', '~71,000', 'Dirham (MAD)', 'Arabe, Français, Amazigh', 'الخريف والربيع', 'Automne et printemps', 'Autumn and spring', 8),
    (33.5731, -7.5898, 140, '0h', '0h', '0h', 'طاجين, كسكس, مأكولات بحرية, مأكولات عالمية', 'Tajine, Couscous, Fruits de mer, Cuisine internationale', 'Tajine, Couscous, Seafood, International cuisine', '~3,360,000', 'Dirham (MAD)', 'Arabe, Français, Anglais, Espagnol', 'طوال السنة', 'Toute l année', 'All year round', 9),
    (33.2566, -8.5088, 89, '1h30', '45min', '30min', 'مأكولات بحرية, طاجين, كسكس', 'Fruits de mer, Tajine, Couscous', 'Seafood, Tajine, Couscous', '~194,000', 'Dirham (MAD)', 'Arabe, Français, Portugais', 'الربيع والصيف', 'Printemps et été', 'Spring and summer', 10),
]

c.executemany("UPDATE villes SET lat=?, lng=?, review_count=?, bus_duration=?, taxi_duration=?, voiture_duration=?, plats_typiques=?, plats_typiques_fr=?, plats_typiques_en=?, population=?, monnaie=?, langues=?, meilleure_periode=?, meilleure_periode_fr=?, meilleure_periode_en=? WHERE id=?", updates)

# Update notes, ratings, etc
c.executemany("UPDATE villes SET note=?, rating=?, rating_fr=?, rating_en=?, atmosphere=?, atmosphere_fr=?, atmosphere_en=?, risques=?, risques_fr=?, risques_en=?, activites=?, activites_fr=?, activites_en=?, infos_utiles=?, infos_utiles_fr=?, infos_utiles_en=?, galerie1=?, galerie2=?, galerie3=? WHERE id=?", [
    (4.7,'ممتاز','Excellent','Excellent','أجواء ساحرة مليئة بالحيوية','Ambiance enchante pleine de vie','Enchanting atmosphere full of life','احذر النشالين في الأماكن المزدحمة','Attention aux pickpockets','Beware of pickpockets','زيارة الأسواق والقصور والمتاحف','Visite des souks palais et musees','Visit souks palaces and museums','أفضل وقت للزيارة: الربيع والخريف','Meilleure periode: printemps et automne','Best time: spring and autumn','https://images.unsplash.com/photo-1597212618440-806262de4f6b?w=800','https://images.unsplash.com/photo-1597212618440-806262de4f6b?w=800','https://images.unsplash.com/photo-1597212618440-806262de4f6b?w=800',1),
    (4.5,'جيد جدا','Tres bien','Very good','أجواء عصرية','Ambiance moderne','Modern atmosphere','احذر حركة المرور','Attention circulation dense','Beware heavy traffic','زيارة المسجد والكورنيش','Visite mosquee et corniche','Visit mosque and corniche','أفضل وقت: طوال السنة','Toute l annee','All year round','https://images.unsplash.com/photo-1558636508-e0db3814bd1d?w=800','https://images.unsplash.com/photo-1558636508-e0db3814bd1d?w=800','https://images.unsplash.com/photo-1558636508-e0db3814bd1d?w=800',9),
    (4.8,'ممتاز','Excellent','Excellent','أجواء تاريخية','Ambiance historique','Historic atmosphere','احذر الضياع في المدينة القديمة','Attention de vous perdre','Beware getting lost','زيارة فاس البالي والمدارس','Visite Fes el-Bali et medersas','Visit Fes el-Bali and madrasas','أفضل وقت: الربيع','Printemps','Spring','https://images.unsplash.com/photo-1567400358593-9eecd275fce0?w=800','https://images.unsplash.com/photo-1567400358593-9eecd275fce0?w=800','https://images.unsplash.com/photo-1567400358593-9eecd275fce0?w=800',3),
    (4.6,'جيد جدا','Tres bien','Very good','أجواء البحر','Ambiance maritime','Maritime atmosphere','احذر الرياح القوية','Attention vents forts','Beware strong winds','زيارة كهف هرقل ومالاباطا','Visite Grotte Hercule Malabata','Visit Hercules Cave Malabata','أفضل وقت: الصيف','Ete','Summer','https://images.unsplash.com/photo-1559847844-5315695dadae?w=800','https://images.unsplash.com/photo-1559847844-5315695dadae?w=800','https://images.unsplash.com/photo-1559847844-5315695dadae?w=800',5),
    (4.5,'جيد','Bien','Good','أجواء صحراوية','Ambiance desertique','Desert atmosphere','احذر الحرارة المرتفعة','Attention fortes chaleurs','Beware high heat','زيارة الاستوديوهات وقصر أيت بن حدو','Visite studios Kasbah Ait Ben Haddou','Visit studios Ait Ben Haddou','أفضل وقت: الخريف والربيع','Automne printemps','Autumn spring','https://images.unsplash.com/photo-1547234935-80c7145ec969?w=800','https://images.unsplash.com/photo-1547234935-80c7145ec969?w=800','https://images.unsplash.com/photo-1547234935-80c7145ec969?w=800',8),
    (4.3,'جيد','Bien','Good','أجواء تاريخية هادئة','Ambiance historique calme','Quiet historic atmosphere','احذر الأماكن المغلقة','Attention espaces confines','Watch confined spaces','زيارة باب المنصور والضريح','Visite Bab Mansour mausolee','Visit Bab Mansour mausoleum','أفضل وقت: الربيع','Printemps','Spring','https://images.unsplash.com/photo-1567636788276-40b696f8e0b1?w=800','https://images.unsplash.com/photo-1567636788276-40b696f8e0b1?w=800','https://images.unsplash.com/photo-1567636788276-40b696f8e0b1?w=800',2),
    (4.9,'ممتاز','Excellent','Excellent','أجواء استوائية','Ambiance tropicale','Tropical atmosphere','احذر التيارات البحرية','Attention courants marins','Beware sea currents','السباحة وركوب الأمواج','Natation surf plongee','Swimming surfing diving','طوال السنة','Toute l annee','All year','https://images.unsplash.com/photo-1537956965359-7573183d1f57?w=800','https://images.unsplash.com/photo-1537956965359-7573183d1f57?w=800','https://images.unsplash.com/photo-1537956965359-7573183d1f57?w=800',6),
    (4.9,'ممتاز','Excellent','Excellent','أجواء هادئة','Ambiance paisible','Peaceful atmosphere','احذر البرد في الشتاء','Attention froid hiver','Beware cold in winter','التجول في الأزقة الزرقاء','Promenade ruelles bleues','Strolling blue alleys','أفضل وقت: الربيع والصيف','Printemps ete','Spring summer','https://images.unsplash.com/photo-1588279106290-911ad85b1fb8?w=800','https://images.unsplash.com/photo-1588279106290-911ad85b1fb8?w=800','https://images.unsplash.com/photo-1588279106290-911ad85b1fb8?w=800',4),
    (4.7,'ممتاز','Excellent','Excellent','أجواء فنية','Ambiance artistique','Artistic atmosphere','احذر الرياح القوية','Attention vents forts','Beware strong winds','ركوب الأمواج وزيارة المدينة','Planche a voile visite medina','Windsurfing visit medina','أفضل وقت: الربيع والصيف','Printemps ete','Spring summer','https://images.unsplash.com/photo-1590075732028-f2e1b73b0cc3?w=800','https://images.unsplash.com/photo-1590075732028-f2e1b73b0cc3?w=800','https://images.unsplash.com/photo-1590075732028-f2e1b73b0cc3?w=800',7),
    (4.5,'جيد جدا','Tres bien','Very good','أجواء أندلسية','Ambiance andalouse','Andalusian atmosphere','احذر التضاريس الجبلية','Attention terrain montagneux','Beware mountain terrain','زيارة المدينة القديمة والمتحف','Visite medina musee','Visit medina museum','أفضل وقت: الربيع','Printemps','Spring','https://images.unsplash.com/photo-1577705998148-6da4f3963bc7?w=800','https://images.unsplash.com/photo-1577705998148-6da4f3963bc7?w=800','https://images.unsplash.com/photo-1577705998148-6da4f3963bc7?w=800',10),
])

db.commit()
db.close()

print(f"Database created: {DB_PATH}")
print("All tables, guides, attractions, menu items, hotel rooms, and sample data inserted!")
