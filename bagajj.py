from veriyapıları import Queue, Stack, LinkedList
import random
import tkinter as tk
from tkinter import messagebox
import csv
import test_senaryolar

YASAKLAR = {
    "silah", "bıçak", "patlayıcı", "yanıcı madde", "zehir",
    "çakı", "alkollü içecek", "barut", "çakmak", "kesici alet",
    "kimyasal madde", "tüpyük", "havai fişek", "kurşun", "ateşleyici cihaz"
}

ESYALAR = [
    "kitap", "dizüstü bilgisayar", "şemsiye", "telefon", "şarj cihazı",
    "gözlük", "parfüm", "giysi", "ayakkabı", "kamera",
    "silah", "bıçak", "patlayıcı", "yanıcı madde", "zehir",
    "tencere", "çakı", "drone", "tablet", "kalem",
    "alkollü içecek", "barut", "batarya", "çakmak",
    "oyuncak", "kulaklık", "güneş kremi", "tüpyük", "havai fişek",
    "kurşun", "ateşleyici cihaz", "dosya", "not defteri"
]

def esya_tehlikeli_mi(esya):
    return esya in YASAKLAR

class Passenger:
    sayac = 1
    def __init__(self, custom_bagaj=None):
        self.id = f"Yolcu #{Passenger.sayac}"
        Passenger.sayac += 1
        self.bagaj = custom_bagaj if custom_bagaj else rastgele_bagaj_uret()

def rastgele_bagaj_uret():
    toplam_esya = random.randint(5, 10)
    tehlikeli_sayisi = toplam_esya * 10 // 100
    normal_sayisi = toplam_esya - tehlikeli_sayisi
    tehlikeli = random.sample(list(YASAKLAR), k=tehlikeli_sayisi) if tehlikeli_sayisi > 0 else []
    normal = random.choices([e for e in ESYALAR if e not in YASAKLAR], k=normal_sayisi)
    return tehlikeli + normal

kuyruk, stack, kara_liste = Queue(), Stack(), LinkedList()
loglar, temizler, yeni_kara_liste = [], [], []
alarm_sayisi = 0

pencere = tk.Tk()
pencere.title("Bagaj Güvenlik Simülatörü")
pencere.geometry("800x600")

lb_kuyruk = tk.Listbox(pencere, width=30); lb_kuyruk.grid(row=0, column=0)
lb_stack = tk.Listbox(pencere, width=30); lb_stack.grid(row=0, column=1)
lb_kara = tk.Listbox(pencere, width=30); lb_kara.grid(row=0, column=2)
txt_log = tk.Text(pencere, width=90, height=10); txt_log.grid(row=1, column=0, columnspan=3)

entry_bagaj = tk.Entry(pencere, width=60)
tk.Label(pencere, text="Manuel Bagaj (virgülle):").grid(row=4, column=0, columnspan=2)
entry_bagaj.grid(row=5, column=0, columnspan=2, pady=5)

def log(m, alarm=False):
    index = txt_log.index(tk.END)
    txt_log.insert(tk.END, m + "\n")
    if alarm:
        txt_log.tag_add("alarm", index, f"{index} lineend")
    loglar.append(m)
    guncelle()

def tehlikeli_goster():
    lb_stack.delete(0, tk.END)

    y = kuyruk.peek()
    if not y:
        tk.messagebox.showinfo("Bilgi", "Kuyrukta yolcu yok.")
        return

    bulundu = False
    for esya in y.bagaj:
        if esya_tehlikeli_mi(esya):
            lb_stack.insert(tk.END, esya)
            bulundu = True

    if not bulundu:
        lb_stack.insert(tk.END, "(Tehlikeli eşya bulunamadı)")

def guncelle():
    lb_kuyruk.delete(0, tk.END)
    [lb_kuyruk.insert(tk.END, y.id) for y in kuyruk.all()]
    lb_stack.delete(0, tk.END)
    [lb_stack.insert(tk.END, e) for e in stack.all()]
    lb_kara.delete(0, tk.END)
    [lb_kara.insert(tk.END, k) for k in kara_liste.all()]
    txt_log.tag_config("alarm", foreground="red")

import pygame
pygame.mixer.init()

def alarm_cal():
    try:
        pygame.mixer.music.load("../alarm.wav")
        pygame.mixer.music.play()
    except Exception as e:
        log(f"Ses çalınamadı: {e}")

def yolcu_manu():
    text = entry_bagaj.get()
    esyalar = [e.strip() for e in text.split(",") if e.strip()]
    tum_gecerli = ESYALAR + list(YASAKLAR)
    gecersiz = [e for e in esyalar if e not in tum_gecerli]
    if not esyalar:
        messagebox.showwarning("Uyarı", "Bagaj boş olamaz!")
        return
    if gecersiz:
        tk.messagebox.showerror("Hata", f"Geçersiz eşya(lar): {', '.join(gecersiz)}")
        return
    yolcu = Passenger(custom_bagaj=esyalar)
    kuyruk.enqueue(yolcu)
    log(f"{yolcu.id} manuel olarak kuyruğa eklendi.")
    entry_bagaj.delete(0, tk.END)

def yeni_yolcu():
    y = Passenger()
    kuyruk.enqueue(y)
    log(f"{y.id} kuyruğa eklendi.")

def toplu_yolcu():
    for _ in range(30):
        y = Passenger()
        kuyruk.enqueue(y)
        log(f"{y.id} yüklendi.")
    log("30 yolcu başarıyla yüklendi.")

def hepsini_tara():
    while not kuyruk.is_empty():
        baslat()

islenen_yolcular_tehlikeli = {}

def baslat():
    global alarm_sayisi
    y = kuyruk.dequeue()
    if not y:
        return
    log(f"{y.id} işleniyor.")
    tehlikeli_sayisi = 0
    tehlikeli_esyalar = []

    for esya in y.bagaj:
        stack.push(esya)
        if esya_tehlikeli_mi(esya):
            alarm_sayisi += 1
            tehlikeli_sayisi += 1
            tehlikeli_esyalar.append(esya)
            log(f"ALARM: {y.id} bagajında {esya} bulundu!", alarm=True)
            alarm_cal()

    # Bu yolcunun tehlikeli eşyalarını sakla
    if tehlikeli_esyalar:
        islenen_yolcular_tehlikeli[y.id] = tehlikeli_esyalar

    guncelle()

    temiz = True
    while stack.all():
        esya = stack.pop()
        if esya_tehlikeli_mi(esya):
            temiz = False

    if temiz:
        temizler.append(y.id)
        log(f"{y.id} temiz geçti.")
    else:
        log(f"{y.id} bagajında toplam {tehlikeli_sayisi} tehlikeli eşya vardı.")
        if not kara_liste.contains(y.id):
            kara_liste.append(y.id)
            yeni_kara_liste.append(y.id)
            log(f"{y.id} kara listeye eklendi.", alarm=True)

    guncelle()

def goster_kara_liste_tehlikeli():
    lb_stack.delete(0, tk.END)
    bulundu = False
    for kisi in kara_liste.all():
        if kisi in islenen_yolcular_tehlikeli:
            lb_stack.insert(tk.END, f"--- {kisi} ---")
            for esya in islenen_yolcular_tehlikeli[kisi]:
                lb_stack.insert(tk.END, f"  {esya}")
            bulundu = True
    if not bulundu:
        lb_stack.insert(tk.END, "(Kara listedekilerde tehlikeli eşya bulunamadı)")

def rapor():
    toplam = Passenger.sayac - 1
    rapor_verisi = {
        "Toplam Yolcu": toplam,
        "Alarm Sayısı": alarm_sayisi,
        "Kara Listeye Eklenenler": len(yeni_kara_liste),
        "Temiz Geçenler": len(temizler)
    }

    with open("rapor.csv", mode="w", newline='', encoding="utf-8") as dosya:
        yazici = csv.writer(dosya)
        yazici.writerow(["İstatistik", "Değer"])
        for anahtar, deger in rapor_verisi.items():
            yazici.writerow([anahtar, deger])

    tk.messagebox.showinfo("Rapor", f"""
Toplam: {toplam}
Alarm: {alarm_sayisi}
Kara Liste: {len(yeni_kara_liste)}
Temiz: {len(temizler)}
→ rapor.csv dosyasına aktartıldı.
""")

def test_senaryolari():
    try:
        test_senaryolar.test_queue()
        test_senaryolar.test_stack()
        test_senaryolar.test_linkedlist()
        test_senaryolar.test_esya_tehlikeli_mi()
        test_senaryolar.test_passenger_bagaj()
        tk.messagebox.showinfo("Test", "Tüm test senaryoları başarıyla çalıştı.")
    except AssertionError as e:
        tk.messagebox.showerror("Test Hatası", f"Bir test başarısız oldu:\n{e}")
    except Exception as e:
        tk.messagebox.showerror("Hata", f"Beklenmeyen bir hata:\n{e}")

tk.Button(pencere, text="Yeni Yolcu", command=yeni_yolcu).grid(row=2, column=0)
tk.Button(pencere, text="Simülasyonu Başlat", command=baslat).grid(row=2, column=1)
tk.Button(pencere, text="Rapor", command=rapor).grid(row=2, column=2)
tk.Button(pencere, text="Toplu Yolcu Yükle", command=toplu_yolcu).grid(row=3, column=1)
tk.Button(pencere, text="Manuel Yolcu Ekle", command=yolcu_manu).grid(row=5, column=2)
tk.Button(pencere, text="Test Senaryoları", command=test_senaryolari).grid(row=3, column=2)
tk.Button(pencere, text="Tümünü Tara", command=hepsini_tara).grid(row=3, column=0)
tk.Button(pencere, text="Kara Listedekilerin Tehlikeli Eşyaları", command=goster_kara_liste_tehlikeli).grid(row=6, column=1)

guncelle()
pencere.mainloop()
