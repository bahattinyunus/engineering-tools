import os
import math

# ANSI Renk Kodları
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def solar_pv_calculator():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}       GÜNEŞ PANELİ (PV) GÜÇ HESAPLAYICI          {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("Bu araç fotovoltaik sistemlerin anlık güç üretimini hesaplar.")
    print("Formül: P = A * r * H * PR")
    print(" P: Güç Çıkışı (Watt)")
    print(" A: Toplam Panel Alanı (m^2)")
    print(" r: Güneş Paneli Verimliliği (%)")
    print(" H: Global Güneş Işınımı (W/m^2)")
    print(" PR: Performans Oranı (Kayıplar için, genelde 0.75 - 0.85)")
    print("-" * 50)
    
    try:
        alan = float(input("Toplam Panel Alanı (m^2): "))
        verim_yuzde = float(input("Panel Verimliliği (%): "))
        isinim = float(input("Güneş Işınımı (W/m^2) [Standart 1000]: ") or "1000")
        pr = float(input("Performans Oranı [0.75 - 0.85]: ") or "0.80")
        
        guc_watt = alan * (verim_yuzde / 100) * isinim * pr
        guc_kw = guc_watt / 1000
        
        print(f"\n{Colors.OKGREEN}>>> Sonuçlar <<<{Colors.ENDC}")
        print(f"Toplam Anlık Güç Çıkışı: {Colors.BOLD}{guc_watt:.2f} Watt ({guc_kw:.2f} kW){Colors.ENDC}")
        
    except ValueError:
        print(f"{Colors.FAIL}Hata: Lütfen geçerli sayısal değerler girin.{Colors.ENDC}")
        
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def wind_turbine_calculator():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}         RÜZGAR TÜRBİNİ GÜÇ HESAPLAYICI           {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("Bu araç rüzgar türbininin teorik ve pratik gücünü hesaplar.")
    print("Formül: P = 0.5 * rho * A * V^3 * Cp")
    print(" P: Güç Çıkışı (Watt)")
    print(" rho: Hava Yoğunluğu (kg/m^3)")
    print(" A: Süpürme Alanı (m^2)")
    print(" V: Rüzgar Hızı (m/s)")
    print(" Cp: Güç Katsayısı (Betz Limiti: Max 0.59)")
    print("-" * 50)
    
    try:
        yaricap = float(input("Kanat Yarıçapı (m): "))
        ruzgar_hizi = float(input("Rüzgar Hızı (m/s): "))
        hava_yogunlugu = float(input("Hava Yoğunluğu (kg/m^3) [Standart 1.225]: ") or "1.225")
        cp = float(input("Güç Katsayısı (Cp) [Max 0.59]: ") or "0.4")
        
        if cp > 0.593:
            print(f"{Colors.WARNING}Uyarı: Güç katsayısı Betz limiti olan 0.593'ten büyük olamaz. Değer 0.593 olarak ayarlandı.{Colors.ENDC}")
            cp = 0.593
            
        alan = math.pi * (yaricap ** 2)
        guc_watt = 0.5 * hava_yogunlugu * alan * (ruzgar_hizi ** 3) * cp
        guc_kw = guc_watt / 1000
        
        print(f"\n{Colors.OKGREEN}>>> Sonuçlar <<<{Colors.ENDC}")
        print(f"Türbin Süpürme Alanı: {alan:.2f} m^2")
        print(f"Mekanik Güç Üretimi: {Colors.BOLD}{guc_watt:.2f} Watt ({guc_kw:.2f} kW){Colors.ENDC}")
        
    except ValueError:
        print(f"{Colors.FAIL}Hata: Lütfen geçerli sayısal değerler girin.{Colors.ENDC}")
        
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def main():
    if os.name == 'nt':
        os.system('color')
        
    while True:
        clear_screen()
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}   🌿 YENİLENEBİLİR ENERJİ GÜÇ HESAPLAYICILARI    {Colors.ENDC}")
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.OKCYAN}1.{Colors.ENDC} Güneş Paneli (Fotovoltaik) Güç Hesaplama")
        print(f"{Colors.OKCYAN}2.{Colors.ENDC} Rüzgar Türbini Güç Hesaplama")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Geri Dön")
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        
        if secim == '1':
            solar_pv_calculator()
        elif secim == '2':
            wind_turbine_calculator()
        elif secim == '0':
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim! Lütfen tekrar deneyin.{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

if __name__ == "__main__":
    main()
