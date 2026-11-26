import numpy as np

def arch_force_residual(u, lambda_load, h_t=4.0):
    """Calculates the difference between internal and external force."""
    f_int = (h_t**2) * (u - 1.5 * u**2 + 0.5 * u**3) + u
    return f_int - lambda_load

def riks_step(u_n, lambda_n, ds, psi=1.0):
    """
    Performs a single Modified Riks (Arc-Length) step.
    Simplified for a 1-DOF system to show logic.
    """
    # Tangent stiffness K = dF/du
    h_t = 4.0
    K = (h_t**2) * (1 - 3*u_n + 1.5*u_n**2) + 1
    
    # Predictor step direction (du, dl)
    # Normalizing tangent vector (K, 1) by arc length ds
    # In a real FEA, this involves the unit tangent of the equilibrium path
    dl = ds / np.sqrt(K**2 + psi)
    du = K * dl
    
    return u_n + du, lambda_n + dl

def run_simulation():
    print("--- RIKS METHOD PATH TRACING ---")
    u, l = 0.0, 0.0
    ds = 0.1
    path = []
    
    # Trace the snap-through path
    for i in range(25):
        u, l = riks_step(u, l, ds)
        path.append((u, l))
        
        # Qualitative check for negative stiffness
        h_t = 4.0
        K = (h_t**2) * (1 - 3*u + 1.5*u**2) + 1
        stiffness_str = "NEGATIVE" if K < 0 else "POSITIVE"
        
        print(f"Step {i:02d}: u={u:.3f}, Load={l:.3f} | Stiffness: {stiffness_str}")

if __name__ == '__main__':
    run_simulation()