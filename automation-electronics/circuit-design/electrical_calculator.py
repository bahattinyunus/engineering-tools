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

# Özdirençler (Ohm * mm^2 / m, 20°C standart)
RESISTIVITY = {
    "bakir": 0.0175,
    "aluminyum": 0.0282
}

def calculate_voltage_drop(voltage, current, length_m, section_mm2, material="bakir", system_type="3phase", cos_phi=0.85):
    """
    Kablo gerilim düşümü ve güç kaybı hesaplar (IEC 60364-5-52 standartlarına uygun).
    system_type: '1phase' (230V AC / DC) veya '3phase' (400V AC)
    """
    if section_mm2 <= 0 or length_m <= 0 or voltage <= 0 or current <= 0:
        return None, "Değerler sıfırdan büyük olmalıdır."
    
    rho = RESISTIVITY.get(material.lower(), RESISTIVITY["bakir"])
    resistance = (rho * length_m) / section_mm2
    
    if system_type == "1phase":
        # Tek faz veya 2 iletkenli DC: Gidiş-dönüş toplam direnç 2 * R
        v_drop = 2.0 * length_m * current * cos_phi * rho / section_mm2
        power_loss = 2.0 * (current ** 2) * resistance
    else:
        # Dengeli üç faz: delta_U = sqrt(3) * I * L * (rho/S) * cos(phi)
        v_drop = math.sqrt(3) * length_m * current * cos_phi * rho / section_mm2
        power_loss = 3.0 * (current ** 2) * resistance

    pct_drop = (v_drop / voltage) * 100.0
    
    # Standart tolerans değerlendirmesi (Aydınlatma maks %3, Güç/Pano maks %5)
    compliant_lighting = pct_drop <= 3.0
    compliant_power = pct_drop <= 5.0
    
    return {
        "Sistem Gerilimi (V)": voltage,
        "Hat Akımı (A)": current,
        "Hat Uzunluğu (m)": length_m,
        "Kablo Kesiti (mm2)": section_mm2,
        "İletken Malzemesi": material.capitalize(),
        "Sistem Tipi": "3 Faz AC (400V)" if system_type == "3phase" else "1 Faz AC / DC",
        "Güç Faktörü (cos φ)": cos_phi,
        "Hat Direnci (Tek Kol - Ω)": resistance,
        "Gerilim Düşümü (V)": v_drop,
        "Gerilim Düşümü Oranı (%)": pct_drop,
        "Kablo Güç Kaybı (W)": power_loss,
        "Aydınlatma Uygunluğu (<= %3)": "UYGUN" if compliant_lighting else "AŞILDI (Kesit Artırılmalı)",
        "Motor/Güç Uygunluğu (<= %5)": "UYGUN" if compliant_power else "AŞILDI (Kesit Artırılmalı)"
    }, None

def calculate_filter_resonance(r_ohm, l_henry, c_farad):
    """
    RC, RL ve RLC filtre frekans tepkilerini hesaplar.
    """
    results = {}
    
    # RC Alçak/Yüksek Geçiren Kesim Frekansı: fc = 1 / (2 * pi * R * C)
    if r_ohm > 0 and c_farad > 0:
        fc_rc = 1.0 / (2.0 * math.pi * r_ohm * c_farad)
        results["RC Kesim Frekansı (Cutoff fc - Hz)"] = fc_rc
        results["RC Zaman Sabiti (Tau = R*C - s)"] = r_ohm * c_farad
        
    # RL Kesim Frekansı: fc = R / (2 * pi * L)
    if r_ohm > 0 and l_henry > 0:
        fc_rl = r_ohm / (2.0 * math.pi * l_henry)
        results["RL Kesim Frekansı (fc - Hz)"] = fc_rl
        results["RL Zaman Sabiti (Tau = L/R - s)"] = l_henry / r_ohm
        
    # RLC Rezonans Frekansı: f0 = 1 / (2 * pi * sqrt(L * C))
    if l_henry > 0 and c_farad > 0:
        f0 = 1.0 / (2.0 * math.pi * math.sqrt(l_henry * c_farad))
        results["RLC Rezonans Frekansı (f0 - Hz)"] = f0
        
        # Seri RLC Kalite Faktörü (Q) ve Bant Genişliği (BW)
        if r_ohm > 0:
            q_factor = (1.0 / r_ohm) * math.sqrt(l_henry / c_farad)
            bw = f0 / q_factor if q_factor > 0 else 0
            results["Seri RLC Kalite Faktörü (Q)"] = q_factor
            results["Seri RLC Bant Genişliği (BW - Hz)"] = bw
            
    return results

def calculate_power_factor_compensation(active_power_kw, current_cos_phi, target_cos_phi=0.98):
    """
    Güç faktörü düzeltmesi (Reaktif Kompanzasyon) için gereken kondansatör gücünü (kVAR) hesaplar.
    Qc = P * (tan(phi1) - tan(phi2))
    """
    if active_power_kw <= 0 or current_cos_phi <= 0 or current_cos_phi >= 1.0:
        return None, "Geçerli bir aktif güç ve cos φ (0 ile 1 arası) değeri girilmelidir."
    if target_cos_phi <= current_cos_phi or target_cos_phi >= 1.0:
        return None, "Hedef cos φ mevcut değerden büyük ve 1'den küçük olmalıdır."
        
    phi1 = math.acos(current_cos_phi)
    phi2 = math.acos(target_cos_phi)
    
    tan_phi1 = math.tan(phi1)
    tan_phi2 = math.tan(phi2)
    
    qc_kvar = active_power_kw * (tan_phi1 - tan_phi2)
    current_apparent_power = active_power_kw / current_cos_phi
    target_apparent_power = active_power_kw / target_cos_phi
    apparent_power_reduction = current_apparent_power - target_apparent_power
    
    return {
        "Aktif Güç (kW)": active_power_kw,
        "Mevcut cos φ": current_cos_phi,
        "Hedef cos φ": target_cos_phi,
        "Gereken Kondansatör Gücü (kVAR)": qc_kvar,
        "Mevcut Görünür Güç (kVA)": current_apparent_power,
        "Hedef Görünür Güç (kVA)": target_apparent_power,
        "Şebekeden Çekilen Güç Tasarrufu (kVA)": apparent_power_reduction
    }, None

def interactive_voltage_drop():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}   KABLO KESİTİ & GERİLİM DÜŞÜMÜ HESAPLAYICI      {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("IEC 60364-5-52 standartlarına göre gerilim düşümü & güç kaybı analizi.")
    print("-" * 50)
    try:
        sys_choice = input("Sistem Tipi: [1] 3 Faz AC (400V) | [2] 1 Faz AC (230V) [Varsayılan: 1]: ").strip()
        system_type = "1phase" if sys_choice == "2" else "3phase"
        default_voltage = 230.0 if system_type == "1phase" else 400.0
        
        voltage_in = input(f"Nominal Gerilim (V) [{default_voltage}]: ").strip()
        voltage = float(voltage_in) if voltage_in else default_voltage
        
        current = float(input("Çekilen Akım (Amper): "))
        length = float(input("Hat Uzunluğu (metre): "))
        section = float(input("Kablo Kesiti (mm² - Örn: 1.5, 2.5, 4, 6, 10, 16, 25, 35, 50): "))
        
        mat_choice = input("İletken Malzemesi [1] Bakır | [2] Alüminyum [Varsayılan: 1]: ").strip()
        material = "aluminyum" if mat_choice == "2" else "bakir"
        
        cos_in = input("Güç Faktörü cos φ [Varsayılan: 0.85]: ").strip()
        cos_phi = float(cos_in) if cos_in else 0.85
        
        res, err = calculate_voltage_drop(voltage, current, length, section, material, system_type, cos_phi)
        if err:
            print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}>>> HESAPLAMA SONUÇLARI <<<{Colors.ENDC}")
            for k, v in res.items():
                if isinstance(v, float):
                    print(f"  {k:<32}: {Colors.BOLD}{v:10.3f}{Colors.ENDC}")
                else:
                    color = Colors.OKGREEN if "UYGUN" in str(v) else (Colors.FAIL if "AŞILDI" in str(v) else Colors.BOLD)
                    print(f"  {k:<32}: {color}{v}{Colors.ENDC}")
    except ValueError:
        print(f"{Colors.FAIL}Hata: Lütfen geçerli sayısal değerler girin.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def interactive_filter_resonance():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}    ELEKTRİK FİLTRE VE REZONANS HESAPLAYICI       {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("RC, RL ve RLC filtrelerinde kesim frekansı, rezonans ve bant genişliği.")
    print("-" * 50)
    try:
        r = float(input("Direnç R (Ohm): ") or "0")
        l_mh = float(input("Endüktans L (milliHenry - mH): ") or "0")
        c_uf = float(input("Kapasitans C (mikroFarad - µF): ") or "0")
        
        l_henry = l_mh * 1e-3
        c_farad = c_uf * 1e-6
        
        results = calculate_filter_resonance(r, l_henry, c_farad)
        if not results:
            print(f"{Colors.FAIL}Hata: En az bir RC, RL veya RLC çifti girilmelidir.{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}>>> HESAPLAMA SONUÇLARI <<<{Colors.ENDC}")
            for k, v in results.items():
                print(f"  {k:<36}: {Colors.BOLD}{v:12.4f}{Colors.ENDC}")
    except ValueError:
        print(f"{Colors.FAIL}Hata: Lütfen geçerli sayısal değerler girin.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def interactive_compensation():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}    KOMPANZASYON KONDANSATÖR GÜCÜ HESAPLAYICI     {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("Güç katsayısını (cos φ) istenen seviyeye çıkarmak için gereken kVAR hesabı.")
    print("-" * 50)
    try:
        p_kw = float(input("Tesis Toplam Aktif Gücü (kW): "))
        current_cos = float(input("Mevcut Güç Faktörü (cos φ1) [Örn: 0.72]: "))
        target_cos = float(input("Hedef Güç Faktörü (cos φ2) [Varsayılan: 0.98]: ") or "0.98")
        
        res, err = calculate_power_factor_compensation(p_kw, current_cos, target_cos)
        if err:
            print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}>>> KOMPANZASYON ANALİZİ <<<{Colors.ENDC}")
            for k, v in res.items():
                print(f"  {k:<38}: {Colors.BOLD}{v:10.3f}{Colors.ENDC}")
    except ValueError:
        print(f"{Colors.FAIL}Hata: Lütfen geçerli sayısal değerler girin.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def main():
    if os.name == 'nt':
        os.system('color')
        
    while True:
        clear_screen()
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}   ⚡ ELEKTRİK & DEVRE MÜHENDİSLİĞİ ARAÇLARI       {Colors.ENDC}")
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.OKCYAN}1.{Colors.ENDC} Kablo Kesiti & Gerilim Düşümü (IEC 60364)")
        print(f"{Colors.OKCYAN}2.{Colors.ENDC} Filtre & RLC Rezonans Frekansı Analizi")
        print(f"{Colors.OKCYAN}3.{Colors.ENDC} Güç Faktörü (cos φ) & Kompanzasyon Hesabı")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Geri Dön")
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        
        if secim == '1':
            interactive_voltage_drop()
        elif secim == '2':
            interactive_filter_resonance()
        elif secim == '3':
            interactive_compensation()
        elif secim == '0':
            break
        else:
            print(f"\n{Colors.FAIL}Geçersiz seçim!{Colors.ENDC}")
            input("Devam etmek için Enter'a basın...")

if __name__ == "__main__":
    main()
