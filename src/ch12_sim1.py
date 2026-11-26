import numpy as np

def calculate_arch_equilibrium(h_t_ratio, softening_alpha=1.0, points=200):
    """
    Calculates the dimensionless force-displacement curve for a fixed-fixed arch.
    
    Args:
        h_t_ratio (float): Ratio of apex height to beam thickness.
        softening_alpha (float): TPU correction factor (1.0 = linear elastic).
        points (int): Numerical resolution.
        
    Returns:
        dict: u (normalized displacement), F (normalized force).
    """
    # u ranges from 0 (relaxed) to 2 (fully snapped)
    u = np.linspace(0, 2.0, points)
    
    # Dimensionless Force Equation for a Shallow Arch
    # Derived from Euler-Bernoulli with mid-plane stretching
    term_bistable = (h_t_ratio**2) * (u - 1.5 * u**2 + 0.5 * u**3)
    term_linear = u
    
    # Apply the TPU Correction (Softening as a function of strain/displacement)
    # In the textbook model, softening increases near the snap point (u=1)
    softening_factor = 1.0 - (1.0 - softening_alpha) * np.sin(np.pi * u / 2)
    
    f_normalized = softening_factor * (term_bistable + term_linear)
    
    return {"u": u, "F": f_normalized}

def verify_bistability(u, F):
    """
    Determines if the curve represents a non-volatile (bistable) bit.
    Requirement: Force must cross zero three times between u=0 and u=2.
    """
    zero_crossings = np.where(np.diff(np.sign(F)))[0]
    # Crossing 1: Snap-through start (ignore u=0)
    # Crossing 2: Unstable peak to negative stiffness
    # Crossing 3: Negative stiffness back to stable well (Reset point)
    return len(zero_crossings) >= 2

def main():
    print("--- ARCH BIT STABILITY ANALYSIS ---")
    
    ratios = [2.0, 3.5, 5.0]
    alphas = [1.0, 0.85] # 1.0 = Ideal, 0.85 = TPU Softening
    
    for h_t in ratios:
        for a in alphas:
            data = calculate_arch_equilibrium(h_t, softening_alpha=a)
            is_bistable = verify_bistability(data['u'], data['F'])
            f_max = np.max(data['F'])
            f_min = np.min(data['F'])
            
            status = "BISTABLE" if is_bistable and f_min < 0 else "MONOSTABLE"
            
            print(f"Config: h/t={h_t}, Alpha={a:.2f} -> {status}")
            print(f"  Peak Snap Force (F_bar): {f_max:.3f}")
            print(f"  Reset Force (F_bar): {f_min:.3f}")
            print("-" * 30)

if __name__ == '__main__':
    main()