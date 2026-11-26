import numpy as np

def calculate_acoustic_horizon(v_g, f_clk, l_cell):
    """
    Calculates the maximum logical depth (stages) before the acoustic pulse
    falls behind the synchronous clock cycle.
    
    Args:
        v_g (float): Group velocity of logic pulse (m/s)
        f_clk (float): Clock frequency (Hz)
        l_cell (float): Length of a unit cell (m)
    Returns:
        D_max (float): Maximum number of synchronous stages
    """
    # E2: D_max = v_g / (f_clk * L_cell)
    denominator = f_clk * l_cell
    if denominator == 0:
        return float('inf')
    return v_g / denominator

def simulate_logic_chain(num_stages, v_g, f_clk, l_cell):
    """
    Simulates timing skew across a chain of N mechanical logic gates.
    Returns a boolean array of timing-valid states.
    """
    t_clock = 1.0 / f_clk
    t_prop_per_cell = l_cell / v_g
    
    valid_states = []
    for stage in range(1, num_stages + 1):
        total_prop_delay = stage * t_prop_per_cell
        # In synchronous logic, pulse must arrive before next clock edge
        is_valid = total_prop_delay < t_clock
        valid_states.append(is_valid)
    
    return np.array(valid_states)

def main():
    # Constants for a typical polymer metamaterial
    VG = 120.0     # m/s
    L_CELL = 0.01  # 1cm per logic unit
    F_CLK = 500.0  # 500Hz clock
    
    # 1. Theoretical calculation
    d_max = calculate_acoustic_horizon(VG, F_CLK, L_CELL)
    
    # 2. Simulation of a 50-gate chain
    chain_results = simulate_logic_chain(50, VG, F_CLK, L_CELL)
    actual_depth = np.sum(chain_results)
    
    print(f"--- Acoustic Horizon Simulation ---")
    print(f"Group Velocity: {VG} m/s")
    print(f"Clock Frequency: {F_CLK} Hz")
    print(f"Theoretical D_max: {d_max:.2f} stages")
    print(f"Simulated Valid Stages: {actual_depth}")
    
    # Verification
    assert abs(d_max - actual_depth) <= 1.0, "Theoretical and simulated depth mismatch"
    
    if actual_depth < 50:
        print(f"CRITICAL: Logic failure at stage {actual_depth + 1} due to acoustic latency.")

if __name__ == '__main__':
    main()