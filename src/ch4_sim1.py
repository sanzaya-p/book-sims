import numpy as np

def calculate_stiffness_scaling(connectivity_z, relative_density):
    """
    Calculates the effective Young's modulus scaling for a lattice.
    
    Parameters:
    connectivity_z (float): Average number of struts per joint.
    relative_density (float): Volume fraction of the material.
    
    Returns:
    dict: Scaling exponents and effective stiffness.
    """
    # Zc is the critical connectivity for 2D (Zc=4) or 3D (Zc=6/12 depends on joints)
    # For this model, we use Zc = 6 as the threshold for 3D stretching-dominated behavior
    Zc = 6.0
    
    if connectivity_z >= Zc:
        # Stretching dominated: E ~ rho^1
        n = 1.0
        mode = "Stretching-Dominated"
    else:
        # Bending dominated: E ~ rho^3 (lower bound) or rho^2
        # We model the transition smoothly based on Gibson-Ashby phenomenology
        n = 1.0 + 2.0 * (1.0 - (connectivity_z / Zc))
        mode = "Bending-Dominated"
        
    e_eff = (relative_density ** n)
    
    return {
        "mode": mode,
        "exponent": round(n, 2),
        "e_eff": round(e_eff, 6)
    }

def main():
    """
    Verifies the transition from bending to stretching dominated regimes.
    """
    densities = [0.01, 0.05, 0.1]
    connectivities = [3.0, 4.0, 6.0, 8.0]
    
    print(f"{'Z':<5} | {'rho':<5} | {'Exponent':<10} | {'E_eff':<10} | {'Regime'}")
    print("-"*60)
    
    for z in connectivities:
        for rho in densities:
            res = calculate_stiffness_scaling(z, rho)
            print(f"{z:<5} | {rho:<5} | {res['exponent']:<10} | {res['e_eff']:<10} | {res['mode']}")

    # Verification check: Is Stretching dominated stiffer than bending at low density?
    bend = calculate_stiffness_scaling(3.0, 0.01)['e_eff']
    stretch = calculate_stiffness_scaling(6.0, 0.01)['e_eff']
    assert stretch > bend, "Stretching dominated lattices must be stiffer at low densities."
    print("\nVerification Successful: Stretching-dominated efficiency confirmed.")

if __name__ == '__main__':
    main()