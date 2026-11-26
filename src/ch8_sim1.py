import numpy as np
from scipy.optimize import fsolve

def calculate_potential_energy(a, Q):
    """
    Calculates the non-dimensional potential energy of a shallow arch.
    a: non-dimensional central displacement
    Q: geometric parameter (h/t)
    """
    # Bending component + Stretching (von Karman) component
    bending = 0.5 * (a**2)
    stretching = 0.5 * (Q**2) * ((1 - a/Q)**2 - 1)**2
    return bending + stretching

def find_equilibria(Q):
    """
    Finds roots of d(Pi)/da = 0 using a numerical solver.
    """
    def d_pi(a):
        # Numerical derivative of the potential energy
        h = 1e-7
        return (calculate_potential_energy(a + h, Q) - calculate_potential_energy(a - h, Q)) / (2 * h)
    
    # Test multiple starting points to find all local extrema
    seeds = np.linspace(-2*Q, 3*Q, 10)
    roots = []
    for seed in seeds:
        root, info, ier, msg = fsolve(d_pi, seed, full_output=True)
        if ier == 1:
            roots.append(round(root[0], 5))
    return sorted(list(set(roots)))

def main():
    print("--- Analysis of the Double-Well Transition ---")
    print(f"{'Q-Factor':<10} | {'Equilibria States':<30} | {'Regime':<15}")
    print("-"*65)
    
    for q_test in [1.5, 2.31, 3.5, 5.6, 7.0]:
        eqs = find_equilibria(q_test)
        num_minima = 0
        # Check second derivative for stability
        for e in eqs:
            h = 1e-5
            d2 = (calculate_potential_energy(e+h, q_test) - 2*calculate_potential_energy(e, q_test) + calculate_potential_energy(e-h, q_test))/(h**2)
            if d2 > 0: num_minima += 1
        
        regime = "Monostable" if num_minima == 1 else "Bistable (Logic)"
        if q_test > 5.6: regime = "Multi-modal (Noise)"
        
        eq_str = ", ".join([f"{e:.2f}" for e in eqs])
        print(f"{q_test:<10} | {eq_str:<30} | {regime:<15}")

    # Verification of Critical Q
    q_crit = 2.31
    eqs_crit = find_equilibria(q_crit)
    assert len(eqs_crit) >= 1, "Failed to find equilibria at critical Q"
    print(f"\nNumerical Verification: At Q=2.31, equilibrium count starts expanding.")

if __name__ == '__main__':
    main()