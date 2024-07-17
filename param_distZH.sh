#!/bin/bash

function changing () {
	x=$(find|grep "$1" "${run_path}")
	#echo "$1"
	#echo "$2"
	#estamos cambiando el argumento 1 por el argumento 2 dentro de run_path
	#al imprimir x, no sale en espacio en blanco, esto debido a que ya hicimos el cambio y no encuentra ahora
	# nada de lo que buscamos. Por default nos da un espacio en blanco en este caso.
	#el dev/null al final sirve para hacer un cambio silencioso sin ningun output
	sed -i "s/$x/$2/g" "${run_path}" > /dev/null 2>&1
	#echo "$x"
}

function run_mg5 () {
	#en realidad no es necesario hacer un loop para este caso ya que se tiene
	#tevs="13"
	#el cual no es una lista y por lo tanto el loop corre una sola iteracion
	#de todas formas se puede dejar asi en caso despues se generalice para distintas energias
	for tev in $tevs
		do
		#Por que fue necesario realizar esta conversion? Es de TeV -> GeV en cada beam
		tev_="$((tev*1000/2))"
		# Define las energias de los beams en el run_card
		beam1="     ${tev_}.0     = ebeam1  ! beam 1 total energy in GeV"
		beam2="     ${tev_}.0     = ebeam2  ! beam 2 total energy in GeV"
		changing " = ebeam1 " "$beam1"
		changing " = ebeam2 " "$beam2"
		
		# Le da el tag apropiado al run
		#example: tag="  some_channel_42_3_13     = run_tag ! name of the run "
		tag="  ${channel}_${mindex}_${aindex}_${tev}     = run_tag ! name of the run "
		#echo $tag
		#exit 0
		changing " = run_tag " "$tag"
			
		#Copia el param_card correspondiente
		#no confundir param_card con run_card, hasta ahora hemos cambiado el run_card
		#el param_card en nuestra carpeta personal tiene otro nombre (etiqueta de masa)
		#pero ahora estamos copiando este y lo estamos sobreescribiendo en folder_destiny
		#elimando el param_card antiguo
		filename_d="${folder_destiny}/param_card.dat"
		cp "${filename_o}" "${filename_d}" 
			
		# Correr el run
		cd "${folder_destiny}"
		cd ..
		#madevenet entra linea por linea en config_path
		./bin/madevent "${config_path}" #> /dev/null 2>&1
	done
}

#echo "Param_dist"
#echo $PWD

#indice de masa
mindex="$2"
aindex="$3"
filename_o="$4"
config_path="${PWD}/HN_run_config.txt"

tevs="13"

small="  1e-12 = small_width_treatment"
nevents="  ${5} = nevents ! Number of unweighted events requested "
ct="  0 = time_of_flight ! threshold (in mm) below which the invariant livetime is not written (-1 means not written)"
decay="   True  = cut_decays    ! Cut decay products "

pta_min=" 10.0  = pta       ! minimum pt for the photons "
ptl_min=" 10.0  = ptl       ! minimum pt for the charged leptons "
ptl_min_WH=" 5.0  = ptl       ! minimum pt for the charged leptons "
ptj_min=" 25.0  = ptj       ! minimum pt for the jets "
etaa_max=" 2.4  = etaa    ! max rap for the photons "
etal_max="# 2.5  = etal    ! max rap for the charged leptons"
etapdg_max=" {11: 2.5, 13: 2.7, 15: 5.0} = eta_max_pdg ! rap cut for other particles (syntax e.g. {6: 2.5, 23: 5})"
ptcl_min=" 27.0  = xptl ! minimum pt for at least one charged lepton "
etaj_max=" -1.0 = etaj    ! max rap for the jets "
drjj_min=" 0.0 = drjj    ! min distance between jets "
drjl_min=" 0.0 = drjl    ! min distance between jet and lepton "
r0gamma="  0.0 = R0gamma ! Radius of isolation code"
 
###################

#procesos con los que hemos trabajado hasta ahora
tipos="ZH WH TTH"

#tipos puede recibir strings y los separa por espacios
for channel in ${tipos}
	do
	#revisar mg5_launches_proper ya que alli se ve como se crean los archivos val-HN etc, los cuales estan dentro
	#de MG5_aMC
	#despues de fijar este folder destiny (por ejemplo para el proceso WH) entonces fijamos el run_path
	#run_path es el archivo que se va a analizar mas adelante, en este caso donde se realizara el changing
	#apropiado para asi describir mejor el texto. El archivo .dat es puro texto que mas adelante (string)
	#los numeros se convertiran en float internamente con Madgraph
	folder_destiny="${6}/val-HN_${channel}/Cards"
	run_path="${folder_destiny}/run_card.dat"

	changing " = small_width_treatment "  "$small"
	changing " = nevents "  "$nevents"
	changing " = time_of_flight "  "$ct"
	changing " = cut_decays "  "$decay"
	changing " = pta "  "$pta_min"
	changing " = ptl "  "$ptl_min"
	if [ $channel == "WH" ]
		then
		#en el caso de WH si varia un poco el ptl_min. No deberia ser lo mismo para todos los casos?
		changing " = ptl "  "$ptl_min_WH"
	#fi is the end of the if statement
	fi
	changing " = ptj "  "$ptj_min"
	changing " = etaa "  "$etaa_max"
	changing " = etal "  "$etal_max"
	changing " = eta_max_pdg "  "$etapdg_max"
	changing " = xptl"  "$ptcl_max"
	changing " = etaj " "$etaj_max"
	changing " = drjj " "$drjj_min"
	changing " = drjl " "$drjl_min"
	changing " = R0gamma " "$r0gamma"
	
	run_mg5 "$channel"

done
