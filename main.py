#!/usr/bin/python
from data_ingress import MaterialProperties, LugConfig, FastenerConfig
from loadcase import LoadCase, loadcase_calc
from backplate import BackplatePins, evaluate_backplate, evaluate_thermal
from flange_reqs import evaluate_flange
from weight_calcs import lug_mass, fastener_mass
import fastener as fst


if __name__ == '__main__':

    # define all your variables here
    lug_spacing = 1.4
    test_lugconfig = LugConfig("iter2")
    forces = loadcase_calc(90, 180, 16)
    # print("lugconfig:", vars(test_lugconfig))
    pos_holes = [[0.013, 0], [-0.013, 0]]
    backplate = BackplatePins(pos_holes, test_lugconfig)
    fastener = FastenerConfig(test_lugconfig, test_lugconfig.base_thickness+test_lugconfig.spacecraft_thickness, 0.009, 0.009)
    print("fastener", vars(fastener))
    delta_T_max = 95
    delta_T_min = -120
    

    lug_material = MaterialProperties(test_lugconfig.material)
    sc_material = MaterialProperties("7075-T6")
    fstmat = "7075-T6"
    print("fastener material:", fstmat)
    fst_material = MaterialProperties(fstmat)

    print("mass is", lug_mass(lug_material, test_lugconfig, fastener, backplate))
    fstmass = fastener_mass(fastener, test_lugconfig, pos_holes, fst_material)
    print("total mass is", fstmass+lug_mass(lug_material, test_lugconfig, fastener, backplate))

    forces.yz_plane_load(lug_spacing)
    print("loadcase:", vars(forces))

    flange_safety_margin = evaluate_flange(test_lugconfig, lug_material, forces, True)

    backplate, xz_forces = evaluate_backplate(pos_holes, test_lugconfig, forces, fastener, lug_material, sc_material)

    evaluate_thermal(backplate, test_lugconfig, lug_material, sc_material, fst_material, fastener, xz_forces, delta_T_max)





