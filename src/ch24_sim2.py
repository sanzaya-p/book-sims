import numpy as np

def hill_criterion(stress_vec, yield_strengths):
    """
    Calculates the Hill Equivalent Stress ratio for orthotropic materials.
    stress_vec: [sig_x, sig_y, sig_z, tau_yz, tau_zx, tau_xy]
    yield_strengths: [X, Y, Z, R, S, T] (directional yield strengths in MPa)
    Yield occurs when the return value >= 1.0
    """
    X, Y, Z, R, S, T = yield_strengths
    
    # Hill parameters derived from directional yield strengths
    # Avoid division by zero if yields are zero
    F = 0.5 * (1.0/(Y**2) + 1.0/(Z**2) - 1.0/(X**2))
    G = 0.5 * (1.0/(Z**2) + 1.0/(X**2) - 1.0/(Y**2))
    H = 0.5 * (1.0/(X**2) + 1.0/(Y**2) - 1.0/(Z**2))
    L = 0.5 / (R**2)
    M = 0.5 / (S**2)
    N = 0.5 / (T**2)
    
    sx, sy, sz, tyz, tzx, txy = stress_vec
    
    # Hill Yield Function f(sigma)
    f_val = F*(sy - sz)**2 + G*(sz - sx)**2 + H*(sx - sy)**2 + \
            2*L*tyz**2 + 2*M*tzx**2 + 2*N*txy**2
    
    return np.sqrt(f_val) 

def main():
    # Material: FDM Printed ABS/PLA
    # X, Y (in-plane layer strength) = 50 MPa
    # Z (inter-layer bond strength) = 20 MPa
    # Shear strengths (estimated ~ 0.6 * tensile)
    yield_fdm = [50.0, 50.0, 20.0, 15.0, 15.0, 30.0]
    
    applied_load_mpa = 15.0
    guardband_threshold = 0.4
    
    print(f"--- Hill Anisotropic Yield Audit ---")
    print(f"Applied Load: {applied_load_mpa} MPa")
    print(f"Material Strengths: X,Y=50, Z=20 (Weak Z-axis)")
    print(f"Target Guardband: 40% (Ratio < {guardband_threshold})\n")
    
    # Scan rotation angles from 0 to 90 degrees
    for angle in [0, 15, 30, 45, 60, 75, 90]:
        rad = np.radians(angle)
        # Stress transformation: apply global load in X-direction and rotate the part
        # Local stresses in part coordinate system:
        sig_x = applied_load_mpa * (np.cos(rad)**2)
        sig_z = applied_load_mpa * (np.sin(rad)**2)
        tau_zx = applied_load_mpa * np.sin(rad) * np.cos(rad)
        
        stress_vec = [sig_x, 0.0, sig_z, 0.0, tau_zx, 0.0]
        eq_stress_ratio = hill_criterion(stress_vec, yield_fdm)
        
        # Safety Factor and Guardband analysis
        safety_factor = 1.0 / eq_stress_ratio if eq_stress_ratio > 0 else float('inf')
        
        # Check if we violate the 40% Guardband (Stress > 40% of Yield)
        status = "SAFE" if eq_stress_ratio < guardband_threshold else "GUARD VIOLATION"
        if eq_stress_ratio >= 1.0: status = "YIELD FAILURE"

        print(f"Angle: {angle:2d}° | Stress Ratio: {eq_stress_ratio:.3f} | SF: {safety_factor:.2f} | Status: {status}")

if __name__ == '__main__':
    main()