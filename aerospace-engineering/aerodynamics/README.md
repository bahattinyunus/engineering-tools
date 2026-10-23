# ✈️ Havacılık ve Aerodinamik Mühendisliği (Aerospace Engineering)

Bu modül, hava araçlarının uçuş mekaniği, standart atmosfer modellemesi (ISA), NACA kanat profili geometrileri ve aerodinamik kuvvet analizlerini analitik yöntemlerle gerçekleştirir.

---

## 📌 Teorik Prensipler ve Formüller

### 1. Uluslararası Standart Atmosfer (ISA - ICAO Doc 7488)
Deniz seviyesinden ($h=0$) stratosfere kadar irtifaya bağlı termodinamik atmosfer parametreleri:

*   **Troposfer ($0 \le h \le 11000\text{ m}$):**
    Sıcaklık lineer olarak düşer ($L = 0.0065\text{ K/m}$):
    $$T(h) = T_0 - L \cdot h$$
    $$P(h) = P_0 \left( \frac{T(h)}{T_0} \right)^{\frac{g_0}{R \cdot L}}$$
    $$\rho(h) = \frac{P(h)}{R \cdot T(h)}$$
    $$a(h) = \sqrt{\gamma \cdot R \cdot T(h)} \quad (\text{Ses Hızı})$$

*   **Mach Sayısı ($M$):**
    $$M = \frac{v}{a}$$
    - $M < 0.8$: Subsonik
    - $0.8 \le M \le 1.2$: Transonik
    - $1.2 < M \le 5.0$: Süpersonik
    - $M > 5.0$: Hipersonik

---

### 2. NACA 4-Basamaklı Kanat Profili Denklemleri

NACA $MPTT$ serisi (Örn: NACA 2412 $\rightarrow M=2\%$, $P=0.4$, $TT=12\%$):

*   **Kalınlık Dağılımı ($y_t$):**
    $$y_t = 5t \left( 0.2969\sqrt{x} - 0.1260x - 0.3516x^2 + 0.2843x^3 - 0.1015x^4 \right)$$
*   **Ortalama Kamburluk Çizgisi ($y_c$):**
    - $0 \le x \le p$:
      $$y_c = \frac{m}{p^2} (2px - x^2)$$
    - $p < x \le 1$:
      $$y_c = \frac{m}{(1-p)^2} \left[ (1-2p) + 2px - x^2 \right]$$

---

### 3. Aerodinamik Kuvvetler & Sonlu Kanat Teorisi

*   **Taşıma Kuvveti (Lift):** $L = C_L \cdot q \cdot S$
*   **Sürükleme Kuvveti (Drag):** $D = C_D \cdot q \cdot S$
*   **İndüklenmiş Sürükleme (Induced Drag - Prandtl):**
    $$C_{Di} = \frac{C_L^2}{\pi \cdot AR \cdot e}$$
    - $AR = b^2 / S$: Kanat açıklık oranı (Aspect Ratio)
    - $e$: Oswald kanat verim faktörü ($\approx 0.80 - 0.90$)

---

## 🚀 Çalıştırma

```bash
python aerospace-engineering/aerodynamics/airfoil_analyzer.py
```
