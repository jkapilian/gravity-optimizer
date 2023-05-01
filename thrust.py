import math

# CONSTANTS
m_i = 2.2e-25
q = 1.6e-19
c = 3e8

def rotations(KE, I_beam, V_beam, r_1):
    return KE/(I_beam * math.sqrt(2*V_beam * (m_i)/q)*r_1)

def rot_time(d_theta, omega):
    t = 2 * d_theta/omega
    return t

def ion_velocity(V_beam):
    return math.sqrt(2*V_beam * q/m_i)

def prop_mass(m, omega, r_1, v_i):
    v_r = omega * r_1
    mass_ratio = math.e**(v_r/v_i)
    return (mass_ratio - 1) * m