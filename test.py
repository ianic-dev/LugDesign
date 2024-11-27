#!/usr/bin/python
from data_ingress import MaterialProperties

mat = MaterialProperties(0, 2e11, 0, True, 0, 0, 0, 13e-6)
mat.to_csv("fastener")
