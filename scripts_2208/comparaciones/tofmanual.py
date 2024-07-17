import numpy as np

c_speed = 299792458	#m/s
tiempo_higgs_decae_neutrinos = 1.1302525652919812e-07
tiempo_N16_decae_neutrinoN14 = 1.2899256001623454e-07
tiempo_N14_decae_foton = 5.9282555998712826e+02

tiempo_higgs_neutrino = tiempo_higgs_decae_neutrinos + tiempo_N16_decae_neutrinoN14 + tiempo_N14_decae_foton
tiempo_N16_foton = tiempo_N16_decae_neutrinoN14 + tiempo_N14_decae_foton
tiempo_N14_decae_foton = 5.9282555998712826e+02

print("opcion 1 tiempo_higgs_neutrino: ",tiempo_higgs_neutrino/c_speed)
print("opcion 2 tiempo_N16_foton: ",tiempo_N16_foton/c_speed)
print("opcion 3 tiempo_N14_decae_foton: ",tiempo_N16_foton/c_speed)

