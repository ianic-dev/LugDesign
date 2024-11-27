import pandas as pd
import math as m
import numpy as np
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
    def __init__(self, density, elasticity_modulus: float, yield_stress: float, metal: bool, UTS: float, curve_n: float) -> None:
        if isinstance(density, str):
            (density, elasticity_modulus, yield_stress, metal, UTS, curve_n) = self.from_csv(density)
        self.density = density
        self.elasticity_modulus = elasticity_modulus
        self.yield_stress = yield_stress
        self.ismetal = metal
        self.ultimate_tensile_str = UTS
        self.axial_curve_number = int(curve_n)
    def from_csv(self, name: str="unnamed") -> list:
        materialpath = Path("materials/material_" + name + ".csv")
        material = pd.read_csv(materialpath).to_numpy()
        material = [material[0, 1], material[1, 1], material[2, 1], material[3, 1], material[4, 1], material[5, 1]]
        return material

class LugConfig:
    def __init__(self, d1, d2: float=0, h: float=0, w: float=0, t1: float=0, t2: float=0, t3: float=0) -> None:
        '''
        creates a LugConfig from either a file, taking d1 as string (name of the config),
        or all values for the config specified as float.
        '''
        if isinstance(d1, str):
            (d1, d2, h, w, t1, t2, t3) = self.from_csv(d1)
        self.pin_diameter = d1
        self.bolt_diameter = d2
        self.inter_flange_width = h
        self.flange_thickness = t1
        self.flange_height = w
        self.base_thickness = t2
        self.spacecraft_thickness = t3

    def from_csv(self, name: str="unnamed") -> list:
        configpath = Path("lugconfig/config_" + name + ".csv")
        config = pd.read_csv(configpath).to_numpy()
        lugconfig = [config[0, 1], config[1, 1], config[2, 1], config[3, 1], config[4, 1], config[5, 1], config[6, 1]]
        return lugconfig
    
    def to_csv(self, name: str="unnamed") -> None:
        filename = "config_" + name + ".csv"
        writepath = "lugconfig/"+ filename
        writepath = Path(writepath)
        config_dict: dict = vars(self)
        # the following line may be indicated as an error, it isn't, it just works
        config_df: pd.DataFrame = pd.DataFrame.from_dict(config_dict, orient='index', columns=['Values (all in base SI units)'])
        config_df.to_csv(writepath)



class BackplatePins:
    #pos_holes - 2D array storing x and z positions of the holes (in that respective order)
    def __init__(self, n: int,pos_holes):
        self.n=n
        self.pos_holes=pos_holes
    def compute_cg(self,lugconfig: LugConfig):
    #this method computes the x and z location of the cg of the backplate pin holes
        x_cg=0
        z_cg=0
        hole_area=((lugconfig.bolt_diameter)**2)*(m.pi*0.25)
        for i in range(len(self.pos_holes)):
            x_cg+=self.pos_holes[i][0]*hole_area
            z_cg+=self.pos_holes[i][1]*hole_area
        x_cg=x_cg/(self.n*hole_area)
        z_cg=z_cg/(self.n*hole_area)
        cg=[x_cg,z_cg]
        return cg
        
        
    def compute_xz_hole_force(self,cg,lugconfig: LugConfig,loadcase: LoadCase):
        #D is the denominator of the experssion, which is the sum of Ai*ri^2 for all holes
        #the x_prime and y_prime are coordinates of a given hole in the coord. centered at C.G.
        m_y_cg=-loadcase.force_x*cg[1]+loadcase.force_z*cg[0]
        xz_forces=[]
        D=0
        hole_area=((lugconfig.bolt_diameter)**2)*(m.pi*0.25)
        for i in range(len(self.pos_holes)):
            x_prime=self.pos_holes[i][0]-cg[0]
            z_prime=self.pos_holes[i][1]-cg[1]
            D+=hole_area*((x_prime**2)+(z_prime**2))
        for i in range(len(self.pos_holes)):
            x_prime=self.pos_holes[i][0]-cg[0]
            z_prime=self.pos_holes[i][1]-cg[1]
            alpha=np.arctan2(z_prime,x_prime)
            fx=(loadcase.force_x/self.n)+((m_y_cg*hole_area*m.sqrt(x_prime**2+z_prime**2))/D)*np.cos(alpha-m.pi/2)
            fz=(loadcase.force_z/self.n)+((m_y_cg*hole_area*m.sqrt(x_prime**2+z_prime**2))/D)*np.sin(alpha-m.pi/2)
            xz_forces.append([fx,fz])
        return xz_forces
