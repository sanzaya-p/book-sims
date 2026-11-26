import numpy as np

def weibull_cross_section(let, sigma_sat, let_th, w, s):
    """
    Calculates the SEE cross section based on Weibull distribution.
    let: Linear Energy Transfer of the ion
    sigma_sat: Saturated cross section
    let_th: Threshold LET
    w: Width parameter
    s: Shape parameter
    """
    if let < let_th:
        return 0.0
    return sigma_sat * (1 - np.exp(-((let - let_th) / w)**s))

def simulate_mission_errors(sigma_params, ion_spectrum):
    """
    Integrates cross section over an ion flux spectrum to estimate error rates.
    ion_spectrum: List of (let_value, flux)
    """
    total_errors = 0
    for let, flux in ion_spectrum:
        sigma = weibull_cross_section(let, **sigma_params)
        total_errors += sigma * flux
    return total_errors

def main():
    # Case 1: Rad-Hard Logic (High threshold)
    hardened_params = {'sigma_sat': 1e-4, 'let_th': 15.0, 'w': 30.0, 's': 1.5}
    
    # Case 2: Commercial Off-The-Shelf (Low threshold)
    cots_params = {'sigma_sat': 5e-4, 'let_th': 1.2, 'w': 10.0, 's': 1.2}
    
    # Simplified ion spectrum (LET, Flux in #/cm^2-day)
    spectrum = [(let, 1000 * np.exp(-let/5)) for let in np.linspace(0.1, 100, 100)]
    
    rate_hard = simulate_mission_errors(hardened_params, spectrum)
    rate_cots = simulate_mission_errors(cots_params, spectrum)
    
    print(f"Mission Analysis (Errors/Day):")
    print(f"- Hardened Device: {rate_hard:.4e}")
    print(f"- COTS Device:     {rate_cots:.4e}")
    print(f"- Risk Multiplier: {rate_cots/rate_hard:.1f}x")

    assert rate_cots > rate_hard, "COTS should have higher error rates in this regime"

if __name__ == '__main__':
    main()