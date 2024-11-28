#!/bin/bash

#echo "In benchs"
#echo $PWD

###AWS
#line=$(($AWS_BATCH_JOB_ARRAY_INDEX + 1))
#line=1
#esto estaba linea abajo del benches
#benches+=$(sed "$line!d" benchmarks.txt)
###

#Este codigo va corriendo en cada linea deterimando parametro

benches=() #Inicializar lista de nombres de param

# Explicar codigo para generar benchamrks y la logica detras
benches1=$(sed -n '46,+2p' benchmarks.txt) #Extrae cierta canitdad de nombres de benchmarks.txt

#echo "Benches before transformations"
#echo "$benches1"

#En nuestro caso tenemos que el echo nos dara
#param_cards-DeltaM_15/param_card.SeesawSM9.4.dat
#param_cards-DeltaM_15/param_card.SeesawSM9.5.dat
#param_cards-DeltaM_15/param_card.SeesawSM9.6.dat

#los benchmark estan separados por lineas, lo que hace el codigo de abajo es lo siguiente:
#comida
#carro
#benches ahora se transforma beches = ("comida", "carro")

IFS=$'\n' benches=( $benches1 ) #Separa el string por newline

#echo "Elements of benches array:"
#for bench in "${benches[@]}"; do
#    echo "$bench"
#done

for vars in "${benches[@]}"
do
    #pwd es la direccion actual y vars sera el param card luego origin = /Collider/limon/param_cards-DeltaM_15/param_card.SeesawSM9.5.dat
    origin="${PWD}/${vars}"
	#echo $origin

	#x=$(find|grep "# gNh55" "${origin}") 	
	#sed -i "s/$x/  4 0e00  # gNh55/" "${origin}"
	
	#x=$(find|grep "# gNh56" "${origin}")
        #sed -i "s/$x/  5 2.000000e-1  # gNh56/" "${origin}"

    # la linea de abajo convierte vars = /Collider/limon/param_cards-DeltaM_15/param_card.SeesawSM9.5.dat --> 9.5
	ids=$(sed 's|.dat|''|g' <<< "$vars")
	ids=$(sed 's|.*/param_card.SeesawSM|''|g' <<< "$ids")

	#echo "ids"
	#echo $ids
    
	# Usamos IFS="." para dividir la variable $ids por el punto y almacenar las partes en el array 'array'
	# echo $array solo imprime el primer elemento del array; para imprimir todos los elementos, usamos ${array[@]}

	IFS="." read -r -a array <<< "$ids"
	
	#echo "array"
	#echo ${array[@]}:

	mass=${array[0]}
	alpha=${array[1]}

	#echo "$mass $alpha"

	bash param_distZH.sh "" "M${mass}" "Alpha${alpha}" "${origin}" "$1" "$2"

	done

