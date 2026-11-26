import numpy as np

class ImplantReliabilityModel:
    def __init__(self, p_design=140, fouling_rate=0.02, fatigue_rate=0.015):
        """
        Models the drift of mechanical trigger pressure over time.
        p_design: Initial target pressure (mmHg)
        fouling_rate: Coefficient for protein-induced stiffening
        fatigue_rate: Coefficient for viscoelastic softening
        """
        self.p_0 = p_design
        self.k_fouling = fouling_rate
        self.k_fatigue = fatigue_rate
        
    def calculate_drift(self, years, cycles_per_year=40e6):
        """
        Calculates pressure threshold over time.
        Delta_P_fouling follows asymptotic saturation (Vroman effect).
        Delta_P_fatigue follows log-linear degradation.
        """
        t = np.linspace(0, years, 100)
        total_cycles = t * cycles_per_year
        
        # Fouling: Stiffening due to encapsulation (mmHg)
        # Max fouling adds 60mmHg to threshold
        dp_fouling = 60 * (1 - np.exp(-self.k_fouling * t * 12))
        
        # Fatigue: Softening due to structural micro-cracks (mmHg)
        # Fatigue scales with log of cycles
        dp_fatigue = self.k_fatigue * 5 * np.log10(total_cycles + 1)
        
        p_logic = self.p_0 + dp_fouling - dp_fatigue
        return t, p_logic, dp_fouling, dp_fatigue

def main():
    # High-fouling clinical scenario
    model = ImplantReliabilityModel(p_design=140, fouling_rate=0.05, fatigue_rate=0.8)
    years, p_t, d_foul, d_fat = model.calculate_drift(5)
    
    print("--- 5-Year Threshold Drift Analysis ---")
    print(f"Initial Threshold: {p_t[0]:.1f} mmHg")
    print(f"Final Threshold:   {p_t[-1]:.1f} mmHg")
    
    # Verification of regime boundaries
    safe_min, safe_max = 110, 170
    was_safe = np.all((p_t > safe_min) & (p_t < safe_max))
    
    if not was_safe:
        failure_idx = np.where((p_t < safe_min) | (p_t > safe_max))[0][0]
        print(f"CRITICAL: Device exited Safe Logic Zone at Year {years[failure_idx]:.2f}")
        if p_t[failure_idx] > safe_max:
            print("Mode: Logical Seizure (Stiffening dominant)")
        else:
            print("Mode: Logical Mush (Fatigue dominant)")
    else:
        print("SUCCESS: Device remained within hemodynamic operating window.")

if __name__ == '__main__':
    main()