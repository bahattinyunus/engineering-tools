# 🔊 Akustik ve Titreşim Mühendisliği (Acoustics & Vibration Analysis)

Bu modül; makine dinamik yükleri, rezonans tahkiki, sönüm oranları ve endüstriyel ortamlarda gürültü seviyelerinin (dB SPL) logaritmik olarak hesaplanması için geliştirilmiştir.

---

## 📌 Teorik Formüller ve Prensipler

### 1. 1-Serbestlik Dereceli (SDOF) Titreşim Modeli

*   **Doğal Frekans ($f_n$):**
    $$\omega_n = \sqrt{\frac{k}{m}} \quad [\text{rad/s}], \qquad f_n = \frac{\omega_n}{2\pi} \quad [\text{Hz}]$$
*   **Kritik Sönüm Katsayısı ($c_c$):**
    $$c_c = 2\sqrt{k \cdot m} = 2m\omega_n$$
*   **Sönüm Oranı ($\zeta$):**
    $$\zeta = \frac{c}{c_c}$$
    - $\zeta < 1$: Düşük sönümlü titreşim ($f_d = f_n \sqrt{1 - \zeta^2}$)
    - $\zeta = 1$: Kritik sönümlü (sistemin en hızlı dengeye gelişi)
    - $\zeta > 1$: Aşırı sönümlü (salınımsız yavaş hareket)
*   **Dinamik Büyütme Faktörü (DMF / Q):**
    Zorlanmış harmonik tahrik altında frekans oranı $r = \omega / \omega_n$:
    $$DMF = \frac{1}{\sqrt{(1 - r^2)^2 + (2\zeta r)^2}}$$
    > [!WARNING]
    > $r \approx 1.0$ civarında sönüm düşükse sistem rezonansa girer ve genlik yıkıcı boyutlara ulaşır.

---

### 2. Endüstriyel Akustik ve Desibel (dB SPL)

*   **Ses Basınç Seviyesi ($L_p$):**
    $$L_p = 20 \log_{10} \left( \frac{p}{p_0} \right) \quad [\text{dB SPL}]$$
    - Referans eşik basıncı: $p_0 = 20\ \mu\text{Pa}$ ($2 \times 10^{-5}\ \text{Pa}$)
*   **Gürültü Kaynaklarının Logaritmik Toplamı:**
    $$L_{toplam} = 10 \log_{10} \left( \sum_{i=1}^n 10^{\frac{L_i}{10}} \right)$$
*   **Noktasal Kaynak Mesafe Zayıflaması (Ters Kare Kanunu):**
    $$L_{p2} = L_{p1} - 20 \log_{10} \left( \frac{r_2}{r_1} \right)$$

---

## 🚀 Çalıştırma

```bash
python mechanical-civil/acoustics-vibration/vibration_analyzer.py
```
