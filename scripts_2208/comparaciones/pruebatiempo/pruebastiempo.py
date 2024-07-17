import numpy as np

def calculate_sqrt(value):
    return np.sqrt(value) if value > 0 else 0.0

def original_calculation(pgamma, rn, Ri):
    normpgamma = np.linalg.norm(pgamma)
    pgamma_xy = pgamma[:2]
    pt_gamma = np.linalg.norm(pgamma_xy)
    
    rx_n, ry_n = rn[:2]
    px_gamma, py_gamma = pgamma_xy
    
    term1 = -(rx_n * px_gamma + ry_n * py_gamma)
    term1_c = (rx_n * py_gamma - ry_n * px_gamma)
    
    value_pro = (term1_c / (Ri * pt_gamma)) ** 2
    
    term2 = Ri * pt_gamma * calculate_sqrt(1 - value_pro)
    totalterm = term1 + term2
    
    result = normpgamma * totalterm / (pt_gamma ** 2)
    
    return result

def alternative_calculation(pgamma, rn, Ri):
    normpgamma = np.linalg.norm(pgamma)
    pgamma_xy = pgamma[:2]
    pt_gamma = np.linalg.norm(pgamma_xy)
    
    rx_n, ry_n = rn[:2]
    px_gamma, py_gamma = pgamma_xy
    
    term1 = -(rx_n * px_gamma + ry_n * py_gamma)
    term1_c = (rx_n * py_gamma - ry_n * px_gamma)
    
    if pt_gamma == 0 or Ri == 0:
        return 0.0
    
    value_pro = (term1_c / (Ri * pt_gamma)) ** 2
    
    argument_sqrt = max(0.0, 1 - value_pro)
    
    term2 = Ri * pt_gamma * calculate_sqrt(argument_sqrt)
    
    totalterm = term1 + term2
    
    if pt_gamma == 0:
        return 0.0
    
    result = normpgamma * totalterm / (pt_gamma ** 2)
    
    return result

# Case where catastrophic cancellation might occur
pgamma = np.array([-16.49938942, -3.60671866, -26.15149371] )  # Very small x and y components

rn = np.array([-130.3967339, -781.63274483, -132.21032495])  # Example vector with larger components
Ri = 1e-8  # Very small Ri

original_result = original_calculation(pgamma, rn, Ri)
alternative_result = alternative_calculation(pgamma, rn, Ri)

print("Original Result:", original_result)
print("Alternative Result:", alternative_result)



