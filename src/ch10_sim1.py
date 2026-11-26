import numpy as np
from scipy.optimize import fsolve

class AsymmetricWellSimulator:
    """
    Simulates the energy landscape and equilibrium points of an asymmetric 
    bistable beam under varying buckling and asymmetry parameters.
    """
    def __init__(self, a=1.0, b=2.0, c=0.1):
        self.a = a  # Non-linear stiffness
        self.b = b  # Linear negative stiffness (buckling force)
        self.c = c  # Asymmetry/Bias coefficient

    def potential(self, x):
        return self.a * x**4 - self.b * x**2 + self.c * x

    def force(self, x):
        # F = dV/dx
        return 4 * self.a * x**3 - 2 * self.b * x + self.c

    def find_equilibria(self):
        """
        Finds roots of the force equation to identify stable and unstable states.
        """
        # Use a range of initial guesses to capture all potential roots
        guesses = np.linspace(-2, 2, 10)
        roots = []
        for g in guesses:
            root, info, ier, msg = fsolve(self.force, g, full_output=True)
            if ier == 1:
                roots.append(round(root[0], 6))
        
        unique_roots = sorted(list(set(roots)))
        
        # Stability analysis: d2V/dx2 > 0 is stable
        stability = []
        for r in unique_roots:
            d2V = 12 * self.a * r**2 - 2 * self.b
            stability.append("Stable" if d2V > 0 else "Unstable")
            
        return list(zip(unique_roots, stability))

def main():
    print("--- Asymmetric Well: Monostability Collapse Analysis ---")
    
    # Sweep asymmetry 'c' to find the collapse point
    a, b = 1.0, 4.0
    c_values = [0.0, 1.0, 3.0, 3.079, 4.0] # 3.079 is approx critical for a=1, b=4
    
    for c in c_values:
        sim = AsymmetricWellSimulator(a=a, b=b, c=c)
        eqs = sim.find_equilibria()
        num_stable = sum(1 for _, s in eqs if s == "Stable")
        
        print(f"Bias c: {c:<6} | Equilibria Found: {len(eqs)} | Stable States: {num_stable}")
        for x, status in eqs:
            energy = sim.potential(x)
            print(f"  x = {x: .4f} ({status}), V(x) = {energy: .4f}")
        
        if num_stable < 2:
            print("  >>> WARNING: MONOSTABILITY COLLAPSE REACHED <<<")
        print("-" * 50)

if __name__ == "__main__":
    main()