#!/bin/bash

#echo "In benchs"
#echo $PWD

#LAPTOP: comentar estas lineas
###AWS
line=$(($AWS_BATCH_JOB_ARRAY_INDEX + 1))
line=1

#Este codigo va corriendo en cada linea deterimando parametro

benches=() #Inicializar lista de nombres de param
#benches+=$(sed "$line!d" benchmarks.txt)
benches1=$(sed -n '46,+2p' benchmarks.txt) #Extrae cierta canitdad de nombres de benchmarks.txt

#echo "Benches before transformations"
#echo "$benches1"
#los benchmark estan separados por lineas, lo que hace .split es lo siguiente:
#comida
#carro
#benches ahora se transforma beches = ("comida", "carro")
# $benches1
IFS=$'\n' benches=( $benches1 ) #Separa el string por newline

#echo "Elements of benches array:"
#for bench in "${benches[@]}"; do
#    echo "$bench"
#done

for vars in "${benches[@]}"
do
    #pwd es la direccion actual y vars sera el param card luego origin = home/hola/azz/paramcard.dat
    origin="${PWD}/${vars}"
	echo $origin

	#x=$(find|grep "# gNh55" "${origin}") 	
	#sed -i "s/$x/  4 0e00  # gNh55/" "${origin}"
	
	#x=$(find|grep "# gNh56" "${origin}")
        #sed -i "s/$x/  5 2.000000e-1  # gNh56/" "${origin}"

    # <<< hace que consideres solo el string que le estes dando y ya no una direccion relativa
	ids=$(sed 's|.dat|''|g' <<< "$vars")
	ids=$(sed 's|.*/param_card.SeesawSM|''|g' <<< "$ids")
	#echo $ids
    
	#los benchmark estan separados por lineas, lo que hace .split es lo siguiente:
    #10.3
    #benches ahora se transforma beches = ("10", "3")
	#10 es es el indicador de masa
	#
	IFS="." read -r -a array <<< "$ids"
	
	mass=${array[0]}
	alpha=${array[1]}

	#LAPTOP: puede descomentar
	#echo "$mass $alpha"

	bash param_distZH.sh "" "M${mass}" "Alpha${alpha}" "${origin}" "$1" "$2"

	done

