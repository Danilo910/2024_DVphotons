import math
import numpy as np

def calculate_norm(px_n, py_n, pz_n):
    norm = np.sqrt(px_n ** 2 + py_n ** 2 + pz_n ** 2)
    return norm

# Example usage:

px_n = 3.0823200253447883e+01 
py_n = -1.0605958558274114e+01
pz_n = 6.6594322546377356e-08
En = 7.6285580385500396e+01
norm = calculate_norm(px_n, py_n, pz_n)
print("Beta 1 is:", norm/En)

px_n = 4.1074778611572825e+01
py_n = -1.3345075592685488e+01
pz_n = 4.7171717307433759e+01
En = 9.4817716668862360e+01
norm = calculate_norm(px_n, py_n, pz_n)
print("Beta 2 is:", norm/En)

px_n = 4.6583176515077561e+01
py_n = -1.2323882814183014e+01
pz_n = 4.9959946735059368e+01
En = 8.8559961041220902e+01
norm = calculate_norm(px_n, py_n, pz_n)
print("Beta 3 is:", norm/En)