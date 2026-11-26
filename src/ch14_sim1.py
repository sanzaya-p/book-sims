import numpy as np

def simulate_mechanical_bus(nodes=50, alpha=0.1, gain=1.2, active=False, threshold=0.3):
    """
    Simulates signal propagation through a 1D mechanical bus.
    
    Parameters:
    nodes: Number of mechanical links/gates.
    alpha: Attenuation coefficient (damping/compliance loss).
    gain: Mechanical gain of a repeater.
    active: Boolean, if True, repeaters regenerate signal.
    threshold: Minimum displacement to trigger a repeater.
    """
    x_in = 1.0  # Initial normalized displacement (logic '1')
    displacements = [x_in]
    energy_logic = 0.0
    energy_reset = 0.0
    
    for i in range(1, nodes):
        # Passive decay from previous node to current
        current_x = displacements[-1] * np.exp(-alpha)
        
        if active:
            # Spend energy to evaluate
            energy_logic += 0.01 * (current_x**2)
            if current_x > threshold:
                # Regeneration: Snap to full amplitude
                current_x = 1.0 * gain
                # The Reset Tax: Energy to 're-cock' the flexure
                energy_reset += 0.5 * gain
            else:
                current_x = 0.0
        
        # Clamp to physical limits
        current_x = max(0.0, min(current_x, 1.5))
        displacements.append(current_x)
    
    return np.array(displacements), energy_logic, energy_reset

def main():
    print("--- Mechanical Signal Propagation Analysis ---")
    
    # Regime 1: Passive Loss
    disp_p, _, _ = simulate_mechanical_bus(active=False, alpha=0.15)
    horizon_p = np.where(disp_p < 0.1)[0]
    h_idx = horizon_p[0] if len(horizon_p) > 0 else 50
    
    # Regime 2: Active Regeneration
    disp_a, e_l, e_r = simulate_mechanical_bus(active=True, alpha=0.15, gain=1.0)
    
    print(f"Passive Regime: Logical Horizon (SNR < 0.1) at Node {h_idx}")
    print(f"Active Regime: Final Amplitude = {disp_a[-1]:.2f}")
    print(f"Active Regime: Logic Energy = {e_l:.4f}, Reset Energy = {e_r:.4f}")
    print(f"Efficiency Ratio (Logic/Total): {e_l/(e_l+e_r + 1e-9):.4f}")

if __name__ == '__main__':
    main()