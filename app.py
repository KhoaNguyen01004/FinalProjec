"""
Main Streamlit application for IRR Solver.
File: app.py

This application implements 4 numerical methods to solve the IRR problem:
1. Bisection method
2. Secant method
3. Newton-Raphson method
4. Fixed-point iteration

It provides an interactive dashboard with visualization, performance comparison,
and detailed trace logs for educational purposes.
"""

import streamlit as st
import numpy as np
import pandas as pd

from utils import npv, count_sign_changes, find_root_interval
from algorithms import (
    bisection_method,
    secant_method,
    newton_raphson_method,
    fixed_point_iteration
)
from ui_components import (
    render_theory_section,
    render_input_section,
    plot_npv_function,
    display_results_table,
    display_detailed_info,
    display_commentary,
    display_trace_tables,
    display_warning_multiple_roots,
    display_error_invalid_input,
    display_error_message
)


# ========================
# PAGE CONFIGURATION
# ========================
st.set_page_config(
    page_title="Ứng dụng Tính IRR",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================
# TITLE AND HEADER
# ========================
st.title("Ứng dụng Tính IRR")
st.write("""
Giải bài toán tìm **Lãi suất Hoàn Vốn Nội Bộ (IRR)** bằng 4 phương pháp số.
Ứng dụng này giúp bạn so sánh hiệu năng và hiểu rõ từng phương pháp.
""")

# ========================
# SIDEBAR
# ========================
st.sidebar.title("Cấu Hình")
st.sidebar.write("Tùy chọn tính toán và hiển thị")

# Tolerance options
tolerance_options = [1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2]
tolerance = st.sidebar.select_slider(
    "Sai số mục tiêu (ε)",
    options=tolerance_options,
    value=1e-5,
    format_func=lambda x: f"{x:.0e}"
)

max_iterations = st.sidebar.slider(
    "Số lần lặp tối đa",
    min_value=100,
    max_value=5000,
    value=1000,
    step=100
)

st.sidebar.divider()
st.sidebar.write(f"**Cài đặt hiện tại:**")
st.sidebar.write(f"- Sai số mục tiêu: {tolerance:.0e}")
st.sidebar.write(f"- Số lần lặp tối đa: {max_iterations}")
st.sidebar.write("**Thông tin ứng dụng**")
st.sidebar.write("- Triển khai: Python 3.12 + Streamlit")
st.sidebar.write("- Thư viện: NumPy, Pandas, Plotly")
st.sidebar.write("- Phương pháp: 4 kỹ thuật giải gần đúng")

# ========================
# MAIN CONTENT
# ========================

# Theory section
render_theory_section()

st.divider()

# Input section
input_result = render_input_section()
if isinstance(input_result, tuple):
    cash_flow_input, cash_flows_preview = input_result
else:
    cash_flow_input = input_result
    cash_flows_preview = None

# Calculate button
if st.button("Tính IRR", type="primary", width="stretch"):
    try:
        # Use preview if available and valid, else parse
        if cash_flows_preview is not None and len(cash_flows_preview) >= 2:
            cash_flows = cash_flows_preview
            from utils import parse_cash_flow
            cash_flows = parse_cash_flow(cash_flow_input)
        
        if len(cash_flows) < 2:
            raise ValueError("Cần ít nhất 2 dòng tiền")
        
        st.success(f"Sử dụng {len(cash_flows)} dòng tiền ({len(cash_flows)-1} năm): { [f'{cf:.0f}' for cf in cash_flows] }")

        
        # Check for multiple sign changes
        sign_changes = count_sign_changes(cash_flows)
        if sign_changes > 1:
            display_warning_multiple_roots()
        
        # Check if root exists (keep original for warning)
        orig_a, orig_b, root_exists = find_root_interval(cash_flows)
        
        # Force standard [0,1] interval for Bisection table consistency (Δ_0=1.0 → 0.5,0.25...)
        a, b = 0.0, 1.0
        
        # Removed interval info per feedback


        
        if not npv(a, cash_flows) * npv(b, cash_flows) < 0:
            st.warning("f(0)*f(1) >= 0 - không đảm bảo nghiệm trong [0,1]")
        
        if not root_exists:
            st.error(
                "Không tìm thấy IRR. Kiểm tra dòng tiền."
            )
            st.stop()


        
        if a != 0 or b != 1:
            st.info(f"Tìm thấy IRR trong khoảng [{a}, {b}]. Mở rộng khoảng tìm kiếm từ [0, 1].")
        
        st.divider()
        
        # Calculate using all methods FIRST (before showing results)
        with st.spinner("Đang tính toán..."):
            methods = [
                ("Chia đôi", bisection_method),
                ("Dây cung", secant_method),
                ("Newton-Raphson", newton_raphson_method),
                ("Lặp điểm cố định", fixed_point_iteration)
            ]
            
            results = []
            traces = {}
            convergence_warnings = {}
            
            for method_name, method_func in methods:
                if method_name == "Chia đôi":
                    root, iters, time_ms, history, columns = method_func(
                        cash_flows, a=a, b=b, tol=tolerance, max_iter=max_iterations
                    )
                    convergence_warnings[method_name] = False
                elif method_name == "Dây cung":
                    root, iters, time_ms, history, columns = method_func(
                        cash_flows, a=a, b=b, x0=a, x1=a+0.1, tol=tolerance, max_iter=max_iterations
                    )
                    convergence_warnings[method_name] = False
                elif method_name == "Lặp điểm cố định":
                    root, iters, time_ms, history, columns, warning = method_func(
                        cash_flows, a=a, b=b, x0=a, tol=tolerance, max_iter=max_iterations
                    )
                    convergence_warnings[method_name] = warning
                else:  # Newton-Raphson
                    root, iters, time_ms, history, columns = method_func(
                        cash_flows, a=a, b=b, x0=a, tol=tolerance, max_iter=max_iterations
                    )
                    convergence_warnings[method_name] = False
                
                results.append([method_name, root, iters, time_ms])
                traces[method_name] = (history, columns)

        
        st.success("Tính toán xong!")
        
        # Create results dataframe
        df = pd.DataFrame(results, columns=["Phương pháp", "IRR", "Số lần lặp", "Thời gian (ms)"])
        
        st.divider()
        
        # FRIENDLY COMMENTARY FOR NON-EXPERTS (Show FIRST)
        st.subheader("Kết Quả & Nhận Xét")
        
        if not df.empty:
            irr_value = df.iloc[0]["IRR"]
            
            # Find fastest method
            min_iterations = df["Số lần lặp"].min()
            fastest_methods = df[df["Số lần lặp"] == min_iterations]["Phương pháp"].tolist()
            fastest_str = ", ".join(fastest_methods) if len(fastest_methods) > 1 else fastest_methods[0]
            
            # Display IRR prominently
            col1, col2 = st.columns(2)
            with col1:
                if np.isfinite(irr_value):
                    irr_percentage = irr_value * 100
                    st.write(f"**Lãi Suất Hoàn Vốn (IRR):** {irr_percentage:.2f}%")
                else:
                    st.write("**Lãi Suất Hoàn Vốn (IRR):** Không xác định")
                    irr_percentage = None
            
            with col2:
                st.write(f"**Phương pháp nhanh nhất:** {fastest_str} ({int(min_iterations)} lần lặp)")
            
            st.write("")
            if irr_percentage is not None:
                st.write("**So sánh với lãi suất ngân hàng:**")
                
                # Interest rate comparison table
                bank_rates = [5, 10, 15, 20, 25, 30]
                comparison_data = []
                for rate in bank_rates:
                    diff = irr_percentage - rate
                    if diff > 0:
                        status = "Nên đầu tư"
                        decision = f"Lợi hơn {abs(diff):.2f}%"
                    else:
                        status = "Gửi ngân hàng"
                        decision = f"Kém hơn {abs(diff):.2f}%"
                    comparison_data.append([f"{rate}%", status, decision])
                
                comparison_df = pd.DataFrame(
                    comparison_data, 
                    columns=["Lãi Suất NH", "Quyết Định", "Chênh Lệch"]
                )
                st.table(comparison_df)
        
        st.divider()
        
        # Plot NPV function
        st.subheader("Trực Quan Hóa Hàm NPV(r)")
        r_values = np.linspace(0, 1, 200)
        npv_values = [npv(r, cash_flows) for r in r_values]
        
        # Find approximate roots
        roots = []
        for i in range(len(npv_values) - 1):
            if npv_values[i] * npv_values[i + 1] < 0:
                root = (r_values[i] + r_values[i + 1]) / 2
                roots.append(root)
        roots = [r for r in roots if np.isfinite(r)]
        
        fig = plot_npv_function(r_values, npv_values, roots)
        st.plotly_chart(fig, width="stretch")
        
        st.divider()
        
        # Results table
        st.subheader("Bảng So Sánh Chi Tiết")
        
        # Format columns for display - FIXED IRR column error
        df_display = df.copy()
        df_display = df_display.rename(columns={'IRR': 'IRR (%)'})
        df_display["Thời gian (ms)"] = df_display["Thời gian (ms)"].apply(lambda x: f"{x:.4f}")
        df_display["IRR (%)"] = df_display["IRR (%)"].apply(lambda x: f"{float(x)*100:.2f}%" if np.isfinite(float(x)) else "N/A")
        st.table(df_display)
        
        # Show applied settings
        st.write(f"**Cấu hình tính toán:** Sai số mục tiêu = {tolerance:.0e}, Số lần lặp tối đa = {max_iterations}")
        
        st.divider()
        
        # Export CSV functionality
        from io import StringIO
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8')
        csv_data = csv_buffer.getvalue()
        st.download_button(
            label="Tải kết quả (CSV)",
            data=csv_data,
            file_name="kết_quả_irr.csv",
            mime="text/csv"
        )
        
        st.divider()
        
        # Detailed info
        display_detailed_info(tolerance, max_iterations)
        
        st.divider()
        
        st.divider()
        
        # Technical details section
        with st.expander("Chi Tiết Kỹ Thuật & Phân Tích Phương Pháp"):
            st.write("""
            **Phân tích từng phương pháp:**
            
            - **Chia đôi:** Luôn hội tụ nếu hàm thay đổi dấu trong khoảng. Ổn định nhất nhưng hội tụ chậm.
            
            - **Dây cung:** Tốc độ hội tụ tốt (~1.618), không cần tính đạo hàm. Nhạy cảm với khởi tạo xấu.
            
            - **Newton-Raphson:** Hội tụ bậc hai (rất nhanh), ít lần lặp. Có thể thất bại nếu f'(r) ≈ 0.
            
            - **Lặp điểm cố định:** Linh hoạt, tương tự Newton-Raphson. Cần kiểm tra điều kiện hội tụ |g'(r)| < 1.
            """)
            
            if convergence_warnings.get("Lặp điểm cố định", False):
                st.write(
                    "**Cảnh báo Lặp điểm cố định:** "
                    "Điều kiện hội tụ |g'(r)| < 1 không thỏa mãn tại điểm khởi tạo. "
                    "Kết quả có thể không chính xác."
                )
            
            st.subheader("Bảng Trace Chi Tiết (Hội Tụ & Sai Số)")
            display_trace_tables(traces)

    
    except Exception as e:
        display_error_message(str(e))

st.divider()

# Information section at bottom
with st.expander("Về Ứng Dụng Này"):
    st.write("""
    ### Tài Liệu Tiểu Luận Nhóm - Đề Tài 05
    
    **Chủ đề:** Ứng dụng các phương pháp giải phương trình phi tuyến trong phân tích dữ liệu tài chính
    
    **Mục tiêu:**
    - Triển khai 4 phương pháp số: Chia đôi, Dây cung, Newton-Raphson, Lặp điểm cố định
    - So sánh hiệu năng (tốc độ, độ ổn định, số lần lặp)
    - Ứng dụng vào bài toán tìm IRR thực tế
    - Xây dựng giao diện demo thân thiện người dùng
    
    **Dữ Liệu Mẫu:**
    - Năm 0: -2,000 triệu VNĐ (vốn đầu tư)
    - Năm 1-5: Dòng tiền từ hoạt động (400, 600, 800, 800, 1,200 triệu VNĐ)
    
    **Mã Nguồn:** Được chia thành 4 module:
    - `utils.py`: Hàm tiện ích (tính NPV, đạo hàm)
    - `algorithms.py`: 4 phương pháp số
    - `ui_components.py`: Thành phần giao diện Streamlit
    - `app.py`: Ứng dụng chính
    """)
