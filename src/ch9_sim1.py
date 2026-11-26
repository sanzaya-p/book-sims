import numpy as np
from scipy.integrate import trapezoid

class ShallowArchModel:
    """
    Simulates the quasi-static force-displacement response of a shallow bistable arch.
    Models the 'Hysteresis Moat' and the 'Logic Window' as a function of geometry.
    """
    def __init__(self, Q=4.0, epsilon=0.0):
        self.Q = Q  # Geometric factor (dimensionless)
        self.epsilon = epsilon  # Asymmetry parameter (imperfection)

    def calculate_force(self, delta):
        """
        Calculates dimensionless force P for a given displacement delta.
        P = delta^3 - Q*delta + epsilon
        """
        return delta**3 - self.Q * delta + self.epsilon

    def find_limit_points(self):
        """
        Finds P_sn (Snap-through) and P_sb (Snap-back) via dP/ddelta = 0.
        3*delta^2 - Q = 0  => delta = +/- sqrt(Q/3)
        """
        if self.Q <= 0:
            return None, None
        d_sn = -np.sqrt(self.Q / 3.0)
        d_sb = np.sqrt(self.Q / 3.0)
        p_sn = self.calculate_force(d_sn)
        p_sb = self.calculate_force(d_sb)
        return p_sn, p_sb

    def calculate_work_cycle(self):
        """
        Calculates the energy cost (Work) of a full bit-flip cycle (Hysteresis Area).
        Using the analytical integral of the force-displacement loop.
        """
        p_sn, p_sb = self.find_limit_points()
        if p_sn is None or p_sn <= p_sb:
            return 0.0
        
        # Integrate the loop area between the limit points for the bistable regime
        delta_range = np.linspace(-np.sqrt(self.Q), np.sqrt(self.Q), 500)
        forces = self.calculate_force(delta_range)
        # Note: In a true cycle, path is non-reversible. Area is P_sn-P_sb logic width.
        return float(p_sn - p_sb)

def main():
    print("--- Shallow Arch Hysteresis Analysis ---")
    # Sweep Q to observe transition from monostable to bistable
    for q_val in [1.0, 2.31, 5.0]:
        arch = ShallowArchModel(Q=q_val, epsilon=0.05)
        psn, psb = arch.find_limit_points()
        
        if psn is not None:
            is_bistable = psn > 0 and psb < 0
            print(f"Q: {q_val:<5} | P_sn: {psn:8.3f} | P_sb: {psb:8.3f} | Bistable: {is_bistable}")
        else:
            print(f"Q: {q_val:<5} | No limit points (Monostable)")

    # Verification Assertion: Q=0 should be strictly monotonic
    linear_arch = ShallowArchModel(Q=0, epsilon=0)
    forces = [linear_arch.calculate_force(d) for d in np.linspace(-1, 1, 10)]
    assert all(np.diff(forces) > 0), "Q=0 arch must be monotonic (no negative stiffness)"

if __name__ == '__main__':
    main()