import math as m

class LoadCase:
    def __init__(self, f_x: float, m_x: float, f_y: float, m_y: float, f_z: float, m_z: float) -> None:
        self.force_x = f_x/2  # transverse load aligned with pin axis
        self.moment_x = m_x  # not carried directly by lug, moment affecting yz plane loads
        self.force_y = f_y/2  # force aligned with solar panel length axis
        self.moment_y = m_y/2  # torque around solar panel length axis
        self.force_z = f_z/2  # vertical force, aligned with thrust direction
        self.moment_z = m_z/2  # moment around thrust vector axis
#        self.yz_resultant = "N/A"  # not assigned yet
        self.y_resultant = "guh"

    def yz_plane_load(self, vert_spacing: float) -> float:
        moment_induced_y_load = self.moment_x/vert_spacing
        self.y_resultant = moment_induced_y_load + self.force_y
        total_y_load = moment_induced_y_load + self.force_y
        self.yz_resultant = m.sqrt(total_y_load**2 + self.force_z**2)
        # absolute value of either "F1" in the diagram
        return (self.yz_resultant)

    @property
    def y_resultant(self) -> float:
        if isinstance(self._y_resultant, str):
            raise RuntimeError(
                "the yz_plane_load function needs to be called at least once before accessing this field")
        return self._y_resultant

    @y_resultant.setter
    def y_resultant(self, value):
        self._y_resultant = value

def loadcase_calc(angle: float, time: float, panel_mass: float) -> LoadCase:
    angle = m.radians(angle)
    launch_g_vert = 8.5*1.25*1.5
    launch_g_side = 3*1.25
    panel_cg_radius = 6.056
    panel_length = 9.089
    panel_height = 1.4
    panel_cg_arm_launch = 0.41/2
    Ixx = panel_mass * (panel_length**2 + panel_height**2)/12
    Izz = panel_mass * panel_length**2 / 12

    # LAUNCH LOAD
    f_z = launch_g_vert * panel_mass * 9.81
    m_x = panel_cg_arm_launch * f_z
    f_x = launch_g_side * panel_mass * 9.81
    m_z = f_x * panel_cg_arm_launch
    f_y = launch_g_side * panel_mass * 9.81
    m_y = 0
    
    # manoeuvre load
    angle /= 2
    time /= 2
    alpha = 2 * angle / (time**2)
    acceleration = panel_cg_radius * alpha
    f_z_m = acceleration * panel_mass
    m_x_m = f_z_m * (panel_length/2) + alpha * Ixx
    f_x_m = acceleration * panel_mass
    m_z_m = f_x_m * (panel_length/2) + alpha * Izz
    f_y_m = panel_mass * panel_cg_radius * alpha**2
    m_y_m = 0
    print("m_z", m_z)

    f_z = max(f_z, f_z_m)
    m_x = max(m_x, m_x_m)
    f_x = max(f_x, f_x_m)
    m_z = max(m_z, m_z_m)
    f_y = max(f_y, f_y_m)
    m_y = max(m_y, m_y_m)

    return LoadCase(f_x, m_x, f_y, m_y, f_z, m_z)

