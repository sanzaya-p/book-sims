import math

class Material:
    def __init__(self, name, melt_temp, degradation_temp, alpha, e_modulus):
        self.name = name
        self.tm = melt_temp
        self.td = degradation_temp
        self.alpha = alpha  # CTE (1e-6 /K)
        self.e = e_modulus  # Young's Modulus (MPa)

def calculate_process_window(p_laser, v_scan, material_a, material_b, h=0.1, t=0.1, delta_t=180):
    """
    Calculates the feasibility of co-processing two materials.
    
    Args:
        p_laser: Laser power (W)
        v_scan: Scan speed (mm/s)
        h: Hatch spacing (mm)
        t: Layer thickness (mm)
        delta_t: Cooling delta from melt to ambient (K)
    """
    # 1. Energy Density (J/mm^3)
    ed = p_laser / (v_scan * h * t)
    
    # 2. Window Mapping (Approximated energy thresholds for sintering)
    # Thresholds typically scale with Tmelt
    ed_min_a = material_a.tm / 20.0
    ed_max_a = material_a.td / 20.0
    
    ed_min_b = material_b.tm / 20.0
    ed_max_b = material_b.td / 20.0
    
    in_window_a = ed_min_a <= ed <= ed_max_a
    in_window_b = ed_min_b <= ed <= ed_max_b
    
    # 3. Residual Stress (Equation E3)
    # Combined modulus for interface
    e_eff = (material_a.e * material_b.e) / (material_a.e + material_b.e)
    d_alpha = abs(material_a.alpha - material_b.alpha) * 1e-6
    res_stress = e_eff * d_alpha * delta_t
    
    # 4. Failure Criterion (Simple yield comparison)
    failure = res_stress > min(material_a.e, material_b.e) * 0.05
    
    return {
        "energy_density": ed,
        "valid_a": in_window_a,
        "valid_b": in_window_b,
        "co_sinter_possible": in_window_a and in_window_b,
        "residual_stress_mpa": res_stress,
        "delamination_risk": failure
    }

def main():
    nylon = Material("Nylon-12", 175, 250, 110, 1500)
    tpu = Material("TPU", 160, 220, 180, 50)
    
    print("--- Multi-Material Sintering Search ---")
    
    # Scenario: High Speed Printing
    res = calculate_process_window(p_laser=30, v_scan=2000, material_a=nylon, material_b=tpu)
    print(f"At 30W/2000mm/s: Ed={res['energy_density']:.2f} J/mm^3")
    print(f"Co-sinter Possible: {res['co_sinter_possible']}")
    print(f"Residual Stress: {res['residual_stress_mpa']:.2f} MPa")
    
    # Scenario: Optimized Window
    res2 = calculate_process_window(p_laser=15, v_scan=800, material_a=nylon, material_b=tpu)
    print(f"\nAt 15W/800mm/s: Ed={res2['energy_density']:.2f} J/mm^3")
    print(f"Co-sinter Possible: {res2['co_sinter_possible']}")
    print(f"Risk of Pop-off: {res2['delamination_risk']}")

if __name__ == '__main__':
    main()