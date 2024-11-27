#!/usr/bin/python
from data_ingress import LoadCase, MaterialProperties, LugConfig
from backplate import BackplatePins


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':

    #define all your variables here
    test_lugconfig = LugConfig(1, 2, 1, 1, 1, 1, 1)
    forces = LoadCase(0,0,-44.818,1,153.036,0)
    pos_holes=[[0.1,0.1],[0.1,-0.1],[-0.1,0.1],[-0.1,-0.1]]
    backplate=BackplatePins(4,pos_holes)
    fastener_diam_head=0
    fastener_diam_butt=0
    sigma_yield_SC=0
    sigma_yield_flange=0
    

    print("CG LOCATION OF HOLES")
    cg=backplate.compute_cg(test_lugconfig)
    print(cg)
    print("")

    print("XZ FORCES FOR HOLES")
    print(backplate.compute_xz_hole_force(cg,test_lugconfig,forces))
    print("")

    print("Y FORCES FOR HOLES")
    print(backplate.compute_y_hole_force(cg,test_lugconfig,forces))
    print("")




    #pull out check for backplate
    print("PULL OUT CHECK FOR BACKPLATE")
    print(backplate.pull_out_check(backplate.compute_y_hole_force(cg,test_lugconfig,forces),test_lugconfig.flange_thickness,fastener_diam_head,sigma_yield_flange))
    print("")

    #pull out check for vehicle plate
    print("PULL OUT CHECK FOR VEHICLE")
    print(backplate.pull_out_check(backplate.compute_y_hole_force(cg,test_lugconfig,forces),test_lugconfig.spacecraft_thickness,fastener_diam_butt,sigma_yield_SC))
    print("")

    #bearing check for backplate
    print("BEARING CHECK FOR BACKPLATE")
    print(backplate.bearing_check(backplate.compute_xz_hole_force(cg,test_lugconfig,forces),test_lugconfig,test_lugconfig.flange_thickness,sigma_yield_flange))
    print("")

    #bearing check for vehicle plate
    print("BEARING CHECK FOR VEHICLE")
    print(backplate.bearing_check(backplate.compute_xz_hole_force(cg,test_lugconfig,forces),test_lugconfig,test_lugconfig.spacecraft_thickness,sigma_yield_SC))
    print("")