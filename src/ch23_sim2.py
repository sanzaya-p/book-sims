import math

def calculate_effective_stiffness(nominal_t, layer_h, theta_deg):
    """
    Calculates the reduction in moment of inertia due to the scalloped 
    profile of FDM/AM layers.
    """
    theta = math.radians(theta_deg)
    # Simplified geometric model: effectively reduces thickness by the scalloped valley depth
    # Scallop depth e = (h/2) * cos(theta)
    e = (layer_h / 2.0) * math.cos(theta)
    t_effective = nominal_t - 2 * e
    
    # Stiffness K is proportional to t^3
    i_ratio = (t_effective / nominal_t)**3
    return max(0, i_ratio)

def rss_vs_worst_case(tolerances):
    """
    Compares Worst-Case stack-up vs Root-Sum-Square.
    """
    worst_case = sum(tolerances)
    rss = math.sqrt(sum(t**2 for t in tolerances))
    return worst_case, rss

def main():
    print("--- CH23 SIM 2: EFFECTIVE GEOMETRY & TOLERANCE STACK ---")
    
    t_nom = 1.0
    layer_heights = [0.05, 0.1, 0.2, 0.3]
    
    print(f"Effective Stiffness Ratio (Nominal Thickness = {t_nom}mm, Angle=45°):")
    for lh in layer_heights:
        ratio = calculate_effective_stiffness(t_nom, lh, 45)
        print(f"  Layer Height {lh}mm: {ratio:.3f}x Nominal")
        
    # Assembly Yield Analysis
    tols = [0.05, 0.05, 0.05, 0.05, 0.05] # 5 parts in series
    wc, rss = rss_vs_worst_case(tols)
    
    print(f"\nAssembly Stack-up (5 parts, 0.05mm tol each):")
    print(f"  Worst-Case: +/- {wc:.3f} mm")
    print(f"  RSS:        +/- {rss:.3f} mm")
    print(f"  Yield Gap Advantage: {((wc-rss)/wc)*100:.1f}%")

    # Numerical Assertion
    assert calculate_effective_stiffness(1.0, 0, 0) == 1.0, "Perfect layers must equal nominal"
    print("\nNumerical Verification: Geometry scaling valid.")

if __name__ == '__main__':
    main()