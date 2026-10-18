# ⚡ Elektrik ve Devre Mühendisliği (Electrical & Circuit Design)

Bu modül, tesis elektrik dağıtım projelerinde kablo kesiti seçimi, gerilim düşümü tahkiki, filtre rezonans frekansları ve reaktif güç kompanzasyonu hesaplamalarını uluslararası standartlara uygun olarak gerçekleştirir.

---

## 📌 Teorik Temeller ve Standartlar

### 1. Kablo Gerilim Düşümü ve İletken Boyutlandırma (IEC 60364-5-52)
Elektrik hatlarında iletken direnci sebebiyle kaynak ile yük arasında gerilim düşümü meydana gelir:

*   **Tek Faz / 2 İletkenli DC Sistem:**
    $$\Delta U = \frac{2 \cdot L \cdot I \cdot \cos\varphi}{\kappa \cdot S} = 2 \cdot I \cdot R \cdot \cos\varphi$$
*   **Dengeli Üç Faz Sistem (400V AC):**
    $$\Delta U = \frac{\sqrt{3} \cdot L \cdot I \cdot \cos\varphi}{\kappa \cdot S}$$
*   **Yüzde Gerilim Düşümü:**
    $$\% \Delta U = \frac{\Delta U}{U_n} \times 100$$

Burada:
- $L$: Hat uzunluğu (metre)
- $I$: Hat akımı (Amper)
- $S$: Kablo kesiti ($\text{mm}^2$)
- $\kappa$: İletken iletkenliği ($\text{m} / (\Omega \cdot \text{mm}^2)$) $\rightarrow$ Bakır için $\approx 56$, Alüminyum için $\approx 35$
- $\cos\varphi$: Güç faktörü

> [!IMPORTANT]
> **Standart Limitler:** IEC ve VDE standartlarına göre ana dağıtım panosundan tali panoya veya aydınlatma linyelerine olan gerilim düşümü **%3'ü**, motor ve güç devrelerinde ise **%5'i** aşmamalıdır.

---

### 2. Filtre Frekansları ve Rezonans

*   **RC Alçak/Yüksek Geçiren Kesim Frekansı (Cutoff Frequency - $f_c$):**
    $$f_c = \frac{1}{2 \pi R C}$$
*   **RL Kesim Frekansı:**
    $$f_c = \frac{R}{2 \pi L}$$
*   **RLC Rezonans Frekansı ($f_0$):**
    $$f_0 = \frac{1}{2 \pi \sqrt{L C}}$$
*   **Seri RLC Kalite Faktörü ($Q$) ve Bant Genişliği ($BW$):**
    $$Q = \frac{1}{R} \sqrt{\frac{L}{C}}, \quad BW = \frac{f_0}{Q}$$

---

### 3. Reaktif Güç Kompanzasyonu

Endüktif yüklerin (asenkron motorlar, transformatörler) şebekeden çektiği reaktif gücü yerel olarak sağlamak için kondansatör bataryaları kullanılır:

$$Q_c = P \cdot (\tan\varphi_1 - \tan\varphi_2)$$

- $P$: Tesis aktif gücü ($\text{kW}$)
- $\cos\varphi_1$: Mevcut güç katsayısı
- $\cos\varphi_2$: Hedef güç katsayısı (genellikle $\ge 0.98$)
- $Q_c$: Gerekli kondansatör gücü ($\text{kVAR}$)

---

## 🚀 Kullanım

```bash
python automation-electronics/circuit-design/electrical_calculator.py
```
