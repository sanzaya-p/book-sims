import numpy as np

class TopOptSensitivitySolver:
    """
    A simplified 1D discrete structural system representing a chain of compliant cells.
    Computes potential energy sensitivity with respect to local material density (SIMP model).
    """
    def __init__(self, n_elements=10):
        self.n = n_elements
        self.densities = np.ones(n_elements)  # Design variables chi
        self.penal = 3.0  # SIMP penalization
        self.k_base = 100.0

    def assemble_stiffness(self):
        """Assembles a 1D stiffness matrix based on element densities."""
        K = np.zeros((self.n + 1, self.n + 1))
        for i in range(self.n):
            # k_elem = chi^p * k_base
            k_elem = (self.densities[i]**self.penal) * self.k_base
            # Simple 1D bar element stiffness
            K[i, i] += k_elem
            K[i, i+1] -= k_elem
            K[i+1, i] -= k_elem
            K[i+1, i+1] += k_elem
        return K

    def solve_displacements(self, tip_force):
        """Solve Ku = F with fixed boundary at node 0 and force at node n."""
        K = self.assemble_stiffness()
        F = np.zeros(self.n + 1)
        F[-1] = tip_force
        
        # Apply boundary condition (fixed node 0)
        K_reduced = K[1:, 1:]
        F_reduced = F[1:]
        u_reduced = np.linalg.solve(K_reduced, F_reduced)
        u = np.insert(u_reduced, 0, 0.0)
        return u

    def compute_sensitivity(self, u):
        """
        Governing Equation: dV/dChi = uT * (dK/dChi) * u
        This represents the change in potential energy relative to density changes.
        """
        sensitivities = []
        for i in range(self.n):
            # Local element displacement difference
            u_local_delta = u[i+1] - u[i]
            # dK/dChi = p * Chi^(p-1) * K_base
            dk_dchi = self.penal * (self.densities[i]**(self.penal-1)) * self.k_base
            # dV/dchi = u_local^T * (dk/dchi) * u_local
            dV_dchi = (u_local_delta**2) * dk_dchi
            sensitivities.append(dV_dchi)
        return np.array(sensitivities)

def main():
    print("--- m-EDA TopOpt Sensitivity Engine ---")
    n_elements = 5
    solver = TopOptSensitivitySolver(n_elements=n_elements)
    
    # Non-uniform density initialization
    solver.densities = np.linspace(1.0, 0.2, n_elements)
    
    # Solve
    tip_load = 10.0
    u = solver.solve_displacements(tip_load)
    sens = solver.compute_sensitivity(u)
    
    print(f"Element Densities: {np.round(solver.densities, 2)}")
    print(f"Node Displacements: {np.round(u, 4)}")
    print(f"Sensitivity dV/dChi: {np.round(sens, 4)}")
    
    max_idx = np.argmax(sens)
    print(f"\nDesign Insight: Reinforcing Element {max_idx} (dV/dChi={sens[max_idx]:.2f}) provides maximum energy shift.")

if __name__ == '__main__':
    main()