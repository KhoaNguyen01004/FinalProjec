# Ứng Dụng Tính IRR - Giải Phương Trình Phi Tuyến Trong Phân Tích Tài Chính

## 📋 Mô Tả Dự Án

Đây là ứng dụng web tương tác được phát triển bằng Python và Streamlit để giải bài toán tìm **Lãi Suất Hoàn Vốn Nội Bộ (IRR)** sử dụng 4 phương pháp số cổ điển. Dự án được thiết kế cho mục đích giáo dục và nghiên cứu, giúp so sánh hiệu năng của các phương pháp giải phương trình phi tuyến trong ngữ cảnh tài chính.

### 🎯 Mục Tiêu Học Thuật
- Triển khai đầy đủ 4 phương pháp số theo sách giáo khoa
- So sánh hiệu năng (tốc độ hội tụ, độ ổn định, số lần lặp)
- Ứng dụng thực tế vào bài toán IRR trong phân tích đầu tư
- Xây dựng giao diện demo thân thiện và trực quan

## ✨ Tính Năng Chính

### 🔢 4 Phương Pháp Số
1. **Phương Pháp Chia Đôi (Bisection Method)**
   - Luôn hội tụ nếu hàm thay đổi dấu trong khoảng
   - Ổn định nhất nhưng tốc độ hội tụ chậm

2. **Phương Pháp Dây Cung (Secant Method)**
   - Tốc độ hội tụ siêu tuyến tính (~1.618)
   - Không cần tính đạo hàm, chỉ sử dụng giá trị hàm

3. **Phương Pháp Newton-Raphson**
   - Hội tụ bậc hai (rất nhanh)
   - Cần tính đạo hàm bậc nhất

4. **Phương Pháp Lặp Điểm Cố Định (Fixed-Point Iteration)**
   - Linh hoạt, có thể chuyển đổi từ Newton-Raphson
   - Cần kiểm tra điều kiện hội tụ |g'(r)| < 1

### 📊 Trực Quan Hóa
- **Biểu đồ NPV**: Hiển thị hàm NPV f(r) để quan sát nghiệm
- **Bảng So Sánh**: Thời gian thực hiện, số lần lặp, độ chính xác
- **Bảng Trace**: Chi tiết từng bước lặp của mỗi phương pháp
- **Nhận Xét Tự Động**: Phân tích hiệu năng và khuyến nghị phương pháp tối ưu

### 🎛️ Tùy Chỉnh
- **Sai số mục tiêu**: Từ 10^-10 đến 10^-2
- **Số lần lặp tối đa**: 100 - 5000 lần
- **Dữ liệu đầu vào**: Dòng tiền tùy chỉnh

## 🏗️ Cấu Trúc Dự Án

```
FinalProjec/
├── app.py                 # Ứng dụng chính Streamlit
├── algorithms.py          # 4 phương pháp số
├── ui_components.py       # Thành phần giao diện
├── utils.py              # Hàm tiện ích (NPV, đạo hàm)
├── test_algorithms.py    # Bộ test tự động
├── requirements.txt      # Dependencies
└── README.md            # Tài liệu này
```

### 📁 Chi Tiết Các File

- **`app.py`**: Ứng dụng chính điều phối toàn bộ logic
- **`algorithms.py`**: Triển khai 4 phương pháp số với trace logging
- **`ui_components.py`**: Các component UI (biểu đồ, bảng, nhận xét)
- **`utils.py`**: Tính NPV, đạo hàm, kiểm tra dấu
- **`test_algorithms.py`**: Test suite đảm bảo tính đúng đắn

## 🚀 Cài Đặt và Chạy

### 📋 Yêu Cầu Hệ Thống
- Python 3.8+
- Windows/Linux/macOS
- Trình duyệt web hiện đại

### ⚡ Các Bước Cài Đặt

1. **Clone hoặc tải dự án**
   ```bash
   cd path/to/your/folder
   # Copy tất cả files vào thư mục FinalProjec
   ```

2. **Tạo môi trường ảo (khuyến nghị)**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Cài đặt dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Chạy ứng dụng**
   ```bash
   streamlit run app.py
   ```

5. **Truy cập ứng dụng**
   - Mở trình duyệt và truy cập: `http://localhost:8501`
   - Hoặc địa chỉ được hiển thị trong terminal

### 🧪 Chạy Test
```bash
python test_algorithms.py
```

## 📖 Cách Sử Dụng

### 1. Nhập Dữ Liệu
- **Dòng tiền**: Nhập các giá trị phân cách bằng dấu phẩy
- **Ví dụ**: `-2000,400,600,800,800,1200`
- **Giải thích**: Vốn đầu tư âm, dòng tiền dương từ năm 1-5

### 2. Cấu Hình Tính Toán
- **Sai số mục tiêu**: Độ chính xác mong muốn (mặc định: 10^-5)
- **Số lần lặp tối đa**: Giới hạn để tránh vòng lặp vô hạn

### 3. Chạy Tính Toán
- Nhấn nút **"Tính IRR"**
- Ứng dụng sẽ thực hiện song song 4 phương pháp

### 4. Xem Kết Quả
- **Biểu đồ NPV**: Quan sát hàm và nghiệm
- **Bảng kết quả**: So sánh 4 phương pháp
- **Nhận xét tự động**: Phương pháp nào nhanh nhất
- **Bảng trace**: Chi tiết từng bước lặp

## 🔬 Cơ Sở Lý Thuyết

### Phương Trình NPV
```
f(r) = C₀ + Σ(Cᵢ/(1+r)ⁱ) = 0  (i=1 đến n)
```

### Tiêu Chuẩn Dừng
- **Sai số tuyệt đối**: |f(r)| < ε
- **Số lần lặp**: Không vượt quá giới hạn

### Khoảng Tìm Kiếm
- **IRR thực tế**: [0, 1] (0% đến 100%)
- **Lý do**: IRR thường nằm trong khoảng này

## 📈 Ví Dụ Minh Họa

**Dữ liệu mẫu:**
- Năm 0: -2,000 triệu VNĐ (đầu tư)
- Năm 1-5: 400, 600, 800, 800, 1,200 triệu VNĐ

**Kết quả mong đợi:**
- IRR ≈ 21.54%
- Newton-Raphson và Fixed-point thường hội tụ nhanh nhất

## 🐛 Xử Lý Lỗi

### Đầu Vào Không Hợp Lệ
- Thông báo lỗi đỏ khi nhập sai định dạng
- Chỉ chấp nhận số phân cách bằng dấu phẩy

### Không Hội Tụ
- Cảnh báo khi phương pháp không tìm được nghiệm
- Kiểm tra điều kiện hội tụ cho từng phương pháp

### Nhiều Nghiệm
- Cảnh báo khi hàm thay đổi dấu nhiều lần
- IRR có thể có nhiều giá trị

## 🤝 Đóng Góp

Dự án này được phát triển cho mục đích học thuật. Để đóng góp:

1. Fork repository
2. Tạo branch feature
3. Commit changes
4. Push và tạo Pull Request

## 📄 Giấy Phép

Dự án này được phát triển cho mục đích giáo dục và nghiên cứu khoa học.

## 👥 Tác Giả

- **Nhóm Sinh Viên**: Đề tài 05 - Phương Pháp Số
- **Ngôn Ngữ**: Python 3.12
- **Framework**: Streamlit
- **Thư Viện**: NumPy, Pandas, Plotly

---

**Lưu ý**: Đây là phiên bản demo giáo dục. Không sử dụng cho quyết định đầu tư thực tế mà không có sự tư vấn chuyên môn.</content>
<parameter name="filePath">d:\SIU\PhuongPhapSo\FinalProjec\README.md