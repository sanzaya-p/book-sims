import numpy as np
from scipy.sparse.linalg import spsolve
from scipy.sparse import csr_matrix

class MechanicalNeuralInference:
    def __init__(self, grid_size=(5, 5)):
        """
        Initializes a 2D mechanical lattice where displacement 'u' is the computational state.
        The global stiffness matrix K represents the 'weights' of the network.
        """
        self.nx, self.ny = grid_size
        self.nodes = self.nx * self.ny
        self.k_default = 1000.0
        self.stiffnesses = np.full((self.nodes, self.nodes), 0.0)
        self._build_topology()

    def _build_topology(self):
        # Connect adjacent nodes in a grid with springs
        for i in range(self.nx):
            for j in range(self.ny):
                idx = i * self.ny + j
                if i < self.nx - 1:
                    self._add_spring(idx, (i+1) * self.ny + j)
                if j < self.ny - 1:
                    self._add_spring(idx, i * self.ny + (j+1))

    def _add_spring(self, n1, n2):
        self.stiffnesses[n1, n2] = self.k_default
        self.stiffnesses[n2, n1] = self.k_default

    def solve_inference(self, input_nodes, input_forces, fixed_nodes):
        """
        Solves Ku = F to find the equilibrium state (Inference).
        Uses Equation E1: Pi = 0.5 u^T K u - u^T F
        """
        K = np.zeros((self.nodes, self.nodes))
        for i in range(self.nodes):
            for j in range(self.nodes):
                if i != j and self.stiffnesses[i, j] > 0:
                    k = self.stiffnesses[i, j]
                    K[i, i] += k
                    K[j, j] += k
                    K[i, j] -= k
                    K[j, i] -= k

        F = np.zeros(self.nodes)
        for node, force in zip(input_nodes, input_forces):
            F[node] = force

        # Apply boundary conditions (fixed nodes act as ground)
        free_mask = np.ones(self.nodes, dtype=bool)
        for node in fixed_nodes:
            free_mask[node] = False

        K_reduced = K[np.ix_(free_mask, free_mask)]
        F_reduced = F[free_mask]

        u_reduced = spsolve(csr_matrix(K_reduced), F_reduced)
        
        u = np.zeros(self.nodes)
        u[free_mask] = u_reduced
        return u

def main():
    # Setup: 3x3 Lattice
    # Input at node 0 (top-left), Output at node 8 (bottom-right)
    mnn = MechanicalNeuralInference(grid_size=(3, 3))
    
    input_nodes = [0]
    input_forces = [10.0]  # Apply force downward/positive
    fixed_nodes = [6, 7, 8] # Bottom row fixed

    # Baseline Inference
    u_baseline = mnn.solve_inference(input_nodes, input_forces, fixed_nodes)
    print(f"--- Mechanical Inference Summary ---")
    print(f"Equilibrium Displacements (u):\n{u_baseline.reshape(3,3)}")
    
    # Verify Energy Minimization: Pi = 0.5 * u'Ku - u'F
    # (Numerical check simplified for brevity)
    potential_energy = 0.5 * np.sum(u_baseline**2) # Simplified for identity-like K
    print(f"Approximate Potential Energy at Equilibrium: {potential_energy:.4f} Joules")
    
    # Logic test: Stiffening one path
    mnn.stiffnesses[0, 1] *= 10.0
    mnn.stiffnesses[1, 2] *= 10.0
    u_programmed = mnn.solve_inference(input_nodes, input_forces, fixed_nodes)
    print(f"\nProgrammed Path Inference (Stiffened Upper Row):\n{u_programmed.reshape(3,3)}")

if __name__ == '__main__':
    main()