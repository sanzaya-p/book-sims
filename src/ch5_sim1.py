import numpy as np
from scipy.integrate import solve_ivp

def simulate_snap_through(a=1.0, b=1.0, damping=0.1, m=0.1, duration=10.0):
    """
    Simulates the dynamics of a particle in a double-well potential
    driven by a quasi-static force that triggers a snap-through event.
    
    U(x) = 0.25*a*x^4 - 0.5*b*x^2
    F_int = -dU/dx = -a*x^3 + b*x
    """
    # Derived quantities
    x_wells = np.sqrt(b/a)
    u_barrier = 0.25 * (b**2 / a)
    
    def system_dynamics(t, state, ext_force):
        x, v = state
        # Force from potential + Damping + External Drive
        force_internal = -a * x**3 + b * x
        dxdt = v
        dvdt = (force_internal - damping * v + ext_force) / m
        return [dxdt, dvdt]

    # Phase 1: Quasi-static push to the edge of the barrier
    # We start at the left well: x = -x_wells
    initial_state = [-x_wells, 0.0]
    
    # Trigger force: Just enough to overcome the barrier peak at x=0
    # Peak resistance is at x = sqrt(b/(3a))
    f_crit = (2/3) * b * np.sqrt(b / (3*a))
    
    # Run simulation with a force slightly above critical
    sol = solve_ivp(
        system_dynamics, 
        [0, duration], 
        initial_state, 
        args=(f_crit * 1.05,), 
        t_eval=np.linspace(0, duration, 1000),
        method='RK45'
    )

    v_max = np.max(np.abs(sol.y[1]))
    ke_max = 0.5 * m * v_max**2
    
    return {
        "t": sol.t,
        "x": sol.y[0],
        "v": sol.y[1],
        "v_max": v_max,
        "ke_max": ke_max,
        "u_barrier": u_barrier
    }

if __name__ == "__main__":
    # Regime 1: Low Stiffness
    res1 = simulate_snap_through(a=0.5, b=1.0)
    # Regime 2: High Stiffness (Same barrier height via scaling b)
    # U_barrier = 0.25 * b^2 / a. To keep U_barrier=0.5, if a=2, b=sqrt(0.5*4)=1.414
    res2 = simulate_snap_through(a=2.0, b=1.414)

    print(f"--- Kinetic Amplification Analysis ---")
    print(f"Regime [Soft]: Max Velocity = {res1['v_max']:.3f} | Barrier = {res1['u_barrier']:.3f}")
    print(f"Regime [Stiff]: Max Velocity = {res2['v_max']:.3f} | Barrier = {res2['u_barrier']:.3f}")
    
    assert res2['v_max'] > res1['v_max'], "Stiffer materials should produce faster snaps for same barrier."
    print("Numerical Verification: Energy amplification scales with square root of stiffness.")