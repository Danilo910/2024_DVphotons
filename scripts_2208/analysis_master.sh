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

#echo "06_basics_observables"
#python 06_basics_observables.py "$1"

#echo "06_deltaR"
#python 06_deltaR.py

#echo "06_graphics_compare_pt.py"
#python 06_graphics_compare_pt.py

#echo "06_deltaR_tracks"
#python 06_deltaR_tracks.py

#echo "06_basics_observables_merge"
#python 06_basics_observables_merge.py

#echo "06_track_iso"
#python 06_track_iso.py

#echo "06_track_iso2"
#python 06_track_iso2.py

#Cuatro archivos finales

#echo "04_run_Delphes_danilo.py"
#python 04_run_Delphes_danilo.py "$3" "$2"

#echo "05_extracting_root_no_cuts.py "
#python 05_extracting_root_no_cuts.py 

#echo "06_merge_opt"
#python 06_merge_opt.py

#echo "06_basics_observables_merge_analisis"
#python 06_basics_observables_merge_analisis.py

#echo "06_compare_pt_opti.py"
#python 06_compare_pt_opti.py

#echo "06_track_opt2"
#python 06_track_opt2.py

#echo "06_track_iso3"
#python 06_track_iso3.py

#echo "06_deltaR_dfpickle"
#python 06_deltaR_dfpickle.py

#echo "06_deltaR_correct_merge.py"
#python 06_deltaR_correct_merge.py

#Cuatro archivos finales version 2

#echo "05_extracting_root_no_cuts.py "
#python 05_extracting_root_no_cuts.py 

#Iso

#echo "06_deltaR_dfpickle_iso"
#python 06_deltaR_dfpickle_iso.py

#echo "06_deltaR_correct_merge_iso.py"
#python 06_deltaR_correct_merge_iso.py

#No iso

#echo "06_deltaR_dfpickle"
#python 06_deltaR_dfpickle.py

#echo "06_deltaR_correct_merge.py"
#python 06_deltaR_correct_merge.py

#opt

#echo "06_deltaR_dfpickle_opt"
#python 06_deltaR_dfpickle_opt.py

#echo "comparacion_deltaR.py"
#python comparacion_deltaR.py

#echo "06_simples_correct_merge.py"
#python 06_simples_correct_merge.py

#echo "06_com_pt_Merges_Channels.py"
#python 06_com_pt_Merges_Channels.py

#echo "06_simples_histograms_Channels.py"
#python 06_simples_histograms_Channels.py

#echo "06_simple_histograms_Merges_Channels.py"
#python 06_simple_histograms_Merges_Channels.py

#Codigos _06

echo "06_com_pt_Channels.py"
python 06_com_pt_Channels.py

echo "06_com_pt_Merges_Channels.py"
python 06_com_pt_Merges_Channels.py



#echo "06_simples_histograms_Channels.py"
#python 06_simples_histograms_Channels.py

#echo "06_simples_histograms_Merges_Channels.py"
#python 06_simples_histograms_Merges_Channels.py



#echo "06_deltaR_Channels.py"
#python 06_deltaR_Channels.py

#echo "06_deltaR_Merge_Channels.py"
#python 06_deltaR_Merge_Channels.py

#echo "06_ISO_vs_NoISO.py"
#python 06_ISO_vs_NoISO.py

