import numpy as np

class VonKarmanArch:
    """
    Models a shallow 2-bar arch (von Mises Truss) representing 
    the von Kármán non-linear strain in a discrete form.
    """
    def __init__(self, L=1.0, H=0.1, E=1e6, A=0.01):
        self.L = L  # Half-span length
        self.H = H  # Apex height
        self.EA = E * A # Axial stiffness
        
    def force_at_deflection(self, w):
        """
        Calculates equilibrium vertical force P for a given deflection w.
        Derived from P = dU/dw where strain epsilon = (ds^2 - dS^2)/(2dS^2)
        Approximated for shallow arch as: P = (EA/L^3) * w * (w - H) * (w - 2H)
        """
        # Displacement measured from apex downwards
        # P = EA * (w/L) * [ (H/L)^2 - 0.5*(w/L)^2 ] simplified form:
        # Consistent with 1D von Karman strain: eps = (w*H - 0.5*w^2)/L^2
        L_sq = self.L**2
        P = (self.EA / (2 * self.L**3)) * (w * (w - self.H) * (w - 2 * self.H))
        return P

def main():
    # Define an arch with apex height 0.2m
    arch = VonKarmanArch(L=1.0, H=0.2, E=200e9, A=0.001)
    
    # Sweep deflection from 0 to 2H (passing through inverted state)
    w_range = np.linspace(0, 0.4, 50)
    forces = [arch.force_at_deflection(w) for w in w_range]
    
    # Analyze snap points (local maxima/minima of Force)
    # dP/dw = 0 => roots of quadratic
    # P' = 3w^2 - 6wH + 2H^2 = 0
    # w_crit = [6H +/- sqrt(36H^2 - 24H^2)] / 6 = H +/- H/sqrt(3)
    w_snap_limit = arch.H * (1 - 1/np.sqrt(3))
    w_release_limit = arch.H * (1 + 1/np.sqrt(3))
    
    print("--- Arch Snap-Through Analysis ---")
    print(f"Apex Height: {arch.H}m")
    print(f"Snap-Through Deflection Threshold: {w_snap_limit:.4f}m")
    print(f"Force at Snap-Through: {arch.force_at_deflection(w_snap_limit):.2e} N")
    
    # Verify negative stiffness region
    mid_point = arch.H
    force_mid = arch.force_at_deflection(mid_point)
    slope_at_mid = (arch.force_at_deflection(mid_point + 0.001) - force_mid) / 0.001
    
    print(f"Stiffness at apex midpoint: {slope_at_mid:.2e} N/m")
    assert slope_at_mid < 0, "Verification failed: No negative stiffness region found."
    print("Numerical Verification: SUCCESS. Arch exhibits geometric instability.")

if __name__ == '__main__':
    main()