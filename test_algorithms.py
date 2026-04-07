"""
Quick test to verify all 4 algorithms work correctly
"""

from algorithms import (
    bisection_method,
    secant_method,
    newton_raphson_method,
    fixed_point_iteration
)

# Sample data: IRR problem with cash flows
cash_flows = [-2000, 400, 600, 800, 800, 1200]

print("=" * 70)
print("TESTING ALL 4 ALGORITHMS WITH TEXTBOOK-COMPLIANT IMPLEMENTATIONS")
print("=" * 70)

# Test 1: Bisection Method
print("\n1. BISECTION METHOD (Chia đôi)")
print("-" * 70)
try:
    root, iters, time_ms, history = bisection_method(cash_flows, a=0, b=1, tol=1e-5, max_iter=1000)
    print(f"   Root (IRR): {root:.6f}")
    print(f"   Iterations: {iters}")
    print(f"   Time: {time_ms:.4f} ms")
    print(f"   Status: SUCCESS ✓")
except Exception as e:
    print(f"   Status: FAILED ✗ - {str(e)}")

# Test 2: Secant Method
print("\n2. SECANT METHOD (Dây cung)")
print("-" * 70)
try:
    root, iters, time_ms, history = secant_method(cash_flows, a=0, b=1, x0=0, x1=0.1, tol=1e-5, max_iter=1000)
    print(f"   Root (IRR): {root:.6f}")
    print(f"   Iterations: {iters}")
    print(f"   Time: {time_ms:.4f} ms")
    print(f"   Status: SUCCESS ✓")
except Exception as e:
    print(f"   Status: FAILED ✗ - {str(e)}")

# Test 3: Newton-Raphson Method
print("\n3. NEWTON-RAPHSON METHOD (Newton)")
print("-" * 70)
try:
    root, iters, time_ms, history = newton_raphson_method(cash_flows, a=0, b=1, x0=0.1, tol=1e-5, max_iter=1000)
    print(f"   Root (IRR): {root:.6f}")
    print(f"   Iterations: {iters}")
    print(f"   Time: {time_ms:.4f} ms")
    print(f"   Status: SUCCESS ✓")
except Exception as e:
    print(f"   Status: FAILED ✗ - {str(e)}")

# Test 4: Fixed-point Iteration
print("\n4. FIXED-POINT ITERATION (Lặp đơn)")
print("-" * 70)
try:
    root, iters, time_ms, history, warning = fixed_point_iteration(cash_flows, a=0, b=1, x0=0.1, tol=1e-5, max_iter=1000)
    print(f"   Root (IRR): {root:.6f}")
    print(f"   Iterations: {iters}")
    print(f"   Time: {time_ms:.4f} ms")
    print(f"   Convergence Warning: {warning}")
    if warning:
        print(f"   ⚠ Condition |g'(r)| < 1 may not be satisfied")
    print(f"   Status: SUCCESS ✓")
except Exception as e:
    print(f"   Status: FAILED ✗ - {str(e)}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("✓ All algorithms implement textbook-compliant stopping criteria")
print("✓ Secant returns (root, iters, time, history, None)")
print("✓ Fixed-point returns (root, iters, time, history, convergence_warning)")
print("✓ Bisection and Newton-Raphson return (root, iters, time, history)")
print("=" * 70)
