from fuzzy.datatype import grade
import fuzzy.memberfuncs as mfs
from matplotlib import pyplot as plt
import numpy as np
import fuzzy.input as finput

dis=finput.Discorse(
    mfs.Trapezoidal(rhead=0, rbase=2),
    mfs.Trapezoidal(1,3,5,7),
    mfs.Triangular(6,8,10),
    mfs.Trapezoidal(9,11,13,15),
    mfs.Trapezoidal(14,16)
)

print(dis.centroids)