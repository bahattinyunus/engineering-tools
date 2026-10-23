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

def calculate_npv(initial_investment, cash_flows, discount_rate):
    """
    Net Bugünkü Değer (NPV) hesabı.
    initial_investment: Pozitif başlangıç yatırım tutarı
    cash_flows: Yıllık net nakit girişleri listesi [CF1, CF2, ...]
    discount_rate: İskonto oranı (Örn: %10 için 0.10)
    """
    if initial_investment < 0 or discount_rate < 0:
        return None, "Yatırım tutarı ve iskonto oranı negatif olamaz."
    if not cash_flows:
        return None, "Nakit akışı listesi boş olamaz."
        
    npv = -initial_investment
    discounted_cfs = []
    
    for t, cf in enumerate(cash_flows, start=1):
        pv = cf / ((1.0 + discount_rate) ** t)
        discounted_cfs.append(pv)
        npv += pv
        
    return {
        "Başlangıç Yatırımı (C0)": initial_investment,
        "İskonto Oranı (r %)": discount_rate * 100.0,
        "Yıllık İndirgenmiş Nakit Akışları": discounted_cfs,
        "Net Mevcut Değer (NPV)": npv,
        "Yatırım Kararı": "YATIRIM KABUL EDİLEBİLİR (NPV > 0)" if npv > 0 else "YATIRIM REDDEDİLMELİ (NPV <= 0)"
    }, None

def calculate_irr(initial_investment, cash_flows, max_iterations=200, tolerance=1e-6):
    """
    İç Karlılık Oranı (IRR - Internal Rate of Return).
    NPV(IRR) = 0 denklemini Newton-Raphson yöntemiyle çözer.
    """
    if initial_investment <= 0 or not cash_flows:
        return None, "Geçerli bir başlangıç yatırımı ve nakit akışları gereklidir."
        
    # Başlangıç tahmini r = %10
    rate = 0.10
    
    for _ in range(max_iterations):
        # f(r) = -C0 + sum(CF_t / (1+r)^t)
        # f'(r) = - sum(t * CF_t / (1+r)^(t+1))
        f_val = -initial_investment
        f_deriv = 0.0
        
        for t, cf in enumerate(cash_flows, start=1):
            denom = (1.0 + rate) ** t
            f_val += cf / denom
            f_deriv -= (t * cf) / (denom * (1.0 + rate))
            
        if abs(f_deriv) < 1e-12:
            break
            
        new_rate = rate - (f_val / f_deriv)
        if abs(new_rate - rate) < tolerance:
            rate = new_rate
            break
        rate = new_rate
        
    return rate

def calculate_payback_period(initial_investment, cash_flows, discount_rate=None):
    """
    Geri Ödeme Süresi (Payback Period).
    discount_rate verilirse İskontolu Geri Ödeme Süresi (Discounted Payback) hesaplanır.
    """
    cumulative = 0.0
    payback_years = None
    
    for t, cf in enumerate(cash_flows, start=1):
        val = cf / ((1.0 + discount_rate) ** t) if discount_rate else cf
        prev_cum = cumulative
        cumulative += val
        
        if cumulative >= initial_investment:
            fraction = (initial_investment - prev_cum) / val if val > 0 else 0
            payback_years = (t - 1) + fraction
            break
            
    return payback_years

def analyze_capital_budgeting(initial_investment, cash_flows, discount_rate):
    """
    NPV, IRR, Payback, Discounted Payback ve ROI değerlerini birleştiren fizibilite analizi.
    """
    npv_res, err = calculate_npv(initial_investment, cash_flows, discount_rate)
    if err:
        return None, err
        
    irr_rate = calculate_irr(initial_investment, cash_flows)
    simple_payback = calculate_payback_period(initial_investment, cash_flows)
    disc_payback = calculate_payback_period(initial_investment, cash_flows, discount_rate)
    
    total_inflow = sum(cash_flows)
    net_profit = total_inflow - initial_investment
    roi_pct = (net_profit / initial_investment) * 100.0 if initial_investment > 0 else 0.0
    
    # Fayda / Maliyet Oranı (Benefit-Cost Ratio BCR)
    pv_inflows = npv_res["Net Mevcut Değer (NPV)"] + initial_investment
    bcr = pv_inflows / initial_investment if initial_investment > 0 else 0.0
    
    return {
        "Başlangıç Yatırımı ($)": initial_investment,
        "Proje Süresi (Yıl)": len(cash_flows),
        "İskonto Oranı (%)": discount_rate * 100.0,
        "Net Bugünkü Değer (NPV - $)": npv_res["Net Mevcut Değer (NPV)"],
        "İç Karlılık Oranı (IRR %)": irr_rate * 100.0 if irr_rate is not None else "Hesaplanamadı",
        "Basit Geri Ödeme Süresi (Yıl)": f"{simple_payback:.2f} Yıl" if simple_payback else "Proje Süresinde Dönmüyor",
        "İskontolu Geri Ödeme Süresi (Yıl)": f"{disc_payback:.2f} Yıl" if disc_payback else "İskontolu Dönmüyor",
        "Yatırım Getirisi (ROI %)": roi_pct,
        "Fayda / Maliyet Oranı (BCR)": bcr,
        "Nihai Yatırım Tavsiyesi": "ONAYLANABİLİR (NPV > 0 & IRR > r)" if npv_res["Net Mevcut Değer (NPV)"] > 0 else "REDDEDİLMELİ (Verimsiz)"
    }, None

def interactive_capital_budgeting():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}   MÜHENDİSLİK EKONOMİSİ & FİZİBİLİTE ANALİZİ    {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("Sermaye bütçelemesi: NPV, IRR, ROI ve İskontolu Geri Ödeme analizi.")
    print("-" * 50)
    try:
        c0 = float(input("Başlangıç Yatırım Tutarı ($ C0) [Örn: 100000]: "))
        r_pct = float(input("Yıllık Sermaye Maliyeti / İskonto Oranı (%) [Örn: 12]: "))
        cfs_str = input("Yıllık Net Nakit Akışlarını boşlukla girin (Örn: 30000 35000 40000 45000 50000): ").strip()
        
        cash_flows = [float(x) for x in cfs_str.split()]
        res, err = analyze_capital_budgeting(c0, cash_flows, r_pct / 100.0)
        if err:
            print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}>>> FİNANSAL FİZİBİLİTE RAPORU <<<{Colors.ENDC}")
            for k, val in res.items():
                if isinstance(val, float):
                    print(f"  {k:<38}: {Colors.BOLD}{val:12.2f}{Colors.ENDC}")
                elif "ONAYLANABİLİR" in str(val):
                    print(f"  {k:<38}: {Colors.OKGREEN}{val}{Colors.ENDC}")
                elif "REDDEDİLMELİ" in str(val):
                    print(f"  {k:<38}: {Colors.FAIL}{val}{Colors.ENDC}")
                else:
                    print(f"  {k:<38}: {Colors.BOLD}{val}{Colors.ENDC}")
    except ValueError:
        print(f"{Colors.FAIL}Hata: Sayısal değer giriniz.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def main():
    if os.name == 'nt':
        os.system('color')
    interactive_capital_budgeting()

if __name__ == "__main__":
    main()
