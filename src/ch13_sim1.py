import numpy as np

class ElasticJunction:
    def __init__(self, c_i=[0.45, 0.45], k_junction=100.0, k_parasitic=10.0):
        """
        Models a 3-node elastic junction where displacements sum vectorially.
        c_i: coupling coefficients for inputs
        k_junction: local stiffness of the T-junction (N/mm)
        k_parasitic: stiffness loss to the surrounding TPU matrix (N/mm)
        """
        self.c_i = np.array(c_i)
        self.k_j = k_junction
        self.k_p = k_parasitic

    def calculate_output(self, inputs, delta_loss=0.05):
        """
        Calculates delta_out based on Equation E1.
        """
        inputs = np.array(inputs)
        summation = np.sum(self.c_i * inputs)
        attenuation = (self.k_p / self.k_j) * delta_loss
        delta_out = summation - attenuation
        return max(0, delta_out) if sum(inputs) >= 0 else min(0, delta_out)

    def evaluate_logic_state(self, delta_out, threshold=1.5):
        """Classifies displacement as Logic 0 or 1 based on threshold."""
        return 1 if abs(delta_out) >= threshold else 0

def main():
    # Scenario: XOR-style cancellation vs OR-style summation
    junction = ElasticJunction(c_i=[0.5, 0.5], k_junction=100, k_parasitic=20)
    
    test_cases = [
        {"name": "Single Input (1,0)", "vals": [5.0, 0.0]},
        {"name": "Additive Sum (1,1)", "vals": [5.0, 5.0]},
        {"name": "Destructive XOR (1,-1)", "vals": [5.0, -5.0]},
        {"name": "High Parasitic Loss (1,1)", "vals": [5.0, 5.0], "kp": 80}
    ]

    print(f"{'Case':<25} | {'Delta Out':<10} | {'Logic'}")
    print("-"*50)
    for case in test_cases:
        if "kp" in case: junction.k_p = case["kp"]
        out = junction.calculate_output(case["vals"])
        logic = junction.evaluate_logic_state(out)
        print(f"{case['name']:<25} | {out:10.3f} | {logic}")

    # Verification
    assert junction.evaluate_logic_state(junction.calculate_output([5, -5])) == 0, "XOR Cancellation Failed"

if __name__ == '__main__':
    main()