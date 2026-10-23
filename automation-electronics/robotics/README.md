# 🤖 Robotik ve Manipülatör Kinematiği (Robotics & Mechatronics)

Bu modül, endüstriyel robotik kollar, SCARA robotlar ve kartezyen mekanizmalar için ileri kinematik (FK), analitik ters kinematik (IK) ve Jakobiyen matrisi hız/tekillik analizlerini gerçekleştirir.

---

## 📌 Teorik Formüller ve Robotik İlkeleri

### 1. İleri Kinematik (Forward Kinematics - FK)
2-Eklemli (2R) düzlemsel robot kolunda eklem açılarından $(\theta_1, \theta_2)$ uç nokta $(X, Y)$ konumunun hesaplanması:

$$X = L_1 \cos(\theta_1) + L_2 \cos(\theta_1 + \theta_2)$$
$$Y = L_1 \sin(\theta_1) + L_2 \sin(\theta_1 + \theta_2)$$
$$\phi = \theta_1 + \theta_2 \quad (\text{Toplam Yönelim Açısı})$$

---

### 2. Ters Kinematik (Inverse Kinematics - IK)
Uç noktanın hedeflenen koordinatına $(X, Y)$ ulaşabilmesi için gereken eklem açılarının çözümü:

1.  **Mesafe ve Çalışma Alanı Denetimi:**
    $$D^2 = X^2 + Y^2$$
    - $|L_1 - L_2| \le D \le (L_1 + L_2)$ kuralı sağlanmalıdır.
2.  **$\theta_2$ Açısının Hesabı:**
    $$\cos(\theta_2) = \frac{X^2 + Y^2 - L_1^2 - L_2^2}{2 L_1 L_2}$$
    - **Dirsek Aşağı (Elbow Down):** $\theta_2 = +\arccos(\cos\theta_2)$
    - **Dirsek Yukarı (Elbow Up):** $\theta_2 = -\arccos(\cos\theta_2)$
3.  **$\theta_1$ Açısının Hesabı:**
    $$\theta_1 = \text{atan2}(Y, X) - \text{atan2}(L_2 \sin\theta_2, L_1 + L_2 \cos\theta_2)$$

---

### 3. Jakobiyen Matrisi ($J$) ve Kinematik Tekillik
Eklem açısal hızları ($\dot{\theta}$) ile kartezyen uç nokta hızları ($\dot{X}, \dot{Y}$) arasındaki doğrusal ilişkiyi kurar:

$$\begin{bmatrix} \dot{X} \\ \dot{Y} \end{bmatrix} = J \begin{bmatrix} \dot{\theta}_1 \\ \dot{\theta}_2 \end{bmatrix}$$

$$J = \begin{bmatrix} -L_1 \sin\theta_1 - L_2 \sin(\theta_1+\theta_2) & -L_2 \sin(\theta_1+\theta_2) \\ L_1 \cos\theta_1 + L_2 \cos(\theta_1+\theta_2) & L_2 \cos(\theta_1+\theta_2) \end{bmatrix}$$

$$\det(J) = L_1 L_2 \sin(\theta_2)$$

> [!WARNING]
> **Kinematik Tekillik (Singularity):** $\theta_2 = 0^\circ$ (kol tamamen açıldığında) veya $\theta_2 = 180^\circ$ (kol kendi üzerine katlandığında) $\det(J) = 0$ olur. Robot kolu o doğrultuda hareket kabiliyetini yitirir ve ters kinematik hız matrisi sonsuza gider.

---

## 🚀 Çalıştırma

```bash
python automation-electronics/robotics/kinematics_calculator.py
```
