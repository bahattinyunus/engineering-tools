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

# Tipik Boru Pürüzlülük Değerleri (mm)
PIPE_ROUGHNESS_MM = {
    "ticari_celik": 0.045,
    "paslanmaz_celik": 0.015,
    "pvc_plastik": 0.0015,
    "bakir": 0.0015,
    "dokum_demir": 0.26
}

def calculate_pipe_friction(flow_rate_m3h, inner_dia_mm, pipe_length_m, roughness_mm=0.045, density_kg_m3=1000.0, dynamic_visc_pa_s=0.001):
    """
    Darcy-Weisbach ve Haaland denklemlerini kullanarak boru basınç kaybını ve Reynolds sayısını hesaplar.
    """
    if flow_rate_m3h <= 0 or inner_dia_mm <= 0 or pipe_length_m <= 0:
        return None, "Debi, çap ve uzunluk pozitif olmalıdır."
    
    # Birim dönüşümleri
    d_m = inner_dia_mm / 1000.0
    q_m3_s = flow_rate_m3h / 3600.0
    area = math.pi * (d_m ** 2) / 4.0
    velocity = q_m3_s / area
    
    # Reynolds Sayısı
    re = (density_kg_m3 * velocity * d_m) / dynamic_visc_pa_s
    
    # Akış Rejimi ve Sürtünme Faktörü (f)
    if re < 2300:
        flow_regime = "Laminer Akış"
        f = 64.0 / re if re > 0 else 0.064
    elif re <= 4000:
        flow_regime = "Kritik / Geçiş Bölgesi"
        # Geçiş bölgesi interpolasyonu
        f_lam = 64.0 / 2300.0
        # Haaland for 4000
        rel_roughness = (roughness_mm / 1000.0) / d_m
        inv_sqrt_f = -1.8 * math.log10(((rel_roughness / 3.7) ** 1.11) + (6.9 / 4000.0))
        f_turb = (1.0 / inv_sqrt_f) ** 2
        f = f_lam + (f_turb - f_lam) * ((re - 2300.0) / 1700.0)
    else:
        flow_regime = "Türbülanslı Akış"
        rel_roughness = (roughness_mm / 1000.0) / d_m
        inv_sqrt_f = -1.8 * math.log10(((rel_roughness / 3.7) ** 1.11) + (6.9 / re))
        f = (1.0 / inv_sqrt_f) ** 2
        
    # Darcy-Weisbach Basınç Düşüşü: Delta P = f * (L / D) * (rho * v^2 / 2)
    dynamic_pressure = 0.5 * density_kg_m3 * (velocity ** 2)
    delta_p_pa = f * (pipe_length_m / d_m) * dynamic_pressure
    delta_p_bar = delta_p_pa / 100000.0
    head_loss_m = delta_p_pa / (density_kg_m3 * 9.81) # Metre Su Sütunu (mSS)
    
    return {
        "Akış Hızı (m/s)": velocity,
        "Reynolds Sayısı (Re)": re,
        "Akış Rejimi": flow_regime,
        "Darcy Sürtünme Katsayısı (f)": f,
        "Dinamik Basınç (Pa)": dynamic_pressure,
        "Basınç Kaybı (Pascal)": delta_p_pa,
        "Basınç Kaybı (Bar)": delta_p_bar,
        "Yük Kaybı (mSS)": head_loss_m
    }, None

def calculate_heat_exchanger_lmtd(th_in, th_out, tc_in, tc_out, u_coeff, flow_type="counter"):
    """
    Isı Eşanjörü Logaritmik Ortalama Sıcaklık Farkı (LMTD) ve Isı Transfer Alanı hesabı.
    flow_type: 'counter' (karşıt akış) veya 'parallel' (paralel akış)
    """
    if flow_type == "counter":
        dt1 = th_in - tc_out
        dt2 = th_out - tc_in
    else: # parallel
        dt1 = th_in - tc_in
        dt2 = th_out - tc_out
        
    if dt1 <= 0 or dt2 <= 0:
        return None, "Sıcaklık farkları termodinamik olarak sıfırdan büyük olmalıdır (2. yasa ihlali)."
        
    if abs(dt1 - dt2) < 1e-6:
        lmtd = dt1
    else:
        lmtd = (dt1 - dt2) / math.log(dt1 / dt2)
        
    # Gerekli eşanjör alanı: Q = U * A * LMTD  => A = Q / (U * LMTD)
    # Burada U_coeff W/(m^2*K) cinsindendir.
    return {
        "Akış Modeli": "Karşıt Akış (Counter-flow)" if flow_type == "counter" else "Paralel Akış (Parallel-flow)",
        "Delta T1 (°C)": dt1,
        "Delta T2 (°C)": dt2,
        "LMTD (°C)": lmtd,
        "Toplam Isı Geçiş Katsayısı U (W/m²K)": u_coeff
    }, None

def calculate_solution_dilution(c1, v1, c2, v2_desired=None, target_c=None):
    """
    Çözelti Derişim ve Seyreltme Dengesi (C1 * V1 + C2 * V2 = C_final * V_final).
    """
    if target_c is not None:
        # C1*V1 = C_target * V_final  (Saf çözücü ekleme ile seyreltme C2=0)
        if target_c >= c1:
            return None, "Hedef derişim seyreltmede başlangıç derişiminden küçük olmalıdır."
        # V_final = (C1 * V1) / target_c
        v_final = (c1 * v1) / target_c
        added_solvent = v_final - v1
        return {
            "Başlangıç Konsantrasyonu (C1)": c1,
            "Başlangıç Hacmi (V1)": v1,
            "Hedef Konsantrasyon (Cf)": target_c,
            "Gereken Toplam Hacim (Vf)": v_final,
            "Eklenmesi Gereken Çözücü Miktarı": added_solvent
        }, None
    else:
        # İki çözeltinin karışımı: C_final = (C1*V1 + C2*V2) / (V1 + V2)
        v_final = v1 + v2_desired
        if v_final <= 0:
            return None, "Toplam hacim sıfırdan büyük olmalıdır."
        c_final = (c1 * v1 + c2 * v2_desired) / v_final
        return {
            "1. Çözelti (C1, V1)": f"{c1}% , {v1} L",
            "2. Çözelti (C2, V2)": f"{c2}% , {v2_desired} L",
            "Toplam Son Hacim (Vf)": v_final,
            "Son Karışım Derişimi (Cf)": c_final
        }, None

def interactive_pipe_flow():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}   BORU BASINÇ DÜŞÜŞÜ & REYNOLDS ANALİZİ          {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("Darcy-Weisbach ve Haaland formülleri ile hidrolik hesaplama.")
    print("-" * 50)
    try:
        q = float(input("Hacimsel Debi (m³/h): "))
        d = float(input("Boru İç Çapı (mm): "))
        l = float(input("Boru Toplam Eşdeğer Uzunluğu (m): "))
        
        print("\nBoru Malzemesi:")
        print("1. Ticari Çelik (e = 0.045 mm)")
        print("2. Paslanmaz Çelik (e = 0.015 mm)")
        print("3. PVC / Plastik / Bakır (e = 0.0015 mm)")
        print("4. Döküm Demir (e = 0.26 mm)")
        mat_sel = input("Seçiminiz [Varsayılan: 1]: ").strip()
        rough_map = {"1": 0.045, "2": 0.015, "3": 0.0015, "4": 0.26}
        roughness = rough_map.get(mat_sel, 0.045)
        
        rho_in = input("Akışkan Yoğunluğu (kg/m³) [Su: 1000]: ").strip()
        rho = float(rho_in) if rho_in else 1000.0
        
        visc_in = input("Dinamik Viskozite (Pa.s) [Su 20°C: 0.001]: ").strip()
        visc = float(visc_in) if visc_in else 0.001
        
        res, err = calculate_pipe_friction(q, d, l, roughness, rho, visc)
        if err:
            print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}>>> HİDROLİK HESAPLAMA SONUÇLARI <<<{Colors.ENDC}")
            for k, v in res.items():
                if isinstance(v, float):
                    print(f"  {k:<32}: {Colors.BOLD}{v:12.4f}{Colors.ENDC}")
                else:
                    print(f"  {k:<32}: {Colors.OKCYAN}{v}{Colors.ENDC}")
    except ValueError:
        print(f"{Colors.FAIL}Hata: Lütfen geçerli sayısal değerler girin.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def interactive_lmtd():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}    ISI EŞANJÖRÜ LMTD VE ALAN HESAPLAYICI         {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("Karşıt ve paralel akışlı eşanjörlerde sıcaklık farkı ve transfer alanı.")
    print("-" * 50)
    try:
        th_in = float(input("Sıcak Akışkan Giriş Sıcaklığı Th,in (°C): "))
        th_out = float(input("Sıcak Akışkan Çıkış Sıcaklığı Th,out (°C): "))
        tc_in = float(input("Soğuk Akışkan Giriş Sıcaklığı Tc,in (°C): "))
        tc_out = float(input("Soğuk Akışkan Çıkış Sıcaklığı Tc,out (°C): "))
        
        flow_sel = input("Akış Tipi: [1] Karşıt Akış (Counter) | [2] Paralel Akış [Varsayılan: 1]: ").strip()
        flow_type = "parallel" if flow_sel == "2" else "counter"
        
        u = float(input("Toplam Isı Geçiş Katsayısı U (W/m²·K) [Örn: Su-Su için 1200]: ") or "1200")
        
        q_kw = float(input("Aktarılacak Isı Yükü Q (kW) [İsteğe bağlı, alan hesabı için]: ") or "0")
        
        res, err = calculate_heat_exchanger_lmtd(th_in, th_out, tc_in, tc_out, u, flow_type)
        if err:
            print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}>>> EŞANJÖR LMTD ANALİZİ <<<{Colors.ENDC}")
            for k, v in res.items():
                if isinstance(v, float):
                    print(f"  {k:<36}: {Colors.BOLD}{v:10.2f}{Colors.ENDC}")
                else:
                    print(f"  {k:<36}: {Colors.OKCYAN}{v}{Colors.ENDC}")
            
            if q_kw > 0:
                lmtd = res["LMTD (°C)"]
                area = (q_kw * 1000.0) / (u * lmtd)
                print(f"  {'Gerekli Isı Transfer Alanı A (m²)':<36}: {Colors.OKGREEN}{area:10.2f} m²{Colors.ENDC}")
    except ValueError:
        print(f"{Colors.FAIL}Hata: Lütfen geçerli sayısal değerler girin.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def interactive_dilution():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}   KİMYASAL KARIŞIM VE SEYRELTME HESAPLAYICI      {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("[1] Saf çözücü ile hedef konsantrasyona seyreltme")
    print("[2] İki farklı derişimdeki çözeltiyi karıştırma")
    print("-" * 50)
    choice = input("İşlem seçimi (1 / 2): ").strip()
    try:
        if choice == "1":
            c1 = float(input("Başlangıç Konsantrasyonu (Örn: %30 için 30): "))
            v1 = float(input("Başlangıç Çözelti Hacmi (Litre): "))
            target_c = float(input("Ulaşılmak İstenen Konsantrasyon (Örn: %10 için 10): "))
            res, err = calculate_solution_dilution(c1, v1, 0, target_c=target_c)
        else:
            c1 = float(input("1. Çözelti Konsantrasyonu (%): "))
            v1 = float(input("1. Çözelti Hacmi (Litre): "))
            c2 = float(input("2. Çözelti Konsantrasyonu (%): "))
            v2 = float(input("2. Çözelti Hacmi (Litre): "))
            res, err = calculate_solution_dilution(c1, v1, c2, v2_desired=v2)
            
        if err:
            print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}>>> KİMYASAL KARIŞIM SONUÇLARI <<<{Colors.ENDC}")
            for k, v in res.items():
                if isinstance(v, float):
                    print(f"  {k:<36}: {Colors.BOLD}{v:10.2f}{Colors.ENDC}")
                else:
                    print(f"  {k:<36}: {Colors.BOLD}{v}{Colors.ENDC}")
    except ValueError:
        print(f"{Colors.FAIL}Hata: Lütfen geçerli sayısal değerler girin.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def main():
    if os.name == 'nt':
        os.system('color')
        
    while True:
        clear_screen()
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}   🧪 KİMYA VE SÜREÇ MÜHENDİSLİĞİ ARAÇLARI        {Colors.ENDC}")
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.OKCYAN}1.{Colors.ENDC} Boru Akışı Basınç Düşüşü & Reynolds Analizi")
        print(f"{Colors.OKCYAN}2.{Colors.ENDC} Isı Eşanjörü LMTD ve Transfer Alanı Hesabı")
        print(f"{Colors.OKCYAN}3.{Colors.ENDC} Çözelti Karışımı ve Seyreltme Hesabı")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Geri Dön")
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        
        if secim == '1':
            interactive_pipe_flow()
        elif secim == '2':
            interactive_lmtd()
        elif secim == '3':
            interactive_dilution()
        elif secim == '0':
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim!{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

if __name__ == "__main__":
    main()
