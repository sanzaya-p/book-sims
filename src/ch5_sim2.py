import numpy as np

def simulate_soliton_propagation(nodes=50, k=2.0, damping=0.1, steps=2000):
    """
    Simulates a 1D chain of coupled bistable oscillators (Sine-Gordon-like discrete chain).
    Each node has potential U(x) = 0.25*x^4 - 0.5*x^2.
    """
    # Constants
    m = 1.0
    a = 1.0
    b = 1.0
    dt = 0.05
    
    # Initial state: all in the left well (-1)
    x = -np.ones(nodes)
    v = np.zeros(nodes)
    
    # Trigger: Force the first node into the right well (+1)
    x[0] = 1.0
    
    history = []
    
    for _ in range(steps):
        # Calculate coupling forces with fixed boundaries
        coupled_f = np.zeros(nodes)
        coupled_f[1:-1] = k * (x[2:] - 2*x[1:-1] + x[:-2])
        
        # Local double-well force
        internal_f = -a * x**3 + b * x
        
        # Total acceleration
        accel = (internal_f + coupled_f - damping * v) / m
        
        # Integrate
        v += accel * dt
        x += v * dt
        
        history.append(x.copy())
    
    history = np.array(history)
    
    # Check if signal reached the end
    reached_end = history[-1, -1] > 0
    
    return reached_end, history

if __name__ == "__main__":
    # Case 1: Strong coupling - Soliton travels
    success_strong, _ = simulate_soliton_propagation(k=5.0)
    # Case 2: Weak coupling - Soliton is pinned (lattice friction)
    success_weak, _ = simulate_soliton_propagation(k=0.5)
    
    print(f"Soliton propagation (k=5.0): {'SUCCESS' if success_strong else 'FAILED'}")
    print(f"Soliton propagation (k=0.5): {'SUCCESS' if success_weak else 'FAILED'}")
    
    assert success_strong == True
    assert success_weak == False
    print("Numerical Verification: Discreteness effects (Peierls-Nabarro barrier) observed.")