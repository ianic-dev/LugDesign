from data_ingress import MaterialProperties, LugConfig, FastenerConfig
from backplate import BackplatePins
import math as m

def lug_mass(material: MaterialProperties, lugconfig: LugConfig, fst: FastenerConfig, backplate: BackplatePins) -> float:
    density = material.density
    backplate_width = 0
    for pos in backplate.pos_holes:
        if pos[0] > backplate_width:
            backplate_width = pos[0]
    backplate_width = max(abs(backplate.pos_holes[1][1]), backplate_width)
    backplate_width += 1.5 * lugconfig.bolt_diameter  # edge margin
    backplate_width *= 2

    backplate_height = 0
    for pos in backplate.pos_holes:
        if pos[1] > backplate_height:
            backplate_height = pos[1]
    backplate_height += 1.5 * lugconfig.bolt_diameter  # edge margin
    backplate_height *= 2

    if backplate_height > lugconfig.flange_height:
        print("Too many bolt holes, the backplate is too tall for the flange")
    elif backplate_height < lugconfig.flange_height:
        print("backplate constrained by flange")
        backplate_height = lugconfig.flange_height

    dist = m.inf
    for hole1 in backplate.pos_holes:
        for hole2 in backplate.pos_holes:
            if not hole1 == hole2:
                dist = m.sqrt((hole1[0]-hole2[0])**2 + (hole1[1]-hole2[1])**2)
            if material.ismetal:
                if dist < 2.5 * lugconfig.bolt_diameter:
                    raise ValueError("ismetal has been used")
            else:
                if dist < 4.5 * lugconfig.bolt_diameter:
                    raise ValueError("ismetal has been used")

    print("backplate is legit and", round(backplate_width*1000, 2), "by", round(backplate_height*1000, 2), "mm")

    flange_len = lugconfig.flange_height/2 + lugconfig.pin_diameter * 1.5

    volume = 0

    volume += (backplate_width * backplate_height - len(backplate.pos_holes) * m.pi * lugconfig.bolt_diameter**2 / 4) * lugconfig.base_thickness

    volume += 2 * (lugconfig.pin_diameter * 1.5 * lugconfig.flange_height + 0.5 * m.pi * lugconfig.flange_height**2 / 4 - m.pi * lugconfig.pin_diameter**2 / 4) * lugconfig.flange_thickness

    mass = volume * density
    
    return mass

def fastener_mass(fst: FastenerConfig, lug: LugConfig, posholes, mat: MaterialProperties):
    mass = 0
    mass += len(posholes)*mat.density*(lug.bolt_diameter**2 * m.pi * (fst.length+0.001))
    print("fst mass:", mass)
    return mass

