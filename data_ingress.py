import pandas as pd
import numpy as np
import math as m
from pathlib import Path


class LoadCase:
    def __init__(self, f_x: float, m_x: float, f_y: float, m_y: float, f_z: float, m_z: float) -> None:
        self.force_x = f_x  # transverse load aligned with pin axis
        self.moment_x = m_x  # not carried directly by lug, moment affecting yz plane loads
        self.force_y = f_y  # force aligned with solar panel length axis
        self.moment_y = m_y  # torque around solar panel length axis
        self.force_z = f_z  # vertical force, aligned with thrust direction
        self.moment_z = m_z  # moment around thrust vector axis
#        self.yz_resultant = "N/A"  # not assigned yet
    
    def yz_plane_load(self, vert_spacing: float) -> float:
        moment_induced_y_load = self.moment_x/vert_spacing
        total_y_load = moment_induced_y_load + self.force_y
        self.yz_resultant = m.sqrt(total_y_load**2 + self.force_z**2)
        return(self.yz_resultant) # absolute value of either "F1" in the diagram


class MaterialProperties:
    def __init__(self, density: float, elasticity_modulus: float, yield_stress: float, metal: bool) -> None:
        self.density = density
        self.elasticity_modulus = elasticity_modulus
        self.yield_stress = yield_stress
        self.ismetal = metal


class LugConfig:
    def __init__(self, d1: float, d2: float, h: float, w: float, t1: float, t2: float, t3: float) -> None:
        self.pin_diameter = d1
        self.bolt_diameter = d2
        self.inter_flange_width = h
        self.flange_thickness = t1
        self.flange_height = w
        self.base_thickness = t2
        self.spacecraft_thickness = t3

    def to_csv(self, name: str="unnamed") -> None:
        filename = "config_" + name + ".csv"
        writepath = "lugconfig/"+ filename
        writepath = Path(writepath)
        config_dict: dict = vars(self)
        config_df: pd.DataFrame = pd.DataFrame.from_dict(config_dict, orient='index', columns=['Value'])
        config_df.to_csv(writepath)


def read_lugconfig_from_csv(name: str="unnamed") -> LugConfig:
    configpath = Path("lugconfig/config_" + name + ".csv")
    config = pd.read_csv(configpath).to_numpy()
    lugconfig = LugConfig(config[0, 1], config[1, 1], config[2, 1], config[3, 1], config[4, 1], config[5, 1], config[6, 1])
    return lugconfig
