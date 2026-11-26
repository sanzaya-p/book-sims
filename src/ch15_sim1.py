import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class MechanicalBit:
    """
    Simulates a bistable mechanical bit governed by a quartic potential.
    """
    def __init__(self, a=1.0, b=2.0, m=1.0, gamma=0.5):
        self.a = a
        self.b = b
        self.m = m
        self.gamma = gamma
        # Equilibria are at x = +/- sqrt(b / (2a))
        self.x_eq = np.sqrt(b / (2 * a))
        self.barrier_height = (b**2) / (4 * a)

    def force(self, x, external_f=0):
        # F = -dV/dx = - (4ax^3 - 2bx)
        return - (4 * self.a * x**3 - 2 * self.b * x) + external_f

    def system_dynamics(self, state, t, force_profile):
        x, v = state
        f_ext = force_profile(t)
        dxdt = v
        dvdt = (self.force(x, f_ext) - self.gamma * v) / self.m
        return [dxdt, dvdt]

def simulate_snap_through():
    bit = MechanicalBit(a=1.0, b=4.0, m=1.0, gamma=1.2)
    t = np.linspace(0, 20, 1000)
    
    # A short push pulse to flip the bit
    def force_pulse(t):
        if 2.0 < t < 4.0:
            return 5.0 # Pulse magnitude
        return 0.0

    initial_state = [-bit.x_eq, 0.0]
    solution = odeint(bit.system_dynamics, initial_state, t, args=(force_pulse,))
    
    x_vals = solution[:, 0]
    
    # Verification
    final_pos = x_vals[-1]
    success = "SUCCESS" if final_pos > 0 else "FAILURE"
    
    print(f"--- Simulation Summary ---")
    print(f"Well Minima: +/-{bit.x_eq:.3f}")
    print(f"Barrier Height: {bit.barrier_height:.3f} Energy Units")
    print(f"Initial State: {initial_state[0]:.3f}")
    print(f"Final State: {final_pos:.3f} ({success})")
    
    assert abs(final_pos - bit.x_eq) < 0.5, "Bit failed to stabilize in the target well."

if __name__ == '__main__':
    simulate_snap_through()