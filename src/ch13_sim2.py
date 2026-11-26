import math

class BistableGateChain:
    def __init__(self, k_arch=500.0, k_link=250.0, threshold=4.0):
        """
        Models a chain of two bistable gates connected by an elastic link.
        k_arch: Negative stiffness slope of the arch gate (N/mm)
        k_link: Stiffness of the transmission filament (N/mm)
        """
        self.k_arch = k_arch
        self.k_link = k_link
        self.threshold = threshold

    def check_stability(self):
        """Calculates Stiffness Ratio Lambda (Equation E2)."""
        return self.k_link / self.k_arch

    def propagate_signal(self, input_displacement):
        """
        Simulates displacement transfer from Gate 1 to Gate 2.
        Returns (Gate1_Snap, Gate2_Snap, Transmission_Efficiency)
        """
        g1_snap = input_displacement >= self.threshold
        
        if not g1_snap:
            return False, False, 0.0

        # Gate 1 provides a fixed displacement burst
        delta_burst = 6.0 
        
        # Displacement reached at Gate 2 depends on the series stiffness
        # delta_2 = delta_burst * (K_link / (K_link + K_arch_downstream))
        # Here we simplify to the stability criterion effect
        transmission_efficiency = self.k_link / (self.k_link + self.k_arch)
        delta_at_g2 = delta_burst * transmission_efficiency
        
        g2_snap = delta_at_g2 >= self.threshold
        
        return g1_snap, g2_snap, transmission_efficiency

def main():
    print("--- Mechanical Ischemia Analysis ---")
    
    # Regime 1: Unstable (Soft Link)
    unstable_chain = BistableGateChain(k_arch=600, k_link=200)
    g1, g2, eff = unstable_chain.propagate_signal(5.0)
    print(f"Regime Lambda < 1: Eff={eff:.2f}, G1_Snap={g1}, G2_Snap={g2} (FAIL)")

    # Regime 2: Stable (Stiff Link)
    stable_chain = BistableGateChain(k_arch=600, k_link=1200)
    g1, g2, eff = stable_chain.propagate_signal(5.0)
    print(f"Regime Lambda > 1: Eff={eff:.2f}, G1_Snap={g1}, G2_Snap={g2} (SUCCESS)")

    # Verification
    assert stable_chain.check_stability() > 1.0
    assert unstable_chain.check_stability() < 1.0

if __name__ == '__main__':
    main()