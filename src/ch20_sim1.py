import numpy as np

def run_simp_optimization(nx=30, ny=10, vol_frac=0.5, p=3.0, r_min=1.5, iterations=20):
    """
    A simplified 2D Topology Optimization (SIMP) engine for educational purposes.
    Minimizes compliance (maximizes stiffness) for a cantilever beam.
    
    Args:
        nx, ny: Grid dimensions
        vol_frac: Target volume fraction
        p: Penalization power (the SIMP parameter)
        r_min: Filter radius (prevents checkerboarding)
        iterations: Optimization cycles
    """
    x = np.full((ny, nx), vol_frac)  # Initial density field
    E0 = 1.0
    E_min = 1e-6

    def get_sensitivity(densities):
        # Mock sensitivity: In a real FEA, this would be -p * x**(p-1) * element_strain_energy
        # Here we simulate a cantilever strain field (high at root, low at tip)
        Y, X = np.indices((ny, nx))
        dist_from_root = X / nx
        strain_energy = (1.0 - dist_from_root)**2 * (1.0 + 0.5 * np.sin(Y/ny * np.pi))
        sens = -p * (densities**(p-1)) * strain_energy
        return sens

    def density_filter(s, x_field, rmin):
        # Simplified linear density filter
        new_s = np.zeros_like(s)
        for i in range(ny):
            for j in range(nx):
                weight_sum = 0.0
                for k in range(max(0, int(i-rmin)), min(ny, int(i+rmin+1))):
                    for l in range(max(0, int(j-rmin)), min(nx, int(j+rmin+1))):
                        dist = np.sqrt((i-k)**2 + (j-l)**2)
                        if dist < rmin:
                            w = rmin - dist
                            new_s[i, j] += w * x_field[k, l] * s[k, l]
                            weight_sum += w * x_field[i, j]
                new_s[i, j] /= (weight_sum if weight_sum > 0 else 1.0)
        return new_s

    print(f"--- Starting SIMP Optimization (p={p}, vol_frac={vol_frac}) ---")
    for i in range(iterations):
        sens = get_sensitivity(x)
        # Optimality Criteria (OC) update simplified
        l1, l2 = 0, 1e9
        while (l2 - l1) > 1e-4:
            l_mid = 0.5 * (l1 + l2)
            x_new = np.maximum(0.001, np.minimum(1.0, x * np.sqrt(-sens / l_mid)))
            if np.mean(x_new) > vol_frac:
                l1 = l_mid
            else:
                l2 = l_mid
        
        change = np.linalg.norm(x_new - x)
        x = x_new
        if i % 5 == 0:
            print(f"Iter {i:02d}: Mean Density={np.mean(x):.3f}, Change={change:.4e}")

    binary_score = np.mean(x * (1 - x)) * 4  # 0 is perfectly binary, 1 is fully gray
    print(f"Optimization complete. Binary/Gray Score (0-1): {binary_score:.4e}")
    return x

if __name__ == '__main__':
    # Test regime 1: Low penalty (Gray result)
    run_simp_optimization(p=1.0, iterations=10)
    # Test regime 2: Standard penalty (Binary result)
    run_simp_optimization(p=3.0, iterations=10)