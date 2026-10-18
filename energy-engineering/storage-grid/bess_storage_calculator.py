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

BATTERY_CHEMISTRIES = {
    "lifepo4": {
        "name": "Lityum Demir Fosfat (LiFePO4)",
        "dod": 0.90,
        "round_trip_eff": 0.94,
        "typical_cycles": 6000,
        "nominal_cell_v": 3.2
    },
    "nmc": {
        "name": "Lityum İyon (NMC)",
        "dod": 0.80,
        "round_trip_eff": 0.92,
        "typical_cycles": 3000,
        "nominal_cell_v": 3.7
    },
    "agm_gel": {
        "name": "Derin Döngü AGM / Jel (Kurşun-Asit)",
        "dod": 0.50,
        "round_trip_eff": 0.82,
        "typical_cycles": 800,
        "nominal_cell_v": 2.0
    }
}

def calculate_bess_sizing(daily_consumption_kwh, autonomy_days, system_voltage_v, chemistry="lifepo4", inverter_eff=0.95):
    """
    Bataryalı Enerji Depolama Sistemi (BESS) kapasite boyutlandırması yapar.
    """
    if daily_consumption_kwh <= 0 or autonomy_days <= 0 or system_voltage_v <= 0:
        return None, "Girdiler pozitif sayı olmalıdır."
        
    chem_data = BATTERY_CHEMISTRIES.get(chemistry.lower(), BATTERY_CHEMISTRIES["lifepo4"])
    dod = chem_data["dod"]
    batt_eff = chem_data["round_trip_eff"]
    
    # Toplam sistem verimliliği (Batarya verimi * İnvertör verimi)
    total_system_eff = batt_eff * inverter_eff
    
    # İhtiyaç duyulan net enerji
    required_usable_energy_kwh = daily_consumption_kwh * autonomy_days
    
    # Nominal depolama kapasitesi (kWh): Nominal = Usable / (DoD * Total_Eff)
    nominal_capacity_kwh = required_usable_energy_kwh / (dod * total_system_eff)
    
    # Nominal Kapasite (Ah): (kWh * 1000) / V_system
    capacity_ah = (nominal_capacity_kwh * 1000.0) / system_voltage_v
    
    return {
        "Batarya Kimyası": chem_data["name"],
        "Günlük Enerji İhtiyacı (kWh)": daily_consumption_kwh,
        "Otonomi Süresi (Gün)": autonomy_days,
        "Sistem DC Barası Gerilimi (V)": system_voltage_v,
        "İzin Verilen Deşarj Derinliği (DoD %)": dod * 100.0,
        "Batarya Çift Yönlü Verimi (RTE %)": batt_eff * 100.0,
        "İnvertör Verimi (%)": inverter_eff * 100.0,
        "Net Kullanılabilir Enerji (kWh)": required_usable_energy_kwh,
        "Gereken Nominal Depolama Kapasitesi (kWh)": nominal_capacity_kwh,
        "Gereken Toplam Kapasite (Ah)": capacity_ah
    }, None

def calculate_lcos(capex_usd, opex_annual_usd, nominal_kwh, chemistry="lifepo4", cycles_per_year=365):
    """
    Düzleştirilmiş Depolama Maliyeti (Levelized Cost of Storage - LCOS $/kWh).
    """
    if capex_usd <= 0 or nominal_kwh <= 0:
        return None, "Yatırım tutarı ve kapasite pozitif olmalıdır."
        
    chem_data = BATTERY_CHEMISTRIES.get(chemistry.lower(), BATTERY_CHEMISTRIES["lifepo4"])
    max_cycles = chem_data["typical_cycles"]
    dod = chem_data["dod"]
    
    project_lifetime_years = max_cycles / cycles_per_year
    total_cycles = max_cycles
    
    # Her döngüde teslim edilen ortalama enerji (kWh)
    delivered_kwh_per_cycle = nominal_kwh * dod * chem_data["round_trip_eff"]
    lifetime_delivered_kwh = delivered_kwh_per_cycle * total_cycles
    
    total_opex = opex_annual_usd * project_lifetime_years
    total_cost = capex_usd + total_opex
    
    lcos_usd_per_kwh = total_cost / lifetime_delivered_kwh if lifetime_delivered_kwh > 0 else 0
    
    return {
        "Kimya": chem_data["name"],
        "Ömür Döngü Sayısı (Cycle Life)": max_cycles,
        "Yıllık Döngü Adedi": cycles_per_year,
        "Tahmini Batarya Ömrü (Yıl)": project_lifetime_years,
        "Ömür Boyu Teslim Edilen Toplam Enerji (kWh)": lifetime_delivered_kwh,
        "Toplam Yatırım + İşletme Maliyeti ($)": total_cost,
        "Düzleştirilmiş Depolama Maliyeti (LCOS $/kWh)": lcos_usd_per_kwh
    }, None

def interactive_bess():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}   BATARYALI ENERJİ DEPOLAMA (BESS) BOYUTLANDIRICI{Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("Güneş & Rüzgar destekli şebeke/ada sistemleri için akü kapasite hesabı.")
    print("-" * 50)
    try:
        daily_kwh = float(input("Günlük Ortalama Tüketim (kWh): "))
        autonomy = float(input("Otonomi Süresi (Elektriksiz dayanma - Gün) [Örn: 1.5]: ") or "1.0")
        
        print("\nSistem DC Bara Gerilimi:")
        print("1. 12V (Küçük Karavan / Tekne)")
        print("2. 24V (Orta Ölçekli Konut)")
        print("3. 48V (Standart Ev & Ticari ESS)")
        print("4. 400V (Yüksek Gerilim Endüstriyel BESS)")
        v_choice = input("Seçiminiz [Varsayılan: 3 (48V)]: ").strip()
        v_map = {"1": 12.0, "2": 24.0, "3": 48.0, "4": 400.0}
        voltage = v_map.get(v_choice, 48.0)
        
        print("\nBatarya Kimyası:")
        print("1. LiFePO4 - Lityum Demir Fosfat (%90 DoD, 6000 döngü)")
        print("2. NMC - Lityum İyon (%80 DoD, 3000 döngü)")
        print("3. AGM / Jel Derin Döngü Kurşun-Asit (%50 DoD, 800 döngü)")
        chem_choice = input("Seçiminiz [Varsayılan: 1]: ").strip()
        chem_map = {"1": "lifepo4", "2": "nmc", "3": "agm_gel"}
        chemistry = chem_map.get(chem_choice, "lifepo4")
        
        res, err = calculate_bess_sizing(daily_kwh, autonomy, voltage, chemistry)
        if err:
            print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}>>> BESS BOYUTLANDIRMA SONUÇLARI <<<{Colors.ENDC}")
            for k, v in res.items():
                if isinstance(v, float):
                    print(f"  {k:<40}: {Colors.BOLD}{v:10.2f}{Colors.ENDC}")
                else:
                    print(f"  {k:<40}: {Colors.OKCYAN}{v}{Colors.ENDC}")
                    
            # Örnek modül sayısı hesabı
            nom_kwh = res["Gereken Nominal Depolama Kapasitesi (kWh)"]
            print(f"\n{Colors.HEADER}--- Örnek Ticari Akü Konfigürasyonları ---{Colors.ENDC}")
            # 48V 100Ah = 4.8 kWh modüller
            modules_48v100ah = math.ceil(nom_kwh / 4.8)
            print(f"  48V 100Ah (4.8 kWh) LiFePO4 Rack Modül Adedi : {Colors.OKGREEN}{modules_48v100ah} Adet{Colors.ENDC}")
            # 12V 200Ah = 2.4 kWh aküler
            modules_12v200ah = math.ceil(nom_kwh / 2.4)
            print(f"  12V 200Ah (2.4 kWh) Akü Adedi              : {Colors.OKGREEN}{modules_12v200ah} Adet{Colors.ENDC}")

            # LCOS Maliyet Analizi İsteği
            calc_cost = input("\nLCOS (Depolanan Enerji Birim Maliyeti) hesabı yapılsın mı? (e/h): ").strip().lower()
            if calc_cost == 'e':
                capex = float(input("Toplam BESS Donanım Yatırımı ($): "))
                opex = float(input("Yıllık Bakım & İşletme Maliyeti ($/yıl) [Örn: 200]: ") or "200")
                cost_res, cost_err = calculate_lcos(capex, opex, nom_kwh, chemistry)
                if not cost_err:
                    print(f"\n{Colors.OKGREEN}>>> LCOS EKONOMİK ANALİZİ <<<{Colors.ENDC}")
                    for ck, cv in cost_res.items():
                        if isinstance(cv, float):
                            print(f"  {ck:<42}: {Colors.BOLD}{cv:10.3f}{Colors.ENDC}")
                        else:
                            print(f"  {ck:<42}: {Colors.BOLD}{cv}{Colors.ENDC}")

    except ValueError:
        print(f"{Colors.FAIL}Hata: Lütfen geçerli sayısal değerler girin.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def main():
    if os.name == 'nt':
        os.system('color')
    interactive_bess()

if __name__ == "__main__":
    main()
