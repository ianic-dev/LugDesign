#!/usr/bin/python
from data_ingress import LoadCase, MaterialProperties, LugConfig, FastenerConfig
from backplate import BackplatePins, evaluate_backplate, evaluate_thermal
from flange_reqs import evaluate_flange
import fastener as fst


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':

    # define all your variables here
    lug_spacing = 0.3
    test_lugconfig = LugConfig("test")
    forces = LoadCase(0, 0, -44.818, 1, 600, 0)
    pos_holes = [[0.02, 0], [-0.02, 0]]
    backplate = BackplatePins(pos_holes, test_lugconfig)
    fastener = FastenerConfig(test_lugconfig, 0.0112, 0.019, 0.019)
    delta_T_max = 95
    delta_T_min = -120

    lug_material = MaterialProperties("2014-T6")
    sc_material = MaterialProperties("spacecraft")
    fst_material = MaterialProperties("fastener")

    forces.yz_plane_load(lug_spacing)

    flange_safety_margin = evaluate_flange(test_lugconfig, lug_material, forces, True)

    backplate, xz_forces = evaluate_backplate(pos_holes, test_lugconfig, forces, fastener, lug_material, sc_material)

    evaluate_thermal(backplate, test_lugconfig, lug_material, sc_material, fst_material, fastener, xz_forces, delta_T_max)

    # print(delta_T_max)
    # print(young_modul_fastener)
    # print(area_fastener)
    # print(area_fastener)
    # print(phi_backplate)
    # print(thermal_load_backplate_maxT)






