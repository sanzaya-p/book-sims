import numpy as np

def simulate_logic_gate_yield(nominal_h=0.6, nominal_d=1.5, sigma=0.04, bias=0.0, n_samples=10000):
    """
    Simulates a population of compliant logic gates subject to manufacturing variability.
    
    Parameters:
    nominal_h (float): Nominal beam thickness [mm]
    nominal_d (float): Nominal pre-compression/displacement [mm]
    sigma (float): Standard deviation of the thickness variation [mm]
    bias (float): Systematic process bias (e.g., over-extrusion) [mm]
    n_samples (int): Population size for Monte Carlo
    """
    # Critical threshold for bistability in first-mode buckling
    Q_CRITICAL = 2.31
    
    # Generate stochastic thickness population
    h_population = np.random.normal(nominal_h + bias, sigma, n_samples)
    # Thickness cannot be negative
    h_population = np.clip(h_population, 0.01, None)
    
    # Calculate Q-factor for each individual
    q_population = nominal_d / h_population
    
    # Identify functional vs failed (monostable)
    is_functional = q_population >= Q_CRITICAL
    yield_rate = np.mean(is_functional) * 100
    
    # Calculate stiffness variation (K proportional to h^3)
    # Nominal stiffness factor
    k_nominal = nominal_h**3
    k_population = h_population**3
    k_mean = np.mean(k_population)
    k_std = np.std(k_population)
    
    stats = {
        "yield_percent": yield_rate,
        "q_mean": np.mean(q_population),
        "q_std": np.std(q_population),
        "k_variation_pct": (k_std / k_nominal) * 100,
        "k_bias_error_pct": ((k_mean - k_nominal) / k_nominal) * 100
    }
    return stats

def main():
    print("--- CH23 SIM 1: MONTE CARLO YIELD ANALYSIS ---")
    
    # Scenario A: Centered distribution
    res_a = simulate_logic_gate_yield(bias=0.0, sigma=0.05)
    print(f"[Nominal Case] Yield: {res_a['yield_percent']:.2f}% | Stiffness Bias: {res_a['k_bias_error_pct']:.2f}%")
    
    # Scenario B: Small systematic under-extrusion (-0.05mm)
    res_b = simulate_logic_gate_yield(bias=-0.05, sigma=0.05)
    print(f"[Biased Case]  Yield: {res_b['yield_percent']:.2f}% | Stiffness Bias: {res_b['k_bias_error_pct']:.2f}%")
    
    # Verification of Cubic sensitivity
    # If h changes by 10%, K changes by ~(1.1)^3 - 1 = 33%
    h1, h2 = 0.6, 0.66
    k_delta = (h2**3 - h1**3) / h1**3
    assert abs(k_delta - 0.331) < 0.001, "Cubic sensitivity check failed"
    print("\nNumerical Verification: Power-law sensitivity confirmed.")

if __name__ == '__main__':
    main()