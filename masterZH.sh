#!/bin/bash
# La línea #!/bin/bash al principio del script no es un comentario, sino una indicación
# para el sistema de que debe usar Bash como intérprete al ejecutar este script.

cd limon #esta linea manda al bash dentro de la carpeta

echo "Este script se ejecuta en Bash"

#echo "El shell predeterminado del usuario es: $SHELL"
# la linea de arriba no es necesaria pues tanto en el servidor como en la computadora personal se tiene
# echo $SHELL   ---> /bin/bash, en otras palabras, la configuracion habitual del interprte de comandos es bash
# igual se puede poner para verificar

x1=5 #esto indica el numero de eventos que genera madgraph

#folder donde tenemos madgraph
madgraph_folder="/Collider/MG5_aMC_v2_9_11"
#folder donde tenemos delphes
delphes_folder="/Collider/MG5_aMC_v2_9_11/Delphes"
#donde se va a crear el folder que deseamos
destiny_folder="/Collider"


#removemos las carpetas
#The code removes the directory located at "/Collider/scripts_2208" and all its contents, 
#and it does so without asking for confirmation (-rf options). 
#The destiny_folder variable is used to specify the base directory where the "scripts_2208" directory is located.

#rm -rf "${destiny_folder}/scripts_2208"

# When you run this command, it creates the directory structure:

#/Collider
# scripts_2208
#  data
#   raw

#mkdir -p "${destiny_folder}/scripts_2208/data/raw" #crea la estructura para guardar los datos del analisis

#the command extracts the contents of the specified compressed archive 
#file (heavNeff4_UFO.tar.xz) that is in limon into the directory ${madgraph_folder}/models/
#tar -xf heavNeff4_UFO.tar.xz -C "${madgraph_folder}/models/"

#el sed remplaza patrones (edita archivos de texto)

# en el archivo mg5_configuration.txt se tiene lo siguiente:
##! Default Running mode
#!  0: single machine/ 1: cluster / 2: multicore
#run_mode = 2

#Las tres configuraciones significan lo siguiente
# El parámetro 'run_mode' controla el modo de ejecución de MadGraph:
# 0: single machine (usa un solo núcleo),
# 1: cluster (distribuye el trabajo en un clúster),
# 2: multicore (distribuye el trabajo en múltiples núcleos de una máquina local).
# Actualmente, el modo multicore (2) es el más utilizado para aprovechar CPUs de múltiples núcleos.


#con sed buscamos en el archivo input/mg5_configuration.txt el string run_mode=2 y lo remplaza por run_mode=2
#no se realiza ningun cambio pues remplazamos run_mode = 2 por run_mode = 2, pero igual se pone si se desea editar


#sed -i 's+run_mode = 2+run_mode = 2+' ${madgraph_folder}/input/mg5_configuration.txt

#normalmente se pone la canitdad de cores de 10 el cual se puede variar si deseas

#sed -i 's+nb_core = 4+nb_core = 1+' ${madgraph_folder}/input/mg5_configuration.txt


#el codigo de abajo solo es necesario si se tiene una nueva imagen de docker ya que esta cambiara las interfaces
#mv "$madgraph_folder/madgraph/interface/madevent_interface.py" "$madgraph_folder/madgraph/interface/madevent_interface-default.py"
#cp "./madevent_interface.py" "$madgraph_folder/madgraph/interface/madevent_interface.py"


#seteamos en madgraph folder pues cuando abrimos el archivo como tal, tiene 
#una direccion ficticia que se llama output FOLDER/ la cual es reemplzada
#la variable madgraph_folder es madgraph_folder="/Collider/MG5_aMC_v3_3_2"
# esta se remplaza por la palabra FOLDER en mg5_launches.txt y se crea un nuevo
#txt con esta edicion llamado mg5_launches_proper.txt. La g hace referencia a global
#por lo que el cambio se hace en todas las palabras FOlDER que aparezcan
#sed "s|FOLDER|$madgraph_folder|g" mg5_launches.txt > mg5_launches_proper.txt

#este codigo solo genera los esqueletos, todavia no afecta los paramcards
#${madgraph_folder}/bin/mg5_aMC mg5_launches_proper.txt #> /dev/null 2>&1  

#bash benchsZH.sh "$x1" "$madgraph_folder"
#este segundo no debería ser activado, pero lo hacemos simplemente por tema de debuggeo
#en el server corre correctamente generando los eventos deseados
#bash hepmc_dist.sh "$madgraph_folder" "$destiny_folder"
#bash crossec_distZH.sh "$destiny_folder" "$madgraph_folder"

source ~/.bashrc
cd ./scripts_2208/
echo $PYTHONPATH
bash analysis_master.sh "$x1" "$delphes_folder"  "$destiny_folder"

echo "Done!"