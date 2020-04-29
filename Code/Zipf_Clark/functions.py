# -- coding: utf-8 --
from Environment import Environment
from model import First_procedure
from model import Second_procedure
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pandas as pd
import seaborn as sbn
import numpy as np
from matplotlib.colors import ListedColormap
import copy
import pickle
import time
from multiprocessing import Pool
import random
import os
import powerlaw
import pickle
import traceback

def cal_population_density(pointlist):
    # get weight center point
    pointx=[item[0] for item in pointlist]
    pointy=[item[1] for item in pointlist]
    
    center_x=np.mean(pointx)
    center_y=np.mean(pointy)

    # cal the distance
    points=np.array(pointlist)
    div_list=list(map(lambda x:[x[0]-center_x,x[1]-center_y],pointlist))
    div_list=list(map(lambda x:np.sqrt(x[0]**2+x[1]**2),div_list))
    return div_list