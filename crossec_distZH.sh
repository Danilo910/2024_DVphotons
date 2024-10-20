#!/bin/bash

echo "crosssec"
echo $PWD

tipos="ZH WH TTH"
#tipos="ZH"

#este codigo reinicia todo el cross_section.dat
#en principio esto tambien se hace en masterZH, pero es necesario hacerlo
echo '' > "${1}/scripts_2208/data/cross_section.dat"

for tipo in ${tipos}
	do
	#declare -a arr
	
	folder_origin="${2}/val-HN_${tipo}/Events"
	cd ${folder_origin}
	#al igual que el hepmc_dist.sh, esta creando un arreglo con los archivos en folder_origin (run_01, run_02, etc)
	runs=( $(ls -d */) )
	for run in "${runs[@]}"
		do
		#entramos a run
		#echo "${run}"
		cd "${run}"
		#esta creando un arreglo con los nombres de los archivos _banner.txt
		file_mc=("$(ls -d *_banner.txt)")
		run="${run::-1}_"
		echo "${run}"
		cross=$(find|grep "Integrated" "${file_mc}")
		cross=$(sed 's| Integrated weight (pb) |''|g' <<<"$cross")
		#cross es la palabra que deseamos analizar
		cross=$(sed 's|\#|''|g' <<<"$cross")
		cross=$(sed 's|\: |''|g' <<<"$cross")
		#It effectively removes the "_banner.txt" substring from the variable's value.
		file_mc="${file_mc/_banner.txt/''}"
		file_mc="${file_mc/$run/''}"
		echo "${file_mc}	${cross}" >> "${1}/scripts_2208/data/cross_section.dat"
		#echo "${file_mc}        ${cross}" >> "/Collider/2023_LLHN_CONCYTEC/cross_section.dat"
		cd ..
	done
done
#cp ${1}/scripts_2208/data/cross_section.dat /Collider/2023_LLHN_CONCYTEC/
