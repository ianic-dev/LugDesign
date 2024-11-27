#!/usr/bin/python
from data_ingress import LoadCase, MaterialProperties, LugConfig
from backplate import BackplatePins
import fastener


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':

    #define all your variables here
    test_lugconfig = LugConfig(1,0.008, 1, 1, 1, 0.005, 0.005)
    forces = LoadCase(0,0,-44.818,1,153.036,0)
    pos_holes=[[0.02,0],[-0.02,0]]
    backplate=BackplatePins(2,pos_holes)
    length_fastener=0.0112
    area_fastener=fastener.fastener_area(test_lugconfig.bolt_diameter)
    fastener_diam_head=0.019
    fastener_diam_butt=0.019
    sigma_yield_SC=450000000
    sigma_yield_flange=450000000
    young_modul_backplate=72000000000
    young_modul_vehicle=72000000000
    young_modul_fastener=200000000000
    thermal_coeff_backplate=25.2*(10**(-6))
    thermal_coeff_vehicle=25.2*(10**(-6))
    thermal_coeff_bolt=13*(10**(-6))
    delta_T_max=95
    delta_T_min=-120



    

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



    #compute the thermal shit
    phi_backplate=fastener.force_ratio(test_lugconfig.base_thickness,young_modul_backplate,young_modul_fastener,fastener_diam_head,test_lugconfig.bolt_diameter,length_fastener/area_fastener)
    phi_vehicle=fastener.force_ratio(test_lugconfig.spacecraft_thickness,young_modul_vehicle,young_modul_fastener,fastener_diam_butt,test_lugconfig.bolt_diameter,length_fastener/area_fastener)

    thermal_load_backplate_maxT=(thermal_coeff_backplate-thermal_coeff_bolt)*delta_T_max*young_modul_fastener*area_fastener*(1-phi_backplate)
    thermal_load_vehicle_maxT=(thermal_coeff_vehicle-thermal_coeff_bolt)*delta_T_max*young_modul_fastener*area_fastener*(1-phi_vehicle)
    
    
    print(thermal_load_backplate_maxT)
    print(thermal_load_vehicle_maxT)
    # print(delta_T_max)
    # print(young_modul_fastener)
    # print(area_fastener)
    # print(area_fastener)
    # print(phi_backplate)
    # print(thermal_load_backplate_maxT)
    




    #pull out check for backplate
    print("PULL OUT CHECK FOR BACKPLATE")
    print(backplate.pull_out_check(backplate.compute_y_hole_force(cg,test_lugconfig,forces),test_lugconfig.base_thickness,fastener_diam_head,sigma_yield_flange))
    print("")

    #pull out check for vehicle plate
    print("PULL OUT CHECK FOR VEHICLE")
    print(backplate.pull_out_check(backplate.compute_y_hole_force(cg,test_lugconfig,forces),test_lugconfig.spacecraft_thickness,fastener_diam_butt,sigma_yield_SC))
    print("")

    #bearing check for backplate
    print("BEARING CHECK FOR BACKPLATE")
    print(backplate.bearing_check(backplate.compute_xz_hole_force(cg,test_lugconfig,forces),test_lugconfig,test_lugconfig.base_thickness,sigma_yield_flange))
    print("")

    #bearing check for vehicle plate
    print("BEARING CHECK FOR VEHICLE")
    print(backplate.bearing_check(backplate.compute_xz_hole_force(cg,test_lugconfig,forces),test_lugconfig,test_lugconfig.spacecraft_thickness,sigma_yield_SC))
    print("")