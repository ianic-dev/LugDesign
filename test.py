#!/usr/bin/python
from data_ingress import MaterialProperties

mat = MaterialProperties(1, 72e9, 420e6, True, 490e6, 2, 11)
mat.to_csv("2014-T6")
