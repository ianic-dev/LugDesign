#!/usr/bin/python
from data_ingress import LoadCase, MaterialProperties, LugConfig

def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    test_lugconfig = LugConfig(1, 2, 1, 1, 1, 1, 1)
    forces = LoadCase(1,1,1,1,1,1)
    test_lugconfig.to_csv("test")
    read_lugconfig_from_csv("test")
    pos_holes=[[2,1],[1,-1],[-1,-1]]
    backplate=BackplatePins(3,pos_holes)
    cg=backplate.compute_cg(test_lugconfig)
    
print(cg)
print(backplate.compute_xz_hole_force(cg,test_lugconfig,forces))