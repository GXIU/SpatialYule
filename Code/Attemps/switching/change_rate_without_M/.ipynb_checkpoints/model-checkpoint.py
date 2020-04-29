import numpy as np
import math
import random
import scipy.stats as stats
import Environment as Environment



class First_procedure():
    '''
    time_distribution in ['exp','power']
    spatial_distribution in ['u','exp','power']
    '''
    def __init__(self,f_time_distribution,f_time_parameters,f_space_distribution,f_space_parameters):
        self.time_distribution=f_time_distribution
        self.time_parameters = f_time_parameters
        self.space_distribution = f_space_distribution
        self.space_parameters = f_space_parameters

    def get_anchorpoint(self,emptry_grid_list):

        anchorPoint=None
        if(emptry_grid_list):
            if(self.space_distribution=='u'):
                next_grid=random.choice(emptry_grid_list)
                x,y=random.uniform(0,1),random.uniform(0,1)
                x = x + next_grid.x
                y = y + next_grid.y
                anchorPoint=(x,y)
            if(self.space_distribution=='power'):
                print ('wait for next update')
            if(self.space_distribution=='exp'):
                print('wait for next update')
        return anchorPoint

    def get_next_T(self,anchor_point_num):
        lamda = self.time_parameters[0]
        n=max(anchor_point_num,1)
        rv = stats.expon.rvs(loc=0, scale=1 / (n*lamda), size=1)[0]
        return rv

    def cal(self, emptry_grid_list):
        # get the first anchor point
        next_anchorpoint = self.get_anchorpoint(emptry_grid_list)
        return next_anchorpoint

class Second_procedure():
    def __init__(self,s_time_distribution,s_time_parameters,step_r):
        self.time_distribution = s_time_distribution
        self.time_parameters = s_time_parameters
        self.step_r = step_r

    def get_next_T(self,point_num):
        lamda = self.time_parameters[0]
        n=max(point_num,1)
        rv = stats.expon.rvs(loc=0, scale=1 / (n*lamda), size=1)[0]
        return rv

    def get_generatedPoint(self,gridDict,x,y):

        r = self.step_r

        grid_x,grid_y=int(x),int(y)
        source_grid=gridDict[(grid_x,grid_y)]

        theta=random.uniform(0,2*math.pi)
        delta_x=math.cos(theta)*r
        delta_y=math.sin(theta)*r
        new_x,new_y=x+delta_x,y+delta_y
        grid_x,grid_y=int(new_x),int(new_y)
        new_point=(new_x,new_y)

        if((grid_x,grid_y) in gridDict):
            target_grid=gridDict[(grid_x,grid_y)]
            if(target_grid.flag==source_grid.flag or target_grid.flag==0):
                return new_point,source_grid.flag
            else:
                return None,None
        else:
            return None,None

    def cal(self, gridDict,rand_point):
        # get the first anchor point
        next_point,flag = self.get_generatedPoint(gridDict,x=rand_point[0],y=rand_point[1])
        return next_point,flag