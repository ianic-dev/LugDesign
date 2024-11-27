from data_ingress import MaterialProperties, LugConfig
import approx_graph_fns as fns

spec_safety_margin = 0.15

def net_section_tension(lugconfig: LugConfig, material: MaterialProperties) -> float
    ultimate_tension_load_ptu = 0
    kt = fns.stress_conc_factor_kt
    return ultimate_tension_load_ptu
