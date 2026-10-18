# 🛠️ Engineering Tools (Mühendislik Araçları ve Standartları)

![Engineering Tools Banner](assets/banner.jpg)

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Tests: 25 Passed](https://img.shields.io/badge/Tests-25%20Passed-brightgreen.svg)
![Maintained: Yes](https://img.shields.io/badge/Maintained-Yes-green.svg)
![Contributions: Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)
![Dependencies: None (Standard Library Only)](https://img.shields.io/badge/Dependencies-Standard%20Library%20Only-orange.svg)

Bu depo, modern mühendislik disiplinlerinde kullanılan temel algoritmalar, matematiksel modellemeler, otomasyon altyapıları, kalite standartları, kimyasal prosesler, yenilenebilir enerji ve sürdürülebilirlik konularının kapsamlı bir referans rehberi ve **interaktif konsol araçları** koleksiyonudur. Çok disiplinli projeler geliştiren mühendisler, araştırmacılar ve teknik ekipler için bir bilgi bankası ve pratik araç kütüphanesi niteliği taşır.

---

## 📌 İçindekiler
1. [Hakkında](#-hakkında)
2. [Hızlı Başlangıç (Launcher Arayüzü)](#-hızlı-başlangıç-launcher-arayüzü)
3. [Mühendislik Branşları ve Araç Kataloğu](#-mühendislik-branşları-ve-araç-kataloğu)
    - [1. Yazılım ve Bilgisayar Mühendisliği](#1-yazılım-ve-bilgisayar-mühendisliği)
    - [2. Elektrik-Elektronik ve Otomasyon Mühendisliği](#2-elektrik-elektronik-ve-otomasyon-mühendisliği)
    - [3. Makine ve İnşaat Mühendisliği (Yapı Statiği & CAD/CAM)](#3-makine-ve-inşaat-mühendisliği-yapı-statiği--cadcam)
    - [4. Kimya ve Süreç Mühendisliği (Proses Hidroliği & Isı Transferi)](#4-kimya-ve-süreç-mühendisliği-proses-hidroliği--ısı-transferi)
    - [5. Endüstri Mühendisliği (Yalın & Altı Sigma)](#5-endüstri-mühendisliği-yalın--altı-sigma)
    - [6. Kalite Standartları ve Güvenlik (ISO & HACCP)](#6-kalite-standartları-ve-güvenlik-iso--haccp)
    - [7. Çevre ve Sürdürülebilirlik (ESG & Karbon Ayak İzi)](#7-çevre-ve-sürdürülebilirlik-esg--karbon-ayak-izi)
    - [8. Enerji Sistemleri Mühendisliği (Güneş, Rüzgar, BESS)](#8-enerji-sistemleri-mühendisliği-güneş-rüzgar-bess)
4. [Proje Klasör Yapısı](#-proje-klasör-yapısı)
5. [Otomatik Testler (Unit Tests & CI/CD)](#-otomatik-testler-unit-tests--cicd)
6. [Kurulum ve Çalıştırma](#-kurulum-ve-çalıştırma)
7. [Katkıda Bulunma (Contributing)](#-katkıda-bulunma)
8. [Mühendislik Alıntıları ve Kaynakça](#-mühendislik-alıntıları-ve-kaynakça)
9. [Lisans](#-lisans)

---

## 📖 Hakkında
Modern mühendislik projeleri artık tek bir disiplinin sınırları içinde kalmamakta, yazılım, otomasyon, mekanik, kimyasal süreçler, kalite ve çevre süreçlerinin entegrasyonuyla şekillenmektedir. Bu deponun temel özellikleri:

*   **Sıfır Dış Bağımlılık (Zero Dependencies):** Projedeki tüm araçlar ve test paketi, üçüncü parti kütüphanelere (NumPy, Pandas vb.) ihtiyaç duymaksızın **saf Python standart kütüphanesi** (`math`, `sqlite3`, `unittest`, `subprocess` vb.) kullanılarak geliştirilmiştir.
*   **Analitik Doğruluk:** Endüstriyel IEC, DIN, ISO, NIST ve PMBOK standartlarına uygun formüller ve algoritmalar temel alınmıştır.
*   **Çift Kullanım Modeli:** Hem interaktif renkli CLI terminalleri üzerinden adım adım hesaplama yapabilir hem de Python scriptlerinizde import ederek fonksiyonları doğrudan çağırabilirsiniz.

---

## 🚀 Hızlı Başlangıç (Launcher Arayüzü)

Merkezi CLI yönlendiriciyi çalıştırarak tüm araçlara interaktif konsoldan erişebilirsiniz:

```bash
# İnteraktif Menü
python run_tools.py

# Tüm araçları listele
python run_tools.py --list

# Otomatik birim test paketini çalıştır
python run_tools.py --test
```

Menü Görünümü:
```text
==================================================
     🛠️  MÜHENDİSLİK ARAÇLARI KONSOL ARAYÜZÜ      
==================================================
1. Yazılım ve Bilgisayar Mühendisliği
2. Elektrik-Elektronik ve Otomasyon Mühendisliği
3. Makine ve İnşaat Mühendisliği
4. Kimya ve Süreç Mühendisliği (Proses & Hidrolik)
5. Endüstri Mühendisliği (Yalın & Altı Sigma)
6. Kalite Standartları ve Güvenlik (ISO & HACCP)
7. Çevre ve Sürdürülebilirlik (ESG)
8. Enerji Sistemleri Mühendisliği (Güneş, Rüzgar, BESS)
9. 🧪 Otomatik Mühendislik Testlerini Çalıştır (Unit Tests)
0. Çıkış
==================================================
```

---

## ⚙️ Mühendislik Branşları ve Araç Kataloğu

### 1. Yazılım ve Bilgisayar Mühendisliği
> 💬 *"First, solve the problem. Then, write the code."* — John Johnson  
> 💬 *"Talk is cheap. Show me the code."* — Linus Torvalds

*   **Veri Analizi ve Polinom Regresyon:** Saf Python ile betimsel istatistik (ortalama, medyan, varyans, standart sapma), 1. derece doğrusal ve 2. derece kuadratik regresyon eğri uydurma.
*   **Birim Dönüştürücü:** Sıcaklık (°C, °F), Basınç (Bar, PSI, Pascal), Uzunluk (inç, mm) ve Hız (m/s, km/h, mph) dönüşümleri.
*   **Malzeme Veri Tabanı Yöneticisi:** SQLite tabanlı, metaller, polimerler ve kompozitlerin yoğunluk, akma mukavemeti, elastisite modülü ve Ashby özgül performans endekslerini ($\sigma_y/\rho$, $E/\rho$) yöneten CRUD aracı.
*   **Bulut TCO & Altyapı Maliyet Hesaplayıcı:** AWS, Azure ve GCP için vCPU, RAM, SSD ve veri transferi (egress) gereksinimlerine göre On-Demand ile 1 ve 3 yıllık Rezerv Plan (Savings Plan) tasarruf ve veri merkezi karbon ayak izi analizi.
*   *Dizin:* [software/](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/software/)

---

### 2. Elektrik-Elektronik ve Otomasyon Mühendisliği
> 💬 *"Automation is good, so long as you know exactly where to put the machine."* — Eliyahu M. Goldratt

*   **PLC Register ve PID Simülatörü:** IEC 61131-3 standartlarında Coils, Discrete Inputs, Input Registers ve Holding Registers yapısını, çevrimsel tarama (Scan Cycle), acil stop mantığı ve sıcaklık kontrolü için oransal valf PID algoritmasını simüle eder.
*   **Kablo Kesiti & Gerilim Düşümü (IEC 60364-5-52):** 1 Faz (230V AC / DC) ve 3 Faz (400V AC) sistemlerde bakır ve alüminyum iletkenler için akım, mesafe ve $\cos\varphi$'ye bağlı voltaj düşümü, güç kaybı ve aydınlatma (%3) / motor (%5) standart limit kontrolü.
*   **Filtre & RLC Rezonans Analizi:** RC, RL alçak/yüksek geçiren filtrelerin kesim frekansı ($f_c$), seri RLC rezonans frekansı ($f_0$), kalite faktörü ($Q$) ve bant genişliği ($BW$).
*   **Reaktif Güç Kompanzasyonu:** İstenen hedef $\cos\varphi$ değerine ulaşmak için gereken kondansatör gücünü ($Q_c\ \text{kVAR}$) ve şebeke yük tasarrufunu belirler.
*   *Dizin:* [automation-electronics/](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/automation-electronics/)

---

### 3. Makine ve İnşaat Mühendisliği (Yapı Statiği & CAD/CAM)
> 💬 *"Scientists study the world as it is; engineers create the world that has never been."* — Theodore von Kármán  
> 💬 *"Design is not just what it looks like and feels like. Design is how it works."* — Steve Jobs

*   **Kiriş Eğilme Momenti ve Sehim Analizi (Euler-Bernoulli):** Dikdörtgen, dolu daire, boru ve kutu profillerde atalet momenti ($I_x$) ve mukavemet momenti ($W_x$) hesabı. 4 temel yükleme durumunda (tekil ve yayılı yük altında basit mesnetli ve ankastre kirişler) maksimum eğilme momenti, eğilme gerilmesi ($\sigma_{max}$), emniyet katsayısı ($SF$) ve sehim limit ($\delta \le L/300$) kontrolü.
*   **CNC G-Kodu Jeneratörü:** Dikdörtgen ve dairesel profiller için kesim derinliği, ilerleme hızı, spindle devri ve takım çapına göre hazır G-kodu (G21, G90, G01, G02 vb.) üretir.
*   **Kritik Yol Metodu (CPM) ve PERT Proje Planlayıcı:** Görev süreleri ve bağımlılıklarını topolojik sıralama ile işleyerek Erken/Geç Başlangıç ve Bitiş zamanlarını, serbest/toplam bollukları (slack) ve kritik yolu hesaplar; %68 ve %95 güvenilirlik aralıklarında proje bitiş tarihlerini çıkarır.
*   *Dizin:* [mechanical-civil/](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/mechanical-civil/)

---

### 4. Kimya ve Süreç Mühendisliği (Proses Hidroliği & Isı Transferi)
> 💬 *"Thermodynamics is the only physical theory of universal content."* — Albert Einstein

*   **Boru Akışı Basınç Düşüşü & Reynolds Sayısı:** Darcy-Weisbach formülü ve Haaland türbülans sürtünme denklemiyle ticari çelik, paslanmaz çelik, plastik veya döküm borularda akış hızını, laminer/türbülanslı rejimi ve bar/mSS cinsinden basınç kaybını hesaplar.
*   **Isı Eşanjörü LMTD ve Transfer Alanı:** Karşıt akış (counter-flow) ve paralel akış (parallel-flow) eşanjörlerde Logaritmik Ortalama Sıcaklık Farkını ($\Delta T_{lm}$) ve aktarılacak ısı yüküne ($Q$) göre gereken minimum eşanjör yüzey alanını ($A$) boyutlandırır.
*   **Çözelti Karışımı ve Seyreltme Dengesi:** Kimyasal reaktör ve tanklarda kütle denkliği ($C_1 V_1 + C_2 V_2 = C_f V_f$) formülüyle saf çözücü ekleme veya farklı derişimlerdeki kimyasalları harmanlama hesaplayıcısı.
*   *Dizin:* [chemical-process/](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/chemical-process/)

---

### 5. Endüstri Mühendisliği (Yalın & Altı Sigma)
> 💬 *"Without data, you're just another person with an opinion."* — W. Edwards Deming  
> 💬 *"If you can't describe what you are doing as a process, you don't know what you are doing."* — W. Edwards Deming

*   **OEE (Toplam Ekipman Etkinliği):** Kullanılabilirlik (Availability), Performans (Performance) ve Kalite (Quality) oranlarını çarparak TPM standartlarında verimlilik analizi yapar.
*   **Altı Sigma Analizi:** Hatalı ürün ve hata fırsatına göre DPO, DPMO ve 1.5 Sigma kaydırılmış süreç Sigma Seviyesini Probit ters normal dağılım fonksiyonuyla belirler.
*   **Takt Zamanı ve Hat Dengeleme:** Müşteri talebi ve net çalışma süresine göre üretim hattı çevrim süresi gereksinimlerini optimize eder.
*   *Dizin:* [industrial-engineering/](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/industrial-engineering/)

---

### 6. Kalite Standartları ve Güvenlik (ISO & HACCP)
> 💬 *"Quality is not an act, it is a habit."* — Aristotle  
> 💬 *"Do it right the first time."* — Philip Crosby

*   **ISO Denetim Asistanı:** ISO 9001 (KYS), ISO 22000 (HACCP Gıda Güvenliği) ve ISO 14001 (ÇYS) maddelerine göre iç tetkik gerçekleştiren, bulguları notlayan, puanlayan ve denetim raporu çıktısı veren sistem.
*   *Dizin:* [quality-standards/](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/quality-standards/)

---

### 7. Çevre ve Sürdürülebilirlik (ESG & Karbon Ayak İzi)
> 💬 *"We do not inherit the Earth from our ancestors; we borrow it from our children."* — Native American Proverb

*   **Sera Gazı Protokolü (GHG Protocol) Hesaplayıcı:** Kapsam 1 (Doğal gaz, şirket dizel/benzin araçları), Kapsam 2 (Satın alınan şebeke elektriği) ve Kapsam 3 (Uçuş seyahatleri, personel ulaşımı) emisyonlarını $tCO_2e$ cinsinden hesaplar ve ESG raporlama formatında sunar.
*   *Dizin:* [environment/](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/environment/)

---

### 8. Enerji Sistemleri Mühendisliği (Güneş, Rüzgar, BESS)
> 💬 *"I'd put my money on the sun and solar energy. What a source of power!"* — Thomas Edison

*   **Güneş (PV) & Rüzgar Güç Hesaplayıcı:** Panel alanı, ışınım ($G$), verimlilik ve sistem kayıp oranıyla fotovoltaik elektrik üretimini; süpürme alanı, hava yoğunluğu, rüzgar hızı ve **Betz Limiti ($C_p \le 0.593$)** kısıtlamasıyla rüzgar türbini gücünü hesaplar.
*   **Bataryalı Enerji Depolama (BESS) & LCOS Boyutlandırma:** Günlük kWh tüketimi, otonomi gün sayısı, LiFePO4, NMC veya AGM akü kimyalarının Deşarj Derinliği (DoD) ve sistem verimlerine göre batarya kapasitesi (kWh ve Ah), invertör seçimi ve seviyelendirilmiş depolama maliyeti ($/kWh LCOS) hesabı.
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
│   └── test_engineering_tools.py          # Saf Python 25+ Otomatik Birim Test Suite'i
│
├── software/
│   ├── python/                             # İstatistik, Regresyon ve Birim Dönüştürücü
│   ├── databases/                          # SQLite Mühendislik Malzeme DB Yöneticisi
│   └── cloud/                              # Bulut TCO & Kapasite Hesaplayıcı, DevOps Rehberi
│
├── automation-electronics/
│   ├── plc-scada/                          # PLC Modbus & PID Regülasyon Simülatörü
│   └── circuit-design/                     # Kablo Kesiti, Gerilim Düşümü (IEC) & Filtre Analizi
│
├── mechanical-civil/
│   ├── cad-cam/                            # CNC G-Kodu Üreteci (CAD/CAM)
│   ├── project-management/                 # CPM (Kritik Yol) & PERT Proje Planlayıcı
│   └── structural-mechanics/               # Kiriş Atalet Momenti, Mukavemet & Sehim Analizi
│
├── chemical-process/
│   └── process-engineering/                # Darcy-Weisbach Boru Basınç Kaybı, LMTD Eşanjör, Seyreltme
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

Depo, 25 adet kapsamlı birim testi içeren otomatik bir test paketine sahiptir. Dış paket yüklemesi yapmadan doğrudan çalıştırılabilir:

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
   git clone https://github.com/arch-yunus/engineering-tools.git
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

1.  **Elektrik Dağıtım ve Kablo Standartları:**
    *   *IEC 60364-5-52: Low-voltage electrical installations - Selection and erection of electrical equipment - Wiring systems.*
2.  **Akışkanlar Mekaniği ve Hidrolik:**
    *   Darcy, H. (1857). *Recherches expérimentales relatives au mouvement de l'eau dans les tuyaux*.
    *   Haaland, S. E. (1983). *Simple and Explicit Formulas for the Friction Factor in Turbulent Pipe Flow*. Journal of Fluids Engineering, 105(1): 89-90.
3.  **Yapı Statiği ve Kiriş Mukavemeti:**
    *   Timoshenko, S. & Gere, J. M. (1972). *Mechanics of Materials*. Van Nostrand Reinhold Co.
    *   Euler-Bernoulli Beam Theory (Classical Beam Theory).
4.  **Enerji Depolama ve Batarya Sistemleri:**
    *   IRENA (2020). *Electricity Storage Valuation Framework: Assessing system value and LCOS*.
5.  **Modbus Protokol Standartları:**
    *   *Modbus Application Protocol Specification V1.1b3*: [Modbus.org](https://modbus.org/)
6.  **CNC ve G-Kodu Standartları:**
    *   *NIST RS274NGC G-Code Standard (Version 3)*: National Institute of Standards and Technology.
7.  **Kritik Yol Metodu (CPM & PERT):**
    *   *PMBOK Guide (A Guide to the Project Management Body of Knowledge)*, PMI.
8.  **Toplam Verimli Bakım ve Kalite:**
    *   Nakajima, S. (1988). *Introduction to TPM: Total Productive Maintenance*. Productivity Press.
    *   Deming, W. E. (1986). *Out of the Crisis*. MIT Press.
9.  **Sera Gazı Protokolü (GHG Protocol):**
    *   *Greenhouse Gas Protocol Corporate Accounting and Reporting Standard*: [GHGProtocol.org](https://ghgprotocol.org/)
10. **ISO Standartları:**
    *   *ISO 9001:2015 - Quality Management Systems*.
    *   *ISO 22000:2018 - Food Safety Management Systems*.
    *   *ISO 14001:2015 - Environmental Management Systems*.

---

## 📜 Lisans

Bu proje **MIT Lisansı** ile lisanslanmıştır. Detaylar için [LICENSE](file:///g:/Diğer bilgisayarlar/Dizüstü Bilgisayarım/github repolarım/engineering-tools/LICENSE) dosyasına bakabilirsiniz.