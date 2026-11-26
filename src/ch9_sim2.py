import numpy as np
from scipy.integrate import solve_ivp

def duffing_oscillator(t, y, zeta, a, b, f_ext_func):
    """
    Standard bistable Duffing oscillator for mechanical logic state dynamics.
    y = [position, velocity]
    """
    x, v = y
    # f_ext_func(t) provides the trigger pulse
    dxdt = v
    dvdt = a*x - b*x**3 - 2*zeta*v + f_ext_func(t)
    return [dxdt, dvdt]

def simulate_snap(zeta=0.1):
    """
    Simulates a logic flip attempt.
    """
    t_span = (0, 50)
    t_eval = np.linspace(0, 50, 1000)
    
    # Starting in the left well (Logic 0)
    y0 = [-1.0, 0.0]
    
    # External force pulse to trigger flip
    def trigger_force(t):
        if 1.0 < t < 2.5:
            return 0.8
        return 0.0

    sol = solve_ivp(
        duffing_oscillator, 
        t_span, 
        y0, 
        t_eval=t_eval, 
        args=(zeta, 1.0, 1.0, trigger_force)
    )
    
    final_pos = sol.y[0, -1]
    success = final_pos > 0
    return success, final_pos, sol.y

def main():
    print("--- Mechanical Bit-Flip Stability Test ---")
    
    # High damping: Reliable flip
    success_h, pos_h, _ = simulate_snap(zeta=0.5)
    print(f"[Zeta=0.5] Final Pos: {pos_h:8.3f} | Success: {success_h}")
    
    # Low damping: Ringing failure
    success_l, pos_l, _ = simulate_snap(zeta=0.02)
    print(f"[Zeta=0.02] Final Pos: {pos_l:8.3f} | Success: {success_l} (Ringing Failure!)")

    # Numerical Assertion: Low damping leads to state corruption (returns to ~ -1)
    assert pos_l < 0, "Low damping should exhibit ringing failure for these params"

if __name__ == '__main__':
    main()