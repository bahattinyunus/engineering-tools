import os
import sys
import subprocess

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

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

def run_tests(interactive=True):
    if interactive:
        clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}    [TEST] MUHENDISLIK BIRIM TEST PAKETI (UNIT TESTS) {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    test_file = os.path.join(os.path.dirname(__file__), "tests", "test_engineering_tools.py")
    ret_code = 0
    if os.path.exists(test_file):
        proc = subprocess.run([sys.executable, test_file])
        ret_code = proc.returncode
    else:
        print(f"{Colors.FAIL}Test dosyası bulunamadı: {test_file}{Colors.ENDC}")
        ret_code = 1
    if interactive:
        input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")
    return ret_code

def list_all_tools():
    print(f"\n{Colors.HEADER}================================================================================{Colors.ENDC}")
    print(f"{Colors.BOLD}          TÜM MÜHENDİSLİK MODÜLLERİ VE ÇALIŞTIRILABİLİR ARAÇLAR LİSTESİ         {Colors.ENDC}")
    print(f"{Colors.HEADER}================================================================================{Colors.ENDC}")
    tools = [
        ("Yazılım & Veri Analizi", "Veri Analizi & Birim Dönüştürücü", "software/python/data_analyzer.py"),
        ("Yazılım & Veritabanı", "Mühendislik Malzeme Veritabanı (SQL)", "software/databases/db_manager.py"),
        ("Bulut & DevOps", "Bulut TCO & Altyapı Maliyet Hesaplayıcı", "software/cloud/cloud_cost_calculator.py"),
        ("Otomasyon & Mekatronik", "PLC Modbus & PID Simülatörü", "automation-electronics/plc-scada/modbus_simulator.py"),
        ("Elektrik & Devre", "Kablo Kesiti & Filtre Rezonans Analizi", "automation-electronics/circuit-design/electrical_calculator.py"),
        ("CAD / CAM", "CNC G-Kodu Jeneratörü (Profil Frezeleme)", "mechanical-civil/cad-cam/gcode_generator.py"),
        ("Proje Yönetimi", "Kritik Yol Metodu (CPM & PERT)", "mechanical-civil/project-management/cpm_calculator.py"),
        ("Yapı Statiği & Mukavemet", "Kiriş Eğilme Momenti & Sehim Analizi", "mechanical-civil/structural-mechanics/beam_stress_calculator.py"),
        ("Kimya & Süreç", "Boru Basınç Kaybı & Reynolds (Darcy)", "chemical-process/process-engineering/fluid_thermal_calculator.py"),
        ("Endüstri & Yalın Üretim", "OEE & Altı Sigma (DPMO) Hesaplayıcı", "industrial-engineering/lean-six-sigma/oee_sigma_calculator.py"),
        ("Kalite & Standartlar", "ISO 9001 / 22000 / 14001 Denetim Asistanı", "quality-standards/iso-standards/audit_checklist.py"),
        ("Çevre & Sürdürülebilirlik", "Kapsam 1-2-3 Sera Gazı (GHG) Ayak İzi", "environment/sustainability-reports/carbon_footprint.py"),
        ("Yenilenebilir Enerji", "Güneş (PV) ve Rüzgar Güç Hesaplayıcı", "energy-engineering/renewables/power_calculator.py"),
        ("Enerji Depolama", "BESS Batarya Boyutlandırma & LCOS Analizi", "energy-engineering/storage-grid/bess_storage_calculator.py")
    ]
    print(f"{'Kategori':<25} | {'Araç Adı':<42} | {'Yol'}")
    print("-" * 110)
    for cat, name, path in tools:
        print(f"{cat:<25} | {name:<42} | {path}")
    print("=" * 110)

def menu_software():
    while True:
        clear_screen()
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}          YAZILIM VE BİLGİSAYAR ARAÇLARI          {Colors.ENDC}")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.OKGREEN}1.{Colors.ENDC} Veri Analizi ve Birim Dönüştürücü (Python)")
        print(f"{Colors.OKGREEN}2.{Colors.ENDC} Mühendislik Malzeme Veritabanı Yöneticisi (SQL)")
        print(f"{Colors.OKGREEN}3.{Colors.ENDC} Bulut TCO & Altyapı Maliyet Hesaplayıcı (DevOps)")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Ana Menüye Dön")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        if secim == '1':
            run_script("software/python/data_analyzer.py")
        elif secim == '2':
            run_script("software/databases/db_manager.py")
        elif secim == '3':
            run_script("software/cloud/cloud_cost_calculator.py")
        elif secim == '0':
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim!{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

def menu_automation():
    while True:
        clear_screen()
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}        ELEKTRİK-ELEKTRONİK VE OTOMASYON          {Colors.ENDC}")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.OKGREEN}1.{Colors.ENDC} PLC Modbus Kaydedici ve PID Simülatörü")
        print(f"{Colors.OKGREEN}2.{Colors.ENDC} Kablo Kesiti, Gerilim Düşümü ve Filtre Analizi (IEC)")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Ana Menüye Dön")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        if secim == '1':
            run_script("automation-electronics/plc-scada/modbus_simulator.py")
        elif secim == '2':
            run_script("automation-electronics/circuit-design/electrical_calculator.py")
        elif secim == '0':
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim!{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

def menu_mechanical_civil():
    while True:
        clear_screen()
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}            MAKİNE VE İNŞAAT ARAÇLARI             {Colors.ENDC}")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.OKGREEN}1.{Colors.ENDC} CNC G-Kodu Jeneratörü (CAD/CAM)")
        print(f"{Colors.OKGREEN}2.{Colors.ENDC} Kritik Yol Metodu (CPM) ve PERT Proje Planlayıcı")
        print(f"{Colors.OKGREEN}3.{Colors.ENDC} Kiriş Eğilme Gerilmesi ve Sehim Analizi (Statik)")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Ana Menüye Dön")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        if secim == '1':
            run_script("mechanical-civil/cad-cam/gcode_generator.py")
        elif secim == '2':
            run_script("mechanical-civil/project-management/cpm_calculator.py")
        elif secim == '3':
            run_script("mechanical-civil/structural-mechanics/beam_stress_calculator.py")
        elif secim == '0':
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim!{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

def menu_chemical():
    while True:
        clear_screen()
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}          KİMYA VE SÜREÇ MÜHENDİSLİĞİ             {Colors.ENDC}")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.OKGREEN}1.{Colors.ENDC} Boru Akışı Basınç Düşüşü & Reynolds Analizi (Darcy)")
        print(f"{Colors.OKGREEN}2.{Colors.ENDC} Isı Eşanjörü LMTD ve Transfer Alanı Hesabı")
        print(f"{Colors.OKGREEN}3.{Colors.ENDC} Çözelti Karışımı ve Seyreltme Dengesi")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Ana Menüye Dön")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        if secim in ['1', '2', '3']:
            run_script("chemical-process/process-engineering/fluid_thermal_calculator.py")
        elif secim == '0':
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim!{Colors.ENDC}")
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
            print(f"\n{Colors.FAIL}Geçersiz seçim!{Colors.ENDC}")
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
            print(f"\n{Colors.FAIL}Geçersiz seçim!{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

def menu_environment():
    while True:
        clear_screen()
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}             ÇEVRE VE SÜRDÜRÜLEBİLİRLİK           {Colors.ENDC}")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.OKGREEN}1.{Colors.ENDC} Kapsam 1, 2, 3 Karbon Ayak İzi Hesaplayıcı (ESG)")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Ana Menüye Dön")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        if secim == '1':
            run_script("environment/sustainability-reports/carbon_footprint.py")
        elif secim == '0':
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim!{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

def menu_energy():
    while True:
        clear_screen()
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}          ENERJİ SİSTEMLERİ MÜHENDİSLİĞİ          {Colors.ENDC}")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        print(f"{Colors.OKGREEN}1.{Colors.ENDC} Güneş (PV) ve Rüzgar Türbini Güç Hesaplayıcı")
        print(f"{Colors.OKGREEN}2.{Colors.ENDC} Bataryalı Enerji Depolama (BESS) ve LCOS Hesaplayıcı")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Ana Menüye Dön")
        print(f"{Colors.OKCYAN}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        if secim == '1':
            run_script("energy-engineering/renewables/power_calculator.py")
        elif secim == '2':
            run_script("energy-engineering/storage-grid/bess_storage_calculator.py")
        elif secim == '0':
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim!{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

def main():
    if os.name == 'nt':
        os.system('color')
        
    # Komut satırı argümanları desteği
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['--test', '-t']:
            code = run_tests(interactive=False)
            sys.exit(code)
        elif arg in ['--list', '-l']:
            list_all_tools()
            sys.exit(0)
        elif arg in ['--help', '-h']:
            print("Kullanım: python run_tools.py [SEÇENEK]")
            print("  --test, -t : Tüm otomatik birim testlerini çalıştırır.")
            print("  --list, -l : Mevcut tüm mühendislik araçlarını listeler.")
            print("  --help, -h : Bu yardım mesajını gösterir.")
            sys.exit(0)

    while True:
        clear_screen()
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}     [TOOLS] MUHENDISLIK ARACLARI KONSOL ARAYUZU   {Colors.ENDC}")
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.OKBLUE}1.{Colors.ENDC} Yazılım ve Bilgisayar Mühendisliği")
        print(f"{Colors.OKBLUE}2.{Colors.ENDC} Elektrik-Elektronik ve Otomasyon Mühendisliği")
        print(f"{Colors.OKBLUE}3.{Colors.ENDC} Makine ve İnşaat Mühendisliği")
        print(f"{Colors.OKBLUE}4.{Colors.ENDC} Kimya ve Süreç Mühendisliği (Proses & Hidrolik)")
        print(f"{Colors.OKBLUE}5.{Colors.ENDC} Endüstri Mühendisliği (Yalın & Altı Sigma)")
        print(f"{Colors.OKBLUE}6.{Colors.ENDC} Kalite Standartları ve Güvenlik (ISO & HACCP)")
        print(f"{Colors.OKBLUE}7.{Colors.ENDC} Çevre ve Sürdürülebilirlik (ESG)")
        print(f"{Colors.OKBLUE}8.{Colors.ENDC} Enerji Sistemleri Mühendisliği (Güneş, Rüzgar, BESS)")
        print(f"{Colors.OKGREEN}9.{Colors.ENDC} [TEST] Otomatik Mühendislik Testlerini Çalıştır (Unit Tests)")
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
            menu_chemical()
        elif secim == '5':
            menu_industrial()
        elif secim == '6':
            menu_quality()
        elif secim == '7':
            menu_environment()
        elif secim == '8':
            menu_energy()
        elif secim == '9':
            run_tests()
        elif secim == '0':
            print(f"\n{Colors.OKGREEN}Programdan çıkılıyor. İyi çalışmalar!{Colors.ENDC}")
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim! Lütfen tekrar deneyin.{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

if __name__ == "__main__":
    main()
