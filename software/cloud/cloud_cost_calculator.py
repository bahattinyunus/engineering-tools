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

# Ortalama Bulut Birim Fiyatları (USD / saat bazında genel pazar tahminleri)
# vCPU başına ortalama: $0.04/saat, GB RAM başına: $0.005/saat, SSD Depolama: $0.08/GB-ay, Egress: $0.09/GB
BASE_RATES = {
    "vcpu_hourly": 0.040,
    "ram_gb_hourly": 0.0053,
    "ssd_gb_monthly": 0.08,
    "egress_gb": 0.085
}

def estimate_cloud_cost(vcpu_count, ram_gb, storage_gb, egress_gb_month, running_hours_month=730):
    """
    Sanal sunucu ve bulut altyapısı için aylık ve yıllık TCO (Maliyet) projeksiyonu hesaplar.
    """
    if vcpu_count <= 0 or ram_gb <= 0 or storage_gb < 0 or egress_gb_month < 0:
        return None, "Kaynak değerleri negatif veya geçersiz olamaz."
        
    compute_hourly = (vcpu_count * BASE_RATES["vcpu_hourly"]) + (ram_gb * BASE_RATES["ram_gb_hourly"])
    compute_monthly_ondemand = compute_hourly * running_hours_month
    
    storage_monthly = storage_gb * BASE_RATES["ssd_gb_monthly"]
    network_monthly = egress_gb_month * BASE_RATES["egress_gb"]
    
    total_monthly_ondemand = compute_monthly_ondemand + storage_monthly + network_monthly
    total_annual_ondemand = total_monthly_ondemand * 12.0
    
    # 1 Yıllık Taahhütlü (Reserved Instance / Savings Plan ~ %38 İndirim)
    compute_monthly_1yr = compute_monthly_ondemand * 0.62
    total_monthly_1yr = compute_monthly_1yr + storage_monthly + network_monthly
    total_annual_1yr = total_monthly_1yr * 12.0
    savings_1yr = total_annual_ondemand - total_annual_1yr
    
    # 3 Yıllık Taahhütlü (~ %58 İndirim)
    compute_monthly_3yr = compute_monthly_ondemand * 0.42
    total_monthly_3yr = compute_monthly_3yr + storage_monthly + network_monthly
    total_annual_3yr = total_monthly_3yr * 12.0
    savings_3yr = (total_annual_ondemand * 3.0) - (total_annual_3yr * 3.0)
    
    # Yeşil Bilişim (Cloud Carbon Footprint):
    # Tipik modern sunucu: 1 vCPU ~ 12W, 1 GB RAM ~ 0.5W, PUE (Power Usage Effectiveness) = 1.18
    power_watts = ((vcpu_count * 12.0) + (ram_gb * 0.5) + (storage_gb * 0.002)) * 1.18
    monthly_kwh = (power_watts * running_hours_month) / 1000.0
    # Ortalama şebeke emisyon faktörü: 0.385 kg CO2e / kWh
    monthly_carbon_kg = monthly_kwh * 0.385
    
    return {
        "vCPU": vcpu_count,
        "RAM (GB)": ram_gb,
        "SSD Depolama (GB)": storage_gb,
        "Aylık Ağ Çıkışı Egress (GB)": egress_gb_month,
        "Aylık Çalışma Süresi (saat)": running_hours_month,
        "Aylık On-Demand Maliyet ($)": total_monthly_ondemand,
        "Yıllık On-Demand Maliyet ($)": total_annual_ondemand,
        "Aylık 1-Yıl Rezerv Maliyet ($)": total_monthly_1yr,
        "Yıllık 1-Yıl Rezerv Tasarrufu ($)": savings_1yr,
        "Aylık 3-Yıl Rezerv Maliyet ($)": total_monthly_3yr,
        "3 Yıllık Toplam Tasarruf ($)": savings_3yr,
        "Aylık Enerji Tüketimi (kWh)": monthly_kwh,
        "Aylık Karbon Emisyonu (kg CO2e)": monthly_carbon_kg
    }, None

def interactive_cloud_cost():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}    BULUT ALTYAPI & TCO MALİYET HESAPLAYICI       {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("AWS / Azure / GCP sunucu, depolama, ağ ve rezerv tasarruf analizi.")
    print("-" * 50)
    try:
        vcpu = int(input("Gereken vCPU Sayısı [Örn: 4]: "))
        ram = float(input("Gereken RAM Miktarı (GB) [Örn: 16]: "))
        storage = float(input("Gereken NVMe/SSD Depolama (GB) [Örn: 200]: "))
        egress = float(input("Aylık Tahmini Dışarı Veri Transferi (GB Egress) [Örn: 100]: ") or "50")
        
        print("\nÇalışma Modeli:")
        print("1. 7/24 Kesintisiz Üretim (730 saat/ay)")
        print("2. Sadece Mesai Saatleri / Test Ortamı (200 saat/ay)")
        work_sel = input("Seçiminiz [Varsayılan: 1]: ").strip()
        hours = 200 if work_sel == "2" else 730
        
        res, err = estimate_cloud_cost(vcpu, ram, storage, egress, hours)
        if err:
            print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}>>> BULUT MALİYET VE VERİMLİLİK RAPORU <<<{Colors.ENDC}")
            print(f"  Hesaplanan Yapılandırma       : {res['vCPU']} vCPU | {res['RAM (GB)']} GB RAM | {res['SSD Depolama (GB)']} GB SSD")
            print(f"  Çalışma Süresi                : {res['Aylık Çalışma Süresi (saat)']} saat/ay")
            print("-" * 50)
            print(f"  {Colors.BOLD}Kullandıkça Öde (On-Demand):{Colors.ENDC}")
            print(f"    Aylık Fatura                : {Colors.WARNING}${res['Aylık On-Demand Maliyet ($)']:.2f}{Colors.ENDC}")
            print(f"    Yıllık Projeksiyon          : ${res['Yıllık On-Demand Maliyet ($)']:.2f}")
            print("-" * 50)
            print(f"  {Colors.BOLD}1 Yıllık Taahhüt (Reserved Instance / Savings Plan):{Colors.ENDC}")
            print(f"    Aylık Fatura                : {Colors.OKGREEN}${res['Aylık 1-Yıl Rezerv Maliyet ($)']:.2f}{Colors.ENDC}")
            print(f"    1 Yılda Net Tasarruf        : {Colors.OKCYAN}${res['Yıllık 1-Yıl Rezerv Tasarrufu ($)']:.2f}{Colors.ENDC}")
            print("-" * 50)
            print(f"  {Colors.BOLD}3 Yıllık Taahhüt (Maksimum Tasarruf):{Colors.ENDC}")
            print(f"    Aylık Fatura                : {Colors.OKGREEN}${res['Aylık 3-Yıl Rezerv Maliyet ($)']:.2f}{Colors.ENDC}")
            print(f"    3 Yılda Toplam Cepte Kalan  : {Colors.OKCYAN}${res['3 Yıllık Toplam Tasarruf ($)']:.2f}{Colors.ENDC}")
            print("-" * 50)
            print(f"  {Colors.BOLD}Yeşil Bilişim (Green Cloud):{Colors.ENDC}")
            print(f"    Aylık Enerji Tüketimi       : {res['Aylık Enerji Tüketimi (kWh)']:.2f} kWh")
            print(f"    Aylık Karbon Emisyonu       : {res['Aylık Karbon Emisyonu (kg CO2e)']:.2f} kg CO2e")
            
    except ValueError:
        print(f"{Colors.FAIL}Hata: Lütfen geçerli sayısal değerler girin.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def main():
    if os.name == 'nt':
        os.system('color')
    interactive_cloud_cost()

if __name__ == "__main__":
    main()
