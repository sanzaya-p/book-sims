import numpy as np

def simulate_entrainment(detuning=0.05, coupling=0.1, duration=100, dt=0.01):
    """
    Simulates two phase-coupled oscillators (Kuramoto simplified).
    """
    omega1 = 1.0
    omega2 = 1.0 + detuning
    
    phi1 = 0.0
    phi2 = 0.5 # Initial phase offset
    
    history = []
    for _ in range(int(duration/dt)):
        # Phase evolution with coupling
        d_phi1 = omega1 + coupling * np.sin(phi2 - phi1)
        d_phi2 = omega2 + coupling * np.sin(phi1 - phi2)
        
        phi1 += d_phi1 * dt
        phi2 += d_phi2 * dt
        
        # Track normalized phase difference
        diff = (phi2 - phi1) % (2 * np.pi)
        if diff > np.pi: diff -= 2 * np.pi
        history.append(diff)
        
    final_drift = np.abs(history[-1] - history[-100])
    is_locked = final_drift < 1e-3
    return is_locked, history[-1]

def main():
    print("--- Sync Bandwidth Verification ---")
    detuning_range = [0.02, 0.05, 0.1, 0.2]
    coupling = 0.08
    
    for d in detuning_range:
        locked, final_diff = simulate_entrainment(detuning=d, coupling=coupling)
        status = "LOCKED" if locked else "DRIFTING"
        print(f"Detuning: {d*100:>4.1f}% | Coupling: {coupling:.3f} | Result: {status}")
        if locked:
            assert d <= coupling * 2, "Locking occurred outside theoretical bandwidth limits!"

if __name__ == '__main__':
    main()