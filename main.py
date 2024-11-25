#!/usr/bin/python
from data_ingress import LoadCase, MaterialProperties, LugConfig
from backplate import BackplatePins


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    test_lugconfig = LugConfig(1, 2, 1, 1, 1, 1, 1)
    forces = LoadCase(0,0,-44.818,1,153.036,0)
    pos_holes=[[0.1,0.1],[0.1,-0.1],[-0.1,0.1],[-0.1,-0.1]]
    backplate=BackplatePins(4,pos_holes)
    cg=backplate.compute_cg(test_lugconfig)
    
print(cg)
print(backplate.compute_xz_hole_force(cg,test_lugconfig,forces))
print(backplate.compute_y_hole_force(cg,test_lugconfig,forces))
print(backplate.pull_out_check(backplate.compute_y_hole_force(cg,test_lugconfig,forces),0.005,0.005,276000000))