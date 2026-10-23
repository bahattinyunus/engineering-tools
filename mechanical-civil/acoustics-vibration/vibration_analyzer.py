import os
import math

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

# Akustik referans ses basıncı (İşitme eşiği p0 = 20 mikroPascal)
P0_ACOUSTIC = 20e-6

def calculate_sdof_vibration(mass_kg, stiffness_n_m, damping_c=0.0, excitation_freq_hz=None):
    """
    1-Serbestlik Dereceli (SDOF) Mekanik Titreşim Sistemi Analizi.
    m: Kütle (kg), k: Yay Katsayısı (N/m), c: Sönüm Katsayısı (N·s/m)
    """
    if mass_kg <= 0 or stiffness_n_m <= 0:
        return None, "Kütle ve yay sertliği pozitif olmalıdır."
    if damping_c < 0:
        return None, "Sönüm katsayısı negatif olamaz."
        
    omega_n = math.sqrt(stiffness_n_m / mass_kg)  # rad/s
    fn_hz = omega_n / (2.0 * math.pi)            # Hz
    period_sec = 1.0 / fn_hz if fn_hz > 0 else 0
    
    # Kritik sönüm katsayısı: Cc = 2 * sqrt(k * m)
    c_critical = 2.0 * math.sqrt(stiffness_n_m * mass_kg)
    zeta = damping_c / c_critical if c_critical > 0 else 0.0
    
    if zeta == 0.0:
        damping_type = "Sönümsüz (Undamped)"
        fd_hz = fn_hz
        log_decrement = 0.0
    elif zeta < 1.0:
        damping_type = "Düşük Sönümlü (Underdamped - Titreşimli Sönüm)"
        omega_d = omega_n * math.sqrt(1.0 - (zeta ** 2))
        fd_hz = omega_d / (2.0 * math.pi)
        log_decrement = (2.0 * math.pi * zeta) / math.sqrt(1.0 - (zeta ** 2))
    elif zeta == 1.0:
        damping_type = "Kritik Sönümlü (Critically Damped - Salınımsız En Hızlı Denge)"
        fd_hz = 0.0
        log_decrement = float('inf')
    else:
        damping_type = "Aşırı Sönümlü (Overdamped - Yavaş Sürünme)"
        fd_hz = 0.0
        log_decrement = float('inf')
        
    results = {
        "Kütle m (kg)": mass_kg,
        "Yay Katsayısı k (N/m)": stiffness_n_m,
        "Sönüm Katsayısı c (N·s/m)": damping_c,
        "Doğal Açısal Frekans ωn (rad/s)": omega_n,
        "Doğal Frekans fn (Hz)": fn_hz,
        "Titreşim Periyodu T (s)": period_sec,
        "Kritik Sönüm Katsayısı Cc (N·s/m)": c_critical,
        "Sönüm Oranı (Zeta ζ)": zeta,
        "Sönüm Rejimi": damping_type,
        "Sönümlü Doğal Frekans fd (Hz)": fd_hz,
        "Logaritmik Azalma (δ)": log_decrement
    }
    
    # Zorlanmış titreşim ve rezonans büyütme faktörü (DMF)
    if excitation_freq_hz is not None and excitation_freq_hz > 0:
        r = excitation_freq_hz / fn_hz # Frekans Oranı r = w / wn
        # Dinamik Büyütme Faktörü: DMF = 1 / sqrt((1 - r^2)^2 + (2*zeta*r)^2)
        denom_sq = ((1.0 - (r ** 2)) ** 2) + ((2.0 * zeta * r) ** 2)
        dmf = 1.0 / math.sqrt(denom_sq) if denom_sq > 0 else float('inf')
        
        is_resonant = 0.8 <= r <= 1.2
        results["Tahrik Frekansı f (Hz)"] = excitation_freq_hz
        results["Frekans Oranı (r = f/fn)"] = r
        results["Dinamik Büyütme Faktörü (DMF / Q)"] = dmf
        results["Rezonans Tehlikesi"] = "TEHLİKELİ REZONANS BÖLGESİ! (0.8 < r < 1.2)" if is_resonant else "GÜVENLİ (Rezonans dışı)"
        
    return results, None

def calculate_acoustics_decibels(sound_pressures_pa=None, sound_levels_db=None, r1_m=None, r2_m=None):
    """
    Endüstriyel Akustik: Ses basıncı (Pa) <=> Desibel (dB SPL) dönüşümü,
    birden çok ses kaynağının logaritmik toplanması ve mesafeyle ses zayıflaması.
    """
    results = {}
    
    # 1. Ses basıncından dB hesabı
    if sound_pressures_pa:
        levels = []
        for p in sound_pressures_pa:
            if p > 0:
                db = 20.0 * math.log10(p / P0_ACOUSTIC)
                levels.append(db)
        results["Hesaplanan Ses Seviyeleri (dB SPL)"] = levels
        sound_levels_db = (sound_levels_db or []) + levels
        
    # 2. Desibellerin logaritmik toplamı: L_toplam = 10 * log10(sum(10^(Li/10)))
    if sound_levels_db:
        sum_power = sum(10.0 ** (db / 10.0) for db in sound_levels_db)
        total_db = 10.0 * math.log10(sum_power) if sum_power > 0 else 0.0
        results["Kaynak Sayısı"] = len(sound_levels_db)
        results["Bireysel Kaynaklar (dB)"] = sound_levels_db
        results["Bileşke Toplam Gürültü Seviyesi (dB SPL)"] = total_db
        
        # İş sağlığı ve güvenliği (İSG) standart sınırı (85 dBA)
        results["İSG Gürültü Maruziyet Değerlendirmesi"] = "GÜRÜLTÜ SINIRI AŞILDI (>= 85 dB - Kulak Koruyucu Zorunlu)" if total_db >= 85.0 else "GÜVENLİ KABUL EDİLEBİLİR SEVİYE (< 85 dB)"
        
        # 3. Mesafeye göre zayıflama: L2 = L1 - 20*log10(r2/r1)
        if r1_m and r2_m and r1_m > 0 and r2_m > 0:
            attenuated_db = total_db - 20.0 * math.log10(r2_m / r1_m)
            results[f"Uzaklaşma Sonucu ({r1_m:.1f} m -> {r2_m:.1f} m)"] = f"{attenuated_db:.2f} dB SPL"
            
    return results

def interactive_vibration():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}   MEKANİK TİTREŞİM VE REZONANS ANALİZİ (SDOF)    {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("Kütle-Yay-Sönümleyici dinamik analizi ve rezonans kontrolü.")
    print("-" * 50)
    try:
        m = float(input("Kütle m (kg) [Örn: 50]: "))
        k = float(input("Yay Sertliği k (N/m) [Örn: 20000]: "))
        c = float(input("Sönüm Katsayısı c (N·s/m) [Örn: 80, Sönümsüz için 0]: ") or "0")
        f_ext = input("Tahrik Frekansı (Hz) [İsteğe bağlı, boş geçilebilir]: ").strip()
        f_in = float(f_ext) if f_ext else None
        
        res, err = calculate_sdof_vibration(m, k, c, f_in)
        if err:
            print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}>>> TİTREŞİM ANALİZ SONUÇLARI <<<{Colors.ENDC}")
            for key, val in res.items():
                if isinstance(val, float):
                    print(f"  {key:<38}: {Colors.BOLD}{val:12.4f}{Colors.ENDC}")
                elif "TEHLİKELİ" in str(val):
                    print(f"  {key:<38}: {Colors.FAIL}{val}{Colors.ENDC}")
                elif "GÜVENLİ" in str(val):
                    print(f"  {key:<38}: {Colors.OKGREEN}{val}{Colors.ENDC}")
                else:
                    print(f"  {key:<38}: {Colors.OKCYAN}{val}{Colors.ENDC}")
    except ValueError:
        print(f"{Colors.FAIL}Hata: Sayısal değer giriniz.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def interactive_acoustics():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}     ENDÜSTRİYEL AKUSTİK VE DESİBEL HESAPLAYICI   {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("Birden fazla makinenin gürültü toplamı ve mesafe zayıflaması.")
    print("-" * 50)
    try:
        raw_db = input("Gürültü Kaynaklarının dB Değerlerini boşlukla girin (Örn: 82 85 78 88): ").strip()
        if not raw_db:
            print(f"{Colors.FAIL}Değer girilmedi.{Colors.ENDC}")
            input("Devam etmek için Enter...")
            return
        db_list = [float(x) for x in raw_db.split()]
        
        dist_choice = input("Mesafeye bağlı zayıflama hesaplansın mı? (e/h): ").strip().lower()
        r1, r2 = None, None
        if dist_choice == 'e':
            r1 = float(input("Ölçülen İlk Mesafe r1 (metre) [Örn: 1.0]: ") or "1.0")
            r2 = float(input("Hedef Yeni Mesafe r2 (metre) [Örn: 10.0]: ") or "10.0")
            
        res = calculate_acoustics_decibels(sound_levels_db=db_list, r1_m=r1, r2_m=r2)
        print(f"\n{Colors.OKGREEN}>>> AKUSTİK GÜRÜLTÜ ANALİZİ <<<{Colors.ENDC}")
        for k, val in res.items():
            if isinstance(val, float):
                print(f"  {k:<42}: {Colors.BOLD}{val:8.2f} dB{Colors.ENDC}")
            elif "AŞILDI" in str(val):
                print(f"  {k:<42}: {Colors.FAIL}{val}{Colors.ENDC}")
            elif "GÜVENLİ" in str(val):
                print(f"  {k:<42}: {Colors.OKGREEN}{val}{Colors.ENDC}")
            else:
                print(f"  {k:<42}: {Colors.BOLD}{val}{Colors.ENDC}")
    except ValueError:
        print(f"{Colors.FAIL}Hata: Sayısal değer giriniz.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def main():
    if os.name == 'nt':
        os.system('color')
    while True:
        clear_screen()
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}   🔊 AKUSTİK VE TİTREŞİM MÜHENDİSLİĞİ ARAÇLARI   {Colors.ENDC}")
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.OKCYAN}1.{Colors.ENDC} Mekanik Titreşim, Sönüm ve Rezonans Analizi (SDOF)")
        print(f"{Colors.OKCYAN}2.{Colors.ENDC} Endüstriyel Akustik, dB Toplama ve Mesafe Zayıflaması")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Geri Dön")
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        if secim == '1':
            interactive_vibration()
        elif secim == '2':
            interactive_acoustics()
        elif secim == '0':
            break

if __name__ == "__main__":
    main()
