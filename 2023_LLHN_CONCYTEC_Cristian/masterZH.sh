#!/bin/bash

cd 2023_LLHN_CONCYTEC
#$SHELL

x1=10000

madgraph_folder="/Collider/MG5_aMC_v2_9_11"
delphes_folder="/Collider/MG5_aMC_v2_9_11/Delphes"
destiny_folder="/Collider"

rm -rf "${destiny_folder}/scripts_2208"
mkdir -p "${destiny_folder}/scripts_2208/data/raw"

tar -xf DarkPhotonScalarLLP.tar.xz -C "${madgraph_folder}/models/"

echo "Copiamos y pegamos el madgraph interface."
mv "$madgraph_folder/madgraph/interface/madevent_interface.py" "$madgraph_folder/madgraph/interface/madevent_interface-default.py"
cp "./madevent_interface.py" "$madgraph_folder/madgraph/interface/madevent_interface.py"

sed -i 's+run_mode = 2+run_mode = 2+' ${madgraph_folder}/input/mg5_configuration.txt
sed -i 's+nb_core = 4+nb_core = 4+' ${madgraph_folder}/input/mg5_configuration.txt

sed "s|FOLDER|$madgraph_folder|g" mg5_launches.txt > mg5_launches_proper.txt

${madgraph_folder}/bin/mg5_aMC mg5_launches_proper.txt #> /dev/null 2>&1  

echo "Corremos benchsZH.sh"
bash benchsZH.sh "$x1" "$madgraph_folder"
#bash hepmc_dist.sh "$madgraph_folder" "$destiny_folder"
bash crossec_distZH.sh "$destiny_folder" "$madgraph_folder"

echo "deberiamos tener las crossec"
source ~/.bashrc

cd ./scripts_2208/
echo $PYTHONPATH
bash analysis_master.sh "$x1" "$delphes_folder"  "$destiny_folder"

echo "Done!"