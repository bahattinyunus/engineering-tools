# 🔥 Termodinamik ve Güç Döngüleri (Thermodynamics & Power Cycles)

Bu modül, enerji santralleri, jet motorları, gaz türbinleri ve içten yanmalı motorlarda uygulanan temel termodinamik çevrimlerin termal verimlerini, iş üretimlerini ve katsayılarını hesaplar.

---

## 📌 Termodinamik Döngü Modelleri

### 1. Carnot Çevrimi (İdeal Üst Sınır)
Termodinamiğin 2. Yasası gereği belirli iki sıcaklık sınırı arasında çalışabilecek en yüksek verimli çevrimdir:

$$\eta_{carnot} = 1 - \frac{T_C}{T_H}$$

- $T_H$: Sıcak kaynak mutlak sıcaklığı (Kelvin)
- $T_C$: Soğuk kaynak mutlak sıcaklığı (Kelvin)

---

### 2. Brayton Çevrimi (Gaz Türbinleri ve Jet İtkisi)
Açık ve kapalı çevrim gaz türbinlerinin temelidir:

$$\eta_{brayton} = 1 - \frac{1}{r_p^{\frac{\gamma - 1}{\gamma}}}$$

- $r_p = P_2 / P_1$: Kompresör basınç oranı
- $\gamma = C_p / C_v$: İzantropik katsayı (Hava için $\approx 1.4$)
- Geri İş Oranı (BWR - Back Work Ratio): $BWR = W_{kompresor} / W_{türbin}$

---

### 3. Otto ve Diesel Çevrimleri (İçten Yanmalı Motorlar)

*   **Otto Çevrimi (Benzin / Buji Ateşlemeli):**
    $$\eta_{otto} = 1 - \frac{1}{r^{\gamma - 1}}$$
    - $r = V_{max} / V_{min}$: Sıkıştırma oranı (genellikle $8 - 12$)

*   **Diesel Çevrimi (Sıkıştırma ile Ateşlemeli):**
    $$\eta_{diesel} = 1 - \frac{1}{r^{\gamma - 1}} \left[ \frac{r_c^\gamma - 1}{\gamma (r_c - 1)} \right]$$
    - $r_c = V_3 / V_2$: Kesme (cut-off) oranı
    - Dizel motorlar daha yüksek sıkıştırma oranına ($r \approx 16 - 22$) ulaştığı için Otto motorlarına göre daha yüksek verim sergiler.

---

## 🚀 Çalıştırma

```bash
python mechanical-civil/thermodynamics/cycle_calculator.py
```
