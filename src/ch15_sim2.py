import numpy as np

def simulate_langevin_stability(n_steps=10000, dt=0.01, noise_sigma=0.5):
    """
    Euler-Maruyama simulation of a bistable bit subject to acoustic jitter.
    """
    m, gamma, a, b = 1.0, 1.0, 1.0, 2.0
    x = -np.sqrt(b / (2 * a)) # Initial state: Left well
    v = 0.0
    
    crossings = 0
    current_well = -1 # -1 for left, 1 for right
    
    for i in range(n_steps):
        # Force term
        f_det = -(4 * a * x**3 - 2 * b * x)
        # Langevin equation update
        v += (f_det - gamma * v) * dt / m + (noise_sigma * np.sqrt(dt) * np.random.normal()) / m
        x += v * dt
        
        # Check for well crossing
        if x > 0 and current_well == -1:
            crossings += 1
            current_well = 1
        elif x < 0 and current_well == 1:
            crossings += 1
            current_well = -1
            
    return crossings, x

def main():
    print("--- Acoustic Jitter Reliability Test ---")
    noise_levels = [0.1, 0.5, 1.5]
    for sigma in noise_levels:
        flips, final_x = simulate_langevin_stability(noise_sigma=sigma)
        status = "STABLE" if flips == 0 else f"UNSTABLE ({flips} flips)"
        print(f"Noise σ={sigma:3.1f}: {status} | Final x: {final_x:+.3f}")

    # Verification test
    flips_low, _ = simulate_langevin_stability(noise_sigma=0.01)
    assert flips_low == 0, "Bit should be stable under negligible noise."

if __name__ == "__main__":
    main()