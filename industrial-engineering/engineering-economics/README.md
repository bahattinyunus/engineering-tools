# 💰 Mühendislik Ekonomisi ve Yatırım Bütçelemesi (Engineering Economics)

Bu modül; sermaye yatırımı gerektiren fabrika modernizasyonu, otomasyon, yeni makine alımı ve Ar-Ge projelerinin finansal fizibilitesini Net Bugünkü Değer (NPV), İç Karlılık Oranı (IRR) ve İskontolu Geri Ödeme yöntemleriyle analiz eder.

---

## 📌 Temel Finansal Formüller

### 1. Net Bugünkü Değer (NPV - Net Present Value)
Gelecekteki nakit akışlarının paranın zaman değeri ($r$) ile bugüne indirgenmiş toplamından ilk yatırımın çıkarılması:

$$NPV = \sum_{t=1}^n \frac{CF_t}{(1 + r)^t} - CF_0$$

- $NPV > 0$: Proje sermaye maliyetinin üzerinde getiri sağlar; yatırım onaylanır.
- $NPV \le 0$: Proje yatırımcının minimum getiri beklentisini karşılamaz; reddedilir.

---

### 2. İç Karlılık Oranı (IRR - Internal Rate of Return)
Net bugünkü değeri tam sıfır yapan iskonto oranıdır:

$$\sum_{t=1}^n \frac{CF_t}{(1 + IRR)^t} - CF_0 = 0$$

Newton-Raphson iterasyonu ile analitik olarak çözülür. $IRR > r$ ise proje caziptir.

---

### 3. Geri Ödeme Süresi (Payback Period) ve ROI
*   **Basit Geri Ödeme:** Nakit akışlarının kümülatif toplamının ilk yatırımı karşıladığı yıl sayısı.
*   **İskontolu Geri Ödeme:** İndirgenmiş nakit akışları kümülatifinin $CF_0$'a ulaştığı süre.
*   **Yatırım Getirisi (ROI):**
    $$ROI = \frac{\sum CF_t - CF_0}{CF_0} \times 100 \quad [\%]$$

---

## 🚀 Çalıştırma

```bash
python industrial-engineering/engineering-economics/capital_budgeting.py
```
