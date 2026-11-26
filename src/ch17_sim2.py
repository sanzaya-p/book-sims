import math

class MechanicalGate:
    def __init__(self, z_load, e_snap):
        self.z_load = z_load    # Impedance of the gate
        self.e_snap = e_snap    # Energy threshold to flip state
        self.state = 0          # Binary state

    def receive_pulse(self, z_source, e_input):
        """
        Calculates energy transmission and checks for state transition.
        Returns (Transmitted Energy, Successfully Switched)
        """
        # E1: T = 4*Z1*Z2 / (Z1 + Z2)^2
        transmission_coeff = (4 * z_source * self.z_load) / ((z_source + self.z_load) ** 2)
        e_transmitted = e_input * transmission_coeff
        
        switched = e_transmitted >= self.e_snap
        if switched:
            self.state = 1 if self.state == 0 else 0
            
        return e_transmitted, switched

def main():
    # Simulation Parameters
    E_SNAP = 10.0   # Joules (Threshold for buckling)
    Z_GATE = 100.0  # Unitless impedance
    
    gate = MechanicalGate(Z_GATE, E_SNAP)
    
    print("--- Pulse-State Coupling Test ---")
    
    # Scenario A: Matched Impedance
    z_matched = 100.0
    e_in = 11.0
    e_t, success = gate.receive_pulse(z_matched, e_in)
    print(f"Matched (Z={z_matched}): Transmitted={e_t:.2f}J, Switched={success}")
    assert success == True, "Should switch when matched and energy > threshold"

    # Scenario B: High Impedance Mismatch
    z_mismatch = 1000.0
    e_t2, success2 = gate.receive_pulse(z_mismatch, e_in)
    print(f"Mismatched (Z={z_mismatch}): Transmitted={e_t2:.2f}J, Switched={success2}")
    
    # Analytical Verification of E1
    expected_t = (4 * 1000 * 100) / (1100**2)
    assert abs(e_t2/e_in - expected_t) < 1e-6, "Transmission calculation error"

if __name__ == '__main__':
    main()