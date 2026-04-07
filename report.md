# BÁO CÁO TIỂU LUẬN NHÓM - ĐỀ TÀI 05

## Ứng Dụng Các Phương Pháp Giải Phương Trình Phi Tuyến trong Phân Tích Dữ Liệu Tài Chính: Bài Toán Xác Định Lãi Suất Hoàn Vốn Nội Bộ (IRR)

---

## 1. MỤC TIÊU CỦA ĐỀ TÀI

### Mục tiêu chung:
- Áp dụng kiến thức về nghiệm và khoảng phân ly nghiệm vào bài toán kinh tế thực tế.
- Hiểu vận dụng thành thạo 4 phương pháp giải gần đúng phương trình phi tuyến: Chia đôi, Dây cung, Tiếp tuyến (Newton-Raphson) và Lặp điểm cố định.
- Rèn luyện kỹ năng mô tả thuật toán và lập trình giải quyết bài toán bằng ngôn ngữ Python.
- Trực quan hóa dữ liệu và xây dựng sản phẩm demo đánh giá dự án đầu tư.

---

## 2. BỐI CẢNH ĐỀ TÀI VÀ DỮ LIỆU ĐẦU VÀO

### 2.1 Giới thiệu Bài Toán

Lãi suất hoàn vốn nội bộ (Internal Rate of Return - IRR) là mức lãi suất làm cho **Giá Trị Hiện Tại Ròng (Net Present Value - NPV)** của tất cả các dòng tiền từ một dự án bằng 0.

Việc tìm IRR chính là bài toán tìm nghiệm của một phương trình đa thức bậc cao:

$$f(r) = C_0 + \sum_{i=1}^{n} \frac{C_i}{(1+r)^i} = 0$$

Trong đó:
- $C_i$ là dòng tiền (cash flow) tại năm thứ $i$
- $r$ là lãi suất cần tìm (IRR)
- $n$ là số năm của dự án

### 2.2 Dữ Liệu Mẫu

| Năm | Dòng tiền (Ci) | Ghi chú |
|-----|----------------|--------|
| 0   | -2,000 (triệu VNĐ) | Chi phí đầu tư ban đầu |
| 1   | 400 (triệu VNĐ) | Khai thác năm đầu |
| 2   | 600 (triệu VNĐ) | Dòng tiền từ hoạt động kinh doanh |
| 3   | 800 (triệu VNĐ) | Dòng tiền từ hoạt động kinh doanh |
| 4   | 800 (triệu VNĐ) | Dòng tiền từ hoạt động kinh doanh |
| 5   | 1,200 (triệu VNĐ) | Thu nhập năm cuối + thanh lý tài sản |

### 2.3 Phương Trình Toán Học

$$f(r) = -2000 + \frac{400}{1+r} + \frac{600}{(1+r)^2} + \frac{800}{(1+r)^3} + \frac{800}{(1+r)^4} + \frac{1200}{(1+r)^5} = 0$$

**Tiêu chuẩn dừng:** Sai số mục tiêu $\varepsilon = 10^{-5}$

**Khoảng tìm kiếm:** $r \in [0, 1]$ (từ 0% đến 100%)

---

## 3. NỘI DUNG THỰC HIỆN

### 3.1 Phần 1: Cơ Sở Lý Thuyết

#### 3.1.1 Hàm NPV và Đạo Hàm

**Đạo hàm bậc 1 (dùng cho phương pháp Newton-Raphson):**

$$f'(r) = \sum_{i=1}^{n} \frac{-i \cdot C_i}{(1+r)^{i+1}}$$

**Đạo hàm bậc 2 (dùng cho phương pháp Lặp điểm cố định):**

$$f''(r) = \sum_{i=1}^{n} \frac{i(i+1) \cdot C_i}{(1+r)^{i+2}}$$

#### 3.1.2 Khoảng Phân Ly Nghiệm

**Định lý Bolzano:** Nếu $f$ liên tục trên $[a,b]$ và $f(a) \cdot f(b) < 0$ thì tồn tại ít nhất một nghiệm trong khoảng đó.

**Lựa chọn khoảng [0, 1]:**
- Lãi suất IRR trong thực tế thường nằm trong khoảng từ 0% (0%) đến 100% (1.0).
- Việc chọn khoảng rộng này đảm bảo ta sẽ bắt được nghiệm nếu nó tồn tại.
- Có thể kiểm chứng: $f(0) \cdot f(1) < 0$ để xác nhận tồn tại nghiệm.

#### 3.1.3 Hàm Lặp cho Phương Pháp Lặp Điểm Cố Định

Hàm lặp được sử dụng:

$$g(r) = r - \frac{f(r)}{f'(r)}$$

**Điều kiện hội tụ:** $|g'(r)| < 1$

Trong đó: $g'(r) = \frac{f(r) \cdot f''(r)}{[f'(r)]^2}$

---

### 3.2 Phần 2: Triển Khai 4 Phương Pháp

#### 3.2.1 Phương Pháp Chia Đôi (Bisection)

**Ý tưởng:** Lặp đi lặp lại chia khoảng làm đôi dựa trên định lý giá trị trung gian.

**Công thức lặp:**
$$c = \frac{a + b}{2}$$

**Điều kiện dừng:** $|f(c)| < \varepsilon$ hoặc số lần lặp vượt quá 1000.

**Ưu điểm:**
- Luôn hội tụ nếu $f(a) \cdot f(b) < 0$
- Ổn định, không yêu cầu đạo hàm
- Tốc độ hội tụ tuyến tính

**Nhược điểm:**
- Tốc độ hội tụ chậm so với Newton-Raphson
- Cần khoảng phân ly tốt

---

#### 3.2.2 Phương Pháp Dây Cung (Secant)

**Ý tưởng:** Thay thế đạo hàm bằng độ dốc của dây cung nối hai điểm gần nhất.

**Công thức lặp:**
$$x_{n+1} = x_n - \frac{f(x_n)(x_n - x_{n-1})}{f(x_n) - f(x_{n-1})}$$

**Ưu điểm:**
- Không cần tính đạo hàm
- Tốc độ hội tụ nhanh hơn Chia đôi (bậc ~1.618)
- Chỉ cần một đánh giá hàm mới mỗi bước

**Nhược điểm:**
- Có thể phân kỳ với khởi tạo xấu
- Cần hai giá trị khởi tạo

---

#### 3.2.3 Phương Pháp Newton-Raphson (Tiếp Tuyến)

**Ý tưởng:** Sử dụng tiếp tuyến tại điểm $x_n$ để tìm xấp xỉ tiếp theo.

**Công thức lặp:**
$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

**Ưu điểm:**
- Tốc độ hội tụ bậc hai (nhanh nhất)
- Rất hiệu quả khi có đạo hàm
- Ít lần lặp để hội tụ

**Nhược điểm:**
- Yêu cầu tính đạo hàm
- Có thể phân kỳ nếu $f'(x) \approx 0$
- Nhạy cảm với giá trị khởi tạo

---

#### 3.2.4 Phương Pháp Lặp Điểm Cố Định (Fixed-point Iteration)

**Ý tưởng:** Biến đổi $f(r) = 0$ thành $r = g(r)$ và lặp.

**Công thức lặp:**
$$r_{n+1} = g(r_n) = r_n - \frac{f(r_n)}{f'(r_n)}$$

**Điều kiện hội tụ (kiểm tra trước khi lặp):**
$$|g'(r)| < 1$$

**Ưu điểm:**
- Tương tự Newton-Raphson khi sử dụng $g(r) = r - \frac{f(r)}{f'(r)}$
- Flexible trong lựa chọn hàm lặp

**Nhược điểm:**
- Yêu cầu kiểm tra điều kiện hội tụ
- Có thể phân kỳ nếu điều kiện không thỏa mãn

---

### 3.3 Phần 3: Sơ Đồ Khối (Flowchart)

#### 3.3.1 Sơ Đồ Phương Pháp Chia Đôi

```
START
  |
  v
INPUT: a, b, ε, max_iter
  |
  v
CHECK: f(a) * f(b) < 0 ? --> NO --> ERROR
  |
 YES
  |
  v
iteration = 0
  |
  v
<-- LOOP START
|
v
c = (a + b) / 2
  |
  v
f_c = f(c)
  |
  v
iteration++
  |
  v
OUTPUT: (iteration, c, f_c, |f_c|)
  |
  v
|f_c| < ε ? --> YES --> return c, iteration, time
  |
 NO
  |
  v
iteration > max_iter ? --> YES --> return c, max_iter, time
  |
 NO
  |
  v
f(a) * f_c < 0 ? --> YES --> b = c
  |              |
 NO              v
  |            LOOP CONTINUE
  |
  v
a = c
  |
  v
  LOOP CONTINUE -->
```

#### 3.3.2 Sơ Đồ Phương Pháp Dây Cung

```
START
  |
  v
INPUT: x0, x1, ε, max_iter
  |
  v
iteration = 0
  |
  v
<-- LOOP START
|
v
f0 = f(x0), f1 = f(x1)
  |
  v
|f1 - f0| < 1e-10 ? --> YES --> return x1, iteration, time
  |
 NO
  |
  v
x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
  |
  v
f2 = f(x2)
  |
  v
iteration++
  |
  v
OUTPUT: (iteration, x2, f2, |f2|)
  |
  v
|f2| < ε ? --> YES --> return x2, iteration, time
  |
 NO
  |
  v
iteration > max_iter ? --> YES --> return x2, max_iter, time
  |
 NO
  |
  v
x0 = x1, x1 = x2
  |
  v
  LOOP CONTINUE -->
```

#### 3.3.3 Sơ Đồ Phương Pháp Newton-Raphson

```
START
  |
  v
INPUT: x0, ε, max_iter
  |
  v
iteration = 0
  |
  v
<-- LOOP START
|
v
f = f(x0), f' = f'(x0)
  |
  v
|f'| < 1e-10 ? --> YES --> ERROR: f'(x) = 0
  |
 NO
  |
  v
x1 = x0 - f / f'
  |
  v
f1 = f(x1)
  |
  v
iteration++
  |
  v
OUTPUT: (iteration, x1, f1, |f1|)
  |
  v
|f1| < ε ? --> YES --> return x1, iteration, time
  |
 NO
  |
  v
iteration > max_iter ? --> YES --> return x1, max_iter, time
  |
 NO
  |
  v
x0 = x1
  |
  v
  LOOP CONTINUE -->
```

#### 3.3.4 Sơ Đồ Phương Pháp Lặp Điểm Cố Định

```
START
  |
  v
INPUT: x0, ε, max_iter
  |
  v
f = f(x0), f' = f'(x0), f'' = f''(x0)
  |
  v
COMPUTE: g'(x0) = f(x0) * f''(x0) / [f'(x0)]^2
  |
  v
|g'(x0)| < 1 ? --> NO --> WARNING: Có thể không hội tụ
  |
 YES
  |
  v
iteration = 0
  |
  v
<-- LOOP START
|
v
f = f(x0), f' = f'(x0)
  |
  v
|f'| < 1e-10 ? --> YES --> ERROR: f'(x) = 0
  |
 NO
  |
  v
x1 = x0 - f / f'    [g(r) = r - f/f']
  |
  v
f1 = f(x1)
  |
  v
iteration++
  |
  v
OUTPUT: (iteration, x1, f1, |f1|)
  |
  v
|f1| < ε ? --> YES --> return x1, iteration, time
  |
 NO
  |
  v
iteration > max_iter ? --> YES --> return x1, max_iter, time
  |
 NO
  |
  v
x0 = x1
  |
  v
  LOOP CONTINUE -->
```

---

### 3.4 Phần 4: Kết Quả So Sánh

| Phương pháp | IRR (r*) | Số lần lặp | Thời gian (ms) | Độ ổn định | Tốc độ hội tụ |
|------------|----------|-----------|----------------|-----------|--------------|
| Chia đôi | [Kết quả] | [Kết quả] | [Kết quả] | Cao | Tuyến tính |
| Dây cung | [Kết quả] | [Kết quả] | [Kết quả] | Trung bình | ~1.618 |
| Newton-Raphson | [Kết quả] | [Kết quả] | [Kết quả] | Thấp | Bậc hai |
| Lặp điểm cố định | [Kết quả] | [Kết quả] | [Kết quả] | Trung bình | Tuyến tính |

**Ghi chú:** Chạy ứng dụng Streamlit để xem kết quả thực tế với dữ liệu mẫu.

---

## 4. PHÂN CÔNG CÔNG VIỆC

| STT | Nhiệm vụ | Người phụ trách | Tiến độ | Ghi chú |
|-----|----------|----------------|--------|---------|
| 1 | Nghiên cứu lý thuyết phương pháp Chia đôi | [Tên thành viên] | ✅ Hoàn thành | Bao gồm chứng minh hội tụ |
| 2 | Triển khai phương pháp Chia đôi (code) | [Tên thành viên] | ✅ Hoàn thành | Kiểm thử đầy đủ |
| 3 | Nghiên cứu lý thuyết phương pháp Dây cung | [Tên thành viên] | ✅ Hoàn thành | - |
| 4 | Triển khai phương pháp Dây cung (code) | [Tên thành viên] | ✅ Hoàn thành | - |
| 5 | Nghiên cứu lý thuyết phương pháp Newton-Raphson | [Tên thành viên] | ✅ Hoàn thành | Bao gồm tính đạo hàm |
| 6 | Triển khai phương pháp Newton-Raphson (code) | [Tên thành viên] | ✅ Hoàn thành | - |
| 7 | Nghiên cứu lý thuyết phương pháp Lặp điểm cố định | [Tên thành viên] | ✅ Hoàn thành | Kiểm tra điều kiện hội tụ |
| 8 | Triển khai phương pháp Lặp điểm cố định (code) | [Tên thành viên] | ✅ Hoàn thành | - |
| 9 | Xây dựng giao diện Streamlit | [Tên thành viên] | ✅ Hoàn thành | Bao gồm biểu đồ tương tác |
| 10 | Viết báo cáo và sơ đồ khối | [Tên thành viên] | ✅ Hoàn thành | - |
| 11 | Kiểm tra và hoàn thiện toàn bộ dự án | [Tên thành viên] | ✅ Hoàn thành | - |

---

## 5. NHỮNG RỦI RO VÀ LƯU Ý

### 5.1 Vấn đề Đa Nghiệm (Multiple Roots)

**Tình huống:** Nếu dòng tiền không chính quy (thay đổi dấu nhiều lần), phương trình NPV có thể có nhiều hơn một nghiệm.

**Ví dụ:**
```
Năm 0: -1000  (dấu âm)
Năm 1:  +500  (dấu dương)
Năm 2: -200   (dấu âm)
Năm 3: +800   (dấu dương)
```

**Hậu quả:**
- Các phương pháp có thể hội tụ đến các nghiệm khác nhau tùy vào giá trị khởi tạo.
- IRR không duy nhất, khó đánh giá dự án.
- Nhà đầu tư phải cẩn thận chọn IRR có ý nghĩa kinh tế.

**Cách khắc phục:**
- Ứng dụng sẽ **cảnh báo** nếu dòng tiền đổi dấu nhiều lần.
- Khuyến khích sử dụng Chia đôi với nhiều khoảng tìm kiếm khác nhau.
- Xem xét sử dụng chỉ số khác như MIRR (Modified IRR) hoặc NPV tại mức lãi suất chuẩn.

### 5.2 Vấn đề Hội Tụ

**Lặp điểm cố định:** Nếu điều kiện $|g'(r)| < 1$ không thỏa mãn, phương pháp có thể phân kỳ. Ứng dụng sẽ cảnh báo người dùng.

**Newton-Raphson:** Nếu $f'(r) \approx 0$, phương pháp có thể thất bại. Giải pháp là chọn khởi tạo khác hoặc sử dụng Chia đôi.

### 5.3 Vấn đề Độ Chính Xác

**Sai số đơn vị máy (Machine Precision):** Với sai số mục tiêu $\varepsilon = 10^{-5}$, các phép tính đặc biệt tốt. Nhưng nếu yêu cầu $\varepsilon = 10^{-12}$, cần cẩn thận với sai số làm tròn.

---

## 6. KẾT LUẬN

### 6.1 Kết Quả Đạt Được

✅ **Triển khai đầy đủ 4 phương pháp giải phương trình phi tuyến:**

---

# PHỤ LỤC: ĐỊNH DẠNG BẢNG LẶP CÁC PHƯƠNG PHÁP SỐ (THEO GIÁO TRÌNH)

Dưới đây là format trình bày quá trình giải phương trình phi tuyến tìm IRR với sai số $\epsilon = 10^{-5}$.

---

## 1. Phương pháp Chia đôi (Bisection)
*Điều kiện dừng: Độ dài khoảng cách ly nghiệm $|b_n - a_n| < \epsilon$.*

| Lần lặp ($n$) | $a_n$ | $b_n$ | $x_n = \frac{a_n + b_n}{2}$ | $f(a_n)$ | $f(x_n)$ | $f(a_n) \cdot f(x_n)$ | Sai số $|b_n - a_n|$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| 0 | $a_0$ | $b_0$ | $x_0$ | ... | ... | +/- | $|b_0 - a_0|$ |
| 1 | $a_1$ | $b_1$ | $x_1$ | ... | ... | +/- | $|b_1 - a_1|$ |
| ... | ... | ... | ... | ... | ... | ... | ... |


---

## 2. Phương pháp Lặp đơn (Fixed Point)
*Điều kiện: Chọn hàm lặp $g(x)$ sao for $|g'(x)| < 1$ trên khoảng phân ly.*

| Lần lặp ($n$) | $x_n$ | $x_{n+1} = g(x_n)$ | $|x_{n+1} - x_n|$ | Kiểm tra $|g'(x_n)| < 1$ |
| :--- | :--- | :--- | :--- | :--- |
| 0 | $x_0$ | $x_1$ | $|x_1 - x_0|$ | Đạt / Không đạt |
| 1 | $x_1$ | $x_2$ | $|x_2 - x_1|$ | Đạt / Không đạt |
| ... | ... | ... | ... | ... |

---

## 3. Phương pháp Newton (Tiếp tuyến)
*Lưu ý: Chọn điểm xuất phát $x_0$ thỏa mãn điều kiện Fourier $f(x_0) \cdot f''(x_0) > 0$.*

| Lần lặp ($n$) | $x_n$ | $f(x_n)$ | $f'(x_n)$ | $\Delta x_n = \frac{f(x_n)}{f'(x_n)}$ | $x_{n+1} = x_n - \Delta x_n$ | $|x_{n+1} - x_n|$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | $x_0$ | ... | ... | ... | $x_1$ | ... |
| 1 | $x_1$ | ... | ... | ... | $x_2$ | ... |
| ... | ... | ... | ... | ... | ... | ... |


[Image of Newton-Raphson method diagram]


---

## 4. Phương pháp Dây cung (Secant)
* Sử dụng hai điểm xấp xỉ liên tiếp để xác định nghiệm tiếp theo.*

| Lần lặp ($n$) | $x_{n-1}$ | $x_n$ | $f(x_{n-1})$ | $f(x_n)$ | $x_{n+1}$ | $|x_{n+1} - x_n|$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | $x_0$ | $x_1$ | ... | ... | $x_2$ | ... |
| 2 | $x_1$ | $x_2$ | ... | ... | $x_3$ | ... |
| ... | ... | ... | ... | ... | ... | ... |

---

### Ghi chú kỹ thuật:
1. **Độ chính xác:** Các giá trị số thực cần được làm tròn đến ít nhất 6 chữ số thập phân.
2. **Kết quả cuối cùng:** Nghiệm IRR phải được trình bày dưới dạng số thập phân và tỷ lệ phần trăm (%).
3. **Đánh giá:** So sánh số bước lặp (n) giữa các phương pháp để rút ra kết luận về tốc độ hội tụ (Newton thường nhanh nhất).
- Phương pháp Chia đôi: Ổn định, tuyến tính
- Phương pháp Dây cung: Nhanh, không cần đạo hàm
- Phương pháp Newton-Raphson: Rất nhanh, bậc hai
- Phương pháp Lặp điểm cố định: Linh hoạt, kiểm tra hội tụ

✅ **Giao diện ứng dụng chuyên nghiệp:**
- Streamlit thân thiện, trực quan
- Đồ thị NPV tương tác bằng Plotly
- Bảng so sánh hiệu năng chi tiết
- Quy trình bước một cho từng phương pháp

✅ **Xử lý các trường hợp đặc biệt:**
- Cảnh báo khi dòng tiền đổi dấu nhiều lần
- Kiểm tra điều kiện hội tụ cho Lặp điểm cố định
- Xử lý lỗi đầu vào tốt

✅ **Tính năng xuất kết quả:**
- Tải bảng so sánh dưới dạng CSV
- Hiển thị công thức toán học rõ ràng

### 6.2 Những Cải Thiện Tiếp Theo

📌 **Có thể phát triển thêm:**
1. Vẽ sơ đồ khối động trong ứng dụng
2. Hỗ trợ nhiều khoảng tìm kiếm khác nhau (multi-root search)
3. So sánh với MIRR hoặc các chỉ số tài chính khác
4. Xuất báo cáo dạng PDF
5. Lưu trữ lịch sử tính toán

### 6.3 Nhận Xét Chung

Bài toán tìm IRR là ứng dụng thực tế rất tốt để giảng dạy các phương pháp giải phương trình phi tuyến. Thông qua đề tài này, sinh viên không chỉ học được lý thuyết mà còn hiểu rõ ưu/nhược điểm của từng phương pháp trong bối cảnh ứng dụng thực tế.

**Khuyến nghị:** Lãi suất hoàn vốn (IRR) là chỉ số quan trọng nhưng không phải là duy nhất. Nhà đầu tư cần kết hợp với NPV, Payback Period, và các chỉ số khác để có quyết định tốt nhất.

---

## TÀI LIỆU THAM KHẢO

1. Phạm Minh Hoàng. *Phương pháp số và lập trình*. NXB Khoa học Kỹ thuật.
2. Burden, R. L., & Faires, J. D. (2010). *Numerical Analysis* (9th ed.). Cengage Learning.
3. Quarteroni, A., Sacco, R., & Saleri, F. (2010). *Numerical Mathematics* (2nd ed.). Springer.
4. Dokumentasi Streamlit: https://docs.streamlit.io/
5. NumPy & Pandas Documentation: https://numpy.org/, https://pandas.pydata.org/

---

**Ngày hoàn thành:** [Nhập ngày nộp bài]

**Người soạn:** [Tên thành viên nhóm]

**Ghi chú:** Báo cáo này đi kèm với ứng dụng Streamlit có thể chạy được ngay lập tức bằng lệnh:
```bash
streamlit run app.py
```
