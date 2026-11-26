import numpy as np

class VenusFlytrapLogic:
    def __init__(self, a=10.0, b=20.0, c=10.5, tau_ca=20.0):
        """
        a, b, c: Landau potential coefficients
        tau_ca: Calcium decay constant (seconds)
        """
        self.a = a
        self.b = b
        self.c = c
        self.tau_ca = tau_ca
        self.calcium = 0.0
        self.phi = -1.0 # Start in the 'open' convex state (local minimum)

    def energy(self, phi, calcium_boost):
        # Effective potential modified by turgor pressure (calcium-driven)
        # A high calcium level reduces the barrier or shifts the minima
        eff_a = self.a * (1.0 - 0.5 * calcium_boost)
        return eff_a*phi**2 - self.b*phi**4 + self.c*phi**6

    def trigger_hair(self):
        self.calcium += 1.0

    def update(self, dt):
        # Calcium decay: dC/dt = -C/tau
        self.calcium -= (self.calcium / self.tau_ca) * dt
        if self.calcium < 0: self.calcium = 0
        
        # Gradient descent on energy landscape (Simplified dynamics)
        # d_phi/dt = - dE/d_phi
        # We simulate the snap when the current state becomes unstable
        eff_a = self.a * (1.0 - 0.8 * self.calcium)
        force = -(2*eff_a*self.phi - 4*self.b*self.phi**3 + 6*self.c*self.phi**5)
        self.phi += force * dt * 5.0 # Mobility factor

def main():
    sim = VenusFlytrapLogic(tau_ca=20.0)
    dt = 0.1
    
    print("Pulse 1 at t=0s")
    sim.trigger_hair()
    
    # Simulate for 10 seconds
    for t in range(100):
        sim.update(dt)
    
    print(f"State at t=10s: Phi={sim.phi:.2f}, Calcium={sim.calcium:.2f}")
    
    print("Pulse 2 at t=10s")
    sim.trigger_hair()
    
    # Simulate for another 5 seconds
    snap_detected = False
    for t in range(50):
        sim.update(dt)
        if sim.phi > 0 and not snap_detected:
            print(f"SNAP DETECTED at t={10 + t*dt:.2f}s!")
            snap_detected = True

    # Numerical Assertion: Check that phi ended up in the other well (~ +1)
    assert sim.phi > 0.5, "Logic failed: System should have snapped."
    print(f"Final State: Phi={sim.phi:.2f}")

if __name__ == '__main__':
    main()