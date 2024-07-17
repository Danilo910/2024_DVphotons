from decimal import Decimal, getcontext

# Set the precision for decimal calculations
getcontext().prec = 30  # Adjust the precision as needed

# Given values as Decimals for high precision
tiempo_higgs_decae_neutrinos = Decimal('1.1302525652919812e-07')
tiempo_N16_decae_neutrinoN14 = Decimal('1.2899256001623454e-07')
tiempo_N14_decae_foton = Decimal('5.9282555998712826e+02')

# Speed of light
c_speed = Decimal('299792458')

# Calculate tiempo_higgs_neutrino
tiempo_higgs_neutrino = tiempo_higgs_decae_neutrinos + tiempo_N16_decae_neutrinoN14 + tiempo_N14_decae_foton

# Calculate tiempo_N16_foton
tiempo_N16_foton = tiempo_N16_decae_neutrinoN14 + tiempo_N14_decae_foton

# Calculate the ratios
tiempo_higgs_neutrino_over_c = tiempo_higgs_neutrino / c_speed
tiempo_N16_foton_over_c = tiempo_N16_foton / c_speed
tiempo_N14_decae_foton_over_c = tiempo_N14_decae_foton / c_speed

# Print the results
print(f'tiempo_higgs_neutrino / c_speed: {tiempo_higgs_neutrino_over_c}')
print(f'tiempo_N16_foton / c_speed: {tiempo_N16_foton_over_c}')
print(f'tiempo_N14_decae_foton / c_speed: {tiempo_N14_decae_foton_over_c}')

# Calculate tiempo_higgs_neutrino
tiempo_higgs_neutrino = -tiempo_higgs_decae_neutrinos - tiempo_N16_decae_neutrinoN14 + tiempo_N14_decae_foton

# Calculate tiempo_N16_foton
tiempo_N16_foton = -tiempo_N16_decae_neutrinoN14 + tiempo_N14_decae_foton

# Calculate the ratios
tiempo_higgs_neutrino_over_c = tiempo_higgs_neutrino / c_speed
tiempo_N16_foton_over_c = tiempo_N16_foton / c_speed
tiempo_N14_decae_foton_over_c = tiempo_N14_decae_foton / c_speed

# Print the results
print(f'tiempo_higgs_neutrino / c_speed resta: {tiempo_higgs_neutrino_over_c}')
print(f'tiempo_N16_foton / c_speed resta: {tiempo_N16_foton_over_c}')
print(f'tiempo_N14_decae_foton / c_speed resta: {tiempo_N14_decae_foton_over_c}')