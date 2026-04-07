"""
Numerical methods for solving non-linear equations: f(r) = 0
File: algorithms.py

Based on standard numerical analysis textbooks with rigorous convergence conditions.
"""

import time
import numpy as np
from utils import npv, npv_derivative, npv_second_derivative, check_fourier_condition, find_min_derivative, find_max_second_derivative, find_max_g_prime


def bisection_method(cash_flows, a=0, b=1, tol=1e-5, max_iter=1000):
    """
    Bisection method (Chia đôi)
    
    Table columns per spec: n, a_n, b_n, c_n, f(c_n), |b_n - a_n|
    
    Parameters:
    -----------
    cash_flows : list or array
        Array of cash flows
    a, b : float
        Interval [a, b] where the root is searched (default [0, 1])
    tol : float
        Tolerance for interval length (default 1e-5)
    max_iter : int
        Maximum number of iterations (default 1000)
    
    Returns:
    --------
    root : float
    iterations : int
    time_ms : float
    history : list[list] - rows for table
    columns : list[str] - ["n", "a_n", "b_n", "c_n", "f(c_n)", "Δ_n = |b_n - a_n|"]
    """
    history = [[0, a, b, None, None, abs(b - a)]]

    columns = ["n", "a_n", "b_n", "c_n", "f(c_n)", "Δ_n"]
    start_time = time.time()
    
    fa = npv(a, cash_flows)
    fb = npv(b, cash_flows)
    
    if fa * fb >= 0:
        return (a + b) / 2, 0, (time.time() - start_time)*1000, history, columns
    
    for it in range(max_iter):
        c = (a + b) / 2
        fc = npv(c, cash_flows)
        delta_n = abs(b - a)
        
        history.append([it+1, a, b, c, fc, delta_n])
        
        if delta_n < tol or fc == 0:
            return c, it+1, (time.time() - start_time)*1000, history, columns
        
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    
    c = (a + b) / 2
    return c, max_iter, (time.time() - start_time)*1000, history, columns



def secant_method(cash_flows, a=0, b=1, x0=0, x1=0.1, tol=1e-5, max_iter=1000):
    """
    Secant (Dây cung) - spec: n, x_n, f(x_n), Sai số
    
    Returns:
    root, iterations, time_ms, history, columns
    columns: ["n", "x_n", "f(x_n)", "Δ_n"]
    """
    r_test = np.linspace(a, b, 100)
    m1 = find_min_derivative(r_test, cash_flows)
    
    if x1 == 0.1:
        x1 = x0 + 0.1
    
    history = []
    columns = ["n", "x_n", "f(x_n)", "Δ_n"]
    start_time = time.time()
    
    for it in range(max_iter):
        f0 = npv(x0, cash_flows)
        f1 = npv(x1, cash_flows)
        
        if abs(f1 - f0) < 1e-10:
            return x1, it, (time.time() - start_time)*1000, history, columns
        
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        delta_n = abs(f1) / m1 if m1 > 0 else abs(f1)
        
        history.append([it+1, x1, f1, delta_n])
        
        if delta_n < tol:
            return x2, it+1, (time.time() - start_time)*1000, history, columns
        
        x0, x1 = x1, x2
    
    return x2, max_iter, (time.time() - start_time)*1000, history, columns



def newton_raphson_method(cash_flows, a=0, b=1, x0=0.1, tol=1e-5, max_iter=1000):
    """
    Newton-Raphson (Tiếp tuyến) - spec: n, x_n, Δ_n = (M/(2m)) * |Δx|^2
    
    Returns:
    --------
    root, iterations, time_ms, history, columns
    columns: ["n", "x_n", "Δ_n"]
    """
    r_test = np.linspace(a, b, 100)
    m = find_min_derivative(r_test, cash_flows)
    M = find_max_second_derivative(r_test, cash_flows)
    
    history = []
    columns = ["n", "x_n", "Δ_n"]
    start_time = time.time()
    
    for it in range(max_iter):
        f = npv(x0, cash_flows)
        f_prime = npv_derivative(x0, cash_flows)
        
        if abs(f_prime) < 1e-10 or not np.isfinite(f_prime):
            return x0, it, (time.time() - start_time)*1000, history, columns
        
        x1 = x0 - f / f_prime
        delta_x = abs(x1 - x0)
        delta_n = (M / (2 * m)) * delta_x**2 if m > 0 else delta_x
        
        history.append([it+1, x1, delta_n])
        
        if delta_n < tol:
            return x1, it+1, (time.time() - start_time)*1000, history, columns
        
        x0 = x1
    
    return x1, max_iter, (time.time() - start_time)*1000, history, columns



def fixed_point_iteration(cash_flows, a=0, b=1, x0=0.1, tol=1e-5, max_iter=1000):
    """
    Fixed-point iteration (Lặp đơn) - per spec: n, x_n, Sai số = q/(1-q)*|x_n - x_{n-1}|
    
    Parameters:
    -----------
    cash_flows : list or array
    a, b, x0, tol, max_iter : see above
    
    Returns:
    --------
    root, iterations, time_ms, history, columns, convergence_warning
    history columns: ["n", "x_n", "Δ_n"]
    """
    r_test = np.linspace(a, b, 100)
    q = find_max_g_prime(r_test, cash_flows)
    convergence_warning = q >= 1
    
    history = []
    columns = ["n", "x_n", "Δ_n"]
    start_time = time.time()
    prev_x = x0  # Initial
    
    for it in range(1, max_iter+1):
        f = npv(x0, cash_flows)
        f_prime = npv_derivative(x0, cash_flows)
        
        if abs(f_prime) < 1e-10 or not np.isfinite(f_prime):
            return x0, it, (time.time() - start_time)*1000, history, columns, convergence_warning
        
        x1 = x0 - f / f_prime
        delta_x = abs(x1 - prev_x)
        delta_n = (q / (1 - q)) * delta_x if q < 1 else delta_x  # Exact formula or fallback
        
        history.append([it, x1, delta_n])
        
        if delta_n < tol:
            return x1, it, (time.time() - start_time)*1000, history, columns, convergence_warning
        
        prev_x = x1
        x0 = x1
    
    return x1, max_iter, (time.time() - start_time)*1000, history, columns, convergence_warning

