import pandas as pd
import math as m
import numpy as np
from pathlib import Path



class MaterialProperties:
    def __init__(self, density, elasticity_modulus: float = 0, yield_stress: float = 0, metal: bool = True, ultimate_stress: float = 0, curve_n: float = 0, transverse_n: float = 0, thermal_coeff: float = 0) -> None:
        if isinstance(density, str):
            (density, elasticity_modulus, yield_stress, metal,
             ultimate_stress, curve_n, transverse_n, thermal_coeff) = self.from_csv(density)
        self.density: float = density
        self.elasticity_modulus: float = elasticity_modulus
        self.yield_stress: float = yield_stress
        self.ismetal: bool = metal
        self.ultimate_tensile_str: float = ultimate_stress
        self.axial_curve_number: int = int(curve_n)
        self.transverse_curve_number: int = int(transverse_n)
        self.thermal_coeff: float = thermal_coeff

    def from_csv(self, name: str = "unnamed"):
        materialpath = Path("materials/material_" + name + ".csv")
        material = pd.read_csv(materialpath).to_numpy()
        material = [material[0, 1], material[1, 1], material[2, 1],
                    material[3, 1], material[4, 1], material[5, 1], material[6, 1], material[7, 1]]
        for i in range(len(material)):
            if str(material[i]).upper() == "TRUE":
                material[i] = True
            else:
                try:
                    material[i] = float(material[i])
                except:
                    print("here's the string")
        return material

    def to_csv(self, name: str = "unnamed") -> None:
        filename = "material_" + name + ".csv"
        writepath = "materials/" + filename
        writepath = Path(writepath)
        config_dict: dict = vars(self)
        # the following line may be indicated as an error, it isn't, it just works
        config_df: pd.DataFrame = pd.DataFrame.from_dict(
            config_dict, orient='index', columns=['Values (all in base SI units)'])
        config_df.to_csv(writepath)


class LugConfig:
    def __init__(self, d1, d2: float = 0, h: float = 0, w: float = 0, t1: float = 0, t2: float = 0, t3: float = 0, material: str = "7075-T6") -> None:
        '''
        creates a LugConfig from either a file, taking d1 as string (name of the config),
        or all values for the config specified as float.
        '''
        if isinstance(d1, str):
            (d1, d2, h, t1, w, t2, t3, material) = self.from_csv(d1)
        self.pin_diameter = d1
        self.bolt_diameter = d2
        self.inter_flange_width = h
        self.flange_thickness = t1
        self.flange_height = w
        self.base_thickness = t2
        self.spacecraft_thickness = t3
        self.material = material

    def from_csv(self, name: str = "unnamed") -> list:
        configpath = Path("lugconfig/config_" + name + ".csv")
        config = pd.read_csv(configpath).to_numpy()
        lugconfig = [config[0, 1], config[1, 1], config[2, 1],
                     config[3, 1], config[4, 1], config[5, 1], config[6, 1], config[7, 1]]
        for i in range(len(lugconfig)):
            if str(lugconfig[i]).upper() == "TRUE":
                lugconfig[i] = True
            else:
                try:
                    lugconfig[i] = float(lugconfig[i])
                except:
                    print("material:", lugconfig[i])
        return lugconfig

    def to_csv(self, name: str = "unnamed") -> None:
        filename = "config_" + name + ".csv"
        writepath = "lugconfig/" + filename
        writepath = Path(writepath)
        config_dict: dict = vars(self)
        # the following line may be indicated as an error, it isn't, it just works
        config_df: pd.DataFrame = pd.DataFrame.from_dict(
            config_dict, orient='index', columns=['Values (all in base SI units)'])
        config_df.to_csv(writepath)

class FastenerConfig:
    def __init__(self, lugconfig: LugConfig, length, head_d, butt_d) -> None:
        self.length = length
        self.head_diam = head_d
        self.butt_diam = butt_d
        self.area = (0.5 * lugconfig.bolt_diameter)**2 * m.pi
