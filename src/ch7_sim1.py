import numpy as np

def analyze_curvature_error(span, amplitude_range, steps=10):
    """
    Analyzes the divergence between linear curvature (w'') and exact curvature
    for a sinusoidal beam deflection w(x) = A*sin(pi*x/L).
    """
    L = span
    x = np.linspace(0, L, 1000)
    
    results = []
    
    for A in np.linspace(amplitude_range[0], amplitude_range[1], steps):
        # Profile: w = A * sin(pi * x / L)
        # dw/dx = A * (pi/L) * cos(pi * x / L)
        # d2w/dx2 = -A * (pi/L)**2 * sin(pi * x / L)
        
        dw_dx = A * (np.pi/L) * np.cos(np.pi * x / L)
        d2w_dx2 = -A * (np.pi/L)**2 * np.sin(np.pi * x / L)
        
        linear_k = np.abs(d2w_dx2)
        exact_k = np.abs(d2w_dx2) / (1 + dw_dx**2)**(1.5)
        
        # Max values occur at center (x=L/2) for curvature, 
        # but max slope occurs at supports (x=0)
        max_slope = np.max(np.abs(dw_dx))
        max_linear_k = np.max(linear_k)
        max_exact_k = np.max(exact_k)
        
        error = np.abs(max_linear_k - max_exact_k) / max_exact_k
        results.append({
            'amp': A,
            'max_slope_deg': np.degrees(np.arctan(max_slope)),
            'error_pct': error * 100
        })

    # Verification: Assert error is small for small slopes
    assert results[0]['error_pct'] < 1.0, "Linear theory should be accurate at small deflections."
    return results

def main():
    print("--- Geometric Divergence Analysis ---")
    results = analyze_curvature_error(span=1.0, amplitude_range=(0.001, 0.5))
    print(f"{'Slope (deg)':<15} | {'Error (%)':<10}")
    print("-" * 30)
    for r in results:
        print(f"{r['max_slope_deg']:<15.2f} | {r['error_pct']:<10.2f}")
    
    # Identify 10% threshold
    threshold = next((r for r in results if r['error_pct'] > 10.0), None)
    if threshold:
        print(f"\nObservation: Linear theory breaks (10% error) at ~{threshold['max_slope_deg']:.1f} degrees slope.")

if __name__ == '__main__':
    main()