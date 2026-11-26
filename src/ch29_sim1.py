import numpy as np
import matplotlib.pyplot as plt

def simulate_tidal_reset():
    """
    Simulates the potential energy landscape of a mechanical bit under varying hydrostatic pressure.
    We use the governing equation V(x) = ax^4 - bx^2 + gamma * sigma * x^2.
    """
    # Parameters
    a = 1.0
    b = 2.0
    gamma = 0.5
    x = np.linspace(-2.0, 2.0, 400)

    # Tidal pressure regimes (MPa)
    pressures = [0.0, 2.0, 4.0, 6.0]
    
    results = {}

    for sigma in pressures:
        # V(x) = ax^4 + (gamma*sigma - b)x^2
        effective_stiffness = gamma * sigma - b
        v_x = a * x**4 + effective_stiffness * x**2
        
        # Find local minima indices
        minima_indices = (np.diff(np.sign(np.diff(v_x))) > 0).nonzero()[0] + 1
        num_wells = len(minima_indices)
        
        results[sigma] = {
            "potential": v_x,
            "num_wells": num_wells,
            "effective_stiffness": effective_stiffness
        }

        # Verification: At high sigma, the system MUST become monostable
        if sigma > 5.0:
            assert num_wells == 1, f"Expected monostability at {sigma} MPa, found {num_wells} wells."

    print("--- Hadal Resilience Report ---")
    for sigma, data in results.items():
        state = "Bistable (Memory Active)" if data["num_wells"] > 1 else "Monostable (Reset State)"
        print(f"Pressure: {sigma} MPa | K_eff: {data['effective_stiffness']:>6.2f} | Logic: {state}")

    return results

if __name__ == "__main__":
    simulate_tidal_reset()