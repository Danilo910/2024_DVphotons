from pathlib import Path
import sys
import os
import glob
from multiprocessing import Pool


def main(in_file):
    #reemplazamos el nombre del hepmc por un .root y lo volvemos un string (no modificamos el hepmc real)
    #in_file: /Collider/scripts_2208/data/raw/complete_ZH_M3_Alpha1_13.hepmc
    #out_file: /Collider/scripts_2208/data/clean/complete_ZH_M3_Alpha1_13.root
    #print("in_file\n")
    #print(in_file)
    out_file = in_file.replace('.hepmc', '.root').replace(origin, destiny)
    #print("out_file\n")
    #print(out_file)
    #estamos accediendo a Delphes_folder="/Collider/MG5_aMC_v2_9_11/Delphes", luego con el && consecutivamente
    #corremos ./DelphesHepMC2 y usamos la configuracion elphes_card_LLHNscanV5.tcl (archivo editado?)
    #finalmente obtenemos out_file como .root y el in_file como hepmc
    os.system(f'cd {sys.argv[2]} && ./DelphesHepMC2 ' 
                f'/Collider/limon/Delphes_cards/delphes_card_LLHNscanVbasic_5.tcl {out_file} {in_file} > /dev/null 2>&1')
                #f'/Collider/limon/Delphes_cards/delphes_card_LLHNscanV5.tcl {out_file} {in_file} > /dev/null 2>&1')
    return

# 1: destiny_folder="/Collider"
# 2: Delphes_folder="/Collider/MG5_aMC_v2_9_11/Delphes"
destiny_base = './data/clean'
types = ['ZH', "WH", "TTH"]
tevs = [13]
<<<<<<< HEAD
#variable externa
root = sys.argv[1]

for mode_atlas in ["", "zsimp"]:
    
    print("mode_atlas: ", mode_atlas)
    origin = root + f"/scripts_2208/data/raw/"
    destiny = root + f"/scripts_2208/data/clean{mode_atlas}/"

    Path(destiny).mkdir(exist_ok=True, parents=True)
    os.system(f'cd {destiny} && find . -name \*.root -type f -delete')

    allcases = []
    #realizamos el mismo procedimiento anterior, pero ahora para correr sobre los hepmc completos (con tf y decayv)

    if(mode_atlas == ""):
        for typex in types[:]:
            for tevx in tevs[:]:
                for file_inx in sorted(glob.glob(origin + f"full_op_{typex}*{tevx}.hepmc"))[:]:
                    allcases.append(file_inx)
    else:
        for typex in types[:]:
            for tevx in tevs[:]:
                for file_inx in sorted(glob.glob(origin + f"{zsimp}_full_op_{typex}*{tevx}.hepmc"))[:]:
                    allcases.append(file_inx)

    print("allcases", allcases)
    
    if __name__ == '__main__':
        with Pool(1) as pool:
            pool.map(main, allcases)
    
=======

#variable externa
root = sys.argv[1]
origin = root + f"/scripts_2208/data/raw/"
destiny = root + f"/scripts_2208/data/clean/"

Path(destiny).mkdir(exist_ok=True, parents=True)
os.system(f'cd {destiny} && find . -name \*.root -type f -delete')

allcases = []
#realizamos el mismo procedimiento anterior, pero ahora para correr sobre los hepmc completos (con tf y decayv)
for typex in types[:]:
    for tevx in tevs[:]:
        for file_inx in sorted(glob.glob(origin + f"full_op_{typex}*{tevx}.hepmc"))[:]:
            allcases.append(file_inx)

if __name__ == '__main__':
    with Pool(1) as pool:
        pool.map(main, allcases)
>>>>>>> 2dcdeddd8589cb0e0380f889e21c11e3e544218c
