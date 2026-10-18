# 🏗️ Yapı Statiği ve Mukavemet Mühendisliği (Structural Mechanics)

Bu modül, makine şasileri, köprüler, taşıyıcı profiller ve inşaat kirişlerinde yük altında oluşan eğilme momentlerini, kesit atalet momentlerini ($I_x$), maksimum gerilmeleri ($\sigma_{max}$) ve elastik sehimleri ($\delta_{max}$) analitik olarak hesaplar.

---

## 📌 Temel Mukavemet Formülleri

### 1. Eğilme Gerilmesi (Euler-Bernoulli Kiriş Teorisi)
Kirişin en dış liflerinde oluşan maksimum normal gerilme:
$$\sigma_{max} = \frac{M_{max} \cdot y_{max}}{I_x} = \frac{M_{max}}{W_x}$$

- $M_{max}$: Kiriş üzerindeki maksimum eğilme momenti ($\text{N}\cdot\text{mm}$)
- $I_x$: Kesit atalet momenti ($\text{mm}^4$)
- $W_x$: Mukavemet momenti ($\text{mm}^3$)
- $\sigma_{max}$: Oluşan maksimum eğilme gerilmesi ($\text{MPa}$ veya $\text{N/mm}^2$)

---

### 2. Emniyet Katsayısı (Safety Factor - SF)
Malzemenin plastik deformasyona uğramadan (akmadan) yükü taşıyabilme payı:
$$SF = \frac{S_y}{\sigma_{max}}$$

- $SF \ge 1.5$: Genel mühendislik yapıları için güvenli kabul edilir.
- $1.0 \le SF < 1.5$: Kritik sınır / Titreşim ve dinamik yüklere dikkat edilmeli.
- $SF < 1.0$: Yapıda kalıcı akma ve hasar meydana gelir.

---

### 3. Yükleme Tipleri ve Sehim Denklemleri

| Mesnet ve Yükleme Şekli | Maksimum Moment ($M_{max}$) | Maksimum Sehim ($\delta_{max}$) |
| :--- | :--- | :--- |
| **Basit Mesnetli - Ortadan Tekil Yük ($F$)** | $$\frac{F \cdot L}{4}$$ | $$\frac{F \cdot L^3}{48 \cdot E \cdot I_x}$$ |
| **Basit Mesnetli - Yayılı Yük ($q$)** | $$\frac{q \cdot L^2}{8}$$ | $$\frac{5 \cdot q \cdot L^4}{384 \cdot E \cdot I_x}$$ |
| **Konsol (Ankastre) - Uçtan Tekil Yük ($F$)** | $$F \cdot L$$ | $$\frac{F \cdot L^3}{3 \cdot E \cdot I_x}$$ |
| **Konsol (Ankastre) - Yayılı Yük ($q$)** | $$\frac{q \cdot L^2}{2}$$ | $$\frac{q \cdot L^4}{8 \cdot E \cdot I_x}$$ |

> [!NOTE]
> Genel mimari ve makine standartlarında izin verilen azami elastik sehim kriteri olarak $\delta_{max} \le \frac{L}{300}$ veya $\frac{L}{250}$ kısıtı uygulanır.

---

## 🚀 Çalıştırma

```bash
python mechanical-civil/structural-mechanics/beam_stress_calculator.py
```
