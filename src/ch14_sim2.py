import numpy as np

def simulate_thermal_stability(well_depth=1.0, temp=0.1, steps=10000):
    """
    Simulates a bistable mechanical gate under thermal noise.
    
    well_depth: Energy barrier Delta U
    temp: Thermal energy k_B T
    """
    # State: -1 (Logic 0), 1 (Logic 1)
    state = -1 
    flips = 0
    history = [state]
    
    # Boltzmann probability of jumping the barrier per timestep
    p_flip = np.exp(-well_depth / (temp + 1e-9))
    
    for _ in range(steps):
        if np.random.random() < p_flip:
            state *= -1
            flips += 1
        history.append(state)
        
    return flips, np.array(history)

def main():
    print("--- Thermal Stability Limit Analysis ---")
    
    well_depths = [0.5, 1.0, 2.0]
    temp = 0.2
    
    for dU in well_depths:
        flips, hist = simulate_thermal_stability(well_depth=dU, temp=temp)
        error_rate = flips / len(hist)
        print(f"Barrier dU={dU:.1f}, Temp={temp:.1f} -> Flips: {flips}, Error Rate: {error_rate:.4%}")
        
    # Verification assertion
    f1, _ = simulate_thermal_stability(well_depth=0.5, temp=0.5)
    f2, _ = simulate_thermal_stability(well_depth=2.0, temp=0.1)
    assert f1 > f2, "Higher temperature/lower barrier must increase flip probability."

if __name__ == '__main__':
    main()