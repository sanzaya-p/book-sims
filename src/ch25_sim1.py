import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class SoftLogicGate:
    def __init__(self, L=0.05, D=0.001, mu=1.8e-5, compliance=1e-9, P_crit=500):
        """
        Represents a Harvard-style kinking gate.
        L: length (m), D: diameter (m), mu: viscosity (Pa*s)
        compliance: dV/dP (m^3/Pa)
        P_crit: Pressure threshold for the 'kink' (Pa)
        """
        self.R = (128 * mu * L) / (np.pi * (D**4))
        self.C = compliance
        self.tau = self.R * self.C
        self.P_crit = P_crit

    def transfer_function(self, P_in):
        """Inverting behavior: high pressure kinks the hose, resulting in low output flow/pressure."""
        # Sigmoid approximation of the buckling/kinking threshold
        return 1000 / (1 + np.exp(0.01 * (P_in - self.P_crit)))

def simulate_ring(num_gates=3, duration=2.0, dt=0.001):
    """Simulates an N-gate ring oscillator."""
    gate = SoftLogicGate(L=0.04, D=0.0012, compliance=2e-10)
    
    def system_dynamics(P, t):
        dPdt = np.zeros_like(P)
        for i in range(num_gates):
            # P[i] is the pressure at gate i
            # Target pressure is defined by the transfer function of the PREVIOUS gate
            P_prev = P[i-1] if i > 0 else P[-1]
            P_target = gate.transfer_function(P_prev)
            # RC charging: dP/dt = (P_target - P_current) / tau
            dPdt[i] = (P_target - P[i]) / gate.tau
        return dPdt

    t = np.arange(0, duration, dt)
    P0 = [500 if i == 0 else 0 for i in range(num_gates)] # Initial perturbation
    states = odeint(system_dynamics, P0, t)
    
    return t, states, gate.tau

def main():
    t, pressures, tau = simulate_ring(num_gates=3)
    
    print(f"--- Fluidic Logic Simulation Summary ---")
    print(f"Theoretical RC Time Constant (tau): {tau:.4f} s")
    print(f"Calculated Frequency (approx): {1/(2*3*tau):.2f} Hz")
    
    # Verification
    assert tau > 0, "Time constant must be positive."
    assert pressures.shape[1] == 3, "Simulation must include 3 gates."
    
    # Check for oscillation (standard deviation of the tail)
    tail_std = np.std(pressures[int(len(t)*0.8):, 0])
    if tail_std > 50:
        print("Status: Oscillation detected.")
    else:
        print("Status: System settled into logical mush (no oscillation).")

if __name__ == "__main__":
    main()