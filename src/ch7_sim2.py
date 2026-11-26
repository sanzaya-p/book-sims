import numpy as np
from scipy.integrate import simps

class VonKarmanBit:
    def __init__(self, L=1.0, E=200e9, I=1e-11, A=1e-5, w0_amp=0.01):
        self.L = L
        self.E = E
        self.I = I
        self.A = A
        self.w0_amp = w0_amp # Initial arch height
        self.x = np.linspace(0, L, 100)
        
    def get_induced_tension(self, w_current):
        """
        Calculates N based on Equation E3: induced axial force from stretching.
        Assumes ends are pinned-pinned or clamped but fixed in x.
        """
        dw_dx = np.gradient(w_current, self.x)
        # Stretching integral
        integral = simps(0.5 * dw_dx**2, self.x)
        N = (self.E * self.A / self.L) * integral
        return N

    def calculate_energy(self, w_current):
        """
        Calculates Bending Energy + Stretching Energy.
        """
        dw_dx = np.gradient(w_current, self.x)
        d2w_dx2 = np.gradient(dw_dx, self.x)
        
        U_bending = simps(0.5 * self.E * self.I * d2w_dx2**2, self.x)
        N = self.get_induced_tension(w_current)
        # Stretching energy is 1/2 * L * N^2 / (EA)
        U_stretching = 0.5 * self.L * (N**2) / (self.E * self.A)
        
        return U_bending, U_stretching

def main():
    # Simulate a Silicon Carbide (SiC) logic bit
    bit = VonKarmanBit(L=100e-6, E=450e9, I=1e-24, A=1e-12, w0_amp=2e-6)
    
    print("--- von Karman Logic Bit Properties ---")
    # Test state 0: The initial arch w(x) = w0_amp * sin(pi*x/L)
    w_state0 = bit.w0_amp * np.sin(np.pi * bit.x / bit.L)
    N0 = bit.get_induced_tension(w_state0)
    Ub0, Us0 = bit.calculate_energy(w_state0)
    
    print(f"Induced Axial Tension (N) in State 0: {N0*1e6:.2f} uN")
    print(f"Total Energy in State 0: {(Ub0+Us0)*1e15:.2f} fJ")

    # Test state 'Flat': Forced w(x) = 0
    Ub_flat, Us_flat = bit.calculate_energy(np.zeros_like(bit.x))
    print(f"Energy Barrier (Potential Well Depth): {(Ub_flat+Us_flat - (Ub0+Us0))*1e15:.2f} fJ")
    
    # Verification check
    assert N0 > 0, "Mid-plane stretching must induce positive tension."
    assert (Ub0 + Us0) > 0, "Potential energy must be positive."

if __name__ == '__main__':
    main()