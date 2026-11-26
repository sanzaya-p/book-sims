import numpy as np

def calculate_mechanical_clock():
    """
    Analyzes the speed ceiling of mechanical logic based on 
    material properties and gate chain depth.
    """
    # Material Database (E in GPa, density in kg/m^3)
    materials = {
        "Silicon": {"E": 170e9, "rho": 2330},
        "Alumina": {"E": 380e9, "rho": 3950},
        "Diamond": {"E": 1200e9, "rho": 3510}
    }
    
    gate_length = 0.005  # 5mm
    logic_depth = 10     # Number of serial gates in a path
    
    print(f"--- Acoustic Logic Scaling (L_gate={gate_length*1000}mm, Depth={logic_depth}) ---")
    
    for mat_name, props in materials.items():
        # Speed of sound c = sqrt(E / rho)
        c_sound = np.sqrt(props['E'] / props['rho'])
        
        # Governing Equation E2
        f_max = c_sound / (gate_length * logic_depth)
        
        # Calculate time-of-flight per bit
        period = 1.0 / f_max
        
        print(f"{mat_name:10} | c: {c_sound:6.1f} m/s | f_max: {f_max/1000:7.2f} kHz")

    # Verification of dimensional sanity
    # f [1/s] = c [m/s] / (L [m] * N [unitless]) -> Valid
    test_val = materials['Alumina']['E'] / materials['Alumina']['rho']
    assert np.sqrt(test_val) > 9000, "Speed of sound for Alumina seems incorrect."

if __name__ == '__main__':
    calculate_mechanical_clock()