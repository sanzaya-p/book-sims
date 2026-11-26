import numpy as np

def simulate_tid_failure():
    """
    Simulates the Threshold Voltage shift (Delta Vth) in a MOSFET over time
    given a specific radiation flux and shielding configuration.
    """
    # Constants
    q = 1.602e-19  # Elementary charge (C)
    eps_ox = 3.9 * 8.854e-12  # Permittivity of SiO2 (F/m)
    d_ox = 10e-9  # Oxide thickness (m)
    
    # Simulation Parameters
    dose_rate_unshielded = 100 / 3600  # 100 Gy/hr converted to Gy/s
    mu_shield = 0.5  # Attenuation coeff for Lead (cm^-1)
    shield_thickness = 5.0  # cm
    exposure_time_years = 1.0
    time_seconds = exposure_time_years * 365 * 24 * 3600
    
    # Equation E3: Attenuation
    flux_attenuated = dose_rate_unshielded * np.exp(-mu_shield * shield_thickness)
    total_dose = flux_attenuated * time_seconds
    
    # Empirical Charge Generation (Simplified model)
    # Trapped charge density rho_ot as a function of total dose
    # Assuming 10^12 holes/cm^2 generated per Gray
    trapped_charge_per_gray = 1e16  # holes/m^2/Gy
    total_rho_area = trapped_charge_per_gray * total_dose
    
    # Equation E1: Integral approximation for uniform distribution
    # If rho_ot(z) is uniform, Integral(z dz) = 0.5 * d_ox^2
    # DeltaVth = -(q/eps_ox) * (Total_Rho_Volumetric) * (0.5 * d_ox^2)
    # Since Total_Rho_Area = Total_Rho_Volumetric * d_ox:
    # DeltaVth = -(q/eps_ox) * (Total_Rho_Area / d_ox) * (0.5 * d_ox^2)
    delta_v_th = -(q / eps_ox) * (total_rho_area * 0.5 * d_ox)
    
    # Failure Criterion: Typically Vth shift > 0.5V leads to logic failure
    failure_threshold = -0.5
    is_failed = delta_v_th < failure_threshold
    
    summary = {
        "effective_dose_rate_gy_s": flux_attenuated,
        "cumulative_dose_gy": total_dose,
        "delta_v_th_volts": delta_v_th,
        "system_status": "FAILED" if is_failed else "OPERATIONAL"
    }
    
    for k, v in summary.items():
        print(f"{k}: {v}")

if __name__ == '__main__':
    simulate_tid_failure()