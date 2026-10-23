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

def calculate_carnot_efficiency(th_celsius, tc_celsius):
    """
    Carnot Çevrimi maksimum teorik termal verimi (Termodinamiğin 2. Yasası).
    eta = 1 - (Tc / Th)
    """
    th_k = th_celsius + 273.15
    tc_k = tc_celsius + 273.15
    
    if th_k <= tc_k or tc_k <= 0:
        return None, "Sıcak kaynak sıcaklığı soğuk kaynaktan yüksek ve mutlak sıfırdan büyük olmalıdır."
        
    eta_carnot = 1.0 - (tc_k / th_k)
    cop_cooling = tc_k / (th_k - tc_k) # Soğutma çevrimi ideal COP
    cop_heat_pump = th_k / (th_k - tc_k) # Isı pompası ideal COP
    
    return {
        "Sıcak Kaynak Th": f"{th_celsius:.1f} °C ({th_k:.2f} K)",
        "Soğuk Kaynak Tc": f"{tc_celsius:.1f} °C ({tc_k:.2f} K)",
        "Maksimum Carnot Verimi η (%)": eta_carnot * 100.0,
        "İdeal Isı Pompası COP (Isıtma)": cop_heat_pump,
        "İdeal Soğutma Makinesi COP (Soğutma)": cop_cooling
    }, None

def calculate_brayton_cycle(pressure_ratio, t1_celsius, t3_celsius, gamma=1.4, cp=1.005):
    """
    Brayton Çevrimi (Gaz Türbinleri ve Jet Motorları).
    rp: Basınç oranı (P2 / P1)
    T1: Kompresör giriş sıcaklığı (°C)
    T3: Türbin giriş sıcaklığı (Yanma odası çıkış - °C)
    cp: kJ/(kg·K)
    """
    if pressure_ratio <= 1.0:
        return None, "Basınç oranı 1'den büyük olmalıdır."
        
    t1_k = t1_celsius + 273.15
    t3_k = t3_celsius + 273.15
    
    if t3_k <= t1_k:
        return None, "Türbin giriş sıcaklığı kompresör girişinden yüksek olmalıdır."
        
    # İzantropik bağıntılar: T2 = T1 * (rp)^((gamma-1)/gamma)
    exponent = (gamma - 1.0) / gamma
    t2_k = t1_k * (pressure_ratio ** exponent)
    
    if t2_k >= t3_k:
        return None, f"Basınç oranı çok yüksek! Kompresör çıkış sıcaklığı ({t2_k-273.15:.1f} °C) yanma odası sıcaklığını aşıyor."
        
    # T4 = T3 / (rp)^((gamma-1)/gamma)
    t4_k = t3_k / (pressure_ratio ** exponent)
    
    # Birim kütle için iş ve ısı transferleri (kJ/kg)
    w_comp = cp * (t2_k - t1_k) # Kompresör işi
    q_in = cp * (t3_k - t2_k)   # Yanma odası ısısı
    w_turb = cp * (t3_k - t4_k) # Türbin işi
    w_net = w_turb - w_comp     # Net üretilen iş
    
    eta_thermal = 1.0 - (1.0 / (pressure_ratio ** exponent))
    bwr = w_comp / w_turb # Back Work Ratio (Geri İş Oranı)
    
    return {
        "Basınç Oranı (rp)": pressure_ratio,
        "T1 (Kompresör Giriş)": f"{t1_celsius:.1f} °C ({t1_k:.1f} K)",
        "T2 (Kompresör Çıkış)": f"{t2_k - 273.15:.1f} °C ({t2_k:.1f} K)",
        "T3 (Türbin Giriş / Yanma)": f"{t3_celsius:.1f} °C ({t3_k:.1f} K)",
        "T4 (Egzoz Çıkış)": f"{t4_k - 273.15:.1f} °C ({t4_k:.1f} K)",
        "Kompresör İşi Wc (kJ/kg)": w_comp,
        "Türbin İşi Wt (kJ/kg)": w_turb,
        "Net İş Üretimi Wnet (kJ/kg)": w_net,
        "Geri İş Oranı (BWR %)": bwr * 100.0,
        "Teorik Termal Verim η (%)": eta_thermal * 100.0
    }, None

def calculate_otto_cycle(compression_ratio, gamma=1.4):
    """
    Otto Çevrimi (Benzinli / Buji Ateşlemeli İçten Yanmalı Motorlar).
    eta = 1 - (1 / r^(gamma - 1))
    """
    if compression_ratio <= 1.0:
        return None, "Sıkıştırma oranı (r) 1'den büyük olmalıdır."
        
    eta_otto = 1.0 - (1.0 / (compression_ratio ** (gamma - 1.0)))
    return {
        "Sıkıştırma Oranı (r)": compression_ratio,
        "Özgül Isı Oranı (k / γ)": gamma,
        "Otto Termal Verimi η (%)": eta_otto * 100.0
    }, None

def calculate_diesel_cycle(compression_ratio, cutoff_ratio, gamma=1.4):
    """
    Diesel Çevrimi (Dizel / Sıkıştırma ile Ateşlemeli Motorlar).
    rc: Cut-off (Püskürtme sonu kesme) oranı (V3 / V2)
    """
    if compression_ratio <= 1.0 or cutoff_ratio <= 1.0:
        return None, "Sıkıştırma oranı ve kesme oranı 1'den büyük olmalıdır."
        
    r = compression_ratio
    rc = cutoff_ratio
    k = gamma
    
    bracket = (rc ** k - 1.0) / (k * (rc - 1.0))
    eta_diesel = 1.0 - (1.0 / (r ** (k - 1.0))) * bracket
    
    return {
        "Sıkıştırma Oranı (r)": r,
        "Kesme Oranı (rc)": rc,
        "Diesel Termal Verimi η (%)": eta_diesel * 100.0
    }, None

def interactive_carnot():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}       CARNOT ÇEVRİMİ TERMAL VERİM HESABI         {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    try:
        th = float(input("Sıcak Kaynak Sıcaklığı Th (°C) [Örn: 550]: "))
        tc = float(input("Soğuk Kaynak Sıcaklığı Tc (°C) [Örn: 30]: "))
        res, err = calculate_carnot_efficiency(th, tc)
        if err:
            print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}>>> CARNOT ANALİZ SONUÇLARI <<<{Colors.ENDC}")
            for k, v in res.items():
                if isinstance(v, float):
                    print(f"  {k:<38}: {Colors.BOLD}{v:10.2f}{Colors.ENDC}")
                else:
                    print(f"  {k:<38}: {Colors.BOLD}{v}{Colors.ENDC}")
    except ValueError:
        print(f"{Colors.FAIL}Hata: Sayısal değer giriniz.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def interactive_brayton():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}   BRAYTON ÇEVRİMİ (GAZ TÜRBİNİ & JET MOTORU)     {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    try:
        rp = float(input("Basınç Oranı (P2 / P1) [Örn: 12.0]: "))
        t1 = float(input("Kompresör Giriş Sıcaklığı T1 (°C) [Örn: 20]: "))
        t3 = float(input("Türbin Giriş Sıcaklığı T3 (°C) [Örn: 1100]: "))
        res, err = calculate_brayton_cycle(rp, t1, t3)
        if err:
            print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}>>> BRAYTON ÇEVRİM SONUÇLARI <<<{Colors.ENDC}")
            for k, v in res.items():
                if isinstance(v, float):
                    print(f"  {k:<38}: {Colors.BOLD}{v:10.2f}{Colors.ENDC}")
                else:
                    print(f"  {k:<38}: {Colors.BOLD}{v}{Colors.ENDC}")
    except ValueError:
        print(f"{Colors.FAIL}Hata: Sayısal değer giriniz.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def interactive_otto_diesel():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}   OTTO VE DIESEL MOTOR ÇEVRİM VERİMLERİ          {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("1. Otto Çevrimi (Benzinli Motorlar)")
    print("2. Diesel Çevrimi (Dizel Motorlar)")
    sec = input("Seçiminiz (1/2): ").strip()
    try:
        if sec == '1':
            r = float(input("Sıkıştırma Oranı r [Örn: 9.5]: "))
            res, err = calculate_otto_cycle(r)
        else:
            r = float(input("Sıkıştırma Oranı r [Örn: 18.0]: "))
            rc = float(input("Püskürtme Kesme Oranı rc [Örn: 2.0]: "))
            res, err = calculate_diesel_cycle(r, rc)
            
        if err:
            print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}>>> MOTOR VERİM SONUÇLARI <<<{Colors.ENDC}")
            for k, v in res.items():
                print(f"  {k:<35}: {Colors.BOLD}{v:10.2f}{Colors.ENDC}")
    except ValueError:
        print(f"{Colors.FAIL}Hata: Sayısal değer giriniz.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def main():
    if os.name == 'nt':
        os.system('color')
    while True:
        clear_screen()
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}   🔥 TERMODİNAMİK VE GÜÇ DÖNGÜLERİ HESAPLAYICI  {Colors.ENDC}")
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.OKCYAN}1.{Colors.ENDC} Carnot Çevrimi (Maksimum İdeal Verim)")
        print(f"{Colors.OKCYAN}2.{Colors.ENDC} Brayton Gaz Türbini & Jet Motoru Çevrimi")
        print(f"{Colors.OKCYAN}3.{Colors.ENDC} Otto & Diesel Motor Çevrim Verimleri")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Geri Dön")
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        if secim == '1':
            interactive_carnot()
        elif secim == '2':
            interactive_brayton()
        elif secim == '3':
            interactive_otto_diesel()
        elif secim == '0':
            break

if __name__ == "__main__":
    main()
