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

def forward_kinematics_2r(l1, l2, theta1_deg, theta2_deg):
    """
    2-Serbestlik Dereceli (2R) Düzlemsel Manipülatör İleri Kinematiği.
    Eklem açılarından uç nokta (end-effector) konumunu (X, Y) ve yönelimini hesaplar.
    """
    if l1 <= 0 or l2 <= 0:
        return None, "Kol uzunlukları pozitif olmalıdır."
        
    t1_rad = math.radians(theta1_deg)
    t2_rad = math.radians(theta2_deg)
    
    # 1. Eklem (Dirsek) konumu
    x1 = l1 * math.cos(t1_rad)
    y1 = l1 * math.sin(t1_rad)
    
    # Uç Nokta (End-Effector) konumu
    x_ee = x1 + l2 * math.cos(t1_rad + t2_rad)
    y_ee = y1 + l2 * math.sin(t1_rad + t2_rad)
    phi_deg = (theta1_deg + theta2_deg) % 360.0
    
    return {
        "1. Eklem / Dirsek (X1, Y1 - mm)": (x1, y1),
        "Uç Nokta Konumu (X, Y - mm)": (x_ee, y_ee),
        "Toplam Yönelim Açısı φ (derece)": phi_deg,
        "Uç Noktadan Orijine Mesafe R (mm)": math.sqrt(x_ee**2 + y_ee**2)
    }, None

def inverse_kinematics_2r(l1, l2, target_x, target_y):
    """
    2R Manipülatör için Analitik Ters Kinematik.
    Hedeflenen (X, Y) koordinatına ulaşmak için gereken Eklem Açılarını (Dirsek Yukarı / Dirsek Aşağı) hesaplar.
    """
    if l1 <= 0 or l2 <= 0:
        return None, "Kol uzunlukları pozitif olmalıdır."
        
    dist_sq = target_x**2 + target_y**2
    dist = math.sqrt(dist_sq)
    
    # Çalışma alanı (Workspace) kontrolü
    max_reach = l1 + l2
    min_reach = abs(l1 - l2)
    
    if dist > max_reach:
        return None, f"Hedef nokta çalışma uzayının dışında! (Maksimum erişim: {max_reach:.2f} mm, İstenen: {dist:.2f} mm)"
    if dist < min_reach:
        return None, f"Hedef nokta çalışma uzayının iç sınırının altında! (Minimum erişim: {min_reach:.2f} mm)"
        
    # Kosinüs teoremi: D^2 = L1^2 + L2^2 + 2*L1*L2*cos(theta2)
    cos_t2 = (dist_sq - l1**2 - l2**2) / (2.0 * l1 * l2)
    # Sayısal yuvarlama hatalarına karşı sınırlandırma
    cos_t2 = max(min(cos_t2, 1.0), -1.0)
    
    # Dirsek Aşağı (Elbow Down): theta2 pozitif
    t2_down_rad = math.acos(cos_t2)
    t1_down_rad = math.atan2(target_y, target_x) - math.atan2(l2 * math.sin(t2_down_rad), l1 + l2 * math.cos(t2_down_rad))
    
    # Dirsek Yukarı (Elbow Up): theta2 negatif
    t2_up_rad = -math.acos(cos_t2)
    t1_up_rad = math.atan2(target_y, target_x) - math.atan2(l2 * math.sin(t2_up_rad), l1 + l2 * math.cos(t2_up_rad))
    
    return {
        "Hedef Konum": (target_x, target_y),
        "Hedefe Uzaklık": dist,
        "Çözüm 1 (Dirsek Aşağı / Elbow Down)": {
            "theta1 (deg)": math.degrees(t1_down_rad),
            "theta2 (deg)": math.degrees(t2_down_rad)
        },
        "Çözüm 2 (Dirsek Yukarı / Elbow Up)": {
            "theta1 (deg)": math.degrees(t1_up_rad),
            "theta2 (deg)": math.degrees(t2_up_rad)
        }
    }, None

def calculate_robot_jacobian(l1, l2, theta1_deg, theta2_deg, omega1_rad_s=0.0, omega2_rad_s=0.0):
    """
    2R Robot için Jakobiyen matrisi, determinantı (tekillik analizi) ve uç nokta kartezyen hızları (Vx, Vy).
    """
    t1_rad = math.radians(theta1_deg)
    t2_rad = math.radians(theta2_deg)
    t12_rad = t1_rad + t2_rad
    
    # J = [[-L1*sin(t1) - L2*sin(t12),  -L2*sin(t12)],
    #      [ L1*cos(t1) + L2*cos(t12),   L2*cos(t12)]]
    j11 = -l1 * math.sin(t1_rad) - l2 * math.sin(t12_rad)
    j12 = -l2 * math.sin(t12_rad)
    j21 = l1 * math.cos(t1_rad) + l2 * math.cos(t12_rad)
    j22 = l2 * math.cos(t12_rad)
    
    # Determinant = L1 * L2 * sin(theta2)
    det_j = l1 * l2 * math.sin(t2_rad)
    is_singular = abs(det_j) < 1e-4
    
    # Uç nokta hızları: [Vx, Vy]^T = J * [w1, w2]^T
    vx = j11 * omega1_rad_s + j12 * omega2_rad_s
    vy = j21 * omega1_rad_s + j22 * omega2_rad_s
    v_total = math.sqrt(vx**2 + vy**2)
    
    return {
        "Jakobiyen Matrisi (J)": [[j11, j12], [j21, j22]],
        "Determinant det(J)": det_j,
        "Kinematik Tekillik Durumu": "TEKİLLİK MEVCUT (Singular! Robot serbestliğini kaybetti)" if is_singular else "GÜVENLİ (Non-singular)",
        "Uç Nokta Hızı Vx (mm/s)": vx,
        "Uç Nokta Hızı Vy (mm/s)": vy,
        "Bileşke Uç Nokta Hızı V (mm/s)": v_total
    }

def interactive_fk():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}   2R ROBOT KOLU İLERİ KİNEMATİK (FK) HESABI      {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("Açılardan uç nokta koordinatlarını hesaplama.")
    print("-" * 50)
    try:
        l1 = float(input("1. Kol Uzunluğu L1 (mm) [Örn: 300]: "))
        l2 = float(input("2. Kol Uzunluğu L2 (mm) [Örn: 250]: "))
        t1 = float(input("1. Eklem Açısı θ1 (derece) [Örn: 30]: "))
        t2 = float(input("2. Eklem Açısı θ2 (derece) [Örn: 45]: "))
        
        res, err = forward_kinematics_2r(l1, l2, t1, t2)
        if err:
            print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}>>> İLERİ KİNEMATİK SONUÇLARI <<<{Colors.ENDC}")
            x1, y1 = res["1. Eklem / Dirsek (X1, Y1 - mm)"]
            x_ee, y_ee = res["Uç Nokta Konumu (X, Y - mm)"]
            print(f"  Dirsek Konumu (X1, Y1)       : ({x1:.2f}, {y1:.2f}) mm")
            print(f"  Uç Nokta Konumu (X, Y)       : {Colors.BOLD}({x_ee:.2f}, {y_ee:.2f}) mm{Colors.ENDC}")
            print(f"  Toplam Yönelim Açısı φ       : {res['Toplam Yönelim Açısı φ (derece)']:.2f}°")
            print(f"  Orijine Uzaklık R            : {res['Uç Noktadan Orijine Mesafe R (mm)']:.2f} mm")
    except ValueError:
        print(f"{Colors.FAIL}Hata: Sayısal değer giriniz.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def interactive_ik():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}    2R ROBOT KOLU TERS KİNEMATİK (IK) HESABI      {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("Hedeflenen (X,Y) koordinatına ulaşmak için gereken motor açıları.")
    print("-" * 50)
    try:
        l1 = float(input("1. Kol Uzunluğu L1 (mm) [Örn: 300]: "))
        l2 = float(input("2. Kol Uzunluğu L2 (mm) [Örn: 250]: "))
        tx = float(input("Hedef X Koordinatı (mm): "))
        ty = float(input("Hedef Y Koordinatı (mm): "))
        
        res, err = inverse_kinematics_2r(l1, l2, tx, ty)
        if err:
            print(f"{Colors.FAIL}Hata: {err}{Colors.ENDC}")
        else:
            print(f"\n{Colors.OKGREEN}>>> TERS KİNEMATİK ÇÖZÜMLERİ <<<{Colors.ENDC}")
            c1 = res["Çözüm 1 (Dirsek Aşağı / Elbow Down)"]
            c2 = res["Çözüm 2 (Dirsek Yukarı / Elbow Up)"]
            print(f"  {Colors.BOLD}Çözüm 1 (Dirsek Aşağı - Elbow Down):{Colors.ENDC}")
            print(f"    θ1 = {c1['theta1 (deg)']:8.2f}° | θ2 = {c1['theta2 (deg)']:8.2f}°")
            print(f"  {Colors.BOLD}Çözüm 2 (Dirsek Yukarı - Elbow Up):{Colors.ENDC}")
            print(f"    θ1 = {c2['theta1 (deg)']:8.2f}° | θ2 = {c2['theta2 (deg)']:8.2f}°")
    except ValueError:
        print(f"{Colors.FAIL}Hata: Sayısal değer giriniz.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def interactive_jacobian():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}    JAKOBİYEN & KİNEMATİK TEKİLLİK ANALİZİ        {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    try:
        l1 = float(input("1. Kol Uzunluğu L1 (mm) [Örn: 300]: "))
        l2 = float(input("2. Kol Uzunluğu L2 (mm) [Örn: 250]: "))
        t1 = float(input("θ1 Açısı (derece): "))
        t2 = float(input("θ2 Açısı (derece) [0 veya 180 tekillik yaratır]: "))
        w1 = float(input("1. Eklem Açısal Hızı w1 (rad/s) [Örn: 1.0]: ") or "0")
        w2 = float(input("2. Eklem Açısal Hızı w2 (rad/s) [Örn: 0.5]: ") or "0")
        
        res = calculate_robot_jacobian(l1, l2, t1, t2, w1, w2)
        print(f"\n{Colors.OKGREEN}>>> JAKOBİYEN VE HIZ SONUÇLARI <<<{Colors.ENDC}")
        j = res["Jakobiyen Matrisi (J)"]
        print(f"  J = [ [{j[0][0]:8.2f}, {j[0][1]:8.2f}],")
        print(f"        [{j[1][0]:8.2f}, {j[1][1]:8.2f}] ]")
        print(f"  Determinant det(J)           : {res['Determinant det(J)']:.4f}")
        color = Colors.FAIL if "TEKİLLİK" in res["Kinematik Tekillik Durumu"] else Colors.OKGREEN
        print(f"  Durum                        : {color}{res['Kinematik Tekillik Durumu']}{Colors.ENDC}")
        print(f"  Uç Nokta Hızı (Vx, Vy)       : ({res['Uç Nokta Hızı Vx (mm/s)']:.2f}, {res['Uç Nokta Hızı Vy (mm/s)']:.2f}) mm/s")
        print(f"  Bileşke Çizgisel Hız V       : {Colors.BOLD}{res['Bileşke Uç Nokta Hızı V (mm/s)']:.2f} mm/s{Colors.ENDC}")
    except ValueError:
        print(f"{Colors.FAIL}Hata: Sayısal değer giriniz.{Colors.ENDC}")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def main():
    if os.name == 'nt':
        os.system('color')
    while True:
        clear_screen()
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.BOLD}   🤖 ROBOTİK VE MANİPÜLATÖR KİNEMATİĞİ ARAÇLARI {Colors.ENDC}")
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        print(f"{Colors.OKCYAN}1.{Colors.ENDC} 2R Robot Kolu İleri Kinematik (FK)")
        print(f"{Colors.OKCYAN}2.{Colors.ENDC} 2R Robot Kolu Ters Kinematik (IK)")
        print(f"{Colors.OKCYAN}3.{Colors.ENDC} Jakobiyen Matrisi, Hız ve Tekillik Analizi")
        print(f"{Colors.WARNING}0.{Colors.ENDC} Geri Dön")
        print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
        secim = input("Seçiminiz: ").strip()
        if secim == '1':
            interactive_fk()
        elif secim == '2':
            interactive_ik()
        elif secim == '3':
            interactive_jacobian()
        elif secim == '0':
            break

if __name__ == "__main__":
    main()
