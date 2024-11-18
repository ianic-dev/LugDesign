import pandas as pd
import math as m


class LoadCase:
    def __init__(self, f_x, m_x, f_y, m_y, f_z, m_z) -> None:
        self.force_x = f_x  # transverse load aligned with pin axis
        self.moment_x = m_x  # not carried directly by lug, moment affecting yz plane loads
        self.force_y = f_y  # force aligned with solar panel length axis
        self.moment_y = m_y  # torque around solar panel length axis
        self.force_z = f_z  # vertical force, aligned with thrust direction
        self.moment_z = m_z  # moment around thrust vector axis
    
    def yz_plane_load(self, vert_spacing) -> float:
        moment_induced_y_load = self.moment_x/vert_spacing
        total_y_load = moment_induced_y_load + self.force_y
        yz_resultant = m.sqrt(total_y_load**2 + self.force_z**2)
        return(yz_resultant)

