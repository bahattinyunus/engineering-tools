# 🛠️ Engineering Tools (Mühendislik Araçları ve Standartları)

![Engineering Tools Banner](assets/banner.jpg)

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Tests: 33 Passed](https://img.shields.io/badge/Tests-33%20Passed-brightgreen.svg)
![Maintained: Yes](https://img.shields.io/badge/Maintained-Yes-green.svg)
![Contributions: Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)
![Dependencies: None (Standard Library Only)](https://img.shields.io/badge/Dependencies-Standard%20Library%20Only-orange.svg)

Bu depo; yazılım, mekatronik, robotik, yapı statiği, termodinamik, kimyasal prosesler, havacılık/aerodinamik, endüstriyel kalite ve yenilenebilir enerji disiplinlerinde kullanılan temel algoritmalar, matematiksel modellemeler ve endüstri standartlarının kapsamlı bir referans rehberi ve **18 adet interaktif konsol aracından oluşan** kütüphanesidir. Çok disiplinli projeler geliştiren mühendisler, araştırmacılar ve teknik ekipler için taşınabilir, saf standart kütüphaneli bir mühendislik araç setidir.

---

## 📌 İçindekiler
1. [Hakkında](#-hakkında)
2. [Hızlı Başlangıç (Launcher Arayüzü)](#-hızlı-başlangıç-launcher-arayüzü)
3. [Mühendislik Branşları ve Araç Kataloğu](#-mühendislik-branşları-ve-araç-kataloğu)
    - [1. Yazılım ve Bilgisayar Mühendisliği](#1-yazılım-ve-bilgisayar-mühendisliği)
    - [2. Elektrik-Elektronik, Otomasyon ve Robotik](#2-elektrik-elektronik-otomasyon-ve-robotik)
    - [3. Makine ve İnşaat Mühendisliği (Statik & Termodinamik)](#3-makine-ve-inşaat-mühendisliği-statik--termodinamik)
    - [4. Kimya ve Süreç Mühendisliği (Proses Hidroliği & Isı Transferi)](#4-kimya-ve-süreç-mühendisliği-proses-hidroliği--ısı-transferi)
    - [5. Havacılık ve Uzay Mühendisliği (Aerodinamik & Atmosfer)](#5-havacılık-ve-uzay-mühendisliği-aerodinamik--atmosfer)
    - [6. Endüstri Mühendisliği (Yalın & Altı Sigma)](#6-endüstri-mühendisliği-yalın--altı-sigma)
    - [7. Kalite Standartları ve Güvenlik (ISO & HACCP)](#7-kalite-standartları-ve-güvenlik-iso--haccp)
    - [8. Çevre ve Sürdürülebilirlik (ESG & Karbon Ayak İzi)](#8-çevre-ve-sürdürülebilirlik-esg--karbon-ayak-izi)
    - [9. Enerji Sistemleri Mühendisliği (Güneş, Rüzgar, BESS)](#9-enerji-sistemleri-mühendisliği-güneş-rüzgar-bess)
4. [Proje Klasör Yapısı](#-proje-klasör-yapısı)
5. [Otomatik Testler (Unit Tests & CI/CD)](#-otomatik-testler-unit-tests--cicd)
6. [Kurulum ve Çalıştırma](#-kurulum-ve-çalıştırma)
7. [Katkıda Bulunma (Contributing)](#-katkıda-bulunma)
8. [Mühendislik Alıntıları ve Kaynakça](#-mühendislik-alıntıları-ve-kaynakça)
9. [Lisans](#-lisans)

---

## 📖 Hakkında
Modern mühendislik projeleri artık tek bir disiplinin sınırları içinde kalmamakta, yazılım, robotik, mekanik, aerodinamik, kimyasal süreçler ve enerji altyapılarının entegrasyonuyla şekillenmektedir. Deponun temel özellikleri:

*   **Sıfır Dış Bağımlılık (Zero Dependencies):** Projedeki tüm araçlar ve 33 adet birim testi, üçüncü parti kütüphanelere (`numpy`, `scipy` vb.) ihtiyaç duymaksızın **saf Python standart kütüphanesi** (`math`, `sqlite3`, `unittest`, `time`, `subprocess` vb.) ile çalışır.
*   **Analitik & Endüstriyel Doğruluk:** IEC 60364, ICAO ISA Doc 7488, Darcy-Weisbach, Haaland, Euler-Bernoulli, Brayton ve PMBOK formülleriyle tam uyumludur.
*   **İki Yönlü Kullanım:** İster interaktif renkli CLI menüsünden adım adım hesaplama yapın, ister kendi Python scriptlerinizde fonksiyonları modüler olarak import edin.

---

## 🚀 Hızlı Başlangıç (Launcher Arayüzü)

Merkezi CLI yönlendirici üzerinden tüm araçları tek ekrandan çalıştırabilirsiniz:

```bash
# İnteraktif Menü
python run_tools.py

# Tüm araçları listele
python run_tools.py --list

# Otomatik birim test paketini çalıştır
python run_tools.py --test
```

---

## ⚙️ Mühendislik Branşları ve Araç Kataloğu

### 1. Yazılım ve Bilgisayar Mühendisliği
> 💬 *"First, solve the problem. Then, write the code."* — John Johnson  
> 💬 *"Talk is cheap. Show me the code."* — Linus Torvalds

*   **Veri Analizi ve Polinom Regresyon:** Betimsel istatistik (ortalama, medyan, varyans, standart sapma), 1. derece doğrusal ve 2. derece kuadratik regresyon eğri uydurma.
*   **Birim Dönüştürücü:** Sıcaklık (°C, °F), Basınç (Bar, PSI, Pascal), Uzunluk (inç, mm) ve Hız (m/s, km/h, mph) dönüşümleri.
*   **Malzeme Veri Tabanı Yöneticisi:** SQLite tabanlı, metaller, polimerler ve kompozitlerin yoğunluk, akma mukavemeti, elastisite modülü ve Ashby özgül performans endekslerini ($\sigma_y/\rho$, $E/\rho$) yöneten CRUD aracı.
*   **Bulut TCO & Altyapı Maliyet Hesaplayıcı:** AWS, Azure ve GCP için vCPU, RAM, SSD ve veri çıkışı (egress) gereksinimlerine göre On-Demand ile 1 ve 3 yıllık Rezerv Plan tasarrufları ve veri merkezi karbon ayak izi analizi.
*   **Big-O Karmaşıklık & Benchmark Analizörü:** Sıralama algoritmalarında ($O(N^2), O(N \log N)$) log-log regresyonu ile ampirik karmaşıklık üssü $\beta$ tahmini.
*   *Dizin:* [software/](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/software/)

---

### 2. Elektrik-Elektronik, Otomasyon ve Robotik
> 💬 *"Automation is good, so long as you know exactly where to put the machine."* — Eliyahu M. Goldratt

*   **PLC Register ve PID Simülatörü:** IEC 61131-3 standartlarında Coils, Discrete Inputs, Input Registers ve Holding Registers yapısını, çevrimsel tarama (Scan Cycle), acil stop ve sıcaklık kontrolü PID valf algoritmasını simüle eder.
*   **Kablo Kesiti & Gerilim Düşümü (IEC 60364-5-52):** 1 Faz (230V AC / DC) ve 3 Faz (400V AC) sistemlerde bakır ve alüminyum iletkenler için akım, mesafe ve $\cos\varphi$'ye bağlı voltaj düşümü, güç kaybı ve tolerans kontrolü.
*   **Filtre & RLC Rezonans Analizi:** RC, RL alçak/yüksek geçiren kesim frekansı ($f_c$), seri RLC rezonans frekansı ($f_0$), kalite faktörü ($Q$) ve bant genişliği ($BW$).
*   **Robotik Kol Kinematiği (FK & IK) ve Jakobiyen:** 2R ve düzlemsel manipülatörler için ileri kinematik, analitik ters kinematik (Dirsek Yukarı/Aşağı çözümleri), kartezyen hızlar ve tekillik ($\det(J)=0$) denetimi.
*   *Dizin:* [automation-electronics/](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/automation-electronics/)

---

### 3. Makine ve İnşaat Mühendisliği (Statik & Termodinamik)
> 💬 *"Scientists study the world as it is; engineers create the world that has never been."* — Theodore von Kármán

*   **Kiriş Eğilme Momenti ve Sehim Analizi (Euler-Bernoulli):** Dikdörtgen, dolu daire, boru ve kutu profillerde atalet momenti ($I_x$) ve mukavemet momenti ($W_x$) hesabı. 4 temel yükleme durumunda maksimum eğilme momenti, eğilme gerilmesi ($\sigma_{max}$), emniyet katsayısı ($SF$) ve sehim limit ($\delta \le L/300$) kontrolü.
*   **Termodinamik Güç Döngüleri:** Carnot (maksimum teorik verim), Brayton (gaz türbinleri ve jet motorları geri iş oranı BWR), Otto ve Diesel içten yanmalı motor termal verimleri.
*   **CNC G-Kodu Jeneratörü:** Dikdörtgen ve dairesel profiller için kesim derinliği, ilerleme hızı, spindle devri ve takım çapına göre hazır G-kodu (G21, G90, G01, G02 vb.) üretir.
*   **Kritik Yol Metodu (CPM) ve PERT Proje Planlayıcı:** Görev süreleri ve bağımlılıklarını topolojik sıralama ile işleyerek kritik yolu ve olasılıksal bitiş aralıklarını hesaplar.
*   *Dizin:* [mechanical-civil/](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/mechanical-civil/)

---

### 4. Kimya ve Süreç Mühendisliği (Proses Hidroliği & Isı Transferi)
> 💬 *"Thermodynamics is the only physical theory of universal content."* — Albert Einstein

*   **Boru Akışı Basınç Düşüşü & Reynolds Sayısı:** Darcy-Weisbach formülü ve Haaland türbülans denklemiyle çelik, paslanmaz, plastik veya döküm borularda laminer/türbülanslı rejim ve bar/mSS yük kaybı hesabı.
*   **Isı Eşanjörü LMTD ve Transfer Alanı:** Karşıt ve paralel akışlı eşanjörlerde Logaritmik Ortalama Sıcaklık Farkını ($\Delta T_{lm}$) ve aktarılacak ısı yüküne ($Q$) göre gereken eşanjör yüzey alanını ($A$) boyutlandırır.
*   **Çözelti Karışımı ve Seyreltme Dengesi:** Kütle denkliği ($C_1 V_1 + C_2 V_2 = C_f V_f$) formülüyle saf çözücü ekleme veya farklı derişimlerdeki kimyasalları harmanlama hesabı.
*   *Dizin:* [chemical-process/](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/chemical-process/)

---

### 5. Havacılık ve Uzay Mühendisliği (Aerodinamik & Atmosfer)
> 💬 *"The desire to fly is an idea handed down to us by our ancestors..."* — Wilbur Wright

*   **Uluslararası Standart Atmosfer (ISA):** 0 - 20.000 metre irtifaya bağlı sıcaklık $T(h)$, basınç $P(h)$, hava yoğunluğu $\rho(h)$, ses hızı $a(h)$ ve Mach sayısı ($M = v/a$) hesabı.
*   **NACA 4-Basamaklı Kanat Profili Geometrisi:** NACA 0012, 2412, 4415 vb. profiller için kosinüs aralıklı üst yüzey, alt yüzey ve kamburluk koordinat üretimi.
*   **Kanat Taşıma (Lift), Sürükleme (Drag) ve L/D Analizi:** İnce profil teorisi ve Prandtl taşıma çizgisi modeliyle taşıma katsayısı ($C_L$), indüklenmiş sürükleme ($C_{Di}$) ve süzülme oranı.
*   *Dizin:* [aerospace-engineering/](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/aerospace-engineering/)

---

### 6. Endüstri Mühendisliği (Yalın & Altı Sigma)
> 💬 *"Without data, you're just another person with an opinion."* — W. Edwards Deming

*   **OEE (Toplam Ekipman Etkinliği):** Kullanılabilirlik, Performans ve Kalite oranlarıyla TPM standartlarında verimlilik analizi.
*   **Altı Sigma Analizi:** Hatalı ürün ve hata fırsatına göre DPO, DPMO ve 1.5 Sigma kaydırılmış süreç Sigma Seviyesini Probit fonksiyonuyla belirleme.
*   **Takt Zamanı ve Hat Dengeleme:** Müşteri talebi ve net çalışma süresine göre çevrim süresi gereksinimlerini optimize eder.
*   *Dizin:* [industrial-engineering/](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/industrial-engineering/)

---

### 7. Kalite Standartları ve Güvenlik (ISO & HACCP)
> 💬 *"Quality is not an act, it is a habit."* — Aristotle

*   **ISO Denetim Asistanı:** ISO 9001 (KYS), ISO 22000 (HACCP Gıda Güvenliği) ve ISO 14001 (ÇYS) maddelerine göre iç tetkik denetim puanı ve raporu hazırlayıcı.
*   *Dizin:* [quality-standards/](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/quality-standards/)

---

### 8. Çevre ve Sürdürülebilirlik (ESG & Karbon Ayak İzi)
> 💬 *"We do not inherit the Earth from our ancestors; we borrow it from our children."* — Native American Proverb

*   **Sera Gazı Protokolü (GHG Protocol) Hesaplayıcı:** Kapsam 1 (Doğrudan fosil yakıtlar), Kapsam 2 (Satın alınan şebeke elektriği) ve Kapsam 3 (Uçuş seyahatleri, lojistik) emisyonlarını $tCO_2e$ cinsinden hesaplar.
*   *Dizin:* [environment/](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/environment/)

---

### 9. Enerji Sistemleri Mühendisliği (Güneş, Rüzgar, BESS)
> 💬 *"I'd put my money on the sun and solar energy. What a source of power!"* — Thomas Edison

*   **Güneş (PV) & Rüzgar Güç Hesaplayıcı:** Panel alanı ve ışınımla PV elektrik üretimi; süpürme alanı, hava yoğunluğu ve **Betz Limiti ($C_p \le 0.593$)** ile rüzgar türbini mekanik gücü hesabı.
*   **Bataryalı Enerji Depolama (BESS) & LCOS Boyutlandırma:** LiFePO4 (%90 DoD), NMC (%80 DoD) ve AGM (%50 DoD) akü kimyalarına göre nominal kapasite (kWh/Ah) ve seviyelendirilmiş depolama maliyeti ($/kWh LCOS) hesabı.
*   *Dizin:* [energy-engineering/](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/energy-engineering/)

---

## 📂 Proje Klasör Yapısı

```text
engineering-tools/
│
├── run_tools.py                            # Merkezi CLI Launcher ve Test Yönlendiricisi
├── README.md                               # Kapsamlı Proje Dokümantasyonu
├── LICENSE                                 # MIT Lisansı
├── .gitignore                              # Git Harici Tutma Kuralları
│
├── .github/
│   └── workflows/
│       └── ci.yml                          # GitHub Actions CI/CD Çoklu Platform Testleri
│
├── tests/
│   └── test_engineering_tools.py          # Saf Python 33 Otomatik Birim Test Suite'i
│
├── software/
│   ├── python/                             # İstatistik, Regresyon ve Birim Dönüştürücü
│   ├── databases/                          # SQLite Mühendislik Malzeme DB Yöneticisi
│   ├── cloud/                              # Bulut TCO & Kapasite Hesaplayıcı, DevOps Rehberi
│   └── algorithms/                         # Big-O Karmaşıklık & Sıralama Benchmark Analizörü
│
├── automation-electronics/
│   ├── plc-scada/                          # PLC Modbus & PID Regülasyon Simülatörü
│   ├── circuit-design/                     # Kablo Kesiti, Gerilim Düşümü (IEC) & Filtre Analizi
│   └── robotics/                           # 2R Robot Kolu İleri/Ters Kinematik & Jakobiyen
│
├── mechanical-civil/
│   ├── cad-cam/                            # CNC G-Kodu Üreteci (CAD/CAM)
│   ├── project-management/                 # CPM (Kritik Yol) & PERT Proje Planlayıcı
│   ├── structural-mechanics/               # Kiriş Atalet Momenti, Mukavemet & Sehim Analizi
│   └── thermodynamics/                     # Carnot, Brayton, Otto & Diesel Güç Çevrimleri
│
├── chemical-process/
│   └── process-engineering/                # Darcy-Weisbach Boru Basınç Kaybı, LMTD Eşanjör, Seyreltme
│
├── aerospace-engineering/
│   └── aerodynamics/                       # Standart Atmosfer (ISA), NACA Kanat Profili & Taşıma
│
├── industrial-engineering/
│   └── lean-six-sigma/                     # OEE, DPMO & Altı Sigma Hesaplayıcı, Yalın Üretim
│
├── quality-standards/
│   └── iso-standards/                      # ISO 9001, ISO 22000 (HACCP) & ISO 14001 Denetim Aracı
│
├── environment/
│   └── sustainability-reports/             # Kapsam 1-2-3 Sera Gazı (GHG) Ayak İzi & ESG
│
└── energy-engineering/
    ├── renewables/                         # Güneş PV ve Rüzgar Türbini Güç Hesaplayıcı
    └── storage-grid/                       # BESS Batarya Depolama Boyutlandırma & LCOS Analizi
```

---

## 🧪 Otomatik Testler (Unit Tests & CI/CD)

Depo, 33 adet kapsamlı birim testi içeren otomatik bir test paketine sahiptir:

```bash
# Testleri doğrudan çalıştırma:
python tests/test_engineering_tools.py

# veya Launcher üzerinden:
python run_tools.py --test
```

GitHub Actions iş akışımız (`.github/workflows/ci.yml`), depoya yapılan her commit ve pull request'te **Ubuntu** ve **Windows** üzerinde **Python 3.9, 3.10, 3.11, 3.12 ve 3.13** sürümlerinde tüm testleri doğrulamaktadır.

---

## 🛠 Kurulum ve Çalıştırma

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/bahattinyunus/engineering-tools.git
   ```
2. Depo klasörüne girin:
   ```bash
   cd engineering-tools
   ```
3. Launcher arayüzünü başlatın:
   ```bash
   python run_tools.py
   ```

---

## 🤝 Katkıda Bulunma

Depoya yeni mühendislik disiplinleri, algoritmaları veya arayüz özellikleri eklemek için:

1. Bu depoyu forklayın (`Fork`).
2. Çalışma dalınızı oluşturun (`git checkout -b feature/YeniMuhendislikAraci`).
3. Kodlarınızı ve `tests/test_engineering_tools.py` içerisine ilgili birim testlerini ekleyin.
4. Tüm testlerin başarıyla geçtiğini doğrulayın (`python run_tools.py --test`).
5. Commit atıp dalınızı pushlayın (`git push origin feature/YeniMuhendislikAraci`).
6. Bir Çekme İsteği (Pull Request) açın.

---

## 📚 Mühendislik Alıntıları ve Kaynakça

### 📖 Resmi Standartlar ve Akademik Referanslar

1.  **Havacılık ve Atmosfer:**
    *   *ICAO Doc 7488/3: Manual of the ICAO Standard Atmosphere (extended to 80 kilometres / 262 500 feet)*.
    *   Abbott, I. H., & Von Doenhoff, A. E. (1959). *Theory of Wing Sections: Including a Summary of Airfoil Data*. Dover Publications.
2.  **Robotik ve Mekatronik:**
    *   Craig, J. J. (2005). *Introduction to Robotics: Mechanics and Control*. Pearson Prentice Hall.
    *   Denavit, J., & Hartenberg, R. S. (1955). *A kinematic notation for lower-pair mechanisms based on matrices*.
3.  **Mühendislik Termodinamiği:**
    *   Moran, M. J., Shapiro, H. N., Boettner, D. D., & Bailey, M. B. (2018). *Fundamentals of Engineering Thermodynamics*. John Wiley & Sons.
4.  **Elektrik Dağıtım ve Kablo Standartları:**
    *   *IEC 60364-5-52: Low-voltage electrical installations - Selection and erection of electrical equipment - Wiring systems.*
5.  **Akışkanlar Mekaniği ve Hidrolik:**
    *   Darcy, H. (1857). *Recherches expérimentales relatives au mouvement de l'eau dans les tuyaux*.
    *   Haaland, S. E. (1983). *Simple and Explicit Formulas for the Friction Factor in Turbulent Pipe Flow*. Journal of Fluids Engineering, 105(1): 89-90.
6.  **Yapı Statiği ve Kiriş Mukavemeti:**
    *   Timoshenko, S. & Gere, J. M. (1972). *Mechanics of Materials*. Van Nostrand Reinhold Co.
7.  **Enerji Depolama ve Batarya Sistemleri:**
    *   IRENA (2020). *Electricity Storage Valuation Framework: Assessing system value and LCOS*.
8.  **Modbus Protokol Standartları:**
    *   *Modbus Application Protocol Specification V1.1b3*: [Modbus.org](https://modbus.org/)
9.  **CNC ve G-Kodu Standartları:**
    *   *NIST RS274NGC G-Code Standard (Version 3)*: National Institute of Standards and Technology.
10. **Kritik Yol Metodu (CPM & PERT):**
    *   *PMBOK Guide (A Guide to the Project Management Body of Knowledge)*, PMI.
11. **Toplam Verimli Bakım ve Kalite:**
    *   Nakajima, S. (1988). *Introduction to TPM: Total Productive Maintenance*. Productivity Press.
    *   Deming, W. E. (1986). *Out of the Crisis*. MIT Press.
12. **Sera Gazı Protokolü (GHG Protocol):**
    *   *Greenhouse Gas Protocol Corporate Accounting and Reporting Standard*: [GHGProtocol.org](https://ghgprotocol.org/)
13. **ISO Standartları:**
    *   *ISO 9001:2015 - Quality Management Systems*.
    *   *ISO 22000:2018 - Food Safety Management Systems*.
    *   *ISO 14001:2015 - Environmental Management Systems*.

---

## 📜 Lisans

Bu proje **MIT Lisansı** ile lisanslanmıştır. Detaylar için [LICENSE](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/LICENSE) dosyasına bakabilirsiniz.
