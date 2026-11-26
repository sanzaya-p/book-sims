import numpy as np
import matplotlib.pyplot as plt

def simulate_poroelastic_delay(L_values, D=1e-7):
    """
    Calculates the poroelastic time constant tau = L^2 / D.
    L: Characteristic length (m)
    D: Hydraulic diffusivity (m^2/s)
    """
    return (np.array(L_values)**2) / D

def solve_diffusion_profile(L, D, total_time, steps=100):
    """
    Solves a 1D diffusion equation representing turgor pressure equalization.
    P_t = D * P_xx
    """
    dx = L / 20
    dt = 0.5 * dx**2 / D * 0.9 # Stability condition
    x = np.linspace(0, L, 21)
    P = np.zeros_like(x)
    P[0] = 1.0 # Applied pressure at boundary
    
    times = [0, total_time * 0.1, total_time * 0.5, total_time]
    profiles = []
    
    curr_t = 0
    for t_target in times:
        while curr_t < t_target:
            P[1:-1] += D * dt / dx**2 * (P[2:] - 2*P[1:-1] + P[:-2])
            curr_t += dt
        profiles.append(P.copy())
    return x, profiles

def main():
    # Realistic biological parameters
    # D for plant tissue is typically 10^-8 to 10^-7 m^2/s
    D_cell = 1e-7 
    L_leaf = 0.005 # 5mm thickness
    
    tau_expected = simulate_poroelastic_delay([L_leaf], D_cell)[0]
    
    print(f"--- Poroelastic Limit Analysis ---")
    print(f"Tissue Thickness (L): {L_leaf*1000:.2f} mm")
    print(f"Hydraulic Diffusivity (D): {D_cell} m^2/s")
    print(f"Theoretical Time Constant (tau): {tau_expected:.2f} seconds")
    print(f"Flytrap Observed Snap Time: ~0.10 seconds")
    print(f"Speed Enhancement Factor: {tau_expected / 0.1:.1f}x")
    
    # Verification of scaling
    L_test = np.array([0.001, 0.002, 0.004])
    tau_test = simulate_poroelastic_delay(L_test, D_cell)
    # Check quadratic scaling: tau(2L) should be 4*tau(L)
    np.testing.assert_allclose(tau_test[1]/tau_test[0], 4.0, rtol=0.01)
    print("\nNumerical Verification: Quadratic scaling L^2/D confirmed.")

if __name__ == '__main__':
    main()