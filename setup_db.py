# setup_db.py
import mysql.connector

db = mysql.connector.connect(host='localhost', user='root', password='', charset='utf8mb4')
c = db.cursor()

c.execute("DROP DATABASE IF EXISTS tourism_dinner")
c.execute("CREATE DATABASE tourism_dinner CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
c.execute("USE tourism_dinner")

c.execute("""CREATE TABLE villes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    nom_fr VARCHAR(200),
    nom_en VARCHAR(200),
    description TEXT,
    description_fr TEXT,
    description_en TEXT,
    type VARCHAR(50),
    distance VARCHAR(50),
    prix_bus VARCHAR(50),
    prix_taxi VARCHAR(50),
    image VARCHAR(500),
    note DECIMAL(3,1) DEFAULT 0,
    note_fr VARCHAR(10) DEFAULT '',
    note_en VARCHAR(10) DEFAULT '',
    rating VARCHAR(20) DEFAULT '',
    rating_fr VARCHAR(20) DEFAULT '',
    rating_en VARCHAR(20) DEFAULT '',
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
    galerie1 VARCHAR(500),
    galerie2 VARCHAR(500),
    galerie3 VARCHAR(500)
)""")

c.execute("""CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_client VARCHAR(100) NOT NULL,
    ville VARCHAR(100) NOT NULL,
    date_depart DATE NOT NULL,
    personnes INT NOT NULL,
    email VARCHAR(200) NOT NULL DEFAULT '',
    telephone VARCHAR(50) NOT NULL DEFAULT '',
    card_last4 VARCHAR(10) DEFAULT ''
)""")

c.execute("""CREATE TABLE attractions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ville_id INT NOT NULL,
    nom VARCHAR(200) NOT NULL,
    nom_fr VARCHAR(200),
    nom_en VARCHAR(200),
    categorie ENUM('restaurant','hotel','musee','pharmacie','lieu') NOT NULL,
    description TEXT,
    description_fr TEXT,
    description_en TEXT,
    adresse VARCHAR(300),
    adresse_fr VARCHAR(300),
    adresse_en VARCHAR(300),
    prix VARCHAR(100),
    image VARCHAR(500),
    note DECIMAL(2,1) DEFAULT 4.0,
    FOREIGN KEY (ville_id) REFERENCES villes(id) ON DELETE CASCADE
)""")

c.execute("""CREATE TABLE attraction_reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    attraction_id INT NOT NULL,
    attraction_nom VARCHAR(200) NOT NULL,
    ville_nom VARCHAR(100) NOT NULL,
    nom_client VARCHAR(100) NOT NULL,
    email VARCHAR(200) NOT NULL,
    telephone VARCHAR(50) NOT NULL,
    card_last4 VARCHAR(10) DEFAULT '',
    date_depart DATE NOT NULL,
    personnes INT NOT NULL,
    details TEXT,
    FOREIGN KEY (attraction_id) REFERENCES attractions(id) ON DELETE CASCADE
)""")

c.execute("""CREATE TABLE menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    attraction_id INT NOT NULL,
    nom_item VARCHAR(200) NOT NULL,
    nom_item_ar VARCHAR(200),
    nom_item_en VARCHAR(200),
    prix VARCHAR(50) NOT NULL,
    description TEXT,
    description_ar TEXT,
    description_en TEXT,
    FOREIGN KEY (attraction_id) REFERENCES attractions(id) ON DELETE CASCADE
)""")

c.execute("""CREATE TABLE hotel_rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    attraction_id INT NOT NULL,
    type_chambre VARCHAR(200) NOT NULL,
    type_chambre_ar VARCHAR(200),
    type_chambre_en VARCHAR(200),
    prix VARCHAR(50) NOT NULL,
    description TEXT,
    description_ar TEXT,
    description_en TEXT,
    capacite INT DEFAULT 2,
    FOREIGN KEY (attraction_id) REFERENCES attractions(id) ON DELETE CASCADE
)""")

c.execute("""CREATE TABLE guides (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    nom_ar VARCHAR(200),
    nom_en VARCHAR(200),
    ville_id INT NOT NULL,
    specialite VARCHAR(200),
    specialite_ar VARCHAR(200),
    specialite_en VARCHAR(200),
    prix VARCHAR(50),
    telephone VARCHAR(50),
    image VARCHAR(500),
    FOREIGN KEY (ville_id) REFERENCES villes(id) ON DELETE CASCADE
)""")

c.execute("""CREATE TABLE favoris (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    ville_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_fav (session_id, ville_id)
)""")

c.execute("""CREATE TABLE ville_prix_hebergement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ville_id INT NOT NULL,
    type_hebergement VARCHAR(50) NOT NULL,
    prix_par_nuit DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (ville_id) REFERENCES villes(id) ON DELETE CASCADE
)""")

c.execute("""CREATE TABLE avis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ville_id INT NOT NULL,
    auteur VARCHAR(100) NOT NULL,
    note DECIMAL(2,1) NOT NULL,
    commentaire TEXT,
    date_post TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
c.executemany("INSERT INTO villes (nom, nom_fr, nom_en, description, description_fr, description_en, type, distance, prix_bus, prix_taxi, image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [(v[0], v[0], v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8]) for v in villes])

c.executemany("INSERT INTO ville_prix_hebergement (ville_id, type_hebergement, prix_par_nuit) VALUES (%s,%s,%s)", [
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

c.executemany("INSERT INTO avis (ville_id, auteur, note, commentaire) VALUES (%s,%s,%s,%s)", [
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

alter_queries = [
    "ALTER TABLE villes ADD COLUMN lat DECIMAL(10,7) DEFAULT 0",
    "ALTER TABLE villes ADD COLUMN lng DECIMAL(10,7) DEFAULT 0",
    "ALTER TABLE villes ADD COLUMN review_count INT DEFAULT 0",
    "ALTER TABLE villes ADD COLUMN bus_duration VARCHAR(50) DEFAULT ''",
    "ALTER TABLE villes ADD COLUMN taxi_duration VARCHAR(50) DEFAULT ''",
    "ALTER TABLE villes ADD COLUMN voiture_duration VARCHAR(50) DEFAULT ''",
    "ALTER TABLE villes ADD COLUMN plats_typiques TEXT",
    "ALTER TABLE villes ADD COLUMN plats_typiques_fr TEXT",
    "ALTER TABLE villes ADD COLUMN plats_typiques_en TEXT",
    "ALTER TABLE villes ADD COLUMN population VARCHAR(50) DEFAULT ''",

    "ALTER TABLE villes ADD COLUMN monnaie VARCHAR(50) DEFAULT ''",
    "ALTER TABLE villes ADD COLUMN langues VARCHAR(200) DEFAULT ''",
    "ALTER TABLE villes ADD COLUMN meilleure_periode TEXT",
    "ALTER TABLE villes ADD COLUMN meilleure_periode_fr TEXT",
    "ALTER TABLE villes ADD COLUMN meilleure_periode_en TEXT",
]
for q in alter_queries:
    try:
        c.execute(q)
    except mysql.connector.Error:
        pass

update_queries = [
    "UPDATE villes SET lat=31.6295, lng=-7.9811, review_count=125, bus_duration='6h', taxi_duration='3h', voiture_duration='2h30', plats_typiques='طاجين, كسكس, pastilla, أطباق اللوز', plats_typiques_fr='Tajine, Couscous, Pastilla, Plats aux amandes', plats_typiques_en='Tajine, Couscous, Pastilla, Almond dishes', population='~928,000', monnaie='Dirham (MAD)', langues='Arabe, Français, Anglais', meilleure_periode='الربيع والخريف', meilleure_periode_fr='Printemps et automne', meilleure_periode_en='Spring and autumn' WHERE id=1",
    "UPDATE villes SET lat=35.1688, lng=-5.2636, review_count=98, bus_duration='6h', taxi_duration='3h30', voiture_duration='2h30', plats_typiques='طاجين, كسكس, جبن الماعز', plats_typiques_fr='Tajine, Couscous, Fromage de chèvre', plats_typiques_en='Tajine, Couscous, Goat cheese', population='~43,000', monnaie='Dirham (MAD)', langues='Arabe, Français, Anglais, Espagnol', meilleure_periode='مارس-يونيو', meilleure_periode_fr='Mars-Juin', meilleure_periode_en='March-June' WHERE id=2",
    "UPDATE villes SET lat=34.0181, lng=-5.0078, review_count=112, bus_duration='3h30', taxi_duration='2h', voiture_duration='1h30', plats_typiques='طاجين فاسي, كسكس, البسطيلة, الحلويات الفاسية', plats_typiques_fr='Tajine fassi, Couscous, Pastilla, Pâtisseries fassies', plats_typiques_en='Fassi tajine, Couscous, Pastilla, Fassi pastries', population='~1,112,000', monnaie='Dirham (MAD)', langues='Arabe, Français, Anglais', meilleure_periode='الربيع', meilleure_periode_fr='Printemps', meilleure_periode_en='Spring' WHERE id=3",
    "UPDATE villes SET lat=31.0444, lng=-4.0033, review_count=87, bus_duration='10h', taxi_duration='6h', voiture_duration='4h30', plats_typiques='طاجين, كسكس, الشاي الصحراوي', plats_typiques_fr='Tajine, Couscous, Thé saharien', plats_typiques_en='Tajine, Couscous, Desert tea', population='~3,000', monnaie='Dirham (MAD)', langues='Arabe, Français, Amazigh', meilleure_periode='الخريف والربيع', meilleure_periode_fr='Automne et printemps', meilleure_periode_en='Autumn and spring' WHERE id=4",
    "UPDATE villes SET lat=31.5085, lng=-9.7595, review_count=93, bus_duration='5h', taxi_duration='2h30', voiture_duration='2h', plats_typiques='مأكولات بحرية, طاجين, كسكس', plats_typiques_fr='Fruits de mer, Tajine, Couscous', plats_typiques_en='Seafood, Tajine, Couscous', population='~77,000', monnaie='Dirham (MAD)', langues='Arabe, Français, Anglais', meilleure_periode='الربيع والصيف', meilleure_periode_fr='Printemps et été', meilleure_periode_en='Spring and summer' WHERE id=5",
    "UPDATE villes SET lat=30.4278, lng=-9.5981, review_count=105, bus_duration='6h', taxi_duration='3h', voiture_duration='2h30', plats_typiques='طاجين, كسكس, مأكولات بحرية', plats_typiques_fr='Tajine, Couscous, Fruits de mer', plats_typiques_en='Tajine, Couscous, Seafood', population='~924,000', monnaie='Dirham (MAD)', langues='Arabe, Français, Anglais, Allemand', meilleure_periode='طوال السنة', meilleure_periode_fr='Toute l année', meilleure_periode_en='All year round' WHERE id=6",
    "UPDATE villes SET lat=33.5217, lng=-5.1122, review_count=76, bus_duration='4h', taxi_duration='2h', voiture_duration='1h45', plats_typiques='طاجين, كسكس, جبن, لحوم', plats_typiques_fr='Tajine, Couscous, Fromage, Viandes', plats_typiques_en='Tajine, Couscous, Cheese, Meats', population='~14,000', monnaie='Dirham (MAD)', langues='Arabe, Français, Amazigh', meilleure_periode='الربيع والصيف', meilleure_periode_fr='Printemps et été', meilleure_periode_en='Spring and summer' WHERE id=7",
    "UPDATE villes SET lat=30.9203, lng=-6.8934, review_count=82, bus_duration='8h', taxi_duration='4h', voiture_duration='3h', plats_typiques='طاجين, كسكس, أطباق صحراوية', plats_typiques_fr='Tajine, Couscous, Plats sahariens', plats_typiques_en='Tajine, Couscous, Desert dishes', population='~71,000', monnaie='Dirham (MAD)', langues='Arabe, Français, Amazigh', meilleure_periode='الخريف والربيع', meilleure_periode_fr='Automne et printemps', meilleure_periode_en='Autumn and spring' WHERE id=8",
    "UPDATE villes SET lat=33.5731, lng=-7.5898, review_count=140, bus_duration='0h', taxi_duration='0h', voiture_duration='0h', plats_typiques='طاجين, كسكس, مأكولات بحرية, مأكولات عالمية', plats_typiques_fr='Tajine, Couscous, Fruits de mer, Cuisine internationale', plats_typiques_en='Tajine, Couscous, Seafood, International cuisine', population='~3,360,000', monnaie='Dirham (MAD)', langues='Arabe, Français, Anglais, Espagnol', meilleure_periode='طوال السنة', meilleure_periode_fr='Toute l année', meilleure_periode_en='All year round' WHERE id=9",
    "UPDATE villes SET lat=33.2566, lng=-8.5088, review_count=89, bus_duration='1h30', taxi_duration='45min', voiture_duration='30min', plats_typiques='مأكولات بحرية, طاجين, كسكس', plats_typiques_fr='Fruits de mer, Tajine, Couscous', plats_typiques_en='Seafood, Tajine, Couscous', population='~194,000', monnaie='Dirham (MAD)', langues='Arabe, Français, Portugais', meilleure_periode='الربيع والصيف', meilleure_periode_fr='Printemps et été', meilleure_periode_en='Spring and summer' WHERE id=10",
]
for q in update_queries:
    c.execute(q)

c.execute("""UPDATE villes SET note=4.7, rating='ممتاز', rating_fr='Excellent', rating_en='Excellent',
    atmosphere='أجواء ساحرة مليئة بالحيوية', atmosphere_fr='Ambiance enchante pleine de vie', atmosphere_en='Enchanting atmosphere full of life',
    risques='احذر النشالين في الأماكن المزدحمة', risques_fr='Attention aux pickpockets', risques_en='Beware of pickpockets',
    activites='زيارة الأسواق والقصور والمتاحف', activites_fr='Visite des souks palais et musees', activites_en='Visit souks palaces and museums',
    infos_utiles='أفضل وقت للزيارة: الربيع والخريف', infos_utiles_fr='Meilleure periode: printemps et automne', infos_utiles_en='Best time: spring and autumn',
    galerie1='https://images.unsplash.com/photo-1597212618440-806262de4f6b?w=800',
    galerie2='https://images.unsplash.com/photo-1597212618440-806262de4f6b?w=800',
    galerie3='https://images.unsplash.com/photo-1597212618440-806262de4f6b?w=800'
    WHERE id=1""")
c.execute("""UPDATE villes SET note=4.5, rating='جيد جدا', rating_fr='Tres bien', rating_en='Very good',
    atmosphere='أجواء عصرية', atmosphere_fr='Ambiance moderne', atmosphere_en='Modern atmosphere',
    risques='احذر حركة المرور', risques_fr='Attention circulation dense', risques_en='Beware heavy traffic',
    activites='زيارة المسجد والكورنيش', activites_fr='Visite mosquee et corniche', activites_en='Visit mosque and corniche',
    infos_utiles='أفضل وقت: طوال السنة', infos_utiles_fr='Toute l annee', infos_utiles_en='All year round',
    galerie1='https://images.unsplash.com/photo-1558636508-e0db3814bd1d?w=800',
    galerie2='https://images.unsplash.com/photo-1558636508-e0db3814bd1d?w=800',
    galerie3='https://images.unsplash.com/photo-1558636508-e0db3814bd1d?w=800'
    WHERE id=2""")
c.execute("""UPDATE villes SET note=4.8, rating='ممتاز', rating_fr='Excellent', rating_en='Excellent',
    atmosphere='أجواء تاريخية', atmosphere_fr='Ambiance historique', atmosphere_en='Historic atmosphere',
    risques='احذر الضياع في المدينة القديمة', risques_fr='Attention de vous perdre', risques_en='Beware getting lost',
    activites='زيارة فاس البالي والمدارس', activites_fr='Visite Fes el-Bali et medersas', activites_en='Visit Fes el-Bali and madrasas',
    infos_utiles='أفضل وقت: الربيع', infos_utiles_fr='Printemps', infos_utiles_en='Spring',
    galerie1='https://images.unsplash.com/photo-1567400358593-9eecd275fce0?w=800',
    galerie2='https://images.unsplash.com/photo-1567400358593-9eecd275fce0?w=800',
    galerie3='https://images.unsplash.com/photo-1567400358593-9eecd275fce0?w=800'
    WHERE id=3""")
c.execute("""UPDATE villes SET note=4.6, rating='جيد جدا', rating_fr='Tres bien', rating_en='Very good',
    atmosphere='أجواء البحر', atmosphere_fr='Ambiance maritime', atmosphere_en='Maritime atmosphere',
    risques='احذر الرياح القوية', risques_fr='Attention vents forts', risques_en='Beware strong winds',
    activites='زيارة كهف هرقل ومالاباطا', activites_fr='Visite Grotte Hercule Malabata', activites_en='Visit Hercules Cave Malabata',
    infos_utiles='أفضل وقت: الصيف', infos_utiles_fr='Ete', infos_utiles_en='Summer',
    galerie1='https://images.unsplash.com/photo-1559847844-5315695dadae?w=800',
    galerie2='https://images.unsplash.com/photo-1559847844-5315695dadae?w=800',
    galerie3='https://images.unsplash.com/photo-1559847844-5315695dadae?w=800'
    WHERE id=4""")
c.execute("""UPDATE villes SET note=4.9, rating='ممتاز', rating_fr='Excellent', rating_en='Excellent',
    atmosphere='أجواء استوائية', atmosphere_fr='Ambiance tropicale', atmosphere_en='Tropical atmosphere',
    risques='احذر التيارات البحرية', risques_fr='Attention courants marins', risques_en='Beware sea currents',
    activites='السباحة وركوب الأمواج', activites_fr='Natation surf plongee', activites_en='Swimming surfing diving',
    infos_utiles='طوال السنة', infos_utiles_fr='Toute l annee', infos_utiles_en='All year',
    galerie1='https://images.unsplash.com/photo-1537956965359-7573183d1f57?w=800',
    galerie2='https://images.unsplash.com/photo-1537956965359-7573183d1f57?w=800',
    galerie3='https://images.unsplash.com/photo-1537956965359-7573183d1f57?w=800'
    WHERE id=5""")
c.execute("""UPDATE villes SET note=4.9, rating='ممتاز', rating_fr='Excellent', rating_en='Excellent',
    atmosphere='أجواء هادئة', atmosphere_fr='Ambiance paisible', atmosphere_en='Peaceful atmosphere',
    risques='احذر البرد في الشتاء', risques_fr='Attention froid hiver', risques_en='Beware cold in winter',
    activites='التجول في الأزقة الزرقاء', activites_fr='Promenade ruelles bleues', activites_en='Strolling blue alleys',
    infos_utiles='أفضل وقت: الربيع والصيف', infos_utiles_fr='Printemps ete', infos_utiles_en='Spring summer',
    galerie1='https://images.unsplash.com/photo-1588279106290-911ad85b1fb8?w=800',
    galerie2='https://images.unsplash.com/photo-1588279106290-911ad85b1fb8?w=800',
    galerie3='https://images.unsplash.com/photo-1588279106290-911ad85b1fb8?w=800'
    WHERE id=6""")
c.execute("""UPDATE villes SET note=4.4, rating='جيد', rating_fr='Bien', rating_en='Good',
    atmosphere='أجواء صحراوية', atmosphere_fr='Ambiance desertique', atmosphere_en='Desert atmosphere',
    risques='احذر الحرارة المرتفعة', risques_fr='Attention fortes chaleurs', risques_en='Beware high heat',
    activites='زيارة الاستوديوهات وقصر أيت بن حدو', activites_fr='Visite studios Kasbah Ait Ben Haddou', activites_en='Visit studios Ait Ben Haddou',
    infos_utiles='أفضل وقت: الخريف والربيع', infos_utiles_fr='Automne printemps', infos_utiles_en='Autumn spring',
    galerie1='https://images.unsplash.com/photo-1547234935-80c7145ec969?w=800',
    galerie2='https://images.unsplash.com/photo-1547234935-80c7145ec969?w=800',
    galerie3='https://images.unsplash.com/photo-1547234935-80c7145ec969?w=800'
    WHERE id=7""")
c.execute("""UPDATE villes SET note=4.3, rating='جيد', rating_fr='Bien', rating_en='Good',
    atmosphere='أجواء تاريخية هادئة', atmosphere_fr='Ambiance historique calme', atmosphere_en='Quiet historic atmosphere',
    risques='احذر الأماكن المغلقة', risques_fr='Attention espaces confines', risques_en='Watch confined spaces',
    activites='زيارة باب المنصور والضريح', activites_fr='Visite Bab Mansour mausolee', activites_en='Visit Bab Mansour mausoleum',
    infos_utiles='أفضل وقت: الربيع', infos_utiles_fr='Printemps', infos_utiles_en='Spring',
    galerie1='https://images.unsplash.com/photo-1567636788276-40b696f8e0b1?w=800',
    galerie2='https://images.unsplash.com/photo-1567636788276-40b696f8e0b1?w=800',
    galerie3='https://images.unsplash.com/photo-1567636788276-40b696f8e0b1?w=800'
    WHERE id=8""")
c.execute("""UPDATE villes SET note=4.7, rating='ممتاز', rating_fr='Excellent', rating_en='Excellent',
    atmosphere='أجواء فنية', atmosphere_fr='Ambiance artistique', atmosphere_en='Artistic atmosphere',
    risques='احذر الرياح القوية', risques_fr='Attention vents forts', risques_en='Beware strong winds',
    activites='ركوب الأمواج وزيارة المدينة', activites_fr='Planche a voile visite medina', activites_en='Windsurfing visit medina',
    infos_utiles='أفضل وقت: الربيع والصيف', infos_utiles_fr='Printemps ete', infos_utiles_en='Spring summer',
    galerie1='https://images.unsplash.com/photo-1590075732028-f2e1b73b0cc3?w=800',
    galerie2='https://images.unsplash.com/photo-1590075732028-f2e1b73b0cc3?w=800',
    galerie3='https://images.unsplash.com/photo-1590075732028-f2e1b73b0cc3?w=800'
    WHERE id=9""")
c.execute("""UPDATE villes SET note=4.5, rating='جيد جدا', rating_fr='Tres bien', rating_en='Very good',
    atmosphere='أجواء أندلسية', atmosphere_fr='Ambiance andalouse', atmosphere_en='Andalusian atmosphere',
    risques='احذر التضاريس الجبلية', risques_fr='Attention terrain montagneux', risques_en='Beware mountain terrain',
    activites='زيارة المدينة القديمة والمتحف', activites_fr='Visite medina musee', activites_en='Visit medina museum',
    infos_utiles='أفضل وقت: الربيع', infos_utiles_fr='Printemps', infos_utiles_en='Spring',
    galerie1='https://images.unsplash.com/photo-1577705998148-6da4f3963bc7?w=800',
    galerie2='https://images.unsplash.com/photo-1577705998148-6da4f3963bc7?w=800',
    galerie3='https://images.unsplash.com/photo-1577705998148-6da4f3963bc7?w=800'
    WHERE id=10""")

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
    (9,'متحف محمد السادس للفن الحديث','Musee Mohammed VI d Art Moderne','Mohammed VI Museum of Modern Art','musee','أكبر متحف للفن المعاصر في المغرب','Le plus grand musee d art contemporain au Maroc','The largest museum of contemporary art in Morocco','شارع محمد الخامس، الدار البيضاء','Avenue Mohammed V, Casablanca','Avenue Mohammed V, Casablanca','50 DH','https://upload.wikimedia.org/wikipedia/commons/0/03/MMVI.JPG',4.6),
    (9,'صيدلية المركز','Pharmacie du Centre','Center Pharmacy','pharmacie','صيدلية مركزية مفتوحة 24 ساعة في قلب المدينة','Pharmacie centrale ouverte 24h/24 au coeur de la ville','Central pharmacy open 24 hours in the heart of the city','شارع أنفا، الدار البيضاء','Avenue Anfa, Casablanca','Avenue Anfa, Casablanca','-','https://images.unsplash.com/photo-1631549916768-4119b2e5f926?w=800&q=80',4.2),
    (9,'مسجد الحسن الثاني','Mosquee Hassan II','Hassan II Mosque','lieu','ثالث أكبر مسجد في العالم يطل مباشرة على المحيط الأطلسي','Troisieme plus grande mosquee du monde surplombant l Atlantique','Third largest mosque in the world overlooking the Atlantic Ocean','شاطئ الدار البيضاء','Plage de Casablanca','Casablanca Beach','120 DH','https://upload.wikimedia.org/wikipedia/commons/e/ec/Sunrise_in_Casablanca_with_Hassan_II_Mosque.jpg',5.0),
    (9,'ساحة محمد الخامس','Place Mohammed V','Mohammed V Square','lieu','أيقونة معمار الدار البيضاء بفوارتها ومبانيها الكولونيالية','Icône architecturale de Casablanca avec sa fontaine et ses bâtiments coloniaux','Architectural icon of Casablanca with its fountain and colonial buildings','وسط الدار البيضاء','Centre de Casablanca','Downtown Casablanca','مجاني','https://upload.wikimedia.org/wikipedia/commons/6/6d/Place_Mohammed_V_-_Casablanca_-_2022.jpg',4.8),
    (9,'كورنيش عين الذياب','Corniche Ain Diab','Ain Diab Corniche','lieu','أجمل كورنيش في المغرب مع مطاعم وفنادق فاخرة','La plus belle corniche du Maroc avec restaurants et hotels de luxe','The most beautiful corniche in Morocco with luxury restaurants and hotels','عين الذياب، الدار البيضاء','Ain Diab, Casablanca','Ain Diab, Casablanca','مجاني','https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80',4.7),
    (10,'مطعم لا بروش','Restaurant La Broche','Restaurant La Broche','restaurant','مطعم يقدم المأكولات البحرية الطازجة بإطلالة على المحيط','Restaurant proposant des fruits de mer frais avec vue sur l ocean','Restaurant serving fresh seafood with ocean view','الميناء، الجديدة','Port, El Jadida','Port, El Jadida','150-350 DH','https://images.unsplash.com/photo-1600891964599-f61ba0e24092?w=800&q=80',4.6),
    (10,'فندق مازاغان بيتش','Hotel Mazagan Beach','Hotel Mazagan Beach','hotel','منتجع فاخر 5 نجوم على شاطئ الجديدة بملعب غولف','Complexe de luxe 5 etoiles sur la plage d El Jadida avec golf','Luxury 5-star resort on El Jadida beach with golf course','الجديدة الشاطئ','Plage d El Jadida','El Jadida Beach','2000-6000 DH/ليلة','https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80',4.9),
    (10,'الصهريج البرتغالي','Citerne Portugaise','Portuguese Cistern','musee','صهريج تاريخي تحت الأرض من العهد البرتغالي القرن 16','Citerne historique souterraine de l epoque portugaise 16e siecle','Historic underground cistern from the Portuguese era 16th century','المدينة البرتغالية، الجديدة','Cite Portugaise, El Jadida','Portuguese City, El Jadida','10 DH','https://upload.wikimedia.org/wikipedia/commons/3/34/Portuguese_Cistern_of_El_Jadida%2C_Morocco.jpg',4.7),
    (10,'صيدلية الجديدة','Pharmacie El Jadida','El Jadida Pharmacy','pharmacie','صيدلية مركزية في شارع محمد الخامس','Pharmacie centrale sur Avenue Mohammed V','Central pharmacy on Avenue Mohammed V','شارع محمد الخامس، الجديدة','Avenue Mohammed V, El Jadida','Avenue Mohammed V, El Jadida','-','https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=800&q=80',4.1),
    (10,'المدينة البرتغالية','Cite Portugaise','Portuguese City','lieu','مدينة تاريخية مدرجة في قائمة التراث العالمي لليونسكو','Cite historique classee au patrimoine mondial de l UNESCO','Historic city listed as UNESCO World Heritage','الجديدة المدينة القديمة','Vieille Ville, El Jadida','Old City, El Jadida','مجاني','https://upload.wikimedia.org/wikipedia/commons/3/34/Portuguese_Cistern_of_El_Jadida%2C_Morocco.jpg',5.0),
    (10,'شاطئ سيدي بوزيد','Plage Sidi Bouzid','Sidi Bouzid Beach','lieu','شاطئ رملي جميل جنوب الجديدة بمياه زرقاء صافية','Belle plage de sable au sud d El Jadida aux eaux bleues cristallines','Beautiful sandy beach south of El Jadida with crystal clear blue waters','سيدي بوزيد، الجديدة','Sidi Bouzid, El Jadida','Sidi Bouzid, El Jadida','مجاني','https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80',4.8),
    (1,'قصر الباهية','Palais Bahia','Bahia Palace','lieu','قصر تاريخي من القرن 19 بأفنية رائعة وزخارف مغربية أصيلة','Palais historique du 19e siecle avec superbes cours et decorations marocaines authentiques','Historic 19th-century palace with stunning courtyards and authentic Moroccan decor','المدينة القديمة، مراكش','Medina, Marrakech','Medina, Marrakech','70 DH','https://upload.wikimedia.org/wikipedia/commons/f/fc/Bahia_Palace_large_court.jpg',4.8),
    (1,'ضريح السعديين','Tombeaux Saadiens','Saadian Tombs','lieu','مقبرة ملكية سعدية من القرن 16 بنقوش وزخارف رائعة','Necropole royale saadienne du 16e siecle aux magnifiques ornements','16th-century Saadian royal necropolis with magnificent decorations','قصر البديع، مراكش','Palais Badi, Marrakech','Badi Palace, Marrakech','70 DH','https://upload.wikimedia.org/wikipedia/commons/1/11/Saadian_Tombs%2C_Marrakech%2C_Morocco%2C_2018.jpg',4.9),
    (1,'حدائق ماجوريل','Jardins Majorelle','Majorelle Garden','lieu','حديقة نباتية ساحرة باللون الأزرق أنشأها الرسام جاك ماجوريل','Jardin botanique enchanteur bleu cree par le peintre Jacques Majorelle','Enchanting blue botanical garden created by painter Jacques Majorelle','شارع إيف سان لوران، مراكش','Rue Yves Saint Laurent, Marrakech','Yves Saint Laurent Street, Marrakech','150 DH','https://upload.wikimedia.org/wikipedia/commons/8/8c/Jardin_Majorelle_%28Marrakech%29.jpg',4.9),
    (2,'المسجد الإسباني','Mosquee Espagnole','Spanish Mosque','lieu','مسجد مهجور على قمة جبل بإطلالة بانورامية خلابة على شفشاون','Mosquee abandonnee au sommet d une montagne avec vue panoramique magnifique sur Chefchaouen','Abandoned mosque on a mountain top with breathtaking panoramic view of Chefchaouen','جبل زغو، شفشاون','Mont Zaghou, Chefchaouen','Mount Zaghou, Chefchaouen','مجاني','https://upload.wikimedia.org/wikipedia/commons/9/95/Chefchaouwen_panorama_from_spanish_mosque.jpg',4.9),
    (2,'ساحة أوطا حامام','Place Outa Hammam','Outa Hammam Square','lieu','الساحة الرئيسية في شفشاون محاطة بالمقاهي والمطاعم','Place principale de Chefchaouen entouree de cafes et restaurants','Main square of Chefchaouen surrounded by cafes and restaurants','وسط المدينة، شفشاون','Centre ville, Chefchaouen','City center, Chefchaouen','مجاني','https://upload.wikimedia.org/wikipedia/commons/8/86/Plaza_Uta_Hamam_02.jpg',4.7),
    (2,'المسجد الأعظم','Grande Mosquee','Grand Mosque','lieu','أقدم وأكبر مسجد في شفشاون بمنارة مثمنة فريدة','La plus ancienne et plus grande mosquee de Chefchaouen au minaret octogonal unique','The oldest and largest mosque in Chefchaouen with a unique octagonal minaret','ساحة أوطا حامام، شفشاون','Place Outa Hammam, Chefchaouen','Outa Hammam Square, Chefchaouen','مجاني','https://upload.wikimedia.org/wikipedia/commons/4/48/CHEFCHAOUEN_GRAND_MOSQUE_-_MOROCCO.jpg',4.6),
    (3,'المدرسة البوعنانية','Medersa Bou Inania','Bou Inania Madrasa','lieu','مدرسة قرآنية رائعة من العصر المريني بزخارف ملونة ونقوش خشبية','Magnifique medersa merinide aux decors colores et boiseries sculptees','Magnificent Marinid madrasa with colorful decorations and carved woodwork','فاس البالي','Fes el-Bali','Fes el-Bali','30 DH','https://upload.wikimedia.org/wikipedia/commons/b/b8/Main_courtyard_of_Bou_Inania_Madrasa%2C_Fez%2C_Marocco.jpg',4.9),
    (3,'القصر الملكي','Palais Royal','Royal Palace','lieu','القصر الملكي لفاس ببوابات ذهبية رائعة وهندسة معمارية ملكية','Palais Royal de Fes aux superbes portes dorees et architecture royale','Royal Palace of Fes with stunning golden gates and royal architecture','فاس الجديد','Fes el-Jdid','Fes el-Jdid','مجاني','https://upload.wikimedia.org/wikipedia/commons/b/b2/Morocco_Fez_Royal_Palace.JPG',4.7),
    (3,'مدرسة العطارين','Medersa Attarine','Attarine Madrasa','lieu','مدرسة تاريخية من القرن 14 تتميز بالزليج والزخارف الإسلامية','Medersa historique du 14e siecle caracterisee par son zellij et ses decors islamiques','Historic 14th-century madrasa featuring zellij and Islamic decorations','قرب جامعة القرويين، فاس','Pres d Al Quaraouiyine, Fes','Near Al Quaraouiyine, Fes','20 DH','https://upload.wikimedia.org/wikipedia/commons/a/a5/M%C3%A9dersa_Attarine.jpg',4.8),
    (4,'قرية خملية','Village Khamlia','Khamlia Village','lieu','قرية صحراوية تعرف بموسيقى كناوة التقليدية والضيافة','Village desertique connue pour sa musique gnaouie traditionnelle et son hospitalite','Desert village known for traditional Gnaoua music and hospitality','مرزوكة الجنوب','Sud de Merzouga','South of Merzouga','مجاني','https://upload.wikimedia.org/wikipedia/commons/2/2b/Khamlia_village.jpg',4.6),
    (4,'مناجم الحفريات','Mines de Fossiles','Fossil Mines','lieu','مناجم أحفوريات تعود لملايين السنين يستخرج منها الأسماك والديناصورات','Mines de fossiles vieilles de millions d annees ou sont extraits poissons et dinosaures','Fossil mines millions of years old where fish and dinosaur fossils are extracted','ضواحي مرزوكة','Environs de Merzouga','Merzouga outskirts','100 DH','https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=800&q=80',4.5),
    (4,'بحيرة داية السرجي','Lac Dayet Srji','Lake Dayet Srji','lieu','بحيرة موسمية بين الكثبان الرملية تجذب الطيور المهاجرة','Lac saisonnier entre les dunes attirant les oiseaux migrateurs','Seasonal lake between the dunes attracting migratory birds','قرب مرزوكة','Pres de Merzouga','Near Merzouga','مجاني','https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=800&q=80',4.4),
    (5,'ميناء الصويرة','Port d Essaouira','Essaouira Port','lieu','ميناء تاريخي مع قوارب الصيد الزرقاء وسقالة الميناء','Port historique avec bateaux de peche bleus et sqala du port','Historic port with blue fishing boats and port sqala','الميناء، الصويرة','Port, Essaouira','Port, Essaouira','مجاني','https://upload.wikimedia.org/wikipedia/commons/d/d0/Essaouira_port%2C_Morocco.jpg',4.8),
    (5,'شاطئ الصويرة','Plage d Essaouira','Essaouira Beach','lieu','شاطئ رملي طويل مع أمواج مثالية لركوب الأمواج','Longue plage de sable avec vagues ideales pour le surf','Long sandy beach with perfect waves for surfing','الصويرة الشاطئ','Plage d Essaouira','Essaouira Beach','مجاني','https://upload.wikimedia.org/wikipedia/commons/7/7b/Beach_and_surfers%2C_Essaouira%2C_Morocco.jpg',4.7),
    (5,'ساحة مولاي الحسن','Place Moulay Hassan','Moulay Hassan Square','lieu','ساحة رئيسية تصطف على جانبيها المقاهي والمطاعم مقابل الميناء','Place principale bordee de cafes et restaurants face au port','Main square lined with cafes and restaurants facing the port','وسط الصويرة','Centre d Essaouira','Central Essaouira','مجاني','https://upload.wikimedia.org/wikipedia/commons/e/e5/Place_Moulay_Hassan_-_Esaoura_907.jpg',4.7),
    (6,'قصبة أكادير أوفلا','Kasbah d Agadir Oufella','Agadir Oufella Kasbah','lieu','أطلال قصبة تاريخية تطل على خليج أكادير بمناظر بانورامية','Ruines d une kasbah historique surplombant la baie d Agadir avec vues panoramiques','Ruins of a historic kasbah overlooking Agadir bay with panoramic views','أكادير أوفلا','Agadir Oufella','Agadir Oufella','مجاني','https://upload.wikimedia.org/wikipedia/commons/4/43/Agadir_-_Kasbah_of_Agadir_-_20240925193718.jpeg',4.6),
    (6,'سوق الحاج','Souk El Had','Souk El Had','lieu','أكبر سوق شعبي في أكادير بتشكيلة واسعة من المنتجات المحلية','Le plus grand marche populaire d Agadir avec large choix de produits locaux','The largest popular market in Agadir with a wide range of local products','أكادير المركز','Centre d Agadir','Agadir Center','مجاني','https://upload.wikimedia.org/wikipedia/commons/d/df/Agadir_Souk_Al_Had.jpg',4.5),
    (6,'مارينا أكادير','Marina d Agadir','Agadir Marina','lieu','مارينا حديثة مع يخوت فاخرة ومطاعم ومقاهي عالمية','Marina moderne avec yachts de luxe restaurants et cafes internationaux','Modern marina with luxury yachts international restaurants and cafes','شاطئ أكادير','Plage d Agadir','Agadir Beach','مجاني','https://upload.wikimedia.org/wikipedia/commons/d/d4/Sailing_ship_for_tourism_in_Agadir_Marina_By_AmlouMed.jpg',4.7),
    (7,'تمثال الأسد','Statue du Lion','Lion Statue','lieu','تمثال الأسد الشهير رمز مدينة إفران وسط الغابات','La celebre statue du lion symbole de la ville d Ifrane au milieu des forets','The famous lion statue symbol of Ifrane city surrounded by forests','وسط إفران','Centre d Ifrane','Center of Ifrane','مجاني','https://upload.wikimedia.org/wikipedia/commons/e/e0/Ifrane_lion.jpg',4.6),
    (7,'جامعة الأخوين','Universite Al Akhawayn','Al Akhawayn University','lieu','جامعة دولية مرموقة بهندسة معمارية مغربية عصرية','Universite internationale de renom a l architecture marocaine moderne','Prestigious international university with modern Moroccan architecture','إفران','Ifrane','Ifrane','مجاني','https://upload.wikimedia.org/wikipedia/commons/4/4d/Al_Akhawayn_Campus.jpg',4.5),
    (7,'بحيرة دايت عوا','Lac Dayet Aoua','Lake Dayet Aoua','lieu','بحيرة طبيعية محاطة بغابات الأرز ومنتزه وطني','Lac naturel entoure de forets de cedres et parc national','Natural lake surrounded by cedar forests and national park','15 كم من إفران','15 km d Ifrane','15 km from Ifrane','مجاني','https://upload.wikimedia.org/wikipedia/commons/1/1c/Dayet_Aoua%2C_Ifrane_national_park.jpg',4.7),
    (8,'قصبة توريرت','Kasbah Taourirt','Taourirt Kasbah','lieu','قصبة تاريخية من القرن 17 في قلب ورزازات','Kasbah historique du 17e siecle au coeur de Ouarzazate','Historic 17th-century kasbah in the heart of Ouarzazate','وسط ورزازات','Centre de Ouarzazate','Center of Ouarzazate','20 DH','https://upload.wikimedia.org/wikipedia/commons/0/0f/Kasbah_Taourirt_in_Ouarzazate_2011.jpg',4.7),
    (8,'استوديوهات أطلس','Studios Atlas','Atlas Film Studios','lieu','أكبر استوديو سينمائي في العالم صورت فيه أشهر الأفلام','Le plus grand studio de cinema au monde ou ont ete tournes les films les plus celebres','The largest film studio in the world where famous movies were filmed','ورزازات','Ouarzazate','Ouarzazate','50 DH','https://upload.wikimedia.org/wikipedia/commons/5/5f/Atlas_Film_Studios_Ouarzazate_Morocco.JPG',4.6),
    (8,'واحة فينت','Oasis Fint','Fint Oasis','lieu','واحة خضراء جميلة بوادي فينت على بعد 15 كم من ورزازات','Belle oasis verte dans la vallee de Fint a 15 km de Ouarzazate','Beautiful green oasis in the Fint valley 15 km from Ouarzazate','وادي فينت، ورزازات','Vallee de Fint, Ouarzazate','Fint Valley, Ouarzazate','مجاني','https://upload.wikimedia.org/wikipedia/commons/6/64/Fint1.JPG',4.5),
    (9,'حي الأحباس','Quartier Habous','Habous District','lieu','حي تاريخي جميل يجمع بين الطراز المغربي والأندلسي','Quartier historique alliant style marocain et andalou','Beautiful historic district blending Moroccan and Andalusian style','الأحباس، الدار البيضاء','Habous, Casablanca','Habous, Casablanca','مجاني','https://upload.wikimedia.org/wikipedia/commons/c/cb/One_of_the_most_instragmable_views_of_the_old_medina_the_habous_in_Casablanca.jpg',4.6),
    (9,'كورنيش الدار البيضاء','Corniche de Casablanca','Casablanca Corniche','lieu','كورنيش عصري بطول 5 كيلومترات مع مطاعم وفنادق وشاطئ','Corniche moderne de 5 km avec restaurants hotels et plage','Modern 5 km corniche with restaurants hotels and beach','عين الذياب، الدار البيضاء','Ain Diab, Casablanca','Ain Diab, Casablanca','مجاني','https://upload.wikimedia.org/wikipedia/commons/4/4d/Corniche%2C_Casablanca.jpg',4.7),
    (9,'ساحة محمد الخامس','Place Mohammed V','Mohammed V Square','lieu','ساحة مركزية أيقونية بنافورة كبيرة ومباني كولونيالية فخمة','Place centrale iconique avec grande fontaine et imposants batiments coloniaux','Iconic central square with large fountain and grand colonial buildings','وسط الدار البيضاء','Centre de Casablanca','Downtown Casablanca','مجاني','https://upload.wikimedia.org/wikipedia/commons/6/6d/Place_Mohammed_V_-_Casablanca_-_2022.jpg',4.8),
    (10,'كنيسة الانتقال','Eglise de l Assomption','Church of the Assumption','lieu','كنيسة برتغالية جميلة من القرن 16 في قلب المدينة البرتغالية','Belle eglise portugaise du 16e siecle au coeur de la cite portugaise','Beautiful 16th-century Portuguese church in the heart of the Portuguese city','المدينة البرتغالية، الجديدة','Cite Portugaise, El Jadida','Portuguese City, El Jadida','مجاني','https://upload.wikimedia.org/wikipedia/commons/f/f0/El_Jadida%2C_Morocco_%F0%9F%87%B2%F0%9F%87%A6_-_Church_of_the_Assumption_Oct_2023.jpg',4.5),
    (10,'ميناء الجديدة','Port d El Jadida','El Jadida Port','lieu','ميناء الصيد البحري للجديدة بقوارب زرقاء ومطاعم سمك','Port de peche d El Jadida aux bateaux bleus et restaurants de poisson','Fishing port of El Jadida with blue boats and fish restaurants','الميناء، الجديدة','Port, El Jadida','Port, El Jadida','مجاني','https://upload.wikimedia.org/wikipedia/commons/c/c0/Port_EL_Jadida.jpg',4.6),
    (10,'منار سيدي بوعافي','Phare Sidi Bou Afi','Sidi Bou Afi Lighthouse','lieu','منارة تاريخية على الساحل الأطلسي توفر إطلالة رائعة على المحيط','Phare historique sur la cote atlantique offrant une vue magnifique sur l ocean','Historic lighthouse on the Atlantic coast with a magnificent ocean view','سيدي بوعافي، الجديدة','Sidi Bou Afi, El Jadida','Sidi Bou Afi, El Jadida','مجاني','https://upload.wikimedia.org/wikipedia/commons/2/2e/Sidi_Bou_Afi_8BCV1513.jpg',4.5),
]
c.executemany("INSERT INTO attractions (ville_id, nom, nom_fr, nom_en, categorie, description, description_fr, description_en, adresse, adresse_fr, adresse_en, prix, image, note) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", attractions)

menu_items = [
    (1,'Tajine de poulet','طاجين الدجاج','Chicken Tajine','90 DH','Tajine de poulet aux olives et citron confit','طاجين الدجاج بالزيتون والليمون المخلل','Chicken tajine with olives and preserved lemon'),
    (1,'Couscous royal','الكسكس الملكي','Royal Couscous','120 DH','Couscous aux legumes et viande','الكسكس بالخضار واللحم','Couscous with vegetables and meat'),
    (1,'Pastilla marocaine','البستيلة المغربية','Moroccan Pastilla','110 DH','Pastilla au poulet et amandes','بستيلة الدجاج واللوز','Chicken and almond pastilla'),
    (1,'The a la menthe','الشاي بالنعناع','Mint Tea','25 DH','The vert a la menthe fraiche','الشاي الأخضر بالنعناع الطازج','Green tea with fresh mint'),
    (2,'Salade marocaine','السلطة المغربية','Moroccan Salad','55 DH','Salade de tomates et poivrons','سلطة الطماطم والفلفل','Tomato and bell pepper salad'),
    (2,"Tajine d'agneau",'طاجين الخروف','Lamb Tajine','130 DH',"Tajine d'agneau aux pruneaux",'طاجين الخروف بالبرقوق','Lamb tajine with prunes'),
    (2,'Briouates','البريوات','Briouates','70 DH','Feuillettes au fromage et epinards','البريوات بالجبن والسبانخ','Cheese and spinach briouates'),
    (2,"Jus d'orange",'عصير البرتقال','Orange Juice','30 DH',"Jus d'orange frais presse",'عصير برتقال طازج','Fresh squeezed orange juice'),
    (11,'Couscous poulet','كسكس الدجاج','Chicken Couscous','90 DH','Couscous au poulet et legumes','كسكس بالدجاج والخضار','Couscous with chicken and vegetables'),
    (11,'Harira','الحريرة','Harira','45 DH','Soupe marocaine traditionnelle','الحريرة المغربية التقليدية','Traditional Moroccan soup'),
    (11,'Brochette kefta','كفتة المشواة','Kefta Brochette','80 DH','Brochette de viande hachee','أسياخ الكفتة المشوية','Grilled kefta skewers'),
    (11,'Lben','اللبن','Lben','15 DH','Lait fermente traditionnel','اللبن المخمر التقليدي','Traditional fermented milk'),
]
c.executemany("INSERT INTO menu_items (attraction_id, nom_item, nom_item_ar, nom_item_en, prix, description, description_ar, description_en) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", menu_items)

hotel_rooms = [
    (3,'Suite Royale','الجناح الملكي','Royal Suite','15000 DH','Suite presidentielle avec terrasse privee','جناح رئاسي مع شرفة خاصة','Presidential suite with private terrace',4),
    (3,'Suite Deluxe','جناح ديلوكس','Deluxe Suite','8000 DH','Suite spacieuse avec salon separe','جناح واسع مع صالون منفصل','Spacious suite with separate living room',3),
    (3,'Chambre Premium','غرفة بريميوم','Premium Room','5000 DH','Chambre luxueuse avec vue jardin','غرفة فاخرة مع إطلالة على الحديقة','Luxury room with garden view',2),
    (3,'Chambre Classique','غرفة كلاسيكية','Classic Room','3000 DH','Chambre confortable et elegante','غرفة مريحة وأنيقة','Comfortable and elegant room',2),
    (4,'Suite Riad','جناح الرياض','Riad Suite','2000 DH','Suite avec patio prive et fontaine','جناح مع فناء خاص ونافورة','Suite with private patio and fountain',3),
    (4,'Chambre Double','غرفة مزدوجة','Double Room','1200 DH','Chambre double typiquement marocaine','غرفة مزدوجة مغربية أصيلة','Authentic Moroccan double room',2),
    (4,'Chambre Simple','غرفة مفردة','Single Room','800 DH','Chambre simple avec petit-dejeuner','غرفة مفردة مع الفطور','Single room with breakfast',1),
    (12,'Suite Panorama','جناح بانوراما','Panorama Suite','1500 DH','Suite avec vue panoramique sur la ville bleue','جناح مع إطلالة بانورامية على المدينة الزرقاء','Suite with panoramic view of the blue city',3),
    (12,'Chambre Double Vue','غرفة مزدوجة مع إطلالة','Double Room with View','1000 DH','Chambre double avec vue sur les montagnes','غرفة مزدوجة مع إطلالة على الجبال','Double room with mountain view',2),
    (12,'Chambre Standard','غرفة قياسية','Standard Room','600 DH','Chambre standard confortable','غرفة قياسية مريحة','Comfortable standard room',2),
]
c.executemany("INSERT INTO hotel_rooms (attraction_id, type_chambre, type_chambre_ar, type_chambre_en, prix, description, description_ar, description_en, capacite) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", hotel_rooms)

guides = [
    ('Youssef','يوسف','Youssef',1,'Histoire et culture','تاريخ وثقافة','History and culture','300 DH','0612345678','https://i.pravatar.cc/150?u=youssef'),
    ('Fatima','فاطمة','Fatima',2,'Architecture','عمارة','Architecture','250 DH','0612345679','https://i.pravatar.cc/150?u=fatima'),
    ('Mohamed','محمد','Mohamed',3,'Arts traditionnels','فنون تقليدية','Traditional arts','280 DH','0612345680','https://i.pravatar.cc/150?u=mohamed'),
    ('Sara','سارة','Sara',4,'Histoire','تاريخ','History','260 DH','0612345681','https://i.pravatar.cc/150?u=sara'),
    ('Hassan','حسن','Hassan',5,'Sports nautiques','رياضات مائية','Water sports','270 DH','0612345682','https://i.pravatar.cc/150?u=hassan'),
    ('Noura','نورة','Noura',6,'Nature','طبيعة','Nature','240 DH','0612345683','https://i.pravatar.cc/150?u=noura'),
    ('Omar','عمر','Omar',7,'Culture desertique','ثقافة صحراوية','Desert culture','320 DH','0612345684','https://i.pravatar.cc/150?u=omar'),
    ('Laila','ليلى','Laila',8,'Histoire islamique','تاريخ إسلامي','Islamic history','260 DH','0612345685','https://i.pravatar.cc/150?u=laila'),
    ('Karim','كريم','Karim',9,'Arts','فنون','Arts','270 DH','0612345686','https://i.pravatar.cc/150?u=karim'),
    ('Mariam','مريم','Mariam',10,'Patrimoine','تراث','Heritage','250 DH','0612345687','https://i.pravatar.cc/150?u=mariam'),
]
c.executemany("INSERT INTO guides (nom, nom_ar, nom_en, ville_id, specialite, specialite_ar, specialite_en, prix, telephone, image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", guides)

db.commit()
c.close()
db.close()
print('Database created successfully!')
