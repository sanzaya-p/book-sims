import numpy as np
import matplotlib.pyplot as plt

def simulate_potential_decay(cycles=100, k_initial=10.0, alpha_initial=0.1):
    """
    Simulates the degradation of the potential energy landscape V(q)
    due to the 'State Overwrite Tax' (accumulated fatigue).
    
    Governing Equation: V(q) = 0.5 * k * (q-q0)^2 - alpha * (q-q0)^4
    """
    q = np.linspace(-5, 5, 500)
    q0 = 0.0
    
    # Fatigue model: Each cycle reduces the restorative stiffness k and increases 
    # the softening coefficient alpha (material softening).
    k_decay = 0.995
    alpha_growth = 1.002
    
    results = []
    
    for i in range(0, cycles + 1, 20):
        k_eff = k_initial * (k_decay ** i)
        alpha_eff = alpha_initial * (alpha_growth ** i)
        
        # Compute Potential
        V = 0.5 * k_eff * (q - q0)**2 - alpha_eff * (q - q0)**4
        
        # Find Barrier Height (local maxima relative to the well)
        # dV/dq = k(q) - 4*alpha(q)^3 = 0 => q = sqrt(k / 4*alpha)
        if k_eff > 0 and alpha_eff > 0:
            q_max = np.sqrt(k_eff / (4 * alpha_eff))
            V_barrier = 0.5 * k_eff * q_max**2 - alpha_eff * q_max**4
        else:
            V_barrier = 0.0
            
        results.append({
            'cycle': i,
            'k': k_eff,
            'alpha': alpha_eff,
            'V': V,
            'barrier': V_barrier
        })

    # Numerical Verification
    assert results[0]['barrier'] > results[-1]['barrier'], "Potential barrier must decrease due to fatigue."
    
    print(f"--- Logic Bit Fatigue Summary ---")
    print(f"Initial Barrier Height: {results[0]['barrier']:.4f}")
    print(f"Final Barrier Height (Cycle {cycles}): {results[-1]['barrier']:.4f}")
    print(f"Percent Degradation: {100*(1 - results[-1]['barrier']/results[0]['barrier']):.2f}%")
    
    return q, results

def main():
    q, results = simulate_potential_decay(cycles=200)
    
    # Visualization setup for documentation output (conceptual)
    plt.figure(figsize=(10, 6))
    for res in results:
        plt.plot(q, res['V'], label=f"Cycle {res['cycle']}")
    plt.title("V(q) Degradation: The State Overwrite Tax")
    plt.xlabel("Generalized Displacement (q)")
    plt.ylabel("Potential Energy V(q)")
    plt.ylim(-10, 10)
    plt.grid(True, linestyle='--')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    # In a non-interactive environment, we print summary instead of plt.show()
    print("Simulation complete. Potential wells are flattening as cycles accumulate.")

if __name__ == '__main__':
    main()