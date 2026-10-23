import time
import math
import random
import os

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def bubble_sort(arr):
    a = list(arr)
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a

def insertion_sort(arr):
    a = list(arr)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def binary_search(sorted_arr, target):
    low = 0
    high = len(sorted_arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_arr[mid] == target:
            return mid
        elif sorted_arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def linear_search(arr, target):
    for idx, val in enumerate(arr):
        if val == target:
            return idx
    return -1

def estimate_big_o_exponent(n_sizes, times_sec):
    """
    Log-Log doğrusal regresyonu (ln(T) = beta * ln(N) + alpha) ile
    ampirik Big-O zaman karmaşıklığı üssü beta'yı tahmin eder.
    """
    if len(n_sizes) < 2 or len(times_sec) < 2:
        return 1.0
        
    ln_n = [math.log(n) for n in n_sizes]
    ln_t = [math.log(max(t, 1e-9)) for t in times_sec]
    
    n_pts = len(ln_n)
    sum_x = sum(ln_n)
    sum_y = sum(ln_t)
    sum_xx = sum(x**2 for x in ln_n)
    sum_xy = sum(x*y for x, y in zip(ln_n, ln_t))
    
    denom = (n_pts * sum_xx - (sum_x ** 2))
    if denom == 0:
        return 1.0
        
    beta = (n_pts * sum_xy - sum_x * sum_y) / denom
    return beta

def benchmark_sorting_algorithms(sizes=[500, 1000, 2000, 4000]):
    """
    Bubble Sort, Insertion Sort ve Dahili Timsort için ampirik kıyaslama yapar.
    """
    results = {
        "sizes": sizes,
        "bubble": [],
        "insertion": [],
        "timsort": []
    }
    
    for n in sizes:
        sample_data = [random.randint(1, 100000) for _ in range(n)]
        
        # 1. Bubble Sort
        t0 = time.perf_counter()
        bubble_sort(sample_data)
        t_bubble = time.perf_counter() - t0
        results["bubble"].append(t_bubble)
        
        # 2. Insertion Sort
        t0 = time.perf_counter()
        insertion_sort(sample_data)
        t_ins = time.perf_counter() - t0
        results["insertion"].append(t_ins)
        
        # 3. Built-in Timsort (O(N log N))
        t0 = time.perf_counter()
        sorted(sample_data)
        t_tim = time.perf_counter() - t0
        results["timsort"].append(t_tim)
        
    results["beta_bubble"] = estimate_big_o_exponent(sizes, results["bubble"])
    results["beta_insertion"] = estimate_big_o_exponent(sizes, results["insertion"])
    results["beta_timsort"] = estimate_big_o_exponent(sizes, results["timsort"])
    
    return results

def interactive_benchmark():
    clear_screen()
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print(f"{Colors.BOLD}   ALGORİTMİK KARMAŞIKLIK & BENCHMARK ANALİZİ     {Colors.ENDC}")
    print(f"{Colors.HEADER}=================================================={Colors.ENDC}")
    print("Farklı N boyutlarında sıralama algoritmalarının mikro-benchmark ölçümü.")
    print("Log-Log regresyonu ile Big-O ampirik üs tahmini yapılır.")
    print("-" * 50)
    print("Test boyutu seçin:")
    print("1. Hızlı Kıyaslama (N = 500, 1000, 1500, 2000)")
    print("2. Kapsamlı Kıyaslama (N = 1000, 2000, 3000, 5000)")
    sel = input("Seçiminiz [Varsayılan: 1]: ").strip()
    
    sizes = [500, 1000, 1500, 2000] if sel != '2' else [1000, 2000, 3000, 5000]
    print(f"\n{Colors.WARNING}[BİLGİ] Benchmark çalıştırılıyor, lütfen bekleyin...{Colors.ENDC}")
    res = benchmark_sorting_algorithms(sizes)
    
    print(f"\n{Colors.OKGREEN}>>> ÖLÇÜM SONUÇLARI (Süre: saniye) <<<{Colors.ENDC}")
    print(f"{'N Boyutu':<10} | {'Bubble Sort O(N²)':<20} | {'Insertion Sort O(N²)':<22} | {'Timsort O(N log N)'}")
    print("-" * 75)
    for i, n in enumerate(sizes):
        tb = res["bubble"][i]
        ti = res["insertion"][i]
        tt = res["timsort"][i]
        print(f"{n:<10} | {tb:18.6f} s | {ti:20.6f} s | {tt:16.6f} s")
    print("-" * 75)
    
    print(f"\n{Colors.BOLD}Ampirik Big-O Analizi (T ∝ N^β):{Colors.ENDC}")
    print(f"  Bubble Sort Tahmini Üs    : β = {res['beta_bubble']:.2f}  (Beklenen: ~2.00  O(N²))")
    print(f"  Insertion Sort Tahmini Üs : β = {res['beta_insertion']:.2f}  (Beklenen: ~2.00  O(N²))")
    print(f"  Timsort Tahmini Üs        : β = {res['beta_timsort']:.2f}  (Beklenen: ~1.10  O(N log N))")
    input(f"\n{Colors.WARNING}Devam etmek için Enter'a basın...{Colors.ENDC}")

def main():
    if os.name == 'nt':
        os.system('color')
    interactive_benchmark()

if __name__ == "__main__":
    main()
