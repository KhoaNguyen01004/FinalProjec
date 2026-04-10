"""
Streamlit UI components and layout management.
File: ui_components.py
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from io import StringIO


def render_theory_section():
    """Render the theoretical foundation section with mathematical formulas."""
    with st.expander("Cơ sở Lý Thuyết", expanded=False):
        st.subheader("1. Phương trình NPV và bài toán IRR")
        st.write("""
        **Lãi suất hoàn vốn nội bộ (IRR)** là mức lãi suất mà tại đó Giá trị hiện tại ròng (NPV) bằng 0.
        Bài toán tìm IRR được phát biểu toán học như sau:
        """)
        st.latex(r"f(r) = C_0 + \sum_{i=1}^{n} \frac{C_i}{(1+r)^i} = 0")
        
        st.write("""
        Trong đó:
        - $C_i$ là dòng tiền tại năm thứ $i$
        - $r$ là lãi suất cần tìm (IRR)
        - $n$ là số năm
        """)
        
        st.subheader("2. Đạo hàm của hàm NPV")
        st.write("Đạo hàm bậc nhất (sử dụng trong phương pháp Newton-Raphson):")
        st.latex(r"f'(r) = -\sum_{i=1}^{n} \frac{i \cdot C_i}{(1+r)^{i+1}}")
        
        st.write("Đạo hàm bậc hai (sử dụng trong phương pháp Lặp điểm cố định):")
        st.latex(r"f''(r) = -\sum_{i=1}^{n} \frac{i(i+1) \cdot C_i}{(1+r)^{i+2}}")
        
        st.subheader("3. Khoảng phân ly nghiệm")
        st.write("""
        Khoảng tìm kiếm: **[0, 1]** (từ 0% đến 100%)
        
        **Giải thích:**
        - Lãi suất IRR trong thực tế thường nằm trong khoảng từ 0% đến 100%.
        - Việc chọn khoảng này đảm bảo rằng ta sẽ bắt được nghiệm nếu nó tồn tại.
        - Đối với phương pháp Chia đôi, ta cần kiểm chứng f(a) · f(b) < 0 (hàm thay đổi dấu).
        """)
        
        st.subheader("4. Tiêu chuẩn dừng")
        st.write(r"Sai số mục tiêu: $\varepsilon = 10^{-5}$")
        st.write(r"""
        Thuật toán dừng khi: $\Delta_n < \varepsilon$
        """)


def render_input_section():
    """Render the input section for cash flows with formatting preview."""
    st.markdown("### Nhập Dòng Tiền")
    st.write("*Hỗ trợ định dạng số lớn: dùng . cho hàng nghìn, ; phân cách dòng tiền.*")
    st.write("*Ví dụ: `-2.000;400;600;800;1200`*")
    
    col1, col2 = st.columns([3,1])
    with col1:
        cash_flow_input = st.text_input(
            "Dòng tiền (phân cách ;):",
            value="-2.000;400;600;800;800;1200",
            help="Nhập số âm cho vốn đầu tư năm 0. Dấu chấm (.) cho hàng nghìn, ; phân cách dòng tiền."
        )
    with col2:
        if st.button("Copy mẫu", key="copy_sample"):
            st.code("-2.000;400;600;800;1200", language="text")
    
    # Live preview
    if cash_flow_input:
        try:
            from utils import parse_cash_flow, format_cash_flow
            cash_flows = parse_cash_flow(cash_flow_input)
            formatted = format_cash_flow(cash_flows)
            
            st.success(f"Đã parse: {len(cash_flows)} dòng tiền")
            st.caption(f"*Định dạng chuẩn: {formatted}*")
            
            # Preview table
            preview_df = pd.DataFrame({
                "Năm": [f"Năm {i}" for i in range(len(cash_flows))],
                "Dòng tiền": [f"{cf:,.0f}" for cf in cash_flows]
            })
            st.dataframe(preview_df, width="stretch", hide_index=True)
            
            # Return both for convenience
            st.session_state.cash_flows_preview = cash_flows
            return cash_flow_input, cash_flows
            
        except ValueError as e:
            st.error(f"Lỗi parse: {e}")
            if st.session_state.get('cash_flows_preview'):
                del st.session_state.cash_flows_preview
            return cash_flow_input, None
    
    return cash_flow_input, None


def plot_npv_function(r_values, npv_values, roots):
    """
    Create an interactive Plotly chart of NPV(r).
    
    Parameters:
    -----------
    r_values : array-like
        Values of r where NPV is calculated
    npv_values : array-like
        Corresponding NPV values
    roots : list
        List of approximate roots to highlight
    
    Returns:
    --------
    fig : plotly Figure object
    """
    fig = go.Figure()
    
    # Plot NPV function
    fig.add_trace(go.Scatter(
        x=r_values,
        y=npv_values,
        mode='lines',
        name='NPV(r)',
        line=dict(color='blue', width=2)
    ))
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="f(r) = 0")
    
    # Highlight roots
    for root in roots:
        if root is not None and np.isfinite(root):
            fig.add_trace(go.Scatter(
                x=[root],
                y=[0],
                mode='markers',
                marker=dict(color='red', size=10),
                name=f'IRR ≈ {root:.5f}',
                showlegend=True
            ))
    
    fig.update_layout(
        title="Đồ Thị Hàm NPV(r)",
        xaxis_title='r (Lãi suất)',
        yaxis_title='NPV(r)',
        hovermode='x unified',
        height=500
    )
    
    return fig


def display_results_table(df):
    """Display the results comparison table and export option."""
    st.subheader("Bảng So Sánh Kết Quả")
    st.table(df)
    
    # Export CSV functionality
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8')
    csv_data = csv_buffer.getvalue()
    
    st.download_button(
        label="Tải kết quả (CSV)",
        data=csv_data,
        file_name="kết_quả_irr.csv",
        mime="text/csv"
    )


def display_detailed_info(a, b, tolerance, max_iterations):
    """Display dynamic algorithm parameters used."""
    st.subheader("Thông số Tính Toán Đã Sử Dụng")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Sai số (ε)", f"{tolerance:.0e}")
    
    with col2:
        st.metric("Khoảng [a,b]", f"[ {a:.2f}, {b:.2f} ]")
    
    with col3:
        st.metric("Số lặp tối đa", max_iterations)


def display_commentary(df):
    """Display automated commentary on method performance."""
    st.subheader("Nhận Xét Tự Động")
    
    if not df.empty:
        min_iters = df["Số lần lặp"].min()
        fastest_methods = df[df["Số lần lặp"] == min_iters]["Phương pháp"].tolist()
        
        if len(fastest_methods) == 1:
            st.write(f"Phương pháp nhanh nhất: {fastest_methods[0]} ({min_iters} lần lặp)")
        else:
            methods_str = ", ".join(fastest_methods)
            st.write(f"Phương pháp nhanh nhất: {methods_str} ({min_iters} lần lặp)")
    
    st.write("""
    Phân tích từng phương pháp:
    
    - Chia đôi: Luôn hội tụ nếu hàm thay đổi dấu trong khoảng. Ổn định nhất nhưng hội tụ chậm.
    
    - Dây cung: Tốc độ hội tụ tốt (~1.618), không cần tính đạo hàm. Nhạy cảm với khởi tạo xấu.
    
    - Newton-Raphson: Hội tụ bậc hai (rất nhanh), ít lần lặp. Có thể thất bại nếu f'(r) ≈ 0.
    
    - Lặp điểm cố định: Linh hoạt, tương tự Newton-Raphson. Cần kiểm tra điều kiện hội tụ |g'(r)| < 1.
    """)


def display_trace_tables(traces):
    """
    Display method-specific trace tables with exact columns per algorithm spec.
    
    traces[method_name] = (history: list[list], columns: list[str])
    """
    st.subheader("Bảng Theo Dõi Hội Tụ & Sai Số")

    display_names = {
        "n": "Bước lặp (n)",
        "a_n": "a_n (đầu trái)",
        "b_n": "b_n (đầu phải)",
        "c_n": "c_n (giữa)",
        "f(c_n)": "f(c_n)",
        "f(x_n)": "f(x_n)",
        "x_n": "x_n (nghiệm xấp xỉ)",
        "Δ_n": "Sai số ước lượng (Δ_n)"
    }

    for method_name, (history, columns) in traces.items():
        with st.expander(method_name, expanded=False):
            # Only non-empty iterations, start from n=0 if present
            valid_history = [row for row in history if any(v is not None and str(v).strip() != '' for v in row[1:])]
            if valid_history:
                trace_df = pd.DataFrame(valid_history, columns=columns)
                
                # Apply Vietnamese display names
                trace_df.columns = [display_names.get(col, col) for col in columns]

            
            # Format numbers
            for col in trace_df.columns:
                if col != "Bước lặp (n)":
                    trace_df[col] = trace_df[col].apply(
                        lambda x: f"{float(x):.8f}" if isinstance(x, (int, float, np.floating)) and np.isfinite(x) else str(x)
                    )
            
            if "Bước lặp (n)" in trace_df.columns and len(trace_df) > 0:
                trace_df = trace_df.set_index("Bước lặp (n)")

            
            st.dataframe(trace_df, width="stretch", height=300)

            
            # Removed caption per feedback




def display_warning_multiple_roots():
    """Display warning if multiple roots are likely."""
    st.write(
        "**Cảnh báo:** Dòng tiền thay đổi dấu nhiều hơn một lần. "
        "Phương trình có thể có **nhiều nghiệm IRR**. "
        "Hãy cẩn thận khi đánh giá dự án!"
    )


def display_error_invalid_input():
    """Display error message for invalid input."""
    st.write("Đầu vào không hợp lệ. Vui lòng nhập giá trị số phân cách bằng dấu phẩy.")


def display_error_message(error_text):
    """Display a generic error message."""
    st.write(f"Đã xảy ra lỗi: {error_text}")
