# ⚡ Algoritmik Karmaşıklık ve Başarım Kıyaslama (Algorithms & Benchmarking)

Bu modül, bilgisayar mühendisliği ve veri yapılarında temel algoritmaların (Sıralama, Arama) asimptotik zaman karmaşıklıklarını ($O(1), O(\log N), O(N), O(N \log N), O(N^2)$) ampirik olarak ölçer ve log-log regresyon analizi ile teyit eder.

---

## 📌 Asimptotik Karmaşıklık Teorisi (Big-O)

Algoritma çalışma süresinin ($T$) girdi boyutu ($N$) büyüdükçe nasıl ölçeklendiğini ifade eder:

$$T(N) \approx k \cdot N^\beta$$

Her iki tarafın doğal logaritması alındığında:

$$\ln(T) = \ln(k) + \beta \ln(N)$$

Burada eğim $\beta$, algoritmanın derecesini (üstel büyüme hızını) verir:
- $\beta \approx 1.0 \implies O(N)$ (Doğrusal)
- $\beta \approx 1.1 - 1.2 \implies O(N \log N)$ (Quicksort, Mergesort, Timsort)
- $\beta \approx 2.0 \implies O(N^2)$ (Bubble Sort, Insertion Sort, Selection Sort)

---

## 🚀 Çalıştırma

```bash
python software/algorithms/complexity_benchmarker.py
```
