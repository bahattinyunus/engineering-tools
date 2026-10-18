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

# Yaygın Malzeme Elastisite Modülleri (GPa) ve Akma Mukavemetleri (MPa)
DEFAULT_MATERIALS = {
    "celik_s235": {"name": "Yapı Çeliği (S235)", "E": 210.0, "Sy": 235.0},
    "celik_s355": {"name": "Yüksek Mukavemetli Çelik (S355)", "E": 210.0, "Sy": 355.0},
    "aluminyum_6061": {"name": "Alüminyum (6061-T6)", "E": 69.0, "Sy": 275.0},
    "titanyum_ti6al4v": {"name": "Titanyum (Ti-6Al-4V)", "E": 114.0, "Sy": 880.0},
    "ahsap_mese": {"name": "Ahşap (Meşe)", "E": 12.0, "Sy": 40.0}
}

def calculate_section_properties(section_type, **kwargs):
    """
    En kesit geometrisi atalet momentini (I mm^4), mukavemet momentini (W mm^3) ve alanı (A mm^2) hesaplar.
    """
    if section_type == "rectangle":
        b = kwargs.get("b", 0) # mm
        h = kwargs.get("h", 0) # mm
        if b <= 0 or h <= 0:
            return None, "Boyutlar pozitif olmalıdır."
        area = b * h
        i_x = (b * (h ** 3)) / 12.0
        w_x = (b * (h ** 2)) / 6.0
        return {"Alan (mm²)": area, "Atalet Momenti Ix (mm⁴)": i_x, "Mukavemet Momenti Wx (mm³)": w_x, "Tip": f"Dikdörtgen {b}x{h} mm"}, None

    elif section_type == "circle":
        d = kwargs.get("d", 0) # mm
        if d <= 0:
            return None, "Çap pozitif olmalıdır."
        area = math.pi * (d ** 2) / 4.0
        i_x = math.pi * (d ** 4) / 64.0
        w_x = math.pi * (d ** 3) / 32.0
        return {"Alan (mm²)": area, "Atalet Momenti Ix (mm⁴)": i_x, "Mukavemet Momenti Wx (mm³)": w_x, "Tip": f"Dolu Daire Ø{d} mm"}, None

    elif section_type == "pipe":
        d_out = kwargs.get("d_out", 0)
        t = kwargs.get("t", 0) # et kalınlığı
        d_in = d_out - 2.0 * t
        if d_out <= 0 or t <= 0 or d_in <= 0:
            return None, "Geçersiz boru boyutları veya et kalınlığı."
        area = (math.pi / 4.0) * (d_out ** 2 - d_in ** 2)
        i_x = (math.pi / 64.0) * (d_out ** 4 - d_in ** 4)
        w_x = (2.0 * i_x) / d_out
        return {"Alan (mm²)": area, "Atalet Momenti Ix (mm⁴)": i_x, "Mukavemet Momenti Wx (mm³)": w_x, "Tip": f"Boru Ø{d_out}x{t} mm"}, None

    elif section_type == "box":
        b_out = kwargs.get("b_out", 0)
        h_out = kwargs.get("h_out", 0)
        t = kwargs.get("t", 0)
        b_in = b_out - 2.0 * t
        h_in = h_out - 2.0 * t
        if b_out <= 0 or h_out <= 0 or t <= 0 or b_in <= 0 or h_in <= 0:
            return None, "Geçersiz kutu profil boyutları."
        area = (b_out * h_out) - (b_in * h_in)
        i_x = (b_out * (h_out ** 3) - b_in * (h_in ** 3)) / 12.0
        w_x = (2.0 * i_x) / h_out
        return {"Alan (mm²)": area, "Atalet Momenti Ix (mm⁴)": i_x, "Mukavemet Momenti Wx (mm³)": w_x, "Tip": f"Kutu Profil {b_out}x{h_out}x{t} mm"}, None

    else:
        return None, "Desteklenmeyen kesit tipi."

def calculate_beam_mechanics(load_case, load_value, length_m, i_x_mm4, w_x_mm3, e_gpa, sy_mpa):
    """
    Kiriş maksimum eğilme momenti, maksimum sehim ve eğilme gerilmesini hesaplar.
    
    load_case:
      1: Basit Mesnetli, Ortadan Tekil Yük F (N)
      2: Basit Mesnetli, Düzgün Yayılı Yük q (N/m)
      3: Konsol (Ankastre), Uçtan Tekil Yük F (N)
      4: Konsol (Ankastre), Düzgün Yayılı Yük q (N/m)
    """
    if length_m <= 0 or i_x_mm4 <= 0 or w_x_mm3 <= 0 or e_gpa <= 0 or sy_mpa <= 0:
        return None, "Girdiler pozitif olmalıdır."
    
    l_mm = length_m * 1000.0 # metre -> mm
    e_mpa = e_gpa * 1000.0   # GPa -> MPa (N/mm^2)
    
    if load_case == 1:
        case_name = "Basit Mesnetli Kiriş - Ortadan Tekil Yük (F)"
        f_n = load_value # Newton
        # M_max = F * L / 4 (N*mm)
        m_max_nmm = (f_n * l_mm) / 4.0
        # delta_max = (F * L^3) / (48 * E * I)
        delta_max_mm = (f_n * (l_mm ** 3)) / (48.0 * e_mpa * i_x_mm4)
    elif load_case == 2:
        case_name = "Basit Mesnetli Kiriş - Düzgün Yayılı Yük (q)"
        q_n_mm = load_value / 1000.0 # N/m -> N/mm
        # M_max = q * L^2 / 8 (N*mm)
        m_max_nmm = (q_n_mm * (l_mm ** 2)) / 8.0
        # delta_max = 5 * q * L^4 / (384 * E * I)
        delta_max_mm = (5.0 * q_n_mm * (l_mm ** 4)) / (384.0 * e_mpa * i_x_mm4)
    elif load_case == 3:
        case_name = "Konsol (Ankastre) Kiriş - Uçtan Tekil Yük (F)"
        f_n = load_value # Newton
        # M_max = F * L
        m_max_nmm = f_n * l_mm
        # delta_max = (F * L^3) / (3 * E * I)
        delta_max_mm = (f_n * (l_mm ** 3)) / (3.0 * e_mpa * i_x_mm4)
    elif load_case == 4:
        case_name = "Konsol (Ankastre) Kiriş - Düzgün Yayılı Yük (q)"
        q_n_mm = load_value / 1000.0 # N/m -> N/mm
        # M_max = q * L^2 / 2
        m_max_nmm = (q_n_mm * (l_mm ** 2)) / 2.0
        # delta_max = (q * L^4) / (8 * E * I)
        delta_max_mm = (q_n_mm * (l_mm ** 4)) / (8.0 * e_mpa * i_x_mm4)
    else:
        return None, "Geçersiz yükleme durumu."
        
    m_max_nm = m_max_nmm / 1000.0 # N*m
    
    # Maksimum Gerilme: sigma = M_max / W_x (MPa)
    sigma_max_mpa = m_max_nmm / w_x_mm3
    
    # Emniyet Faktörü (Safety Factor)
    safety_factor = sy_mpa / sigma_max_mpa if sigma_max_mpa > 0 else 999.0
    
    # İzin verilen sehim (Standard L/300)
    allowable_deflection_mm = l_mm / 300.0
    deflection_pass = delta_max_mm <= allowable_deflection_mm
    
    return {
        "Yükleme Durumu": case_name,
        "Kiriş Açıklığı (L)": f"{length_m:.2f} m ({l_mm:.0f} mm)",
        "Maksimum Eğilme Momenti": f"{m_max_nm:.2f} N·m ({m_max_nmm:.1f} N·mm)",
        "Maksimum Eğilme Gerilmesi (σ_max)": f"{sigma_max_mpa:.2f} MPa",
        "Malzeme Akma Dayanımı (Sy)": f"{sy_mpa:.1f} MPa",
        "Emniyet Katsayısı (SF = Sy / σ)": f"{safety_factor:.2f}",
        "Maksimum Sehim (Çökme - δ_max)": f"{delta_max_mm:.3f} mm",
        "İzin Verilen Sehim Sınırı (L/300)": f"{allowable_deflection_mm:.3f} mm",
        "Gerilme Emniyeti": "GÜVENLİ (SF >= 1.5)" if safety_factor >= 1.5 else ("KRİTİK (1.0 <= SF < 1.5)" if safety_factor >= 1.0 else "GÜVENSİZ (AKMA MEYDANA GELDİ)"),
        "Sehim Uygunluğu": "UYGUN (δ <= L/300)" if deflection_pass else "LİMİT AŞILDI (Kiriş Aşırı Eğildi)"
    }, None

def interactive_beam_stress():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}    KİRİŞ EĞİLME GERİLMESİ VE SEHİM ANALİZİ       {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("Mukavemet ve Yapı Mühendisliği standart kiriş analizi.")
    print("-" * 50)
    
    # 1. Kesit Seçimi
    print("En Kesit Tipini Seçin:")
    print("1. Dolu Dikdörtgen (b x h)")
    print("2. Dolu Daire / Mil (Çap D)")
    print("3. Boru / Silindirik Tüp (Dış Çap x Et Kalınlığı)")
    print("4. Kutu Profil (Dış b x Dış h x Et Kalınlığı)")
    sec_choice = input("Seçiminiz [1-4]: ").strip()
    
    try:
        if sec_choice == "1":
            b = float(input("Genişlik b (mm): "))
            h = float(input("Yükseklik h (mm): "))
            sec_props, err = calculate_section_properties("rectangle", b=b, h=h)
        elif sec_choice == "2":
            d = float(input("Çap d (mm): "))
            sec_props, err = calculate_section_properties("circle", d=d)
        elif sec_choice == "3":
            d_out = float(input("Dış Çap (mm): "))
            t = float(input("Et Kalınlığı t (mm): "))
            sec_props, err = calculate_section_properties("pipe", d_out=d_out, t=t)
        elif sec_choice == "4":
            b_out = float(input("Dış Genişlik (mm): "))
            h_out = float(input("Dış Yükseklik (mm): "))
            t = float(input("Et Kalınlığı t (mm): "))
            sec_props, err = calculate_section_properties("box", b_out=b_out, h_out=h_out, t=t)
        else:
            print(f"{Colors.FAIL}Geçersiz kesit seçimi.{Colors.ENDC}")
            input("Devam etmek için Enter...")
            return

        if err:
            print(f"{Colors.FAIL}Kesit Hatası: {err}{Colors.ENDC}")
            input("Devam etmek için Enter...")
            return

        ix = sec_props["Atalet Momenti Ix (mm⁴)"]
        wx = sec_props["Mukavemet Momenti Wx (mm³)"]
        print(f"\n{Colors.OKCYAN}Kesit Özellikleri ({sec_props['Tip']}):{Colors.ENDC}")
        print(f"  Ix = {ix:.1f} mm⁴ | Wx = {wx:.1f} mm³ | Alan = {sec_props['Alan (mm²)']:.1f} mm²")

        # 2. Malzeme Seçimi
        print("\nMalzeme Seçimi:")
        print("1. Yapı Çeliği (S235: E=210 GPa, Sy=235 MPa)")
        print("2. Yüksek Mukavemetli Çelik (S355: E=210 GPa, Sy=355 MPa)")
        print("3. Alüminyum (6061-T6: E=69 GPa, Sy=275 MPa)")
        print("4. Özel Malzeme (Manuel giriş)")
        mat_choice = input("Seçiminiz [Varsayılan: 1]: ").strip()
        
        if mat_choice == "2":
            mat = DEFAULT_MATERIALS["celik_s355"]
        elif mat_choice == "3":
            mat = DEFAULT_MATERIALS["aluminyum_6061"]
        elif mat_choice == "4":
            e_gpa = float(input("Elastisite Modülü E (GPa): "))
            sy_mpa = float(input("Akma Dayanımı Sy (MPa): "))
            mat = {"E": e_gpa, "Sy": sy_mpa}
        else:
            mat = DEFAULT_MATERIALS["celik_s235"]

        # 3. Yükleme ve Geometri
        print("\nYükleme ve Mesnet Durumu:")
        print("1. Basit Mesnetli Kiriş - Ortadan Tekil Yük (F)")
        print("2. Basit Mesnetli Kiriş - Düzgün Yayılı Yük (q)")
        print("3. Konsol Kiriş (Ankastre) - Serbest Uçtan Tekil Yük (F)")
        print("4. Konsol Kiriş (Ankastre) - Düzgün Yayılı Yük (q)")
        case_choice = int(input("Yükleme Durumu [1-4]: ").strip() or "1")
        
        length_m = float(input("Kiriş Boyu L (metre): "))
        if case_choice in [1, 3]:
            load_val = float(input("Uygulanan Yük F (Newton): "))
        else:
            load_val = float(input("Yayılı Yük q (Newton / metre): "))

        results, err = calculate_beam_mechanics(case_choice, load_val, length_m, ix, wx, mat["E"], mat["Sy"])
        if err:
            print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}================= MUKAVEMET RAPORU ================={Colors.ENDC}")
            for k, v in results.items():
                if "UYGUN" in str(v) or "GÜVENLİ" in str(v):
                    color = Colors.OKGREEN
                elif "KRİTİK" in str(v):
                    color = Colors.WARNING
                elif "GÜVENSİZ" in str(v) or "AŞILDI" in str(v):
                    color = Colors.FAIL
                else:
                    color = Colors.BOLD
                print(f"  {k:<38}: {color}{v}{Colors.ENDC}")
            print(f"{Colors.OKGREEN}===================================================={Colors.ENDC}")

    except ValueError:
        print(f"{Colors.FAIL}Hata: Lütfen geçerli sayısal değerler girin.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def main():
    if os.name == 'nt':
        os.system('color')
    interactive_beam_stress()

if __name__ == "__main__":
    main()
