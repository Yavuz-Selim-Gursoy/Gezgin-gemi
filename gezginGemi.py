import tkinter as tk
import sqlite3 as sql
import random as rnd
import runpy
import os

if "gezginGemi.db" not in os.listdir(os.getcwd()):
    runpy.run_path("query.py")
    # Eğer database halihazırda oluşturulmuşsa, tekrar oluşturmak yerine database'e bağlan.
    # Oluşturulmamışsa "query.py" dosyasındaki query'i çalıştır ve bir database oluştur.


# Gemi sınıfı. (kullanıcı erişemez)
class SHIP:
    def __init__(self, serialNum, name, grossTonnage, madeIn):
        self.serialNum = serialNum
        self.name = name
        self.grossTonnage = grossTonnage
        self.madeIn = madeIn


# Yolcu Gemisi sınıfı.
class CRUISE_SHIP(SHIP):
    def __init__(self, serialNum, name, grossTonnage, madeIn, capacity):
        super().__init__(serialNum, name, grossTonnage, madeIn)
        self.capacity = capacity
        self.type = 'CRUISE'


# Petrol Gemisi sınıfı.
class OIL_SHIP(SHIP):
    def __init__(self, serialNum, name, grossTonnage, madeIn, oilCapacity):
        super().__init__(serialNum, name, grossTonnage, madeIn)
        self.oilCapacity = oilCapacity
        self.type = 'OIL'


# Konteyner Gemisi sınıfı.
class CONTAINER_SHIP(SHIP):
    def __init__(self, serialNum, name, grossTonnage, madeIn, containerCapacity, maxCapacity):
        super().__init__(serialNum, name, grossTonnage, madeIn)
        self.containerCapacity = containerCapacity
        self.maxCapacity = maxCapacity
        self.type = 'CONTAINER'


# Yolculuklar sınıfı.
class EXPEDITIONS:
    def __init__(self, emp_ID, s_Serial, startDate, returnDate, harborName, harborCountry, numOfCaptains, numOfCrews):
        self.emp_ID = emp_ID
        self.s_Serial = s_Serial
        self.startDate = startDate
        self.returnDate = returnDate
        self.harborName = harborName
        self.harborCountry = harborCountry
        self.numOfCaptains = numOfCaptains
        self.numOfCrews = numOfCrews


# Liman sınıfı.
class HARBOR:
    def __init__(self, name, country, population, passportNeeded, fee):
        self.name = name
        self.country = country
        self.population = int(population)
        self.passportNeeded = passportNeeded
        self.fee = int(fee)


# Ziyaret Edilen Limanlar sınıfı.
class VISITED_HARBORS:
    def __init__(self, name, country, s_Serial, visitState):
        self.name = name
        self.country = country
        self.s_Serial = s_Serial
        self.visitState = visitState


# Çalışan sınıfı. (kullanıcı erişemez)
class EMPLOYEE:
    def __init__(self, ID, job):
        self.ID = ID
        self.job = job


# Kaptan sınıfı.
class CAPTAIN(EMPLOYEE):
    def __init__(self, ID, license, name, lname, adress, citizenship, birthDate, startDate, ship):
        super().__init__(ID, 'CAPTAIN')
        self.license = license
        self.name = name
        self.lname = lname
        self.adress = adress
        self.citizenship = citizenship
        self.birthDate = birthDate
        self.startDate = startDate
        self.ship = ship


# Mürettebat sınıfı.
class CREW(EMPLOYEE):
    def __init__(self, ID, name, lname, adress, citizenship, birthDate, startDate, duty, ship):
        super().__init__(ID, 'CREW')
        self.name = name
        self.lname = lname
        self.adress = adress
        self.citizenship = citizenship
        self.birthDate = birthDate
        self.startDate = startDate
        self.duty = duty
        self.ship = ship




def _repeats(list1, list2):
    '''Eğer birinci liste ikinci listenin içinde geçiyorsa True, geçmiyorsa False döndürür.'''
    replicated = list()
    replicated += list1

    for i in list1:
        if i in list2:
            replicated.remove(i)

        else:
            continue

    if len(replicated) > 0:
        return False

    else:
        return True




def _construct_main_menu():
    button = tk.Button(text="Kapat", bg="grey35", fg="white", command=root.destroy, padx=15, pady=2)
    button.place(x=30, y=290)

    button = tk.Button(text="Tablo Görüntüle", bg="grey35", fg="white", command=lambda: _construct_menu(3), padx=15,
                       pady=2)
    button.place(x=30, y=230)

    button = tk.Button(text="Kayıt Güncelle", bg="grey35", fg="white", command=lambda: _construct_menu(2), padx=15,
                       pady=2)
    button.place(x=30, y=170)

    button = tk.Button(text="Kayıt Sil", bg="grey35", fg="white", command=lambda: _construct_menu(1), padx=15, pady=2)
    button.place(x=30, y=110)

    button = tk.Button(text="Kayıt Ekle", bg="grey35", fg="white", command=lambda: _construct_menu(0), padx=15, pady=2)
    button.place(x=30, y=50)

    text = tk.Text(root, height=20, width=50, bg="grey75", fg="black")
    text.place(x=200, y=30)

    msg = tk.Message(root, bg="grey20", fg="white", text=f"{choice} tablosunun önizlemesi:",
                     width=500, font=("Calibri", 11))
    msg.place(x=200, y=2)

    outputList = c.fetchall()
    for i in outputList:
        text.insert(tk.END, str(i) + "\n")
    text.config(state=tk.DISABLED)
    # Ana menüyü oluştur ve metin kutusunu rastgele seçilen tablonun önizlemesini yerleştirdikten sonra değiştirilemez hale getir.

def _handle_input(textBox, sampleTable, action, classType, c):
    inputText = textBox.get(1.0, tk.END)
    textBox.delete(1.0, tk.END)
    # Menüdeki text box kısmını temizle.

    outputStr = str()
    splittedOnce = list()
    sampleAttrs = list()

    for i in inputText:
        if i == '\n':
            continue
        else:
            outputStr += i
        splittedOnce = outputStr.split(';')

    for x in splittedOnce:
        sampleAttrs += x.split(',')
    # Girilen değerleri virgülle ayır.

    actionCaseList = [insert_sample, delete_sample, update_sample, display_table]

    for index, case in enumerate(actionCaseList):
        if index == action and (index == 0 or index == 1):
            return case(sampleTable, sampleAttrs, classType, c)

        elif index == action and index == 2:
            return case(sampleTable, sampleAttrs, c)

        elif index == action and index == 3:
            return case(sampleTable)
    # Tıklanılan butona göre ikincil menüyü aç ve virgülle ayrılan değerleri fonksiyonlara yolla.

def _construct_menu(action):
    actionList = ["Kayıt ekle", "Kayıt sil", "Kayıt güncelle", "Tablo görüntüle"]
    enumerate(actionList)

    newWindow = tk.Toplevel(root)
    newWindow.title(f'{actionList[action]}')
    newWindow.resizable(False, False)
    newWindow.grab_set()
    newWindow.geometry('640x380')

    text = tk.Text(newWindow, height=20, width=40, bg="grey75", fg="black")
    text.place(x=290, y=20)

    button = tk.Button(newWindow, text="Kaptan", bg="grey35", fg="white",
                       command=lambda: _handle_input(text, "CAPTAIN", action, CAPTAIN, c), padx=15, pady=2)
    button.place(x=30, y=50)

    button = tk.Button(newWindow, text="Mürettebat", bg="grey35", fg="white",
                       command=lambda: _handle_input(text, "CREW", action, CREW, c), padx=15, pady=2)
    button.place(x=30, y=110)

    button = tk.Button(newWindow, text="Ziyaret", bg="grey35", fg="white",
                       command=lambda: _handle_input(text, "VISITED_HARBORS", action, VISITED_HARBORS, c), padx=15,
                       pady=2)
    button.place(x=30, y=170)

    button = tk.Button(newWindow, text="Yolculuk", bg="grey35", fg="white",
                       command=lambda: _handle_input(text, "EXPEDITIONS", action, EXPEDITIONS, c), padx=15, pady=2)
    button.place(x=30, y=230)

    button = tk.Button(newWindow, text="Geri dön", bg="grey35", fg="white", command=newWindow.destroy, padx=15, pady=2)
    button.place(x=30, y=290)

    button = tk.Button(newWindow, text="Liman", bg="grey35", fg="white",
                       command=lambda: _handle_input(text, "HARBOR", action, HARBOR, c), padx=15, pady=2)
    button.place(x=150, y=50)

    button = tk.Button(newWindow, text="Petrol gemisi", bg="grey35", fg="white",
                       command=lambda: _handle_input(text, "OIL_SHIP", action, OIL_SHIP, c), padx=15, pady=2)
    button.place(x=150, y=110)

    button = tk.Button(newWindow, text="Yolcu gemisi", bg="grey35", fg="white",
                       command=lambda: _handle_input(text, "CRUISE_SHIP", action, CRUISE_SHIP, c), padx=15, pady=2)
    button.place(x=150, y=170)

    button = tk.Button(newWindow, text="Konteyner gemisi", bg="grey35", fg="white",
                       command=lambda: _handle_input(text, "CONTAINER_SHIP", action, CONTAINER_SHIP, c), padx=15,
                       pady=2)
    button.place(x=150, y=230)

    button = tk.Button(newWindow, text="Temizle", bg="grey35", fg="white", command=lambda: text.delete(1.0, tk.END),
                       padx=15, pady=2)
    button.place(x=150, y=290)

    # İkincil menüde girilen değerleri kullanarak database'in yönet. (Her butonun farklı bir fonksiyonu var)



def insert_sample(sampleTable, sampleAttrs, classType, c):
    try:
        objInstance = classType(*sampleAttrs)
        objAttrDict = vars(objInstance)
        objAttrList = list(objAttrDict.values())
        objects.append(objInstance)
        # Girilen değerleri kullanarak nesneyi oluştur.

        if isinstance(objInstance, CAPTAIN) or isinstance(objInstance, CREW):
            c.execute('''INSERT INTO EMPLOYEE(EMP_ID, EMP_JOB) VALUES(?,?)''', (objInstance.ID, objInstance.job))
            objAttrList.pop(1)
            # Eğer nesne kaptan ya da mürettebat örneğiyse, bu tabloların yanı sıra çalışan tablosunu da güncelle.

        elif isinstance(objInstance, OIL_SHIP) or isinstance(objInstance, CRUISE_SHIP) or isinstance(objInstance,
                                                                                                     CONTAINER_SHIP):
            c.execute('''INSERT INTO SHIP(S_SERIAL_NUM, S_TYPE) VALUES(?,?)''', (objInstance.serialNum, objInstance.type))
            objAttrList.pop(-1)
            # Eğer nesne petrol gemisi, konteyner gemisi ya da yolcu gemisi örneğiyse, bu tabloların yanı sıra
            # gemi tablosunu da güncelle.

        c.execute(tables[sampleTable][0], objAttrList)
        conn.commit()
        # Değişiklikleri database'e bildir.

    except TypeError or ValueError:
        print('Girdiler hatalı. Tablonun özelliklerini kontrol edip yeniden deneyin.')

def delete_sample(sampleTable, sampleAttrs, classType, c):
    sqlStr = f"{tables[sampleTable][1]}"
    c.execute(sqlStr, sampleAttrs)
    conn.commit()
    # tables sözlüğündeki 2. girdiyi (DELETE) çalıştır ve değişiklikleri databese'e bildir.

    for i in objects:
        if isinstance(i, classType) and _repeats(sampleAttrs, list(vars(i).values())):
            objects.remove(i)
            del i
            # Eğer eklenen örnek bu oturumda eklendiyse silinmeden önce geri döndürülebilir.
            # Ancak kullanıcı örneği silmek istediğine eminse, bu örneği objects listesinden kaldır.

def update_sample(sampleTable, sampleAttrs, c):
    sqlStr = f"UPDATE {sampleTable} SET {sampleAttrs[-2]} = {sampleAttrs[-1]} WHERE "
    # SQL'i çalıştırmak için bir string hazırla.

    for i in range(len(tables[sampleTable][2])):
        sqlStr += f"{tables[sampleTable][2][i]} = {sampleAttrs[i]}"
        sqlStr += f" AND "
    # İlk indisler birincil anahtar değerleri (sütun adları değil değerleri),
    # Sondan önceki indis değiştirilecek sütunun ismi,
    # Son indis ise yeni değer.

    sqlStr = sqlStr[:-5]
    # For döngüsünden sonra metnin sonunda bir " AND " ifadesi kalacak.
    # Onu sil.

    c.execute(sqlStr)
    conn.commit()
    # Değişiklikleri database'e bildir.

def display_table(sampleTable):
    newWindow = tk.Toplevel(root)
    newWindow.title(f'{sampleTable}')
    newWindow.resizable(False, False)
    newWindow.grab_set()
    newWindow.geometry('1240x720')
    # İkincil menünün üstüne boyutu değiştirilemeyen bir sekme aç.

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {sampleTable}")
    records = cursor.fetchall()
    # Tablo verilerini al.

    text = tk.Text(newWindow, height=40, width=142, bg="grey75", fg="black")
    text.place(x=50, y=18)

    button = tk.Button(newWindow, text="Geri Dön", bg="grey35", fg="white", command=newWindow.destroy, padx=15, pady=2)
    button.place(x=30, y=680)
    # Butonu ve metin kutusunu oluştur.

    try:

        cursor.execute(f"PRAGMA table_info({sampleTable})")
        columns = [column[1] for column in cursor.fetchall()]
        # Tablo başlıklarını al.

        columnKeyWidths = [len(str(column)) for column in columns]
        columnValueWidths = [max(len(str(record[i])) for record in records) for i in range(len(columns))]
        columnWidths = []
        # Her sütun için en uzun girdiyi bul.

        for i in range(len(columnKeyWidths)):
            if columnKeyWidths[i] >= columnValueWidths[i]:
                columnWidths.append(columnKeyWidths[i])
            else:
                columnWidths.append(columnValueWidths[i])
            # Başlık ve örnek değerlerinden hangisi daha büyükse onu columnWidths listesine koy.

        text.insert(tk.END, "|")
        for i, column in enumerate(columns):
            text.insert(tk.END, f"{column.center(columnWidths[i])} | ")
        text.insert(tk.END, "\n" + "-" * (sum(columnWidths) + len(columns) * 3) + "\n")
        # Başlıkları ve çizgileri ekrana yazdır.

        for record in records:
            text.insert(tk.END, "|")
            for i, field in enumerate(record):
                text.insert(tk.END, f"{str(field).center(columnWidths[i])} | ")
            text.insert(tk.END, "\n")
        # Verileri ekrana yazdır.

        text.config(state=tk.DISABLED)
        # Metin kutusunun durumunu değiştirilemez olarak değiştir.

    except ValueError:
        text.insert(tk.END, "")




objects = []
tables = {'EMPLOYEE': ['''INSERT INTO EMPLOYEE (EMP_ID, EMP_JOB) VALUES (?,?)''',
                       '''DELETE FROM EMPLOYEE WHERE EMP_ID=(?)''',
                       ['EMP_ID']],

          'CAPTAIN': ['''INSERT INTO CAPTAIN (EMP_ID, CAP_LICENSE, CAP_NAME, CAP_LNAME, CAP_ADRESS, CAP_CITIZENSHIP, CAP_BIRTH_DATE, CAP_START_DATE, CAP_SHIP) VALUES (?,?,?,?,?,?,?,?,?)''',
                      '''DELETE FROM CAPTAIN WHERE EMP_ID=(?)''',
                      ['EMP_ID']],

          'CREW': ['''INSERT INTO CREW (EMP_ID, CREW_NAME, CREW_LNAME, CREW_ADRESS, CREW_CITIZENSHIP, CREW_BIRTH_DATE, CREW_START_DATE, CREW_DUTY, CREW_SHIP) VALUES (?,?,?,?,?,?,?,?,?)''',
                   '''DELETE FROM CREW WHERE EMP_ID=(?)''',
                   ['EMP_ID']],

          'HARBOR': ['''INSERT INTO HARBOR (H_NAME, H_COUNTRY, H_POPULATION, H_PASSPORT, H_FEE) VALUES (?,?,?,?,?)''',
                     '''DELETE FROM HARBOR WHERE (H_NAME, H_COUNTRY)=(?,?)''',
                     ['H_NAME', 'H_COUNTRY']],

          'SHIP': ['''INSERT INTO SHIP (S_SERIAL_NUM, S_TYPE) VALUES (?,?)''',
                   '''DELETE FROM SHIP WHERE S_SERIAL_NUM=(?)''',
                   ['S_SERIAL_NUM']],

          'CONTAINER_SHIP': ['''INSERT INTO CONTAINER_SHIP (S_SERIAL_NUM, S_NAME, S_TONNAGE, S_MADE_IN, S_CONTAINER_AMOUNT, S_MAX_CAPACITY) VALUES (?,?,?,?,?,?)''',
                             '''DELETE FROM CONTAINER_SHIP WHERE S_SERIAL_NUM=(?)''',
                             ['S_SERIAL_NUM']],

          'OIL_SHIP': ['''INSERT INTO OIL_SHIP (S_SERIAL_NUM, S_NAME, S_TONNAGE, S_MADE_IN, S_OIL_CAPACITY) VALUES (?,?,?,?,?)''',
                       '''DELETE FROM OIL_SHIP WHERE S_SERIAL_NUM=(?)''',
                       ['S_SERIAL_NUM']],

          'CRUISE_SHIP': ['''INSERT INTO CRUISE_SHIP (S_SERIAL_NUM, S_NAME, S_TONNAGE, S_MADE_IN, S_CAPACITY) VALUES (?,?,?,?,?)''',
                          '''DELETE FROM CRUISE_SHIP WHERE S_SERIAL_NUM=(?)''',
                          ['S_SERIAL_NUM']],

          'VISITED_HARBORS': ['''INSERT INTO VISITED_HARBORS (H_NAME, H_COUNTRY, S_SERIAL_NUM, VH_STATE) VALUES (?,?,?,?)''',
                              '''DELETE FROM VISITED_HARBORS WHERE (H_NAME, H_COUNTRY, S_SERIAL_NUM)=(?,?,?)''',
                              ['H_NAME', 'H_COUNTRY', 'S_SERIAL_NUM']],

          'EXPEDITIONS': ['''INSERT INTO EXPEDITIONS (EMP_ID, S_SERIAL_NUM, E_START_DATE, E_RETURN_DATE, E_START_HARBOR, E_START_COUNTRY, E_CAP, E_CREW) VALUES (?,?,?,?,?,?,?,?)''',
                          '''DELETE FROM EXPEDITIONS WHERE EMP_ID=(?)''',
                          ['S_SERIAL_NUM', 'E_START_DATE']]}
# Her bir sınıfa özel SQL komutları ve sınıfların database'deki yansımaları olan tabloların birincil anahtarlarını tutan bir sözlük.


conn = sql.connect('gezginGemi.db')
c = conn.cursor()
# Database'e bağlan.

root = tk.Tk()
root.geometry('640x380')
root.resizable(False, False)
root.title("Gezgin Gemi Veritabanı")
# Ana menüyü oluştur ve pencerenin boyutunun değiştirilmesine izin verme.

choice = rnd.choice(list(tables.keys()))
c.execute(f'SELECT * FROM {choice}')
# Menüde rastgele tablo göstermek için bir tabloyu seç.

_construct_main_menu()
# Menüyü oluştur.


root.mainloop()