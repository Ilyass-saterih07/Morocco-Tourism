# migrate_db.py - adds new columns and tables to existing database without data loss
import mysql.connector

db = mysql.connector.connect(host='localhost', user='root', password='', charset='utf8mb4', database='tourism_dinner')
c = db.cursor()

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
        print(f'OK: {q[:50]}...')
    except mysql.connector.Error as e:
        if 'Duplicate column' in str(e):
            print(f'SKIP (exists): {q[:50]}...')
        else:
            print(f'ERR: {e}')

c.execute("""
    CREATE TABLE IF NOT EXISTS ville_prix_hebergement (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ville_id INT NOT NULL,
        type_hebergement VARCHAR(50) NOT NULL,
        prix_par_nuit DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (ville_id) REFERENCES villes(id) ON DELETE CASCADE
    )
""")
print('OK: ville_prix_hebergement table')

c.execute("""
    CREATE TABLE IF NOT EXISTS avis (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ville_id INT NOT NULL,
        auteur VARCHAR(100) NOT NULL,
        note DECIMAL(2,1) NOT NULL,
        commentaire TEXT,
        date_post DATE DEFAULT (CURRENT_DATE),
        FOREIGN KEY (ville_id) REFERENCES villes(id) ON DELETE CASCADE
    )
""")
print('OK: avis table')

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
print('OK: ville data updated')

# seed prix_hebergement
c.execute("SELECT COUNT(*) FROM ville_prix_hebergement")
if c.fetchone()[0] == 0:
    prix_data = [
        (1, 'hotel', 600), (1, 'riad', 800), (1, 'auberge', 300), (1, 'camp', 200),
        (2, 'hotel', 400), (2, 'riad', 550), (2, 'auberge', 200), (2, 'camp', 150),
        (3, 'hotel', 500), (3, 'riad', 700), (3, 'auberge', 250), (3, 'camp', 180),
        (4, 'hotel', 350), (4, 'riad', 500), (4, 'auberge', 180), (4, 'camp', 250),
        (5, 'hotel', 450), (5, 'riad', 600), (5, 'auberge', 220), (5, 'camp', 160),
        (6, 'hotel', 550), (6, 'riad', 750), (6, 'auberge', 280), (6, 'camp', 200),
        (7, 'hotel', 350), (7, 'riad', 500), (7, 'auberge', 180), (7, 'camp', 120),
        (8, 'hotel', 400), (8, 'riad', 550), (8, 'auberge', 200), (8, 'camp', 250),
        (9, 'hotel', 700), (9, 'riad', 900), (9, 'auberge', 350), (9, 'camp', 250),
        (10, 'hotel', 350), (10, 'riad', 500), (10, 'auberge', 180), (10, 'camp', 120),
    ]
    c.executemany("INSERT INTO ville_prix_hebergement (ville_id, type_hebergement, prix_par_nuit) VALUES (%s,%s,%s)", prix_data)
    print('OK: prix_hebergement seeded')

# seed avis
c.execute("SELECT COUNT(*) FROM avis")
if c.fetchone()[0] == 0:
    avis_data = [
        (1, 'Ahmed R.', 4.5, 'Superbe séjour, je recommande.'), (1, 'John D.', 4.8, 'Un voyage inoubliable.'),
        (2, 'Marie L.', 5.0, 'La ville bleue est un rêve !'), (2, 'Hassan T.', 4.7, 'Endroit paisible et magnifique.'),
        (3, 'Fatima Z.', 4.9, 'Fes est un musée à ciel ouvert.'), (3, 'Pierre A.', 4.6, 'Histoire et culture exceptionnelles.'),
        (4, 'Youssef K.', 5.0, 'Le désert est magique, surtout au coucher du soleil.'),
        (5, 'Leila B.', 4.8, 'Essaouira, ville du vent et de l art.'),
        (6, 'Karim S.', 4.7, 'Plage magnifique, soleil garanti.'),
        (7, 'Nadia A.', 4.5, 'Ifrane, la petite Suisse du Maroc.'),
        (8, 'Omar J.', 4.6, 'Les studios de cinéma valent le détour.'),
        (9, 'Hind M.', 4.9, 'Casablanca une ville moderne et accueillante.'),
        (10, 'Samir D.', 4.7, 'El Jadida, un joyau portugais au Maroc.'),
    ]
    c.executemany("INSERT INTO avis (ville_id, auteur, note, commentaire) VALUES (%s,%s,%s,%s)", avis_data)
    print('OK: avis seeded')

db.commit()
c.close()
db.close()
print('Migration complete!')
