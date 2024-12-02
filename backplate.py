from data_ingress import LugConfig, LoadCase, FastenerConfig, MaterialProperties
import fastener as fst
import math as m
import numpy as np

def evaluate_backplate(pos_holes: list, lugconfig: LugConfig, loadcase: LoadCase, fastener: FastenerConfig, lugmaterial: MaterialProperties, sc_material: MaterialProperties):
    backplate = BackplatePins(pos_holes, lugconfig)

    # print("\nCG LOCATION OF HOLES")
    cg = backplate.compute_cg(lugconfig)
    # print(cg)

    # print("\nXZ FORCES FOR HOLES")
    xz_forces = backplate.compute_xz_hole_force(lugconfig, loadcase)
    # print(xz_forces)

    # print("\nY FORCES FOR HOLES")
    y_forces = backplate.compute_y_hole_force(lugconfig, loadcase)
    # print(y_forces)

    # pull out check for backplate
    print("\nPULL OUT CHECK FOR BACKPLATE")
    backplate.pull_out_check(y_forces, lugconfig.base_thickness, fastener.head_diam, lugmaterial.yield_stress)

    # pull out check for vehicle plate
    print("\nPULL OUT CHECK FOR VEHICLE")
    backplate.pull_out_check(y_forces, lugconfig.spacecraft_thickness, fastener.butt_diam, sc_material.yield_stress)

    # bearing check for backplate
    print("\nBEARING CHECK FOR BACKPLATE")
    backplate.bearing_check(xz_forces, lugconfig, "lug", lugmaterial.yield_stress)

    # bearing check for vehicle plate
    print("\nBEARING CHECK FOR VEHICLE")
    backplate.bearing_check(xz_forces, lugconfig, "spacecraft", sc_material.yield_stress)

    return backplate, xz_forces


class BackplatePins:
    """
    pos_holes : 2D list storing x and z positions of the holes:
    [[x1, z1], [x2, z2], ... ]
    """

    def __init__(self, pos_holes, lugconfig: LugConfig):
        self.n = len(pos_holes)
        self.pos_holes: list[list[int]] = pos_holes

        self.cg = self.compute_cg(lugconfig)

    def compute_cg(self, lugconfig: LugConfig):
        """
        compute [x, z] location of the backplate hole cg
        """
        x_cg = 0
        z_cg = 0
        hole_area = ((lugconfig.bolt_diameter)**2)*(m.pi*0.25)
        for i in range(len(self.pos_holes)):
            x_cg += self.pos_holes[i][0]*hole_area
            z_cg += self.pos_holes[i][1]*hole_area
        x_cg = x_cg / (self.n*hole_area)
        z_cg = z_cg / (self.n*hole_area)
        cg = [x_cg, z_cg]
        return cg

    def compute_xz_hole_force(self, lugconfig: LugConfig, loadcase: LoadCase):
        """
        # D is the denominator of the experssion, which is the sum of Ai*ri^2 for all holes
        # the x_prime and y_prime are coordinates of a given hole in the coord. centered at C.G.
        """
        m_y_cg = -loadcase.force_x * self.cg[1] + loadcase.force_z * self.cg[0]
        xz_forces = []
        D = 0
        hole_area = lugconfig.bolt_diameter**2 * m.pi/4
        for i in range(len(self.pos_holes)):
            x_prime = self.pos_holes[i][0] - self.cg[0]
            z_prime = self.pos_holes[i][1] - self.cg[1]
            D += hole_area * (x_prime**2 + z_prime**2)
        for i in range(len(self.pos_holes)):
            x_prime = self.pos_holes[i][0] - self.cg[0]
            z_prime = self.pos_holes[i][1] - self.cg[1]
            alpha = np.arctan2(z_prime, x_prime)
            fx = (loadcase.force_x / self.n) + ((m_y_cg * hole_area *
                                                 m.sqrt(x_prime**2 + z_prime**2)) / D) * np.cos(alpha - m.pi/2)
            fz = (loadcase.force_z / self.n) + ((m_y_cg * hole_area *
                                                 m.sqrt(x_prime**2 + z_prime**2)) / D) * np.sin(alpha - m.pi/2)
            xz_forces.append([fx, fz])
        return xz_forces

    def compute_y_hole_force(self, lugconfig: LugConfig, loadcase: LoadCase):
        y_forces = []
        D = 0
        hole_area = ((lugconfig.bolt_diameter)**2)*(m.pi*0.25)
        for i in range(len(self.pos_holes)):
            x_prime = self.pos_holes[i][0] - self.cg[0]
            z_prime = self.pos_holes[i][1] - self.cg[1]
            D += hole_area * (x_prime**2 + z_prime**2)
        for i in range(len(self.pos_holes)):
            x_prime = self.pos_holes[i][0] - self.cg[0]
            z_prime = self.pos_holes[i][1] - self.cg[1]
            fy = (loadcase.y_resultant / self.n) + ((loadcase.moment_z *
                                                 np.sign(x_prime) * hole_area * m.sqrt(x_prime**2 + z_prime**2)) / D)
            # print("d is ", D)
            # print("hole area is ", hole_area)
            # print((loadcase.moment_z * np.sign(x_prime) * hole_area * m.sqrt(x_prime**2 + z_prime**2)) / D)
            y_forces.append(fy)
        return y_forces

    def pull_out_check(self, y_forces: list[float], thickness: float, head_diam: float, tau_allowable: float):
        tau_allowable = float(tau_allowable)
        for i in range(len(self.pos_holes)):
            # print("Y force:", y_forces[i], "head diam:", head_diam, "thickness:", thickness)
            tau = (y_forces[i] / (m.pi * head_diam * thickness))
            print("The pullout stress at hole:", i, "is", tau,
                  "and Von Mises stress is:", (m.sqrt(3 * tau**2)))
            if m.sqrt(3 * tau**2) >= (0.9*tau_allowable):
                print("Pullout stress exceeded at hole:", i)
            print("Safety margin is: ", ((tau_allowable/m.sqrt(3 * tau**2))-1))

    def bearing_check(self, xz_forces, lugconfig: LugConfig, plate: str, sigma_allowable):
        sigma_allowable = float(sigma_allowable)
        if plate == "spacecraft":
            thickness = lugconfig.spacecraft_thickness
        elif plate == "lug":
            thickness = lugconfig.base_thickness
        else:
            raise ValueError("can only check for \"lug\" or \"spacecraft\" plates")

        for i in range(len(self.pos_holes)):
            p = m.sqrt(xz_forces[i][0]**2 + xz_forces[i][1]**2)
            sigma = p / (lugconfig.bolt_diameter * thickness)
            print("The bearing stress at hole:", i, "is", sigma)
            if abs(sigma) >= 0.9 * sigma_allowable:
                print("Bearing stress exceeded at hole: ", i)
            print("Safety margin is:", ((sigma_allowable/sigma)-1))

    def bearing_check_thermal_included(self, xz_forces, lugconfig: LugConfig, thickness, sigma_allowable, thermal_force):
        sigma_allowable = float(sigma_allowable)
        for i in range(len(self.pos_holes)):
            p = m.sqrt(xz_forces[i][0]**2 + xz_forces[i][1]**2) + thermal_force
            sigma = p / (lugconfig.bolt_diameter*thickness)
            print("The bearing stress at hole:", i, "is", sigma)
            if abs(sigma) >= 0.9 * sigma_allowable:
                print("Bearing stress exceeded at hole:", i)
            print("Safety margin is:", ((sigma_allowable/sigma)-1))


def evaluate_thermal(backplate: BackplatePins, lugconfig: LugConfig, lug_material: MaterialProperties, sc_material: MaterialProperties, fst_material: MaterialProperties, fastener: FastenerConfig, xz_forces, delta_T_max):
    sanitycheck = False

    phi_backplate = fst.force_ratio_head(lugconfig, lug_material, fst_material, fastener)
    phi_vehicle = fst.force_ratio_butt(lugconfig, sc_material, fst_material, fastener)


    load_lug_maxT = (lug_material.thermal_coeff - fst_material.thermal_coeff) * delta_T_max * fst_material.elasticity_modulus * fastener.area * (1 - phi_backplate)
    load_sc_maxT = (sc_material.thermal_coeff - fst_material.thermal_coeff) * delta_T_max * fst_material.elasticity_modulus * fastener.area * (1 - phi_vehicle)
    

    if sanitycheck:
        print("lug vs fastener coeff difference", (lug_material.thermal_coeff- fst_material.thermal_coeff))
        print("sc vs fastener coeff difference", (sc_material.thermal_coeff- fst_material.thermal_coeff))
        print("thermal load lug", load_lug_maxT)

    # bearing check for backplate with thermal
    print("\nBEARING CHECK FOR BACKPLATE WITH THERMAL LOADS")
    backplate.bearing_check_thermal_included(xz_forces, lugconfig, lugconfig.base_thickness, lug_material.yield_stress, load_lug_maxT)

    # bearing check for vehicle plate with thermal
    print("\nBEARING CHECK FOR VEHICLE WITH THERMAL LOADS")
    backplate.bearing_check_thermal_included(xz_forces, lugconfig, lugconfig.spacecraft_thickness, sc_material.yield_stress, load_sc_maxT)
