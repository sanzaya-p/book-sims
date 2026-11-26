import numpy as np

def simulate_thermal_breakdown(freq_hz=1000, duration_s=10.0):
    """
    Predicts the temperature rise and logic stability in a mechanical computer.
    Uses Equation E3: Delta T_rate = (A_hys * f) / (rho * Cp).
    Models material softening: E(T) = E0 * (1 - alpha * (T - T_amb)).
    """
    # Material Constants (Typical engineering polymer)
    rho = 1200  # kg/m^3
    cp = 1500   # J/(kg*K)
    t_amb = 293 # K
    a_hys = 0.05 # J/m^3 per cycle (Hysteresis loss energy density)
    alpha = 0.005 # Stiffness reduction coefficient per Kelvin
    h_coeff = 10.0 # Convective heat transfer coefficient (W/m^2*K)
    l_char = 1e-4 # Characteristic length of the beam (m)
    
    # Time-stepping thermal model
    dt = 0.1 # seconds
    steps = int(duration_s / dt)
    t_curr = t_amb
    stiffness_ratio = 1.0
    history = []

    for i in range(steps):
        # Heat generated per unit volume per second: a_hys * f
        q_gen = a_hys * freq_hz
        # Newton's law of cooling: Heat lost approx q_loss = h * (T - T_amb) / l_char
        q_loss = h_coeff * (t_curr - t_amb) / l_char
        
        # Energy balance: rho * cp * dT/dt = q_gen - q_loss
        dtdt = (q_gen - q_loss) / (rho * cp)
        t_curr += dtdt * dt
        
        # Update material stiffness (determines potential well depth)
        stiffness_ratio = max(0.0, 1.0 - alpha * (t_curr - t_amb))
        
        history.append(t_curr)
        
        # Failure condition: If stiffness drops below 30%, bit-stability is lost
        if stiffness_ratio < 0.3:
            return {
                "status": "FAILURE: Thermal Meltdown",
                "time_to_fail": i * dt,
                "final_temp": round(t_curr, 2),
                "stiffness_rem": round(stiffness_ratio, 2)
            }
            
    return {
        "status": "STABLE",
        "time_to_fail": None,
        "final_temp": round(t_curr, 2),
        "stiffness_rem": round(stiffness_ratio, 2)
    }

def main():
    print("--- Thermal Feedback in Viscoelastic Logic ---")
    
    # Test 1: Low frequency operation (100 Hz)
    res1 = simulate_thermal_breakdown(freq_hz=100)
    print(f"100 Hz: Status={res1['status']}, Temp={res1['final_temp']}K")
    
    # Test 2: High frequency operation (50 kHz)
    res2 = simulate_thermal_breakdown(freq_hz=50000)
    print(f"50 kHz: Status={res2['status']}, FailTime={res2['time_to_fail']}s, Temp={res2['final_temp']}K")

    # Numerical Assertion
    assert res1['status'] == "STABLE", "Low frequency should be thermally stable."
    assert res2['final_temp'] > res1['final_temp'], "Higher frequency must generate more heat."

if __name__ == "__main__":
    main()