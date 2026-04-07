"""
Utility functions for NPV calculation and derivatives.
File: utils.py
"""

import numpy as np


def npv(r, cash_flows):
    """
    Calculate Net Present Value at discount rate r.
    
    Parameters:
    -----------
    r : float
        Discount rate (e.g., 0.1 for 10%)
    cash_flows : list or array
        Array of cash flows [C0, C1, C2, ..., Cn]
    
    Returns:
    --------
    float
        NPV(r) = C0 + C1/(1+r) + C2/(1+r)^2 + ... + Cn/(1+r)^n
    """
    if abs(1 + r) < 1e-10:  # Handle r = -1 (division by zero)
        return float('inf') if cash_flows[0] > 0 else float('-inf')
    
    return cash_flows[0] + sum(c / (1 + r)**i for i, c in enumerate(cash_flows[1:], 1))


def npv_derivative(r, cash_flows):
    """
    Calculate the first derivative of NPV with respect to r.
    
    This is used in Newton-Raphson method.
    
    Parameters:
    -----------
    r : float
        Discount rate
    cash_flows : list or array
        Array of cash flows
    
    Returns:
    --------
    float
        f'(r) = -sum(i * C_i / (1+r)^(i+1)) for i=1 to n
    """
    if abs(1 + r) < 1e-10:  # Handle r = -1 (division by zero)
        return float('inf') if cash_flows[1] > 0 else float('-inf')
    
    return sum(-i * c / (1 + r)**(i+1) for i, c in enumerate(cash_flows[1:], 1))


def npv_second_derivative(r, cash_flows):
    """
    Calculate the second derivative of NPV with respect to r.
    
    This is used in Fixed-point iteration to check convergence condition.
    
    Parameters:
    -----------
    r : float
        Discount rate
    cash_flows : list or array
        Array of cash flows
    
    Returns:
    --------
    float
        f''(r) = -sum(i*(i+1) * C_i / (1+r)^(i+2)) for i=1 to n
    """
    if abs(1 + r) < 1e-10:  # Handle r = -1 (division by zero)
        return float('inf') if cash_flows[1] > 0 else float('-inf')
    
    return -sum(i * (i + 1) * c / (1 + r)**(i + 2) for i, c in enumerate(cash_flows[1:], 1))


def check_root_existence(cash_flows, a=0, b=1):
    """
    Check if a root exists in the interval [a, b] using Bolzano's theorem.
    
    Parameters:
    -----------
    cash_flows : list or array
        Array of cash flows
    a, b : float
        Endpoints of the interval
    
    Returns:
    --------
    bool
        True if f(a) * f(b) < 0, indicating a root exists in [a, b]
    """
    fa = npv(a, cash_flows)
    fb = npv(b, cash_flows)
    return fa * fb < 0


def find_root_interval(cash_flows, max_range=100):
    """
    Automatically find an interval [a, b] where a root exists.
    
    Parameters:
    -----------
    cash_flows : list or array
        Array of cash flows
    max_range : float
        Maximum range to search (default 100, meaning -100 to 100%)
    
    Returns:
    --------
    tuple : (a, b, found)
        a, b: interval where root exists
        found: True if root exists, False otherwise
    """
    # Test points from positive to negative, prioritize positive roots
    test_points = [0, 0.01, 0.1, 0.5, 1, 2, 5, 10, 20, 50, 100, -0.1, -0.5, -1, -2, -5, -10, -20, -50, -100]
    
    for i in range(len(test_points) - 1):
        fa = npv(test_points[i], cash_flows)
        fb = npv(test_points[i + 1], cash_flows)
        
        if fa * fb < 0:
            return test_points[i], test_points[i + 1], True
    
    # No root found in extended range
    return -1, 1, False


def count_sign_changes(cash_flows):
    """
    Count the number of sign changes in the cash flow sequence.
    
    Parameters:
    -----------
    cash_flows : list or array
        Array of cash flows
    
    Returns:
    --------
    int
        Number of times consecutive cash flows have opposite signs
    """
    return sum(1 for i in range(1, len(cash_flows)) if cash_flows[i-1] * cash_flows[i] < 0)


def parse_cash_flow(input_str: str) -> list[float]:
    """
    Robustly parse comma-separated cash flows, handling thousands separators.
    
    Supports:
    - Standard: "-2000, 400, 600"
    - Formatted commas: "-2,000, 400, 600"
    - Vietnamese dots: "-2.000, 400, 600" 
    - Mixed/whitespace tolerant
    
    Parameters:
    -----------
    input_str : str
        User input string
    
    Returns:
    --------
    list[float]
        Parsed cash flows
    
    Raises:
    -------
    ValueError: If parsing fails
    """
    if not input_str or input_str.strip() == "":
        raise ValueError("Empty input")
    
    # Normalize: replace thousands separators . or space with nothing, change ; to , for splitting
    normalized = input_str.replace('.', '').replace(' ', ';').replace(';', ',')
    
    # Split on top-level commas
    parts = [part.strip() for part in normalized.split(',') if part.strip()]
    
    try:
        cash_flows = [float(part) for part in parts]
        if len(cash_flows) < 2:
            raise ValueError("At least 2 cash flows required")
        return cash_flows
    except ValueError as e:
        raise ValueError(f"Invalid number format: {input_str}") from e


def format_cash_flow(cash_flows: list[float]) -> str:
    """
    Format cash flows as comma-separated string with dot thousands separators (Vietnamese style).
    
    Parameters:
    -----------
    cash_flows : list[float]
        Cash flows
    
    Returns:
    --------
    str
        Formatted string e.g. "-2.000, 400, 600"
    """
    def format_number(n):
        s = f"{abs(n):.0f}"
        # Insert dots every 3 digits from right
        s = ','.join([s[max(0, i-3):i] for i in range(len(s), 0, -3)][::-1])
        return '-' + s if n < 0 else s
    return ', '.join(format_number(cf) for cf in cash_flows)


def find_min_derivative(r_values, cash_flows):
    """
    Find the minimum absolute value of f'(r) in the interval.
    Used for Newton-Raphson error estimation: |x_n - x*| <= |f(x_n)| / m1
    
    Parameters:
    r_values : array
        Values where to evaluate f'(r)
    cash_flows : list or array
        Array of cash flows
    
    Returns:
    float
        Minimum |f'(r)| value (m1)
    """
    derivatives = [abs(npv_derivative(r, cash_flows)) for r in r_values]
    return min(derivatives) if derivatives else 1.0


def check_fourier_condition(r, cash_flows):
    """
    Check Fourier condition for Newton-Raphson: f(x0) * f''(x0) > 0
    This ensures monotone convergence to the root.
    
    Parameters:
    -----------
    r : float
        Initial point
    cash_flows : list or array
        Array of cash flows
    
    Returns:
    --------
    bool
        True if Fourier condition is satisfied
    """
    f = npv(r, cash_flows)
    f_double_prime = npv_second_derivative(r, cash_flows)
    return f * f_double_prime > 0


def find_max_second_derivative(r_values, cash_flows):
    """
    Find the maximum absolute value of f''(r) in the interval.
    Used for Newton-Raphson error estimation.
    
    Parameters:
    r_values : array
        Values where to evaluate f''(r)
    cash_flows : list or array
        Array of cash flows
    
    Returns:
    float
        Maximum |f''(r)| value (M)
    """
    second_derivatives = [abs(npv_second_derivative(r, cash_flows)) for r in r_values]
    return max(second_derivatives) if second_derivatives else 1.0


def find_max_g_prime(r_values, cash_flows):
    """
    Find the maximum absolute value of g'(r) in the interval.
    Used for Fixed-point iteration convergence check.
    
    Parameters:
    r_values : array
        Values where to evaluate g'(r)
    cash_flows : list or array
        Array of cash flows
    
    Returns:
    float
        Maximum |g'(r)| value (q)
    """
    g_primes = []
    for r in r_values:
        f = npv(r, cash_flows)
        f_prime = npv_derivative(r, cash_flows)
        f_second = npv_second_derivative(r, cash_flows)
        if abs(f_prime) > 1e-10:
            g_prime = 1 - (f_prime**2 - f * f_second) / (f_prime ** 2)
            g_primes.append(abs(g_prime))
    return max(g_primes) if g_primes else 1.0
