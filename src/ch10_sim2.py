import numpy as np

class MechanicalADC:
    """
    Simulates a N-bit Flash ADC made of mechanical bistable beams with
    graduated geometric imperfections.
    """
    def __init__(self, n_bits=8, p_sn0=100.0, k=10.0, hysteresis=20.0):
        self.n_bits = n_bits
        self.p_sn0 = p_sn0  # Symmetric snap-through force (mN)
        self.k = k          # Sensitivity constant
        self.hysteresis = hysteresis # Force difference for snap-back
        
        # Create imperfection gradient (0.001 to 0.05)
        self.epsilons = np.linspace(0.001, 0.05, n_bits)
        
        # Calculate forward and backward thresholds for each bit
        self.p_snap_forward = p_sn0 * (1 - self.k * self.epsilons)
        self.p_snap_back = self.p_snap_forward - self.hysteresis
        
        # State: 0 (State A), 1 (State B)
        self.states = np.zeros(n_bits, dtype=int)

    def update(self, input_force):
        """
        Updates logic states based on current input force and hysteresis history.
        """
        for i in range(self.n_bits):
            if self.states[i] == 0:
                if input_force >= self.p_snap_forward[i]:
                    self.states[i] = 1
            else:
                if input_force <= self.p_snap_back[i]:
                    self.states[i] = 0
        return self.states

def main():
    # Example run with force ramping
    adc = MechanicalADC(n_bits=8, p_sn0=100.0, k=10.0, hysteresis=20.0)
    
    print(f"{'Force (mN)':<12} | {'Thermometer Code':<20} | {'Digital Value'}")
    print("-" * 60)
    
    # Ramp force up
    for f in range(0, 110, 10):
        states = adc.update(f)
        code_str = "".join(map(str, states))
        print(f"{f:<12} | {code_str:<20} | {sum(states)}")
        
    print("\n--- Decreasing Force (Hysteresis Check) ---")
    # Ramp force down
    for f in range(100, -10, -10):
        states = adc.update(f)
        code_str = "".join(map(str, states))
        print(f"{f:<12} | {code_str:<20} | {sum(states)}")

if __name__ == "__main__":
    main()