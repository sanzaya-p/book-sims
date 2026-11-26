import numpy as np

def simulate_snap_through(a=1.0, b=2.0, force=0.0, dt=0.01, steps=1000, initial_x=0.0):
    """
    Simulates the overdamped dynamics of a particle in a double-well potential.
    dx/dt = -dU/dx = -(4ax^3 - 2bx - F)
    """
    x = initial_x
    trajectory = []
    
    for _ in range(steps):
        # Calculate gradient (force field)
        du_dx = 4 * a * (x**3) - 2 * b * x - force
        # Overdamped update: velocity proportional to force
        x_new = x - du_dx * dt
        trajectory.append(x_new)
        x = x_new
        
    return np.array(trajectory)

def find_critical_force(a, b):
    """
    Analytical solution for the force required to eliminate one well (snapping point).
    Occurs when dU/dx = 0 and d^2U/dx^2 = 0.
    """
    if b <= 0:
        return 0.0
    # The inflection points are at x = +/- sqrt(b/6a)
    x_crit = np.sqrt(b / (6 * a))
    f_crit = 4 * a * (x_crit**3) - 2 * b * x_crit
    return abs(f_crit)

def main():
    # Material parameters (Geometric constants)
    a_coeff = 0.5
    b_coeff = 2.0
    
    print(f"--- Stability Analysis (a={a_coeff}, b={b_coeff}) ---")
    
    # 1. Test Static Equilibrium
    traj_stable = simulate_snap_through(a_coeff, b_coeff, initial_x=1.5)
    final_x = traj_stable[-1]
    print(f"Natural Equilibrium State: x = {final_x:.4f}")
    
    # 2. Test Threshold Triggering
    fc = find_critical_force(a_coeff, b_coeff)
    print(f"Calculated Snap-Through Force Threshold: {fc:.4f}")
    
    # Apply force just below threshold
    traj_below = simulate_snap_through(a_coeff, b_coeff, force=fc*0.9, initial_x=-final_x)
    print(f"Applied 90% threshold: State remains at x = {traj_below[-1]:.4f}")
    
    # Apply force just above threshold
    traj_above = simulate_snap_through(a_coeff, b_coeff, force=fc*1.1, initial_x=-final_x)
    print(f"Applied 110% threshold: State snapped to x = {traj_above[-1]:.4f}")
    
    assert traj_above[-1] * traj_below[-1] < 0, "Verification failed: Snap-through did not toggle displacement sign."
    print("Numerical Verification: SUCCESS. System functions as a non-linear switch.")

if __name__ == '__main__':
    main()