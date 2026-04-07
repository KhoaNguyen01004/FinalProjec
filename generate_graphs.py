import matplotlib.pyplot as plt
import numpy as np
from algorithms import bisection_method, secant_method, newton_raphson_method, fixed_point_iteration
from utils import npv

cash_flows = [-2000, 400, 600, 800, 800, 1200]

# Generate data
data = {}
bis_root, _, _, bis_hist, bis_cols = bisection_method(cash_flows, max_iter=25)
sec_root, _, _, sec_hist, sec_cols = secant_method(cash_flows, max_iter=10)
new_root, _, _, new_hist, new_cols = newton_raphson_method(cash_flows, max_iter=10)
fix_root, _, _, fix_hist, fix_cols, _ = fixed_point_iteration(cash_flows, max_iter=10)

# Extract deltas (last column)
bis_deltas = [row[-1] for row in bis_hist[1:]]  # skip header row [0,a,b,None,None,delta]
sec_deltas = [row[-1] for row in sec_hist]
new_deltas = [row[-1] for row in new_hist]
fix_deltas = [row[-1] for row in fix_hist]

bis_n = list(range(1, len(bis_deltas)+1))
sec_n = list(range(1, len(sec_deltas)+1))
new_n = list(range(1, len(new_deltas)+1))
fix_n = list(range(1, len(fix_deltas)+1))

# Convergence plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.semilogy(bis_n, bis_deltas, 'o-', label='Bisection', linewidth=2, markersize=6)
ax.semilogy(sec_n, sec_deltas, 's-', label='Secant', linewidth=2, markersize=6)
ax.semilogy(new_n, new_deltas, '^-', label='Newton', linewidth=2, markersize=6)
ax.semilogy(fix_n, fix_deltas, 'd-', label='Fixed-pt', linewidth=2, markersize=6)
ax.set_xlabel('Iterations (n)')
ax.set_ylabel('log|Δ_n|')
ax.set_title('Đồ Thị Hội Tụ (IRR ≈ 0.2154)')
ax.grid(True, alpha=0.3)
ax.legend()
plt.savefig('images/convergence.png', dpi=300, bbox_inches='tight')
plt.close()

# NPV graph (matching ASCII 2.4)
r = np.linspace(0, 1, 200)
npv_vals = [npv(ri, cash_flows) for ri in r]
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(r, npv_vals, 'b-', linewidth=2, label='NPV(r)')
ax2.axhline(0, color='r', linestyle='--', alpha=0.7)
ax2.axvline(0.2154, color='g', linestyle='--', label='IRR ≈ 0.2154')
ax2.set_xlabel('Lãi suất r')
ax2.set_ylabel('NPV (triệu VNĐ)')
ax2.set_title('Đồ Thị NPV với Điểm IRR')
ax2.grid(True, alpha=0.3)
ax2.legend()
plt.savefig('images/npv.png', dpi=300, bbox_inches='tight')
plt.close()

print('Graphs saved: images/convergence.png, images/npv.png')
