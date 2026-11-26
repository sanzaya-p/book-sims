import numpy as np
from scipy.optimize import minimize_scalar

def simulate_logic_stability():
    """
    Simulates the stability of a mechanical bistable gate under deep-sea pressure.
    The potential energy U(x) = (ax^4 - bx^2) + P * delta_V(x).
    """
    # Constants for a bistable beam (arbitrary logic units)
    a = 1.0
    b = 2.0
    
    # Simulation Parameters
    pressures = np.linspace(0, 150, 10)  # MPa
    delta_v_slope = 0.05  # m^3 per state displacement unit

    print(f"{'Pressure (MPa)':<15} | {'State 0 Energy':<15} | {'State 1 Energy':<15} | {'Stability':<15}")
    print("-" * 65)

    for P in pressures:
        # Define potential function: U(x) = U0(x) + P * delta_V(x)
        # We assume delta_V is linear with x for simplicity: delta_V = slope * x
        def U(x):
            U0 = a * x**4 - b * x**2
            return U0 + P * delta_v_slope * x

        # Find local minima
        res_left = minimize_scalar(U, bounds=(-2, 0), method='bounded')
        res_right = minimize_scalar(U, bounds=(0, 2), method='bounded')

        e_0 = res_left.fun
        e_1 = res_right.fun
        
        # Barrier height (approximate at x=0)
        barrier = U(0) - max(e_0, e_1)
        
        # Determine if gate is still functionally bistable
        # If the energy difference is too high or barrier vanishes, it's unstable
        is_bistable = barrier > 0 and abs(e_0 - e_1) < 2.0
        status = "Bistable" if is_bistable else "Monostable (FAILED)"

        print(f"{P:<15.1f} | {e_0:<15.3f} | {e_1:<15.3f} | {status:<15}")

    # Verification check
    assert U(0) == 0, "Potential origin must be at x=0 for this model."

if __name__ == '__main__':
    simulate_logic_stability()