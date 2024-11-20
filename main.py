#!/usr/bin/python
from data_ingress import LoadCase, MaterialProperties, LugConfig

def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    test_lugconfig = LugConfig(1, 1, 1, 1, 1, 1, 1)
    test_lugconfig.to_csv("test")

def force_ratio(t, E_a, E_b, D_fo, D_fi, sum_L_over_A):
    delta_a = (4 * t) / (E_a * pi * ((D_fo ** 2) - (D_fi ** 2)))
    delta_b = (1/E_b) * sum_L_over_A
    phi = delta_a / (delta_a + delta_b)
    return phi
