import numpy as np
from scipy.optimize import fsolve

class BistableLogicBit:
    def __init__(self, a=1.0, b=2.0, c=0.0):
        self.a = a
        self.b = b
        self.c = c

    def potential(self, x):
        # E2: Potential energy landscape
        return self.a*x**4 - self.b*x**2 + self.c*x

    def force(self, x):
        # F = -dV/dx
        return -(4*self.a*x**3 - 2*self.b*x + self.c)

    def find_equilibria(self):
        """Find roots of the force equation to identify stable/unstable states."""
        roots = np.roots([4*self.a, 0, -2*self.b, self.c])
        real_roots = np.sort(roots[np.isreal(roots)].real)
        return real_roots

    def simulate_switching(self, start_x, force_applied):
        """Euler integration of a damped mechanical bit."""
        x = start_x
        v = 0.0
        dt = 0.01
        damping = 0.5
        for _ in range(500):
            f_total = self.force(x) + force_applied
            accel = f_total - damping * v
            v += accel * dt
            x += v * dt
        return x

def main():
    # Scenario: High bias due to radiation-induced PEEK hardening
    bit = BistableLogicBit(a=1, b=4, c=1.5)
    eqs = bit.find_equilibria()
    
    print(f"--- Bistable Potential Analysis (c={bit.c}) ---")
    print(f"Equilibrium Positions: {eqs}")
    
    # Test switching logic
    # State 0 is negative root, State 1 is positive root
    init_state = eqs[0]
    final_pos = bit.simulate_switching(init_state, force_applied=5.0)
    
    print(f"Initial Position: {init_state:.3f}")
    print(f"Final Position after 5N pulse: {final_pos:.3f}")
    
    success = "YES" if final_pos > 0 else "NO"
    print(f"Successful Logic Flip: {success}")

    # Assertion: Verify that with c=0, wells are symmetric
    bit_sym = BistableLogicBit(a=1, b=4, c=0)
    eq_sym = bit_sym.find_equilibria()
    assert np.allclose(abs(eq_sym[0]), abs(eq_sym[2])), "Symmetric potential must have symmetric roots"

if __name__ == '__main__':
    main()