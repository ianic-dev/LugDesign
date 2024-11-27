import math as m


def sum_L_over_A(D_shaft,A_shaft,A_head,A_nut):
    return ((0.4*D_shaft/A_shaft)+(0.5*D_shaft/A_head)+(0.4*D_shaft/A_nut))


def force_ratio(t, E_a, E_b, D_fo, D_fi, sum_L_over_A):
    delta_a = (4 * t) / (E_a * m.pi * ((D_fo ** 2) - (D_fi ** 2)))
    print(delta_a)
    delta_b = (1/E_b) * sum_L_over_A
    print(delta_b)
    phi = delta_a / (delta_a + delta_b)
    return phi

def fastener_area(D_fi):
    return m.pi*0.25*(D_fi**2)