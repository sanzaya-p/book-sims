import numpy as np

def simulate_gradient_stress(n_voxels=100, e_rigid=2000, e_soft=10, grad_width=20, p=1.0):
    """
    Simulates the stress distribution across a multi-material transition.
    
    Args:
        n_voxels: Spatial discretization
        e_rigid: Modulus of Material A (e.g., Titanium/Rigid Polymer)
        e_soft: Modulus of Material B (e.g., Elastomer)
        grad_width: Number of voxels used for the functional gradient
        p: SIMP-style penalization factor for the interpolation
    """
    # Spatial coordinates
    x = np.linspace(0, 1, n_voxels)
    
    # Define material distribution (rho)
    # 0.0 is soft, 1.0 is rigid
    rho = np.zeros(n_voxels)
    midpoint = n_voxels // 2
    half_w = grad_width // 2
    
    start_grad = max(0, midpoint - half_w)
    end_grad = min(n_voxels, midpoint + half_w)
    
    rho[:start_grad] = 0.0
    rho[end_grad:] = 1.0
    
    if grad_width > 0:
        # Linear ramp for density in the transition zone
        ramp = np.linspace(0, 1, end_grad - start_grad)
        rho[start_grad:end_grad] = ramp

    # E(rho) interpolation (Equation E1 logic)
    # E = E_soft + rho^p * (E_rigid - E_soft)
    e_profile = e_soft + (rho**p) * (e_rigid - e_soft)
    
    # Mechanical Model: Constant displacement (Strain-controlled)
    # In a 1D bar, stress = E(x) * Strain
    # Assuming unit strain for visualization of relative stress concentrations
    epsilon = 1.0
    stress_profile = e_profile * epsilon
    
    # Calculate Stress Gradient (Singularity proxy)
    dstress_dx = np.gradient(stress_profile)
    
    return {
        "max_stress": np.max(stress_profile),
        "max_gradient": np.max(np.abs(dstress_dx)),
        "avg_modulus": np.mean(e_profile)
    }

def main():
    print("--- Multi-Material Interface Stress Analysis ---")
    
    # Regime 1: Sharp Interface
    sharp = simulate_gradient_stress(grad_width=0)
    print(f"Sharp Interface: Peak Stress Gradient = {sharp['max_gradient']:.2f}")
    
    # Regime 2: Linear Gradient
    linear = simulate_gradient_stress(grad_width=40, p=1.0)
    print(f"Linear Gradient (W=40%): Peak Stress Gradient = {linear['max_gradient']:.2f}")
    
    # Regime 3: Non-Linear Power Law Gradient
    power = simulate_gradient_stress(grad_width=40, p=3.0)
    print(f"Power-Law Gradient (p=3): Peak Stress Gradient = {power['max_gradient']:.2f}")
    
    assert linear['max_gradient'] < sharp['max_gradient'], "Gradient should reduce stress concentration!"

if __name__ == '__main__':
    main()