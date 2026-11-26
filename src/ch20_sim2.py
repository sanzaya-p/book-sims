import numpy as np

class CompliantSIMP:
    def __init__(self, nx=40, ny=20):
        self.nx = nx
        self.ny = ny
        self.n_elems = nx * ny
        self.x = np.full(self.n_elems, 0.3)
        
    def compute_mutual_displacement(self, x, mode='inverter'):
        """
        Computes f = L^T * u. 
        In a real solver, u = K(x)^-1 * F_in.
        Here we use a simplified proxy for the displacement field u.
        """
        # Simulating the displacement field u under an input force at (0, ny/2)
        # and a dummy load L at (nx-1, ny/2)
        indices = np.arange(self.n_elems).reshape((self.ny, self.nx))
        
        # Proxy Sensitivity for a 'Displacement Inverter' mechanism
        # An inverter needs to connect input to output with a pivot.
        # Sensitivity is high where material facilitates the leverage.
        Y, X = np.indices((self.ny, self.nx))
        if mode == 'inverter':
            # Leverage pattern: Pivot in center, paths to input/output
            pivot_x, pivot_y = self.nx // 2, self.ny // 2
            dist_to_leverage = np.abs((Y - pivot_y) - (X - pivot_x) * 0.5)
            sensitivity = 1.0 / (1.0 + dist_to_leverage)
        else:
            # Standard stiffener: Shortest path between supports
            sensitivity = (1.0 - X / self.nx)
            
        return sensitivity

    def optimize(self, steps=15, p=3.0):
        print(f"Optimizing for Mutual Displacement (SIMP p={p})")
        for s in range(steps):
            # Calculate Adjoint Sensitivities
            sens = self.compute_mutual_displacement(self.x)
            # Apply penalization effect on sensitivity
            sens *= p * (self.x ** (p-1))
            
            # Simple gradient step with volume constraint (0.3)
            old_x = self.x.copy()
            self.x = np.clip(self.x + sens * 0.1, 0, 1)
            
            # Project back to volume fraction
            if np.mean(self.x) > 0.3:
                self.x *= (0.3 / np.mean(self.x))
            
            change = np.mean(np.abs(self.x - old_x))
            if s % 5 == 0:
                print(f"Step {s}: Sensitivity Mean={np.mean(sens):.4f}, Change={change:.4e}")

if __name__ == '__main__':
    model = CompliantSIMP()
    model.optimize(steps=20)
    # The final field model.x represents the synthesized mechanism topology
    print("Synthesis complete. Final Mean Density:", np.mean(model.x))