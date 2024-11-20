#!/usr/bin/python
from data_ingress import LoadCase, MaterialProperties, LugConfig

def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    test_lugconfig = LugConfig(1, 1, 1, 1, 1, 1, 1)
    test_lugconfig.to_csv("test")
