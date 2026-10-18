# 🔋 Bataryalı Enerji Depolama Sistemleri (BESS & Grid Storage)

Bu modül, yenilenebilir enerji kaynaklarıyla (Güneş PV, Rüzgar) entegre çalışan veya bağımsız (off-grid / microgrid) çalışan Bataryalı Enerji Depolama Sistemlerinin (Battery Energy Storage System - BESS) kapasite, gerilim, Ah boyutlandırmalarını ve seviyelendirilmiş depolama maliyetini (LCOS) hesaplar.

---

## 📌 Temel Prensipler ve Formüller

### 1. BESS Kapasite Boyutlandırma
Günlük tüketilen enerji ve istenen özerklik (otonomi) süresine bağlı olarak bataryadan çekilmesi gereken net enerji belirlenir:

$$E_{net} = E_{günlük} \times N_{gün}$$

Akülerin kimyasal yapısına göre izin verilen maksimum deşarj derinliği ($\text{DoD}$) ve çevrim verimlilikleri göz önüne alındığında gerekli nominal depolama kapasitesi:

$$E_{nominal} = \frac{E_{net}}{\text{DoD} \times \eta_{batarya} \times \eta_{invertör}}$$

- $C_{Ah} = \frac{E_{nominal} \times 1000}{V_{DC}}$ (Amper-saat kapasite)

### 2. Batarya Kimyaları Karşılaştırması

| Batarya Kimyası | Tipik DoD (%) | Çift Yönlü Verim (RTE) | Döngü Ömrü (Cycles) |
| :--- | :--- | :--- | :--- |
| **LiFePO4 (Lityum Demir Fosfat)** | %90 | %92 - %96 | 6000+ |
| **NMC (Lityum Nikel Mangan Kobalt)** | %80 | %90 - %94 | 3000 |
| **AGM / Jel (Kurşun-Asit)** | %50 | %80 - %85 | 500 - 800 |

---

### 3. Düzleştirilmiş Depolama Maliyeti (LCOS - Levelized Cost of Storage)

Depolanan her 1 kWh enerjinin batarya ömrü boyunca toplam maliyet karşılığı:

$$LCOS = \frac{\text{CAPEX} + \sum \text{OPEX}}{\text{Yaşam Boyu Teslim Edilen Toplam Enerji (kWh)}}$$

---

## 🚀 Çalıştırma

```bash
python energy-engineering/storage-grid/bess_storage_calculator.py
```
