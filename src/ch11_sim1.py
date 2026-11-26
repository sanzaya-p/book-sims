import numpy as np
from scipy.integrate import solve_ivp

def simulate_sls_logic_gate(viscosity_eta=0.5, spring_k1=1.0, spring_k2=2.0, mass=0.1, duration=20.0):
    """
    Simulates a bistable beam using the Standard Linear Solid (SLS) model.
    The SLS model is represented as a spring (k1) in parallel with a 
    Maxwell arm (spring k2 and dashpot eta).
    
    Governing ODEs:
    1) m*v' = -dV/dx - k1*x - z + F_ext
    2) z' = k2*v - (k2/eta)*z
    where z is the force in the Maxwell arm and V(x) is a quartic bistable potential.
    """
    # Bistable Potential V(x) = 0.25*x^4 - 0.5*x^2
    # dV/dx = x^3 - x
    
    def system(t, state):
        x, v, z = state
        # External trigger pulse: apply force to push from -1 to 1 for t in [1, 2]
        f_ext = 0.8 if 1.0 <= t <= 2.5 else 0.0
        
        dvdt = (f_ext - (x**3 - x) - spring_k1*x - z) / mass
        dzdt = spring_k2 * v - (spring_k2 / viscosity_eta) * z
        return [v, dvdt, dzdt]

    # Initial state: Resting in the left well (approx x = -1)
    y0 = [-1.0, 0.0, 0.0]
    t_span = (0, duration)
    t_eval = np.linspace(0, duration, 1000)
    
    sol = solve_ivp(system, t_span, y0, t_eval=t_eval, method='RK45')
    
    # Metrics
    final_pos = sol.y[0][-1]
    settling_time = "N/A"
    successful_snap = final_pos > 0.5
    
    if successful_snap:
        # Find first time it crosses 0.9 and stays within 1.0 +/- 0.05
        within_tol = np.where(np.abs(sol.y[0] - 1.0) < 0.05)[0]
        if len(within_tol) > 0:
            settling_time = round(sol.t[within_tol[0]], 3)

    return {
        "success": successful_snap,
        "final_position": round(final_pos, 4),
        "settling_time": settling_time,
        "max_overshoot": round(np.max(sol.y[0]), 4)
    }

def main():
    print("--- SLS Viscoelastic Damping Simulation ---")
    
    # Regime 1: Under-damped (Low Viscosity)
    regime1 = simulate_sls_logic_gate(viscosity_eta=0.05)
    print(f"Low Viscosity (Elastic): Success={regime1['success']}, Settling={regime1['settling_time']}, Max_X={regime1['max_overshoot']}")
    
    # Regime 2: Critical Damping (Optimal Viscosity)
    regime2 = simulate_sls_logic_gate(viscosity_eta=0.6)
    print(f"Medium Viscosity (Logic Sweet Spot): Success={regime2['success']}, Settling={regime2['settling_time']}, Max_X={regime2['max_overshoot']}")
    
    # Regime 3: Over-damped (High Viscosity/Stalling)
    regime3 = simulate_sls_logic_gate(viscosity_eta=5.0)
    print(f"High Viscosity (Stalled): Success={regime3['success']}, Settling={regime3['settling_time']}, Max_X={regime3['max_overshoot']}")

    assert regime2['success'] == True, "Middle regime should succeed in snapping."
    assert regime1['max_overshoot'] > regime2['max_overshoot'], "Lower damping should oscillate more."

if __name__ == "__main__":
    main()