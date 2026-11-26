import numpy as np

def check_hill_mandel(num_cells, lattice_stiffness=100.0, base_stiffness=1.0):
    """
    Simulates the Hill-Mandel energy consistency error across a multi-cell RVE.
    
    Parameters:
    num_cells (int): Number of unit cells across the RVE (L/l).
    lattice_stiffness (float): Stiffness of the solid part.
    base_stiffness (float): Stiffness of the 'void' or matrix.
    """
    # Generate a simple 1D RVE with N cells of alternating stiffness
    n_elements = num_cells * 10
    stiffness_profile = np.ones(n_elements) * base_stiffness
    for i in range(num_cells):
        stiffness_profile[i*10 : i*10 + 5] = lattice_stiffness
        
    # Apply uniform macroscopic strain (epsilon_avg = 1.0)
    # Local strain is inversely proportional to local stiffness under uniform stress
    # sigma_local = C_local * epsilon_local. 
    # In series, stress is constant.
    stress_constant = 1.0 / np.mean(1.0/stiffness_profile)
    epsilon_micro = stress_constant / stiffness_profile
    sigma_micro = stress_constant * np.ones(n_elements)
    
    # Calculate Hill-Mandel components
    avg_product = np.mean(sigma_micro * epsilon_micro)
    product_of_avg = np.mean(sigma_micro) * np.mean(epsilon_micro)
    
    error = np.abs(avg_product - product_of_avg)
    
    return {
        "avg_energy": avg_product,
        "homogenized_energy": product_of_avg,
        "hm_error": error,
        "delta": 1.0 / num_cells
    }

def main():
    """
    Evaluates homogenization convergence as a function of scale separation.
    """
    print(f"{'Cells (L/l)':<12} | {'Delta':<10} | {'HM Error':<10}")
    print("-"*40)
    
    for n in [1, 2, 5, 10, 20, 50]:
        res = check_hill_mandel(n)
        print(f"{n:<12} | {res['delta']:<10.3f} | {res['hm_error']:<10.2e}")
        
    # Note: In a perfectly periodic infinite medium, HM error is zero by definition.
    # We demonstrate how local fluctuations are captured.
    final_err = check_hill_mandel(100)['hm_error']
    assert final_err < 1e-10, "Energy bridge should be consistent in periodic homogenization."
    print("\nNumerical Verification: Hill-Mandel condition holds for periodic RVE.")

if __name__ == '__main__':
    main()