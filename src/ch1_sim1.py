import numpy as np

def calculate_intrinsic_density(T, E_g=1.12):
    """
    Calculates intrinsic carrier concentration n_i for Silicon.
    T: Absolute temperature in Kelvin
    E_g: Bandgap in eV (default 1.12 for Si)
    Returns: n_i in cm^-3
    """
    # Physical Constants
    k = 8.617e-5  # Boltzmann constant in eV/K
    k_si = 1.38e-23 # Boltzmann constant in J/K
    h = 6.626e-34 # Planck constant in J*s
    m0 = 9.11e-31 # Electron mass kg
    
    # Effective masses for Silicon
    me = 1.08 * m0
    mh = 0.81 * m0
    
    # Pre-factor calculation (using SI units first, then convert to cm^-3)
    # 2 * (2 * pi * k * T / h^2)^(3/2) * (me*mh)^(3/4)
    term1 = 2 * ((2 * np.pi * k_si * T) / (h**2))**1.5
    term2 = (me * mh)**0.75
    n_i_m3 = term1 * term2 * np.exp(-E_g / (2 * k * T))
    
    return n_i_m3 * 1e-6 # Convert m^-3 to cm^-3

def main():
    print("--- Silicon Intrinsic Limit Analysis ---")
    target_doping = 1e15 # Typical source/drain doping threshold
    found_limit = False
    
    for T in range(300, 700, 20):
        ni = calculate_intrinsic_density(T)
        state = "OPERATIONAL" if ni < target_doping else "INTRINSIC FAILURE"
        
        print(f"Temp: {T}K ({T-273:3d}C) | ni: {ni:.2e} cm^-3 | Status: {state}")
        
        if ni >= target_doping and not found_limit:
            print(f"\n[!] CRITICAL THRESHOLD REACHED AT ~{T}K")
            found_limit = True
            
    # Verification check: ni at 300K should be approx 10^10 cm^-3
    ni_300 = calculate_intrinsic_density(300)
    assert 5e9 < ni_300 < 2e10, f"Calculation error: ni at 300K is {ni_300}"
    print("\nNumerical verification passed: ni(300K) is within expected order of magnitude.")

if __name__ == '__main__':
    main()