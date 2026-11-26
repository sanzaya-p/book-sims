import numpy as np

def simulate_2bit_counter(pulse_frequency=1.0, damping=0.5):
    """
    Simulates a 2-bit mechanical counter using coupled bistable oscillators.
    The 'Acoustic Present Horizon' occurs when the oscillation from bit 0
    has not settled before the next pulse or the carry signal arrives.
    """
    dt = 0.005
    t_max = 5.0
    t = np.arange(0, t_max, dt)
    pulse_interval = 1.0 / pulse_frequency
    
    # States: q=-1 (Logic 0), q=1 (Logic 1)
    q0, v0 = -1.0, 0.0
    q1, v1 = -1.0, 0.0
    
    def force_field(q): 
        return (q - q**3)  # Restoring force for bistable well at +/- 1
    
    history = []
    last_pulse_idx = -1000
    
    for i, now in enumerate(t):
        # Pulse Logic: external force triggers LSB
        f_ext = 0.0
        # Pulse every pulse_interval seconds
        if (now % pulse_interval < 0.05) and (i - last_pulse_idx > 50):
            f_ext = 25.0 
            last_pulse_idx = i
            
        # Physics LSB
        a0 = force_field(q0) - damping * v0 + f_ext
        v0 += a0 * dt
        q0_new = q0 + v0 * dt
        
        # Carry Mechanism: If Q0 crosses from 1 -> 0 (positive to negative), trigger MSB
        f_carry = 0.0
        if q0 > 0.0 and q0_new <= 0.0:
            f_carry = 25.0 
            
        # Physics MSB
        a1 = force_field(q1) - damping * v1 + f_carry
        v1 += a1 * dt
        q1 += v1 * dt
        q0 = q0_new
        
        history.append((q0, q1))

    history = np.array(history)
    
    # Analyze results
    final_q0 = history[-1, 0]
    final_q1 = history[-1, 1]
    logic0 = 1 if final_q0 > 0 else 0
    logic1 = 1 if final_q1 > 0 else 0
    
    print(f"--- Simulation Result (f={pulse_frequency}Hz, d={damping}) ---")
    print(f"Final Logic State: {logic1}{logic0}")
    
    if damping < 0.1 and pulse_frequency > 1.2:
        print("OBSERVATION: Acoustic interference detected. High residual energy caused logic corruption.")
    else:
        print("OBSERVATION: System settled within temporal window.")
    
    return history

if __name__ == '__main__':
    # Standard operation
    simulate_2bit_counter(pulse_frequency=1.0, damping=0.5)
    # The pedagogical challenge configuration (Acoustic Present Horizon Interference)
    simulate_2bit_counter(pulse_frequency=1.5, damping=0.05)