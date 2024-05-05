import sqlite3

# Veritabanı bağlantısı oluşturma veya mevcut bir veritabanına bağlanma
conn = sqlite3.connect('gezginGemi.db')
c = conn.cursor()
c.execute('''PRAGMA foreign_keys=ON''')

# HARBOR tablosunu oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS HARBOR(
            H_NAME TEXT NOT NULL,
            H_COUNTRY TEXT NOT NULL,
            H_POPULATION INTEGER NOT NULL,
            H_PASSPORT TEXT NOT NULL,
            H_FEE INTEGER NOT NULL,
            PRIMARY KEY (H_NAME, H_COUNTRY),
            CONSTRAINT H_NAME_H_COUNTRY UNIQUE(H_NAME,H_COUNTRY))''')

# SHIP tablosunu oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS SHIP(
            S_SERIAL_NUM INTEGER PRIMARY KEY NOT NULL UNIQUE,
            S_TYPE TEXT NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS CRUISE_SHIP(
            S_SERIAL_NUM INTEGER PRIMARY KEY NOT NULL UNIQUE,
            S_NAME TEXT NOT NULL,
            S_TONNAGE INTEGER NOT NULL,
            S_MADE_IN DATE NOT NULL,
            S_CAPACITY INTEGER NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS OIL_SHIP(
            S_SERIAL_NUM INTEGER PRIMARY KEY NOT NULL UNIQUE,
            S_NAME TEXT NOT NULL,
            S_TONNAGE INTEGER NOT NULL,
            S_MADE_IN DATE NOT NULL,
            S_OIL_CAPACITY INTEGER NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS CONTAINER_SHIP(
            S_SERIAL_NUM INTEGER PRIMARY KEY NOT NULL UNIQUE,
            S_NAME TEXT NOT NULL,
            S_TONNAGE INTEGER NOT NULL,
            S_MADE_IN DATE NOT NULL,
            S_CONTAINER_AMOUNT INTEGER NOT NULL,
            S_MAX_CAPACITY INTEGER NOT NULL)''')

# VISITED_HARBORS tablosunu oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS VISITED_HARBORS(
            H_NAME TEXT NOT NULL,
            H_COUNTRY TEXT NOT NULL,
            S_SERIAL_NUM INTEGER NOT NULL,
            VH_STATE TEXT NOT NULL,
            PRIMARY KEY (H_NAME, H_COUNTRY, S_SERIAL_NUM),
            FOREIGN KEY (H_NAME, H_COUNTRY) REFERENCES HARBOR(H_NAME, H_COUNTRY) ON UPDATE CASCADE,
            FOREIGN KEY (S_SERIAL_NUM) REFERENCES SHIP(S_SERIAL_NUM),
            CONSTRAINT HARBOR_CHECK UNIQUE(H_NAME, H_COUNTRY, S_SERIAL_NUM))''')

# EXPEDITIONS tablosunu oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS EXPEDITIONS(
            EMP_ID INTEGER NOT NULL,
            S_SERIAL_NUM INTEGER NOT NULL,
            E_START_DATE DATE NOT NULL,
            E_RETURN_DATE DATE NOT NULL,
            E_START_HARBOR TEXT NOT NULL,
            E_START_COUNTRY TEXT NOT NULL,
            E_CAP INTEGER NOT NULL,
            E_CREW INTEGER NOT NULL,
            FOREIGN KEY (E_START_HARBOR, E_START_COUNTRY) REFERENCES HARBOR(H_NAME, H_COUNTRY) ON UPDATE CASCADE,
            FOREIGN KEY (S_SERIAL_NUM) REFERENCES SHIP(S_SERIAL_NUM),
            FOREIGN KEY (EMP_ID) REFERENCES EMPLOYEE(EMP_ID),
            CONSTRAINT EMP_CHECK UNIQUE(EMP_ID, S_SERIAL_NUM, E_START_DATE, E_START_HARBOR, E_START_COUNTRY),
            CONSTRAINT DATE_CHECK UNIQUE(S_SERIAL_NUM, E_START_DATE, E_START_HARBOR, E_START_COUNTRY),
            CONSTRAINT COUNT_CHECK CHECK(E_CAP >= 2), CHECK(E_CREW >= 1),
            PRIMARY KEY (S_SERIAL_NUM, E_START_DATE))''')

# EMPLOYEE tablosunu oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS EMPLOYEE(
            EMP_ID INTEGER PRIMARY KEY NOT NULL UNIQUE,
            EMP_JOB TEXT NOT NULL)''')

# CAPTAIN tablosunu oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS CAPTAIN(
            EMP_ID INTEGER PRIMARY KEY NOT NULL UNIQUE,
            CAP_LICENSE DATE NOT NULL,
            CAP_NAME TEXT NOT NULL,
            CAP_LNAME TEXT NOT NULL,
            CAP_ADRESS TEXT NOT NULL,
            CAP_CITIZENSHIP TEXT NOT NULL,
            CAP_BIRTH_DATE DATE NOT NULL,
            CAP_START_DATE DATE NOT NULL,
            CAP_SHIP INTEGER NOT NULL,
            FOREIGN KEY (CAP_SHIP) REFERENCES EXPEDITIONS(S_SERIAL_NUM),
            FOREIGN KEY (EMP_ID) REFERENCES EMPLOYEE(EMP_ID) ON UPDATE CASCADE)''')

# CREW tablosunu oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS CREW(
            EMP_ID INTEGER PRIMARY KEY NOT NULL UNIQUE,
            CREW_NAME TEXT NOT NULL,
            CREW_LNAME TEXT NOT NULL,
            CREW_ADRESS TEXT NOT NULL,
            CREW_CITIZENSHIP TEXT NOT NULL,
            CREW_BIRTH_DATE DATE NOT NULL,
            CREW_START_DATE DATE NOT NULL,
            CREW_DUTY TEXT NOT NULL,
            CREW_SHIP INTEGER NOT NULL,
            FOREIGN KEY (CREW_SHIP) REFERENCES EXPEDITIONS(S_SERIAL_NUM), 
            FOREIGN KEY (EMP_ID) REFERENCES EMPLOYEE(EMP_ID) ON UPDATE CASCADE)''')

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()