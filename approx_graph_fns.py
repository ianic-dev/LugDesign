
def stress_conc_factor_kt(flange_height: float, pin_diameter, curve_number: int) -> float:
    """
    a Margin of Safety of 0.15 should be used
    values should only be used at room temperature but they're the ones we've got so we're using them
    """
    w_over_d = flange_height/pin_diameter
    if w_over_d < 1:
        raise ValueError("w_over_d must be at least 1")
    if curve_number == 1:
        y0 = 1
        x1 = 2.9
        y1 = 0.92
        e1 = 1.4
        s1 = 0
        x2 = 4.3
        y2 = 0.72
        e2 = 4.9
        s2 = 0.7
        x3 = 0
        y3 = 0
        e3 = 0
        s3 = 0
    elif curve_number == 2:
        if w_over_d > 4.3:
            raise ValueError("w_over_d is outside acceptable range (1-4.3) for curve 2")
        y0 = 1
        x1 = 2.9
        y1 = 0.92
        e1 = 1.4
        s1 = 0
        x2 = 4.3
        y2 = 0.72
        e2 = 4.9
        s2 = 0.7
        x3 = 0
        y3 = 0
        e3 = 0
        s3 = 0

    elif curve_number == 3:
        y0 = 1
        x1 = 2.1
        y1 = 0.93
        e1 = 1.6
        s1 = 1.1
        x2 = 4
        y2 = 0.81
        e2 = -5
        s2 = 54
        x3 = 5
        y3 = 0.74
        e3 = 1.5
        s3 = 0.2
    elif curve_number == 4:
        y0 = 1
        x1 = 2
        y1 = 0.9
        e1 = 1.3
        s1 = 0.2
        x2 = 3.8
        y2 = 0.745
        e2 = -0.1
        s2 = 2
        x3 = 5
        y3 = 0.69
        e3 = 1
        s3 = 0.2
    elif curve_number == 5:
        y0 = 1
        x1 = 1.6
        y1 = 0.9
        e1 = 1.5
        s1 = 0.2
        x2 = 2.5
        y2 = 0.79
        e2 = -0.1
        s2 = 1
        x3 = 5
        y3 = 0.52
        e3 = 1
        s3 = 0.2
    elif curve_number == 6:
        y0 = 1
        x1 = 2.1
        y1 = 0.68
        e1 = 1.5
        s1 = 0.7
        x2 = 4.2
        y2 = 0.24
        e2 = 1
        s2 = 1
        x3 = 5
        y3 = 0.12
        e3 = 0.8
        s3 = 0.2
    elif curve_number == 6:
        y0 = 0.67
        x1 = 2
        y1 = 0.58
        e1 = 0.8
        s1 = 0.7
        x2 = 3.5
        y2 = 0.46
        e2 = 1
        s2 = 1
        x3 = 5
        y3 = 0.32
        e3 = 1.1
        s3 = 0.2
    else:
        raise ValueError("curve_number is not valid or not an implemented curve")
    if w_over_d < x1:
        kt: float =  y0 - (y0-y1)*(s1**e1-(w_over_d-1+s1)**e1)/((s1+(x1-1))**e1-s1**e1)
    elif x1 <= w_over_d and w_over_d < x2:
        kt: float = y1 + (y1-y2)*(s2**e2-(w_over_d-x1+s2)**e2)/((s2 + (x2-x1))**e2 - s2**e2)
    elif x2 <= w_over_d <= x3:
        kt: float = y2 + (y2-y3)*(s3**e3-(w_over_d-x2+s3)**e3)/((s3 + (x3-x2))**e3 - s3**e3)
    else:
        raise ValueError("w_over_d is outside acceptable range")
    return kt

def shear_bearing_efficiency_kbr(flange_height: float, pin_diameter: float, flange_thickness: float) -> float:
    """
    when using aluminium material and a lug thickness of 0.0127 m or greater, no kbr greater than 2.0 should be used
    a Margin of Safety of 0.15 should be used
    values should only be used at room temperature but they're the ones we've got so we're using them
    """
    e_over_d = (flange_height/2)/pin_diameter
    d_over_t = pin_diameter/flange_thickness
    kbr = 0

    return kbr


        
