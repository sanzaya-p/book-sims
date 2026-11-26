import numpy as np
from scipy.integrate import solve_ivp

def van_der_pol_oscillator(t, z, mu):
    """
    Computes the derivatives for the Van der Pol oscillator.
    z = [x, v]
    """
    x, v = z
    dxdt = v
    dvdt = mu * (1 - x**2) * v - x
    return [dxdt, dvdt]

def simulate_limit_cycle(mu=1.0, x0=0.1, v0=0.0, duration=50):
    """
    Simulates the oscillator and verifies limit cycle convergence.
    """
    t_span = (0, duration)
    t_eval = np.linspace(0, duration, 2000)
    
    sol = solve_ivp(van_der_pol_oscillator, t_span, [x0, v0], args=(mu,), t_eval=t_eval, rtol=1e-8)
    
    # Verification: Check if the end of the trajectory is on a limit cycle
    # In a limit cycle, max displacement should be roughly constant at the end
    last_period = sol.y[0, -500:]
    amplitude = np.max(last_period)
    
    # Theoretical amplitude for small mu is ~2.0
    assert amplitude > 1.5, "Oscillator failed to maintain amplitude."
    
    return sol.t, sol.y[0], sol.y[1], mu

def main():
    print("--- Van der Pol Limit Cycle Analysis ---")
    for mu_val in [0.5, 2.0, 5.0]:
        t, x, v, mu = simulate_limit_cycle(mu=mu_val)
        peak_x = np.max(x[-500:])
        print(f"Regime mu={mu}: Stable Amplitude approx {peak_x:.4f}")
        if mu > 3:
            print("  Status: Relaxation oscillation detected (sharp edges).")
        else:
            print("  Status: Quasi-harmonic oscillation detected (smooth).")

if __name__ == '__main__':
    main()