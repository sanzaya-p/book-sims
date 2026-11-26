import numpy as np

def simulate_crack_propagation(a_initial, a_final, delta_sigma, C, m, Y=1.12):
    """
    Integrates Paris Law to find N cycles and tracks stiffness degradation.
    
    Args:
        a_initial: Starting crack length (mm)
        a_final: Failure crack length (mm)
        delta_sigma: Stress range (MPa)
        C: Paris constant
        m: Paris exponent
        Y: Geometry factor
    """
    a = a_initial
    N = 0
    history = []
    da = (a_final - a_initial) / 500.0 # Step size
    
    while a < a_final:
        delta_K = Y * delta_sigma * np.sqrt(np.pi * (a / 1000.0)) # a in meters for K
        da_dN = C * (delta_K)**m
        
        if da_dN <= 0: break
        
        dN = da / (da_dN * 1000.0) # convert da back to m/cycle context
        N += dN
        
        # Simplified stiffness: k ~ (h - a)^3 for a bending beam
        # Normalized freq f/f0 = sqrt(k/k0) = sqrt(((h-a)/h)^3)
        h = a_final * 1.2 # Assume beam height
        freq_ratio = np.sqrt(((h - a) / h)**3)
        
        history.append((N, a, freq_ratio))
        a += da
        
        if len(history) > 10000: break
        
    return history

def main():
    # Material: Aluminum 7075-T6
    C = 1.5e-11 # Typical for Al in m/cycle (MPa sqrt(m))
    M_BRITTLE = 4.0
    M_DUCTILE = 2.5
    
    DSIGMA = 100.0
    A0 = 0.5 # mm
    AF = 5.0 # mm
    
    print(f"--- Crack Propagation & Frequency Shift ---")
    
    hist_brittle = simulate_crack_propagation(A0, AF, DSIGMA, C, M_BRITTLE)
    hist_ductile = simulate_crack_propagation(A0, AF, DSIGMA, C, M_DUCTILE)
    
    print(f"Brittle (m={M_BRITTLE}) Total Life: {hist_brittle[-1][0]:.2e} cycles")
    print(f"Ductile (m={M_DUCTILE}) Total Life: {hist_ductile[-1][0]:.2e} cycles")
    
    # Check for frequency drop at 90% of life
    target_n = hist_brittle[-1][0] * 0.9
    for n, a, f in hist_brittle:
        if n >= target_n:
            print(f"\nAt 90% life (Brittle): Freq has dropped to {f*100:.1f}% of original.")
            break
            
    assert hist_brittle[-1][0] < hist_ductile[-1][0], "Higher m should lead to faster failure for same C"

if __name__ == '__main__':
    main()