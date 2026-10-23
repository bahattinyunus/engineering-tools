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

# Uluslararası Standart Atmosfer (ISA - Sea Level Değerleri)
T0_ISA = 288.15        # Kelvin (15 °C)
P0_ISA = 101325.0      # Pascal (1013.25 hPa)
RHO0_ISA = 1.225       # kg/m^3
G_ACCEL = 9.80665      # m/s^2
R_AIR = 287.05287      # J/(kg·K)
GAMMA_AIR = 1.4        # Özgül ısılar oranı (Cp/Cv)
LAPSE_RATE = 0.0065    # K/m (Troposfer sıcaklık düşüş gradyanı)

def calculate_isa_atmosphere(altitude_m, velocity_kmh=None):
    """
    Uluslararası Standart Atmosfer (ISA) modeline göre irtifaya bağlı
    sıcaklık, basınç, hava yoğunluğu, ses hızı ve Mach sayısını hesaplar (0 - 20,000 metre).
    """
    if altitude_m < 0 or altitude_m > 20000:
        return None, "İrtifa 0 ile 20.000 metre arasında olmalıdır."
        
    if altitude_m <= 11000.0:
        # Troposfer katmanı
        temp_k = T0_ISA - (LAPSE_RATE * altitude_m)
        pressure_pa = P0_ISA * ((temp_k / T0_ISA) ** (G_ACCEL / (R_AIR * LAPSE_RATE)))
    else:
        # Alt Stratosfer katmanı (11 km - 20 km arası izotermal bölge)
        temp_11k = T0_ISA - (LAPSE_RATE * 11000.0)  # 216.65 K
        p_11k = P0_ISA * ((temp_11k / T0_ISA) ** (G_ACCEL / (R_AIR * LAPSE_RATE)))
        dh = altitude_m - 11000.0
        temp_k = temp_11k
        pressure_pa = p_11k * math.exp(- (G_ACCEL * dh) / (R_AIR * temp_k))
        
    density_kg_m3 = pressure_pa / (R_AIR * temp_k)
    speed_of_sound_ms = math.sqrt(GAMMA_AIR * R_AIR * temp_k)
    speed_of_sound_kmh = speed_of_sound_ms * 3.6
    
    results = {
        "İrtifa (m)": altitude_m,
        "Sıcaklık (°C)": temp_k - 273.15,
        "Sıcaklık (Kelvin)": temp_k,
        "Basınç (Pascal)": pressure_pa,
        "Basınç (hPa / mbar)": pressure_pa / 100.0,
        "Hava Yoğunluğu (kg/m³)": density_kg_m3,
        "Yoğunluk Oranı (sigma = rho/rho0)": density_kg_m3 / RHO0_ISA,
        "Ses Hızı (m/s)": speed_of_sound_ms,
        "Ses Hızı (km/h)": speed_of_sound_kmh
    }
    
    if velocity_kmh is not None and velocity_kmh > 0:
        v_ms = velocity_kmh / 3.6
        mach_number = v_ms / speed_of_sound_ms
        dynamic_pressure = 0.5 * density_kg_m3 * (v_ms ** 2)
        
        if mach_number < 0.8:
            regime = "Subsonik (Ses Altı)"
        elif mach_number <= 1.2:
            regime = "Transonik (Ses Hızı Geçişi)"
        elif mach_number <= 5.0:
            regime = "Süpersonik (Ses Üstü)"
        else:
            regime = "Hipersonik"
            
        results["Uçuş Hızı (km/h)"] = velocity_kmh
        results["Uçuş Hızı (m/s)"] = v_ms
        results["Mach Sayısı (M)"] = mach_number
        results["Uçuş Rejimi"] = regime
        results["Dinamik Basınç q (Pa)"] = dynamic_pressure
        
    return results, None

def generate_naca_4digit(digit_code, num_points=21):
    """
    NACA 4-basamaklı kanat profilinin (örn. '2412', '0012') üst ve alt yüzey koordinatlarını hesaplar.
    """
    if len(digit_code) != 4 or not digit_code.isdigit():
        return None, "NACA kodu 4 basamaklı rakamlardan oluşmalıdır (Örn: 2412, 0012, 4415)."
        
    m = int(digit_code[0]) / 100.0      # Maksimum kamburluk (chord %'si)
    p = int(digit_code[1]) / 10.0       # Maksimum kamburluk konumu
    t = int(digit_code[2:]) / 100.0     # Maksimum kalınlık (chord %'si)
    
    x_coords = []
    # Kök ve hücum kenarında yoğunlaşan kosinüs dağılımı
    for i in range(num_points):
        beta = math.pi * i / (num_points - 1)
        x = 0.5 * (1.0 - math.cos(beta))
        x_coords.append(x)
        
    upper_surface = []
    lower_surface = []
    camber_line = []
    
    for x in x_coords:
        # Kalınlık dağılımı
        yt = 5.0 * t * (0.2969 * math.sqrt(x) - 0.1260 * x - 0.3516 * (x**2) + 0.2843 * (x**3) - 0.1015 * (x**4) if x >= 0 else 0)
        
        # Ortalama kamburluk çizgisi (Camber line)
        if p == 0 or m == 0:
            yc = 0.0
            dyc_dx = 0.0
        else:
            if x <= p:
                yc = (m / (p ** 2)) * (2.0 * p * x - (x ** 2))
                dyc_dx = (2.0 * m / (p ** 2)) * (p - x)
            else:
                yc = (m / ((1.0 - p) ** 2)) * ((1.0 - 2.0 * p) + 2.0 * p * x - (x ** 2))
                dyc_dx = (2.0 * m / ((1.0 - p) ** 2)) * (p - x)
                
        theta = math.atan(dyc_dx)
        
        xu = x - yt * math.sin(theta)
        yu = yc + yt * math.cos(theta)
        xl = x + yt * math.sin(theta)
        yl = yc - yt * math.cos(theta)
        
        upper_surface.append((round(xu, 4), round(yu, 4)))
        lower_surface.append((round(xl, 4), round(yl, 4)))
        camber_line.append((round(x, 4), round(yc, 4)))
        
    return {
        "NACA Kodu": digit_code,
        "Maksimum Kamburluk m (% chord)": m * 100.0,
        "Maksimum Kamburluk Konumu p": p,
        "Maksimum Kalınlık t (% chord)": t * 100.0,
        "Ust Yuzey (Xu, Yu)": upper_surface,
        "Alt Yuzey (Xl, Yl)": lower_surface,
        "Kamburluk Cizgisi (Xc, Yc)": camber_line
    }, None

def calculate_aerodynamic_lift_drag(cl_slope_2pi, alpha_deg, wing_area_m2, aspect_ratio, span_eff_e=0.85, cd0=0.015, dynamic_pressure_pa=1000.0, alpha_zero_lift_deg=0.0):
    """
    İnce profil teorisi ve Prandtl taşıma çizgisi modeline göre Taşıma (Lift), İndüklenmiş Sürükleme (Drag) ve L/D oranını hesaplar.
    """
    if wing_area_m2 <= 0 or aspect_ratio <= 0 or dynamic_pressure_pa <= 0:
        return None, "Geometri ve basınç pozitif olmalıdır."
        
    alpha_rad = math.radians(alpha_deg - alpha_zero_lift_deg)
    
    # 2D kaldırma eğrisi eğimi (2pi rad^-1) ve 3D sonlu kanat düzeltmesi:
    # a_3d = a_2d / (1 + a_2d / (pi * AR * e))
    a_2d = 2.0 * math.pi
    a_3d = a_2d / (1.0 + (a_2d / (math.pi * aspect_ratio * span_eff_e)))
    
    cl = a_3d * alpha_rad
    # İndüklenmiş sürükleme katsayısı: C_di = C_L^2 / (pi * AR * e)
    cd_ind = (cl ** 2) / (math.pi * aspect_ratio * span_eff_e)
    cd_total = cd0 + cd_ind
    
    lift_force_n = cl * dynamic_pressure_pa * wing_area_m2
    drag_force_n = cd_total * dynamic_pressure_pa * wing_area_m2
    lift_to_drag = cl / cd_total if cd_total > 0 else 0.0
    
    return {
        "Hücum Açısı α (derece)": alpha_deg,
        "Taşıma Katsayısı (CL)": cl,
        "Parazit Sürükleme Katsayısı (CD0)": cd0,
        "İndüklenmiş Sürükleme (CDi)": cd_ind,
        "Toplam Sürükleme Katsayısı (CD)": cd_total,
        "Süzülme / Verim Oranı (L/D)": lift_to_drag,
        "Toplam Taşıma Kuvveti (Lift - Newton)": lift_force_n,
        "Toplam Taşıma Kuvveti (Lift - kgf)": lift_force_n / 9.80665,
        "Toplam Sürükleme Kuvveti (Drag - Newton)": drag_force_n
    }, None

def interactive_isa():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}   ULUSLARARASI STANDART ATMOSFER (ISA) MODELİ    {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("İrtifaya bağlı hava yoğunluğu, basınç, sıcaklık ve ses hızı hesabı.")
    print("-" * 50)
    try:
        alt = float(input("Uçuş İrtifası (metre, 0 - 20000): "))
        v_in = input("Uçuş Hızı (km/h) [İsteğe bağlı, boş geçilebilir]: ").strip()
        v = float(v_in) if v_in else None
        
        res, err = calculate_isa_atmosphere(alt, v)
        if err:
            print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}>>> ISA ATMOSFERİK DEĞERLERİ <<<{Colors.ENDC}")
            for k, val in res.items():
                if isinstance(val, float):
                    print(f"  {k:<38}: {Colors.BOLD}{val:12.4f}{Colors.ENDC}")
                else:
                    print(f"  {k:<38}: {Colors.OKCYAN}{val}{Colors.ENDC}")
    except ValueError:
        print(f"{Colors.FAIL}Hata: Sayısal değer giriniz.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def interactive_naca():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}    NACA 4-BASAMAKLI KANAT PROFİLİ GEOMETRİSİ     {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("Örnek profiller: 0012 (Simetrik), 2412 (Genel Havacılık), 4415 (Planör)")
    print("-" * 50)
    code = input("NACA Kodu [Varsayılan: 2412]: ").strip() or "2412"
    res, err = generate_naca_4digit(code, num_points=11)
    if err:
        print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
    else:
        print(f"\n{Colors.OKGREEN}>>> NACA {code} PROFİL VERİLERİ <<<{Colors.ENDC}")
        print(f"Maksimum Kamburluk : %{res['Maksimum Kamburluk m (% chord)']:.1f}")
        print(f"Maksimum Kalınlık  : %{res['Maksimum Kalınlık t (% chord)']:.1f}")
        print("-" * 50)
        print(f"{'X/c':<8} | {'Üst Yüzey (Yu)':<16} | {'Alt Yüzey (Yl)':<16} | {'Kamburluk (Yc)'}")
        print("-" * 50)
        for i in range(len(res["Ust Yuzey (Xu, Yu)"])):
            xu, yu = res["Ust Yuzey (Xu, Yu)"][i]
            xl, yl = res["Alt Yuzey (Xl, Yl)"][i]
            xc, yc = res["Kamburluk Cizgisi (Xc, Yc)"][i]
            print(f"{xu:8.4f} | {yu:16.4f} | {yl:16.4f} | {yc:16.4f}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def interactive_aerodynamics():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}   KANAT AERODİNAMİK TAŞIMA & SÜRÜKLEME ANALİZİ   {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("İnce profil teorisi ve Prandtl taşıma çizgisi modeli.")
    print("-" * 50)
    try:
        alpha = float(input("Hücum Açısı α (derece) [Örn: 5.0]: "))
        area = float(input("Kanat Referans Alanı S (m²) [Örn: 16.0]: "))
        ar = float(input("Kanat Açıklık Oranı (Aspect Ratio - AR) [Örn: 7.5]: "))
        q_pa = float(input("Dinamik Basınç q (Pa) [Örn: 1500]: "))
        
        res, err = calculate_aerodynamic_lift_drag(2.0 * math.pi, alpha, area, ar, dynamic_pressure_pa=q_pa)
        if err:
            print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}>>> AERODİNAMİK KUVVET SONUÇLARI <<<{Colors.ENDC}")
            for k, val in res.items():
                print(f"  {k:<42}: {Colors.BOLD}{val:10.4f}{Colors.ENDC}")
    except ValueError:
        print(f"{Colors.FAIL}Hata: Sayısal değer giriniz.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def main():
    if os.name == 'nt':
        os.system('color')
    while True:
        clear_screen()
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}   ✈️  HAVACILIK VE AERODİNAMİK MÜHENDİSLİĞİ      {Colors.ENDC}")
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.OKCYAN}1.{Colors.ENDC} Uluslararası Standart Atmosfer (ISA) ve Mach Sayısı")
        print(f"{Colors.OKCYAN}2.{Colors.ENDC} NACA 4-Basamaklı Kanat Profili Geometrisi")
        print(f"{Colors.OKCYAN}3.{Colors.ENDC} Kanat Taşıma (Lift), Sürükleme (Drag) ve L/D Analizi")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Geri Dön")
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        if secim == '1':
            interactive_isa()
        elif secim == '2':
            interactive_naca()
        elif secim == '3':
            interactive_aerodynamics()
        elif secim == '0':
            break

if __name__ == "__main__":
    main()
