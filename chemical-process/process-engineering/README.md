# 🧪 Kimya ve Süreç Mühendisliği (Chemical & Process Engineering)

Bu modül, kimya tesislerinde, proses borulamalarında, rafinerilerde ve gıda/ilaç üretim hatlarında yaygın olarak ihtiyaç duyulan hidrolik basınç kayıpları, ısı değiştirici (eşanjör) tasarımı ve çözelti seyreltme hesaplamalarını kapsar.

---

## 📌 Teorik Prensipler ve Formüller

### 1. Borularda Basınç Düşüşü ve Reynolds Sayısı

*   **Reynolds Sayısı ($Re$):** Akışın laminer mi yoksa türbülanslı mı olduğunu belirleyen boyutsuz sayıdır:
    $$Re = \frac{\rho \cdot v \cdot D}{\mu}$$
    - $Re < 2300$: Laminer Akış
    - $2300 \le Re \le 4000$: Geçiş Rejimi
    - $Re > 4000$: Türbülanslı Akış

*   **Sürtünme Faktörü ($f$):**
    - Laminer akış:
      $$f = \frac{64}{Re}$$
    - Türbülanslı akış (Colebrook-White denkleminin açık çözümü olan **Haaland Formülü**):
      $$\frac{1}{\sqrt{f}} = -1.8 \log_{10} \left[ \left(\frac{\varepsilon / D}{3.7}\right)^{1.11} + \frac{6.9}{Re} \right]$$

*   **Darcy-Weisbach Basınç Kaybı:**
    $$\Delta P = f \cdot \frac{L}{D} \cdot \frac{\rho \cdot v^2}{2} \quad [\text{Pascal}]$$

---

### 2. Isı Eşanjörleri ve LMTD (Log Mean Temperature Difference)

Eşanjör boyunca sıcak ve soğuk akışkan arasındaki sıcaklık farkı değişkenlik gösterdiğinden, transfer edilen ısı logaritmik ortalama fark ile hesaplanır:

$$\Delta T_{lm} = \frac{\Delta T_1 - \Delta T_2}{\ln(\Delta T_1 / \Delta T_2)}$$

*   **Karşıt Akış (Counter-flow):**
    $$\Delta T_1 = T_{h,in} - T_{c,out}, \quad \Delta T_2 = T_{h,out} - T_{c,in}$$
*   **Paralel Akış (Parallel-flow):**
    $$\Delta T_1 = T_{h,in} - T_{c,in}, \quad \Delta T_2 = T_{h,out} - T_{c,out}$$

Toplam Isı Geçişi ve Gerekli Alan:
$$Q = U \cdot A \cdot \Delta T_{lm} \implies A = \frac{Q}{U \cdot \Delta T_{lm}}$$

---

### 3. Çözelti Karışım ve Kütle Dengesi

Kimyasal reaktörlerde ve seyreltme tanklarında kütle korunumu ilkesi:
$$C_1 V_1 + C_2 V_2 = C_f V_f$$

---

## 🚀 Çalıştırma

```bash
python chemical-process/process-engineering/fluid_thermal_calculator.py
```
