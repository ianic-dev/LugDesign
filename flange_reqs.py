from data_ingress import LoadCase, MaterialProperties, LugConfig
import approx_graph_fns as fns
import math as m

spec_safety_margin = 0.15


def net_section_tension(lugconfig: LugConfig, material: MaterialProperties) -> float:
    ultimate_tension_load_ptu = 0
    kt: float = fns.stress_conc_factor_kt(
        lugconfig.flange_height, lugconfig.pin_diameter, material.axial_curve_number)
    tension_area: float = (lugconfig.flange_height -
                           lugconfig.pin_diameter) * lugconfig.flange_thickness
    ultimate_tension_load_ptu: float = kt * \
        material.ultimate_tensile_str * tension_area
    return ultimate_tension_load_ptu


def shear_out_bearing_ultimate(lugconfig: LugConfig, material: MaterialProperties) -> float:
    ultimate_tension_load_ptu = 0
    kbru = fns.shear_bearing_efficiency_kbr(
        lugconfig.flange_height, lugconfig.pin_diameter, lugconfig.flange_thickness)
    bearing_area = lugconfig.pin_diameter * lugconfig.flange_thickness
    ultimate_tension_load_ptu = kbru * material.ultimate_tensile_str * bearing_area
    return ultimate_tension_load_ptu


def shear_out_bearing_yield(lugconfig: LugConfig, material: MaterialProperties) -> float:
    yield_tension_load_pty = 0
    kbry = fns.shear_bearing_efficiency_kbry(
        lugconfig.flange_height, lugconfig.pin_diameter, lugconfig.flange_thickness)
    bearing_area = lugconfig.pin_diameter * lugconfig.flange_thickness
    yield_tension_load_pty = kbry * material.ultimate_tensile_str * bearing_area
    return yield_tension_load_pty


def bushing_yield(lugconfig: LugConfig, bushing_material_compressivie_yield, bushing_inner_rad) -> float:
    bushing_yield_load = 0
    area = bushing_inner_rad * lugconfig.flange_thickness * 2
    bushing_yield_load = 1.85 * bushing_material_compressivie_yield * area
    return bushing_yield_load


def transverse_load_ultimate(lugconfig: LugConfig, material: MaterialProperties) -> float:
    ultimate_transverse_load = 0
    average_area = 6/(4/((lugconfig.flange_height/2 - lugconfig.pin_diameter * m.sin(m.radians(45))) *
                      lugconfig.flange_thickness) + 2/((lugconfig.flange_height-lugconfig.pin_diameter)*lugconfig.flange_thickness/2))
    bearing_area = lugconfig.pin_diameter * lugconfig.flange_thickness
    kt_x = average_area/bearing_area  # x-axis value in ktu graph
    ktu = 0.5  # fns.transverse_ktu(kt_x, material.transverse_curve_n)
    ultimate_transverse_load = ktu * bearing_area * material.ultimate_tensile_str
    return ultimate_transverse_load


def transverse_load_yield(lugconfig: LugConfig, material: MaterialProperties) -> float:
    yield_transverse_load = 0
    average_area = 6/(4/((lugconfig.flange_height/2 - lugconfig.pin_diameter * m.sin(m.radians(45))) *
                      lugconfig.flange_thickness) + 2/((lugconfig.flange_height-lugconfig.pin_diameter)*lugconfig.flange_thickness/2))
    bearing_area = lugconfig.pin_diameter * lugconfig.flange_thickness
    kt_x = average_area/bearing_area  # x-axis value in ktu graph
    kty = 0.5  # fns.transverse_kty(kt_x, material.transverse_curve_n)
    yield_transverse_load = kty * bearing_area * material.yield_stress
    return yield_transverse_load


def evaluate_flange(lugconfig: LugConfig, material: MaterialProperties, loadcase: LoadCase) -> float:
    print("==== FLANGE EVALUATION ====\n")
    safety_margin = 0

    tension_ultimate_load = net_section_tension(lugconfig, material)
    print("Net section tension ultimate load =", tension_ultimate_load)

    shear_out_ultimate_load = shear_out_bearing_ultimate(lugconfig, material)
    print("Shear-bearing ultimate load =", shear_out_ultimate_load)

    transverse_ultimate_load = transverse_load_ultimate(lugconfig, material)
    print("Transverse ultimate load =", transverse_ultimate_load)

    axial_ratio = abs(loadcase.y_resultant) / \
        min(tension_ultimate_load, shear_out_ultimate_load)
    print("Axial actual/maximum load ratio =", axial_ratio)

    transverse_ratio = abs(loadcase.force_z)/transverse_ultimate_load
    print("Transverse actual/maximum load ratio =", transverse_ratio)

    safety_margin = 1/((axial_ratio**1.6 + transverse_ratio**1.6)**0.625) - 1
    print("Final oblique margin of safety =", safety_margin)
    return safety_margin
