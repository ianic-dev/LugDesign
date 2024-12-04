#!/usr/bin/python
from data_ingress import MaterialProperties, LugConfig, FastenerConfig
from loadcase import LoadCase, loadcase_calc
from backplate import BackplatePins, evaluate_backplate, evaluate_thermal
from flange_reqs import evaluate_flange
from weight_calcs import lug_mass
import fastener as fst
# change

def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':

    # define all your variables here
    lug_spacing = 1.4
    test_lugconfig = LugConfig("iter1")
    # print("lugconfig:", vars(test_lugconfig))
    forces = loadcase_calc(90, 180, 5.2)
    print("lugconfig:", vars(test_lugconfig))
    pos_holes = [[0.02, 0], [-0.02, 0]]
    backplate = BackplatePins(pos_holes, test_lugconfig)
    fastener = FastenerConfig(test_lugconfig, 0.0112, 0.009, 0.009)
    delta_T_max = 95
    delta_T_min = -120

    lug_material = MaterialProperties("7075-T6")
    # print("lug material", vars(lug_material))
    sc_material = MaterialProperties("7075-T6")
    fst_material = MaterialProperties("7075-T6")

    print("mass is", lug_mass(lug_material, test_lugconfig, fastener, backplate))

    forces.yz_plane_load(lug_spacing)

    flange_safety_margin = evaluate_flange(test_lugconfig, lug_material, forces, True)

    backplate, xz_forces = evaluate_backplate(pos_holes, test_lugconfig, forces, fastener, lug_material, sc_material)

    evaluate_thermal(backplate, test_lugconfig, lug_material, sc_material, fst_material, fastener, xz_forces, delta_T_max)





