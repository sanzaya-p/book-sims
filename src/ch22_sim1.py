import numpy as np

def calculate_fatigue_life(sigma_a, sigma_m, sigma_f_prime, sigma_ut, b):
    """
    Calculates reversals to failure using the Goodman-corrected Basquin Law.
    
    Args:
        sigma_a: Stress amplitude (MPa)
        sigma_m: Mean stress (MPa)
        sigma_f_prime: Fatigue strength coefficient (MPa)
        sigma_ut: Ultimate tensile strength (MPa)
        b: Fatigue strength exponent (Basquin exponent, typical -0.05 to -0.12)
        
    Returns:
        N_f: Cycles to failure (1/2 of reversals)
    """
    # Goodman correction for mean stress effect on fatigue strength
    # Adjusted sigma_f_prime accounts for the 'budget' consumed by mean stress
    if sigma_m >= sigma_ut:
        return 0.5 # Immediate static failure
    
    # Modified Basquin incorporating Goodman: sigma_a / (1 - sigma_m/sigma_ut) = sigma_f_prime * (2Nf)^b
    # Solving for 2Nf:
    try:
        goodman_factor = 1.0 - (sigma_m / sigma_ut)
        if goodman_factor <= 0:
            return 0.5
        
        reversals = (sigma_a / (sigma_f_prime * goodman_factor))**(1/b)
        return reversals / 2.0
    except (ZeroDivisionError, OverflowError):
        return float('inf')

def main():
    # Material: 17-7 PH Stainless Steel (Condition CH900)
    SIGMA_UT = 1300.0  # MPa
    SIGMA_F_PRIME = 1500.0 # MPa
    B = -0.08
    
    print(f"--- Fatigue Life Analysis: Goodman-Basquin --- ")
    print(f"Material Parameters: UTS={SIGMA_UT}MPa, b={B}\n")
    
    # Scenario: Constant Peak Stress vs Variable Mean Stress
    # Case 1: Pure oscillation (sigma_m = 0)
    amp_1 = 600.0
    mean_1 = 0.0
    life_1 = calculate_fatigue_life(amp_1, mean_1, SIGMA_F_PRIME, SIGMA_UT, B)
    
    # Case 2: High mean stress, lower amplitude
    amp_2 = 400.0
    mean_2 = 400.0
    life_2 = calculate_fatigue_life(amp_2, mean_2, SIGMA_F_PRIME, SIGMA_UT, B)
    
    # Verify numerical sanity
    assert life_2 < life_1, "Mean stress penalty should reduce fatigue life"
    
    print(f"Case 1 (Pure Cyclic): Amp={amp_1}MPa, Mean={mean_1}MPa -> Life: {life_1:.2e} cycles")
    print(f"Case 2 (Biased Cyclic): Amp={amp_2}MPa, Mean={mean_2}MPa -> Life: {life_2:.2e} cycles")
    print(f"Penalty Ratio: {life_1/life_2:.2f}x reduction in life due to mean stress.")

if __name__ == '__main__':
    main()