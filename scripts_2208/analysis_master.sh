#Script para asignar un valor de coupling the Higgs a n5 n5 en todos los param cards.
#!/bin/bash

echo "Analysis master"

# Variables entrantes: "$x1" "$delphes_folder"  "$destiny_folder"
# donde x1=500 , delphes_folder="/Collider/MG5_aMC_v2_9_11/Delphes", destiny_folder="/Collider"
#echo "01"
#python 01_cases_hepmc_reader.py
#echo "02"
#python 02_cases_photons_data.py
#echo "03"
#python 03_making_complete_hepmc.py
#echo "04"
#python 04_run_Delphes_danilo.py "$3" "$2"
#echo "05"
#python 05_extracting_root_no_cuts.py 
#echo "06"
#python 06_bins_after_Delphes_danilo.py "$1"
#echo "07"
#python "07a_making_graphs (copy).py"
#echo "09"
#python 09_contour_graphs.py

#Optimizacion

#echo "03"
#python 03_making_full_hepmc.py

#echo "01"
#python 01_optimizacion.py

#echo "03"
#python 03_making_full_exec_hepmc2.py

#echo "prueba"
#python prueba1.py

#echo "03"
#python 03_making_full_exec_hepmc.py

#echo "masparecidosinselec"
#python masparecidosinselec.py

#echo "comp"
#python comparehepmc.py

#echo "comp"
#python comparewrite.py

#echo "comp"
#python comparewriteoptm.py


#echo "continue"
#python continuefunction.py

#echo "01"
#python 01_beta.py

#echo "02"
#python 02_beta.py

#echo "searchtau"
#python searchctau.py

#echo "calculomanual"
#python calculomanual.py

#echo "masparecido3"
#python masparecido3.py

#echo "codigoWalter"
#python 03_making_full_selection_hepmc.py

#echo "codigoWalter"
#python 03_making_full_selection_hepmc.py

#echo "codigoWalter"
#python 03_ultimo_full_selection_hepmc.py

#echo "codigoWalter"
#python masparecidofinal.py

#echo "codigoWalter"
#python masparecidounidades.py

#echo "datacompletoa"
#python datacompletoa.py

#echo "datacompletob"
#python datacompletob.py

#echo "memoria2"
#python memoria2.py

#echo "datacompletoadescargado"
#python datacompletoadescargado.py

#echo "datacompleto_1D"
#python datacompleto_1D.py

#echo "datacompletoa_debbug.py"
#python datacompletoa_debbug.py


#TRUES Cristian

#echo "01_TrueCR"
#python 01_cases_hepmc_reader_true.py
#echo "02_TrueCR"
#python 02_cases_photons_data_true.py
#echo "03_TrueCR"
#python 03_making_complete_hepmc_true.py

#Trues WD

#echo "01_TrueWD"
#python datacompleto_1D_true.py


#Functiones 
#echo "datacompleto_1D_functions.py"
#python datacompleto_1D_functions.py

#echo "analisis_f_max_pt.py"
#python analisis_f_max_pt.py

#echo "analisis_f.py"
#python analisis_f.py

#echo "analisis_f_max_pt_selection_4.py"
#python analisis_f_max_pt_selection_4.py

#echo "analisis_f_max_pt_selection_5.py"
#python analisis_f_max_pt_selection_5.py

#echo "analisis_f_max_pt_selection_6.py"
#python analisis_f_max_pt_selection_6.py

echo "06_basics_observables"
python 06_basics_observables.py "$1"