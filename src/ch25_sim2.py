import numpy as np

class MetamaterialChain:
    def __init__(self, n_cells=10, barrier_height=1.0, coupling=0.5, asymmetry=0.1):
        self.n = n_cells
        self.x = np.ones(n_cells) * -1.0 # Initial state '0' (left well)
        self.v = np.zeros(n_cells)
        self.k = barrier_height
        self.gamma = coupling
        self.beta = asymmetry
        self.dt = 0.05

    def get_forces(self, x):
        # Double-well force: F = -dU/dx = k(x - x^3)
        f_well = self.k * (x - x**3)
        
        # Coupling forces (Harmonic + Cubic Asymmetry)
        f_couple = np.zeros_like(x)
        for i in range(self.n):
            # Forward coupling to next cell
            if i < self.n - 1:
                diff = x[i+1] - x[i]
                f_couple[i] += self.gamma * diff + self.beta * (diff**2)
            # Backward coupling
            if i > 0:
                diff = x[i-1] - x[i]
                f_couple[i] += self.gamma * diff - self.beta * (diff**2)
        
        return f_well + f_couple

    def step(self, drive_force=0.0):
        # Verlet-like integration
        f = self.get_forces(self.x)
        f[0] += drive_force # Input signal at the first cell
        
        # Damping to stabilize states
        damping = -0.3 * self.v
        
        self.v += (f + damping) * self.dt
        self.x += self.v * self.dt

def main():
    # Simulate a signal attempting to traverse the chain
    chain = MetamaterialChain(n_cells=5, asymmetry=0.2)
    
    print("Simulating Metamaterial Count Pulse...")
    for t in range(200):
        # Apply a pulse at the start for the first 20 steps
        pulse = 5.0 if t < 20 else 0.0
        chain.step(drive_force=pulse)
        
        if t % 50 == 0:
            state_str = " ".join([f"{val:+.1f}" for val in chain.x])
            print(f"Step {t:03d}: State = [{state_str}]")

    # Final check: did the signal reach the end?
    if chain.x[-1] > 0:
        print("Success: Signal propagated to terminal node.")
    else:
        print("Failure: Signal attenuated or blocked.")

    assert len(chain.x) == 5, "Chain length mismatch."

if __name__ == "__main__":
    main()