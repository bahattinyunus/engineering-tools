import os
import sys
import subprocess

# ANSI Renk Kodları (Standard Kütüphane)
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_script(path):
    abs_path = os.path.join(os.path.dirname(__file__), path)
    if not os.path.exists(abs_path):
        print(f"\n{Colors.FAIL}[HATA] '{path}' dosyası bulunamadı. Lütfen dosyanın varlığından emin olun.{Colors.ENDC}")
        input("\nDevam etmek için Enter'a basın...")
        return
    try:
        subprocess.run([sys.executable, abs_path])
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}[BİLGİ] İşlem kullanıcı tarafından iptal edildi.{Colors.ENDC}")
        input("\nDevam etmek için Enter'a basın...")
    except Exception as e:
        print(f"\n{Colors.FAIL}[HATA] Çalıştırılırken bir hata oluştu: {e}{Colors.ENDC}")
        input("\nDevam etmek için Enter'a basın...")

def menu_software():
    while True:
        clear_screen()
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}          YAZILIM VE BİLGİSAYAR ARAÇLARI          {Colors.ENDC}")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.OKGREEN}1.{Colors.ENDC} Veri Analizi ve Birim Dönüştürücü (Python)")
        print(f"{Colors.OKGREEN}2.{Colors.ENDC} Mühendislik Malzeme Veritabanı Yöneticisi (SQL)")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Ana Menüye Dön")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        if secim == '1':
            run_script("software/python/data_analyzer.py")
        elif secim == '2':
            run_script("software/databases/db_manager.py")
        elif secim == '0':
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim! Lütfen tekrar deneyin.{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

def menu_automation():
    while True:
        clear_screen()
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}        ELEKTRİK-ELEKTRONİK VE OTOMASYON          {Colors.ENDC}")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.OKGREEN}1.{Colors.ENDC} PLC Modbus Kaydedici ve Register Simülatörü")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Ana Menüye Dön")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        if secim == '1':
            run_script("automation-electronics/plc-scada/modbus_simulator.py")
        elif secim == '0':
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim! Lütfen tekrar deneyin.{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

def menu_mechanical_civil():
    while True:
        clear_screen()
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}            MAKİNE VE İNŞAAT ARAÇLARI             {Colors.ENDC}")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.OKGREEN}1.{Colors.ENDC} CNC G-Kodu Jeneratörü (CAD/CAM)")
        print(f"{Colors.OKGREEN}2.{Colors.ENDC} Kritik Yol Metodu (CPM) Proje Planlayıcı")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Ana Menüye Dön")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        if secim == '1':
            run_script("mechanical-civil/cad-cam/gcode_generator.py")
        elif secim == '2':
            run_script("mechanical-civil/project-management/cpm_calculator.py")
        elif secim == '0':
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim! Lütfen tekrar deneyin.{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

def menu_industrial():
    while True:
        clear_screen()
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}          ENDÜSTRİ MÜHENDİSLİĞİ ARAÇLARI          {Colors.ENDC}")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.OKGREEN}1.{Colors.ENDC} OEE (Toplam Ekipman Etkinliği) ve Altı Sigma Hesaplayıcı")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Ana Menüye Dön")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        if secim == '1':
            run_script("industrial-engineering/lean-six-sigma/oee_sigma_calculator.py")
        elif secim == '0':
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim! Lütfen tekrar deneyin.{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

def menu_quality():
    while True:
        clear_screen()
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}          KALİTE VE STANDARTLAR ARAÇLARI          {Colors.ENDC}")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.OKGREEN}1.{Colors.ENDC} ISO 9001 & ISO 22000 (HACCP) Denetim Asistanı")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Ana Menüye Dön")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        if secim == '1':
            run_script("quality-standards/iso-standards/audit_checklist.py")
        elif secim == '0':
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim! Lütfen tekrar deneyin.{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

def menu_environment():
    while True:
        clear_screen()
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}             ÇEVRE VE SÜRDÜRÜLEBİLİRLİK           {Colors.ENDC}")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.OKGREEN}1.{Colors.ENDC} Kapsam 1, 2, 3 Karbon Ayak İzi Hesaplayıcı")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Ana Menüye Dön")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        if secim == '1':
            run_script("environment/sustainability-reports/carbon_footprint.py")
        elif secim == '0':
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim! Lütfen tekrar deneyin.{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

def menu_energy():
    while True:
        clear_screen()
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}          ENERJİ SİSTEMLERİ MÜHENDİSLİĞİ          {Colors.ENDC}")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.OKGREEN}1.{Colors.ENDC} Güneş (PV) ve Rüzgar Türbini Güç Hesaplayıcı")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Ana Menüye Dön")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        if secim == '1':
            run_script("energy-engineering/renewables/power_calculator.py")
        elif secim == '0':
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim! Lütfen tekrar deneyin.{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

def main():
    # Windows 10'da ANSI renkleri desteklemek için os.system çağrısı
    if os.name == 'nt':
        os.system('color')
        
    while True:
        clear_screen()
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}     🛠️  MÜHENDİSLİK ARAÇLARI KONSOL ARAYÜZÜ      {Colors.ENDC}")
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.OKBLUE}1.{Colors.ENDC} Yazılım ve Bilgisayar Mühendisliği")
        print(f"{Colors.OKBLUE}2.{Colors.ENDC} Elektrik-Elektronik ve Otomasyon Mühendisliği")
        print(f"{Colors.OKBLUE}3.{Colors.ENDC} Makine ve İnşaat Mühendisliği")
        print(f"{Colors.OKBLUE}4.{Colors.ENDC} Endüstri Mühendisliği (Yalın & Altı Sigma)")
        print(f"{Colors.OKBLUE}5.{Colors.ENDC} Kalite Standartları ve Güvenlik (ISO & HACCP)")
        print(f"{Colors.OKBLUE}6.{Colors.ENDC} Çevre ve Sürdürülebilirlik")
        print(f"{Colors.OKBLUE}7.{Colors.ENDC} Enerji Sistemleri Mühendisliği (Güneş & Rüzgar)")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Çıkış")
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()

        if secim == '1':
            menu_software()
        elif secim == '2':
            menu_automation()
        elif secim == '3':
            menu_mechanical_civil()
        elif secim == '4':
            menu_industrial()
        elif secim == '5':
            menu_quality()
        elif secim == '6':
            menu_environment()
        elif secim == '7':
            menu_energy()
        elif secim == '0':
            print(f"\n{Colors.OKGREEN}Programdan çıkılıyor. İyi çalışmalar!{Colors.ENDC}")
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim! Lütfen tekrar deneyin.{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

if __name__ == "__main__":
    main()
