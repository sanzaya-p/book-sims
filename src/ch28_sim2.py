import numpy as np

class TwinPathTrainer:
    def __init__(self, num_struts=10, eta=0.01):
        """
        Demonstrates physical learning in a single-degree-of-freedom chain.
        Each 'strut' i has a stiffness k_i.
        """
        self.k = np.ones(num_struts) * 100.0
        self.eta = eta
        self.target_displacement = 5.0
        self.input_force = 20.0

    def forward(self):
        """
        The 'Free State': Just input forces.
        Total stiffness K_eff = 1 / sum(1/k_i)
        """
        K_eff = 1.0 / np.sum(1.0 / self.k)
        u_free = self.input_force / K_eff
        # Local strain epsilon_i is proportional to 1/k_i
        strains_free = (u_free * K_eff) / self.k
        return u_free, strains_free

    def nudged(self):
        """
        The 'Nudged State': Input forces + clamping the output to target.
        """
        u_nudge = self.target_displacement
        K_eff = 1.0 / np.sum(1.0 / self.k)
        # Local strain in the nudged configuration
        strains_nudge = (u_nudge * K_eff) / self.k
        return u_nudge, strains_nudge

    def update():
        """
        Update k_i using Equation E2.
        """
        u_f, eps_f = self.forward()
        u_n, eps_n = self.nudged()
        
        # Equation E2: Delta k_i = eta * (eps_n^2 - eps_f^2)
        delta_k = self.eta * (eps_n**2 - eps_f**2)
        self.k += delta_k
        # Ensure physical validity (k > 0)
        self.k = np.clip(self.k, 0.1, 1000.0)
        
        loss = (u_f - self.target_displacement)**2
        return loss

def main():
    trainer = TwinPathTrainer(num_struts=5, eta=0.5)
    print(f"Initial Stiffnesses: {trainer.k}")
    
    for epoch in range(101):
        u_f, eps_f = trainer.forward()
        u_n, eps_n = trainer.nudged()
        
        loss = (u_f - trainer.target_displacement)**2
        
        # Gradient Update
        delta_k = trainer.eta * (eps_n**2 - eps_f**2)
        trainer.k += delta_k
        
        if epoch % 20 == 0:
            print(f"Epoch {epoch:3}: Error={loss:8.4f}, Output Displacement={u_f:5.2f}")

    print(f"Final Stiffnesses: {trainer.k}")
    assert loss < 0.1, "Learning failed to converge within threshold."

if __name__ == '__main__':
    main()