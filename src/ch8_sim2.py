import numpy as np

def potential_with_asymmetry(a, Q, alpha):
    """
    Π(a, α) calculation with linear tilt representing geometric imperfection.
    """
    u_symmetric = 0.5*(a**2) + 0.5*(Q**2) * ((1 - a/Q)**2 - 1)**2
    return u_symmetric - alpha * a

def calculate_barrier_height(Q, alpha):
    """
    Determines the energy barrier between wells.
    Returns (E_barrier, num_minima)
    """
    a_space = np.linspace(-Q, 2.5*Q, 1000)
    energies = potential_with_asymmetry(a_space, Q, alpha)
    
    # Identify local minima
    minima_indices = (np.diff(np.sign(np.diff(energies))) > 0).nonzero()[0] + 1
    maxima_indices = (np.diff(np.sign(np.diff(energies))) < 0).nonzero()[0] + 1
    
    if len(minima_indices) < 2:
        return 0.0, len(minima_indices)
    
    # Find the peak between the first two minima
    relevant_maxima = [idx for idx in maxima_indices if minima_indices[0] < idx < minima_indices[1]]
    if not relevant_maxima:
        return 0.0, len(minima_indices)
    
    e_min_1 = energies[minima_indices[0]]
    e_min_2 = energies[minima_indices[1]]
    e_peak = energies[relevant_maxima[0]]
    
    return min(e_peak - e_min_1, e_peak - e_min_2), len(minima_indices)

def main():
    Q = 4.0
    print(f"--- Imperfection Sensitivity Analysis (Q = {Q}) ---")
    print(f"{'Alpha (Tilt)':<12} | {'Barrier Height ΔE':<20} | {'Stability'}")
    print("-"*60)
    
    alphas = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]
    for a in alphas:
        delta_e, count = calculate_barrier_height(Q, a)
        state = "Bistable" if count == 2 else "Monostable (SWALLOWED)"
        print(f"{a:<12.1f} | {delta_e:<20.4f} | {state}")

    # Numerical Assertion: For Q=4, alpha=3 should swallow the well
    _, count_high = calculate_barrier_height(4.0, 3.0)
    assert count_high == 1, "Error: High asymmetry should reduce the system to monostability"

if __name__ == '__main__':
    main()