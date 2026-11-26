import numpy as np
import matplotlib.pyplot as plt

class SnapThroughSimulator:
    """
    Simulates a non-linear shallow arch (von Mises Truss) logic gate.
    Models the equation F = K(u)u where K depends on geometry updates.
    """
    def __init__(self, L=100.0, H=5.0, E=2000.0, A=10.0):
        self.L = L  # Half-span
        self.H = H  # Initial arch height
        self.E = E  # Young's Modulus
        self.A = A  # Cross-sectional area
        
    def calculate_force(self, u):
        """
        Calculates internal force F_int for a given displacement u.
        Derived from: F = (EA/L) * (u/L) * (H - u/2) * (H - u)
        This is a simplified 1D non-linear equilibrium model.
        """
        # Strain calculation in the Lagrangian frame
        L_prime = np.sqrt(self.L**2 + (self.H - u)**2)
        L_0 = np.sqrt(self.L**2 + self.H**2)
        strain = (L_prime - L_0) / L_0
        
        # Force projection onto vertical axis
        axial_force = self.E * self.A * strain
        cos_theta = (self.H - u) / L_prime
        return axial_force * cos_theta

    def run_sweep(self):
        """Sweeps displacement from 0 to 2*H to capture snap-through."""
        displacements = np.linspace(0, 2 * self.H, 200)
        forces = [self.calculate_force(u) for u in displacements]
        
        # Find critical limit points
        peak_idx = np.argmax(forces[:len(forces)//2])
        snap_force = forces[peak_idx]
        
        return displacements, forces, snap_force

def main():
    print("--- Snap-Through Non-Linearity Verification ---")
    
    # Case 1: High Bistability (Tall Arch)
    sim_high = SnapThroughSimulator(H=10.0)
    d1, f1, s1 = sim_high.run_sweep()
    
    # Case 2: Marginal Bistability (Shallow Arch)
    sim_low = SnapThroughSimulator(H=3.0)
    d2, f2, s2 = sim_low.run_sweep()
    
    print(f"High Arch Snap Force: {s1:.2f} N")
    print(f"Low Arch Snap Force: {s2:.2f} N")
    
    # Verification of negative stiffness regime
    f1_grad = np.gradient(f1)
    unstable_points = np.where(f1_grad < 0)[0]
    
    if len(unstable_points) > 0:
        print(f"Stability Check: Unstable regime detected between u={d1[unstable_points[0]]:.2f} and {d1[unstable_points[-1]]:.2f}")
    else:
        print("Stability Check: Logic gate is monostable (Failed Design).")

if __name__ == '__main__':
    main()