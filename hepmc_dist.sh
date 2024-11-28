#!/bin/bash

echo "hepmc dist"
#echo $PWD

folder_destiny="${2}/scripts_2208/data/raw"

tipos="ZH WH TTH"

mkdir -p "${folder_destiny}"

for tipo in ${tipos}
	do
	#declare -a arr
	#estas tres lineas de codigo crean un directorio en la locacion folder_origin  y trabaja en este. Luego crea un arreglo
	#que contine los nombres de los subdirectorios en el direccion donde trabaja actualmente.
	folder_origin="${1}/val-HN_${tipo}/Events"
	cd ${folder_origin} > /dev/null 2>&1
	echo $PWD
	#en este caso runs son carpetas (se nombran con run_01, run_02, run_03 ...	)
	runs=( $(ls -d */) )
	# el / al parecer cambia la sintaxis, en ese caso mejor seria?
	#runs=( $(ls -d *) )
	#echo "${runs}"
	for run in "${runs[@]}"
		do
		cd "${run}"
		echo "${run}"
		count="$(ls -1 *.hepmc 2>/dev/null | wc -l)"
		echo "${count}"
		if [ $count == 0 ]
			then
			#echo "hola"
			file_gz=("$(ls -d *.hepmc.gz)")
			gzip -dk "${file_gz}"
		fi
		file_mc=("$(ls -d *.hepmc)")
		echo "${file_mc}"
		file_final="$(echo "${file_mc}" | sed 's/_pythia8_events//')"
		mv "${file_mc}" "${folder_destiny}/run_${file_final}"	
		cd ..
	done
done
