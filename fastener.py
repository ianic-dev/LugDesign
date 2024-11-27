import math as m

from data_ingress import FastenerConfig, LugConfig, MaterialProperties


def sum_L_over_A(D_shaft, A_shaft, A_head, A_nut):
    return ((0.4*D_shaft/A_shaft)+(0.5*D_shaft/A_head)+(0.4*D_shaft/A_nut))


def force_ratio(t, E_a, E_b, D_fo, D_fi, sum_L_over_A):
    delta_a = (4 * t) / (E_a * m.pi * ((D_fo ** 2) - (D_fi ** 2)))
    delta_b = (1/E_b) * sum_L_over_A
    phi = delta_a / (delta_a + delta_b)
    return phi

def force_ratio_head(lugconfig: LugConfig, material: MaterialProperties, fst_material: MaterialProperties, fastener: FastenerConfig):
    t = lugconfig.base_thickness
    E_a = float(material.elasticity_modulus)
    E_b = float(fst_material.elasticity_modulus)
    D_fo = fastener.head_diam
    D_fi = lugconfig.bolt_diameter
    sum_L_over_A = fastener.length/fastener.area
    delta_a = (4 * t) / (E_a * m.pi * ((D_fo ** 2) - (D_fi ** 2)))
    delta_b = (1/E_b) * sum_L_over_A
    phi = delta_a / (delta_a + delta_b)
    return phi

def force_ratio_butt(lugconfig: LugConfig, material: MaterialProperties, fst_material: MaterialProperties, fastener: FastenerConfig):
    t = lugconfig.base_thickness
    E_a = float(material.elasticity_modulus)
    E_b = float(fst_material.elasticity_modulus)
    D_fo = fastener.head_diam
    D_fi = lugconfig.bolt_diameter
    sum_L_over_A = fastener.length/fastener.area
    delta_a = (4 * t) / (E_a * m.pi * ((D_fo ** 2) - (D_fi ** 2)))
    delta_b = (1/E_b) * sum_L_over_A
    phi = delta_a / (delta_a + delta_b)
    return phi

def fastener_area(D_fi):
    return m.pi*0.25*(D_fi**2)
