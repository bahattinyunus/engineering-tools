# ☀️ Yenilenebilir Enerji Mühendisliği (Renewable Energy)

Bu modül, fotovoltaik (PV) güneş enerjisi santralleri ve rüzgar türbinlerinin enerji üretim potansiyellerini hesaplamak amacıyla geliştirilmiştir.

---

## 📌 Teorik Temeller

### 1. Güneş Paneli (PV) Güç Üretim Modeli

Fotovoltaik panellerin anlık elektriksel güç çıkışı:
$$P_{pv} = A \cdot \eta \cdot G \cdot PR$$

- $P_{pv}$: Üretilen Anlık Güç ($\text{Watt}$)
- $A$: Toplam Panel Alanı ($\text{m}^2$)
- $\eta$: Panel Verimliliği (Monokristal için $\approx \%20-\%23$, Polikristal için $\approx \%16-\%18$)
- $G$: Yüzeye Düşen Güneş Işınımı ($\text{W/m}^2$, Standart Test Koşullarında $1000\ \text{W/m}^2$)
- $PR$: Performans Oranı (Performance Ratio: Sıcaklık, kablo ve invertör kayıpları $\approx 0.75 - 0.85$)

---

### 2. Rüzgar Türbini Güç Modeli ve Betz Limiti

Rüzgarın kinetik enerjisinden türbin rotoru vasıtasıyla elde edilebilecek mekanik güç:

$$P_{wind} = \frac{1}{2} \cdot \rho \cdot A \cdot v^3 \cdot C_p$$

- $\rho$: Hava Yoğunluğu ($\approx 1.225\ \text{kg/m}^3$ deniz seviyesinde)
- $A$: Rotor Süpürme Alanı ($A = \pi \cdot R^2$, $\text{m}^2$)
- $v$: Rüzgar Hızı ($\text{m/s}$)
- $C_p$: Türbin Güç Katsayısı (Aerodinamik verim)

> [!IMPORTANT]
> **Betz Yasası (1919):** Hiçbir rüzgar türbini, rüzgardaki kinetik enerjinin $\frac{16}{27}$'sinden (%59.3) fazlasını elektriğe dönüştüremez. Dolayısıyla teorik üst sınır $C_{p,max} = 0.593$'tür. Modern türbinler $0.40 - 0.48$ aralığında çalışır.

---

## 🚀 Çalıştırma

```bash
python energy-engineering/renewables/power_calculator.py
```
