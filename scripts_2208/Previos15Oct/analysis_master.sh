#Script para asignar un valor de coupling the Higgs a n5 n5 en todos los param cards.
#!/bin/bash

echo "Analysis master"

# Variables entrantes: "$x1" "$delphes_folder"  "$destiny_folder"
# donde x1=10 000 , delphes_folder="/Collider/MG5_aMC_v2_9_11/Delphes", destiny_folder="/Collider"

#echo "01"
#python 01_making_opt_hepmc.py

#echo "02"
#python 02_run_Delphes.py "$3" "$2"

#echo "03"
#python 03_extracting_root_avoid_jet_constitu.py

#echo "03"
#python 03_extracting_root.py

#python 03_extracting_root_jetiso.py

#python 03_extracting_root_jetiso_clean.py

echo "04"

#python 04_bins_after_Delphes_Muon_Isolation.py "$1"

python 04_bins_after_Delphes_MI_Clean.py "$1"

#python 04_bins_after_Delphes_Walter.py "$1"
#python 04_cuts_after_Delphes.py "$1"

#python 04_jets_solving.py

#echo "04"
#python 04_bins_after_Delphes_jetiso_Walter.py "$1"

#05

#echo "05_com_pt_Channels.py"
#python 05_com_pt_Channels.py

#echo "05_com_pt_Merges_Channels.py"
#python 05_com_pt_Merges_Channels.py



#echo "05_simples_histograms_Channels.py"
#python 05_simples_histograms_Channels.py

#echo "05_simples_histograms_Merges_Channels.py"
#python 05_simples_histograms_Merges_Channels.py



#echo "05_deltaR_Channels.py"
#python 05_deltaR_Channels.py

#echo "05_deltaR_Merge_Channels.py"
#python 05_deltaR_Merge_Channels.py

#06

#echo "06_ISO_vs_NoISO.py"
#python 06_ISO_vs_NoISO.py
