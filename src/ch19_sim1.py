import numpy as np
from scipy.optimize import minimize

class BistableGateSimulator:
    """
    Simulates a mechanical logic gate characterized by a bistable potential energy landscape.
    Provides methods to find logical states (minima) and switching thresholds.
    """
    def __init__(self, k, alpha, f_ext):
        self.k = k
        self.alpha = alpha
        self.f_ext = f_ext

    def potential(self, q):
        """Equation E1: V(q) = 0.5*k*q^2 + 0.25*alpha*q^4 - F*q"""
        return 0.5 * self.k * q**2 + 0.25 * self.alpha * q**4 - self.f_ext * q

    def derivative(self, q):
        """dV/dq = k*q + alpha*q^3 - F"""
        return self.k * q + self.alpha * q**3 - self.f_ext

    def find_equilibria(self):
        """Finds stable logical states (local minima) by searching different basins."""
        equilibria = []
        # Search starting from various initial guesses to capture bistability
        guesses = [-5.0, 0.0, 5.0]
        for g in guesses:
            res = minimize(self.potential, g)
            if res.success:
                q_val = np.round(res.x[0], 6)
                if not any(np.isclose(q_val, e, atol=1e-4) for e in equilibria):
                    # Verify it is a minimum via 2nd derivative
                    if (self.k + 3 * self.alpha * q_val**2) > 0:
                        equilibria.append(q_val)
        return sorted(equilibria)

def main():
    print("--- Mechanical Logic Gate Characterization (m-EDA) ---")
    
    # Regime 1: Symmetric Monostable (High Stiffness)
    g1 = BistableGateSimulator(k=10.0, alpha=1.0, f_ext=0.0)
    eq1 = g1.find_equilibria()
    print(f"Regime 1 (Linear): k=10.0 -> Equilibria at {eq1} (Logic 0 only)")

    # Regime 2: Symmetric Bistable (Buckled)
    g2 = BistableGateSimulator(k=-10.0, alpha=1.0, f_ext=0.0)
    eq2 = g2.find_equilibria()
    print(f"Regime 2 (Bistable): k=-10.0 -> Equilibria at {eq2} (Logic 0, Logic 1)")
    
    # Regime 3: Switching Triggered (High External Force)
    g3 = BistableGateSimulator(k=-10.0, alpha=1.0, f_ext=15.0)
    eq3 = g3.find_equilibria()
    print(f"Regime 3 (Biased): k=-10.0, F=15.0 -> Equilibria at {eq3} (State forced to Logic 1)")

    # Numerical Verification: Threshold of annihilation (Saddle-Node Bifurcation)
    # Critical force for k=-10, alpha=1: F_crit = sqrt(-4k^3/27alpha)
    f_crit = np.sqrt((-4 * (-10.0)**3) / (27 * 1.0))
    print(f"\nTheoretical Switching Threshold F_crit: {f_crit:.4f}")
    
    g_check = BistableGateSimulator(k=-10.0, alpha=1.0, f_ext=f_crit * 0.9)
    print(f"Below Threshold (F={f_crit*0.9:.2f}): {len(g_check.find_equilibria())} stable states found.")
    
    g_check2 = BistableGateSimulator(k=-10.0, alpha=1.0, f_ext=f_crit * 1.1)
    print(f"Above Threshold (F={f_crit*1.1:.2f}): {len(g_check2.find_equilibria())} stable states found.")

if __name__ == '__main__':
    main()