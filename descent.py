import math
import numpy as np

def get_mass(r_1, r_2, h, t_rocket, d_rocket):
  sa = math.pi * (r_1**2 - r_2**2) + 2 * math.pi * r_1 * h + 2 * math.pi * r_2 * h
  v = sa * t_rocket
  return v * d_rocket

def calculate_obj(a, C, t_wheel, t_rocket, d_wheel, d_rocket, h_rocket, r_rocket, alpha, beta, r_1, r_2, h):
  omega = math.sqrt(a/r_1)

  KE = 1/2 * math.pi * (r_1**2 - r_2**2 + 2*h*r_1 + 2*h*r_2)*t_wheel * d_wheel * r_1**2 * omega**2 + math.pi * (r_rocket + h_rocket) * t_rocket * d_rocket * r_rocket**3 * omega**2
  V = math.pi * (r_1**2 - r_2**2) * h

  obj = alpha * KE - beta * V/C

  obj_grad_omega_KE = omega* math.pi * (r_1**2 - r_2**2 + 2*h*r_1 + 2*h*r_2)*t_wheel * d_wheel * r_1**2 + 2 * omega * math.pi * (r_rocket + h_rocket) * t_rocket * d_rocket * r_rocket**3
  obj_grad_omega = alpha * obj_grad_omega_KE

  obj_grad_r_1_KE = math.pi * d_wheel * omega**2 * t_wheel * r_1 * (2*r_1**2+3*h*r_1 - r_2**2 + 2*h*r_2)
  obj_grad_r_1_V = math.pi * (2*r_1) * h
  obj_grad_r_1 = alpha * obj_grad_r_1_KE - beta * obj_grad_r_1_V

  obj_grad_r_2_KE = -math.pi * d_wheel * omega**2 * r_1**2 * t_wheel * (r_2 - h)
  obj_grad_r_2_V = math.pi * ( -2*r_2) * h
  obj_grad_r_2 = alpha * obj_grad_r_2_KE - beta * obj_grad_r_2_V

  obj_grad_h_KE = math.pi * r_1**2 * d_wheel * t_wheel * omega**2 * (r_1 + r_2)
  obj_grad_h_V = math.pi * (r_1**2 - r_2**2)
  obj_grad_h = alpha * obj_grad_h_KE - beta * obj_grad_h_V


  return obj, omega, obj_grad_omega, obj_grad_r_1, obj_grad_r_2, obj_grad_h, KE, V


def grad_descent(a, C, t_wheel, t_rocket, d_wheel, d_rocket, h_rocket, r_rocket, alpha, beta, alpha_grad):
  epsilon = 10

  # initial guesses
  omega = 0.562
  r_1 = 32
  r_2 = 30
  h = 68 * C/(math.pi * (r_1**2 - r_2**2))

  obj = None
  while True:
    if omega > 0.733:
      print("constraint violation - omega too large", omega)
      omega = 0.733
    if r_1 < 12.2:
      print("constraint violation - outer radius too small", r_1)
      r_1 = 12.2

    if omega < 0.1:
      print("constraint violation - omega too small", omega)
      omega = 0.1
    if r_2 < r_rocket:
      print("constraint violation - r_2 too small", r_2)
      r_2 = r_rocket
    if h < 2:
      print("constraint violation - h too small", h)
      h = 2
    
    if  (r_1 - r_2) < 2:
      print("constraint violation - radii too close", r_1, r_2)
      r_2 = r_1 - 2
    
    new_obj, omega, obj_grad_omega, obj_grad_r_1, obj_grad_r_2, obj_grad_h, _, _ = calculate_obj(a, C, t_wheel, t_rocket, d_wheel, d_rocket, h_rocket, r_rocket, alpha, beta, r_1, r_2, h)
    print(new_obj, omega, r_2, h)
    if obj and abs(obj-new_obj) < epsilon:
      return new_obj, r_1, omega, r_2, h
    obj = new_obj
    r_2 -= alpha_grad * obj_grad_r_2
    h -= alpha_grad * obj_grad_h
    
    omega_constr_grad = 2 * r_1 * omega
    r_1_constr_grad = omega**2

    obj_grad = np.array([obj_grad_omega, obj_grad_r_1])
    obj_constr = np.array([omega_constr_grad, r_1_constr_grad])

    # normalize
    obj_grad = obj_grad/np.linalg.norm(obj_grad)
    obj_constr = obj_constr/np.linalg.norm(obj_constr)

    if obj_grad @ obj_constr < 0:
      obj_constr = -1 * obj_constr
    
    diff = obj_grad - obj_constr

    omega -= diff[0]
    r_1 -= diff[1]