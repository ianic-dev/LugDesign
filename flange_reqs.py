from data_ingress import MaterialProperties, LugConfig
import approx_graph_fns as fns
import math as m

spec_safety_margin = 0.15

def net_section_tension(lugconfig: LugConfig, material: MaterialProperties) -> float:
    ultimate_tension_load_ptu = 0
    kt = fns.stress_conc_factor_kt(lugconfig.flange_height, lugconfig.pin_diameter, material.axial_curve_number)
    tension_area = (lugconfig.flange_height - lugconfig.pin_diameter) * lugconfig.flange_thickness
    ultimate_tension_load_ptu = kt * material.ultimate_tensile_str * tension_area
    return ultimate_tension_load_ptu

def shear_out_bearing_ultimate(lugconfig: LugConfig, material: MaterialProperties) -> float:
    ultimate_tension_load_ptu = 0
    kbru = fns.shear_bearing_efficiency_kbr(lugconfig.flange_height, lugconfig.pin_diameter, lugconfig.flange_thickness)
    bearing_area = lugconfig.pin_diameter * lugconfig.flange_thickness
    ultimate_tension_load_ptu = kbru * material.ultimate_tensile_str * bearing_area
    return ultimate_tension_load_ptu

def shear_out_bearing_yield(lugconfig: LugConfig, material: MaterialProperties) -> float:
    yield_tension_load_pty = 0
    kbry = fns.shear_bearing_efficiency_kbry(lugconfig.flange_height, lugconfig.pin_diameter, lugconfig.flange_thickness)
    bearing_area = lugconfig.pin_diameter * lugconfig.flange_thickness
    yield_tension_load_pty = kbry * material.ultimate_tensile_str * bearing_area
    return yield_tension_load_pty

def bushing_yield(lugconfig: LugConfig, bushing_material_compressivie_yield, bushing_inner_rad) -> float:
    bushing_yield_load = 0
    area = lugconfig.pin_diameter * lugconfig.flange_thickness
    bushing_yield_load = 1.85 * bushing_material_compressivie_yield * area
    return bushing_yield_load

