import numpy as np
import math

def simulate_logic_snap(a, b, L, D, glucose_concentration, time_steps=500):
    """
    Simulates the interaction between slow chemical diffusion (hydrogel swelling)
    and the fast nonlinear snap-through of a mechanical logic bit.
    
    Parameters:
    a (float): Quadratic coefficient (negative for bistability)
    b (float): Quartic coefficient (must be positive for stability)
    L (float): Hydrogel thickness (mm)
    D (float): Diffusion coefficient (mm^2/s)
    glucose_concentration (float): External chemical signal intensity
    """
    # Time constant for diffusion
    tau = (L**2) / D
    
    # Displacement domain
    x = np.linspace(-2.0, 2.0, 1000)
    
    # Evolution of chemical bias force F_chem over time
    # F_chem follows a first-order saturation based on tau
    time_domain = np.linspace(0, 5 * tau, time_steps)
    f_chem_t = glucose_concentration * (1 - np.exp(-time_domain / tau))
    
    results = []
    for t_idx, F_ext in enumerate(f_chem_t):
        # Potential Energy V(x) = ax^2 + bx^4 + F_ext * x
        V = a * x**2 + b * x**4 - F_ext * x
        
        # Find local minima (stable states)
        # A state 'snaps' when the current local minimum disappears
        grad = 2*a*x + 4*b*x**3 - F_ext
        roots = x[np.where(np.diff(np.sign(grad)))[0]]
        
        results.append({
            'time': time_domain[t_idx],
            'bias': F_ext,
            'num_stable_states': len(roots) // 2 + 1,
            'minima_locations': roots.tolist()
        })
        
    # Verification: Logic bit must start bistable if a < 0
    if a < 0:
        assert results[0]['num_stable_states'] >= 2, "Initial state must be bistable."
    
    return results, tau

def main():
    # Physical parameters for a sub-millimeter glucose-responsive gate
    a_coeff = -5.0
    b_coeff = 2.0
    gel_thickness = 0.5 # mm
    diff_coeff = 0.001 # mm^2/s (typical for large molecules in hydrogels)
    signal = 8.0
    
    data, tau = simulate_logic_snap(a_coeff, b_coeff, gel_thickness, diff_coeff, signal)
    
    print(f"--- Logic Snap Simulation Summary ---")
    print(f"Calculated Diffusion Time Constant (tau): {tau:.2f} seconds")
    
    # Find the snap time (when state count drops from 2 to 1)
    snap_time = next((r['time'] for r in data if r['num_stable_states'] < 2), None)
    
    if snap_time:
        print(f"Bifurcation Triggered at: {snap_time:.2f} seconds")
        print(f"Snap Delay Ratio (snap_time / tau): {snap_time/tau:.2f}")
    else:
        print("No snap occurred: Bias force insufficient to overcome energy barrier.")

if __name__ == '__main__':
    main()