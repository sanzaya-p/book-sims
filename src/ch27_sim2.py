import math

def calculate_fluidic_latency():
    """
    Quantifies logic-gate switching delay as a function of depth-dependent viscosity.
    Governing Equation: mu(P) = mu0 * exp(alpha * P)
    """
    # System Parameters
    mu_0 = 0.001  # Pa*s (Viscosity of water at surface)
    alpha = 2.5e-8 # Pa^-1 (Typical pressure-viscosity coefficient for high-density oils)
    density = 1050 # kg/m^3 (Deep sea water density approximation)
    gate_diameter = 0.005 # 5mm logic channel diameter
    flow_velocity_surface = 0.1 # m/s
    g = 9.81

    print(f"{'Depth (m)':<12} | {'Pressure (MPa)':<15} | {'Viscosity (mPa*s)':<18} | {'Latency Scale':<12} | {'Re':<8}")
    print("-" * 75)

    for depth in [0, 2000, 4000, 6000, 8000, 11000]:
        # Hydrostatic pressure P = rho * g * h
        pressure = density * g * depth # Pascals
        p_mpa = pressure / 1e6
        
        # Barus Equation for Viscosity at Pressure
        mu_p = mu_0 * math.exp(alpha * pressure)
        
        # Reynolds Number Re = (rho * v * D) / mu
        # In fluidic logic, as viscosity increases, Re drops, potentially killing logic function
        re = (density * flow_velocity_surface * gate_diameter) / mu_p
        
        # Latency factor (delay) scales linearly with viscosity in laminar circuits
        latency_factor = mu_p / mu_0

        print(f"{depth:<12} | {p_mpa:<15.1f} | {mu_p*1000:<18.3f} | {latency_factor:<12.2f} | {re:<8.1f}")

    # Verification check
    assert mu_p >= mu_0, "Viscosity must increase with pressure."

if __name__ == '__main__':
    calculate_fluidic_latency()