import numpy as np

def simulate_divergence():
    """
    Models the divergence between a physical mechanical state and its digital representation.
    Governing Eq: tau_total = 1/f_s + 1/f_p
    Metric: D(t) = |x_phys(t) - x_dig(t)|
    """
    # Time parameters
    t_end = 1.0
    dt = 0.001
    time = np.arange(0, t_end, dt)
    
    # Mechanical frequency (Hz)
    f_mech = 5.0
    x_phys = np.sin(2 * np.pi * f_mech * time)
    
    # Digital parameters
    f_sample = 50.0  # Hz
    f_proc = 100.0   # Digital processing speed limit (Hz)
    
    # Total Latency tau = 1/f_s + 1/f_p
    tau = (1.0 / f_sample) + (1.0 / f_proc)
    
    # Digital reconstruction (sampled and delayed)
    # We simulate sampling by holding the value and delaying by tau
    x_dig = np.zeros_like(x_phys)
    
    for i, t in enumerate(time):
        sample_time = t - tau
        if sample_time < 0:
            x_dig[i] = 0
        else:
            # Nearest sample point at sampling frequency
            quantized_t = np.floor(sample_time * f_sample) / f_sample
            x_dig[i] = np.sin(2 * np.pi * f_mech * quantized_t)
            
    # Calculate Divergence D(t)
    divergence = np.abs(x_phys - x_dig)
    mean_divergence = np.mean(divergence)
    
    # Verification
    print(f"--- Latency Divergence Audit ---")
    print(f"Mechanical Freq: {f_mech} Hz")
    print(f"Total Digital Latency (tau): {tau*1000:.2f} ms")
    print(f"Mean State Divergence D(t): {mean_divergence:.4f}")
    
    # Logical check: if tau is half the period, divergence should be high
    period_mech = 1.0 / f_mech
    if tau > 0.25 * period_mech:
        print("CRITICAL: System entering 'Digital Hallucination' regime.")
        
    return mean_divergence

if __name__ == "__main__":
    simulate_divergence()