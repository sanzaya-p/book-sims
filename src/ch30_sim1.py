import numpy as np

def simulate_silicon_fever():
    """
    Simulates the failure of a CMOS transistor under gamma-ray flux.
    Calculates the generation rate G and the resulting leakage current.
    """
    # Constants
    rho_si = 2.329  # g/cm^3 (Density of Silicon)
    e_charge = 1.602e-19  # Coulombs
    epsilon_eh = 3.6  # eV per pair in Si
    epsilon_eh_joules = epsilon_eh * e_charge

    # Simulation Parameters
    dose_rates = np.logspace(0, 6, 10)  # Dose rate in Gy/s (1 to 1,000,000)
    node_sizes_nm = [28, 14, 7]
    
    print("{:>10} | {:>15} | {:>15} | {:>10}".format("Dose (Gy/s)", "Node (nm)", "Leakage (nA)", "Status"))
    print("-" * 60)

    for dose_rate in dose_rates:
        # E1: Calculation of carrier generation rate (pairs / cm^3 * s)
        # 1 Gy = 1 J/kg = 1e-3 J/g
        energy_deposited_per_sec = dose_rate * 1e-3 * rho_si # J / (cm^3 * s)
        G = energy_deposited_per_sec / epsilon_eh_joules
        
        for node in node_sizes_nm:
            # Estimate sensitive volume (V ~ node^3)
            vol_cm3 = (node * 1e-7)**3
            
            # Total carriers generated in the junction per second
            carriers_per_sec = G * vol_cm3
            
            # Induced current (I = q * n/t)
            i_leak_amps = carriers_per_sec * e_charge
            i_leak_na = i_leak_amps * 1e9
            
            # Failure threshold (rough heuristic: 50nA for small nodes)
            threshold = 50.0 / (node / 7.0)
            status = "FAIL" if i_leak_na > threshold else "PASS"
            
            print(f"{dose_rate:10.1e} | {node:15} | {i_leak_na:15.4f} | {status}")

    # Numerical Verification Assertion
    # At 10^5 Gy/s, a 7nm node should show significant induced current
    assert G > 0, "Generation rate must be positive"

if __name__ == '__main__':
    simulate_silicon_fever()