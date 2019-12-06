# -- coding: utf-8 --
import numpy as np
import random
import matplotlib.pyplot as plt

class ListDict(object):
    def __init__(self):
        self.item_to_position = {}
        self.items = []

    def add_item(self, item):
        if item in self.item_to_position:
            return
        self.items.append(item)
        self.item_to_position[item] = len(self.items)-1

    def remove_item(self, item):
        position = self.item_to_position.pop(item)
        last_item = self.items.pop()
        if position != len(self.items):
            self.items[position] = last_item
            self.item_to_position[last_item] = position

    def choose_random_item(self):
        return random.choice(self.items)
    
    def len_list(self):
        return len(self.items)
    
class grid():
    def __init__(self,x,y,pop=0,flag=0):
        self.x=x
        self.y=y
        self.pop=pop
        self.flag=flag

    def is_within(self,point):
        x,y=point[0],point[1]
        if((int(x)==self.x) & (int(y)==self.y)):
            return True
        else:
            return False

    def is_captured(self):
        if(self.flag>0):
            return True
        else:
            return False

class Environment():
    def __init__(self,shape='square',Memory=1000,r=500):
        self.shape=shape
        self.r=r
        self.gridDict={}
        self.set_gridDict()
        self.pointlist=ListDict()
        self.anchorPoint=[]
        self.Memory=Memory
        self.point_num=0
    def set_gridDict(self):
        if(self.shape=='square'):
            if(self.r):
                for i in range(-self.r,self.r+1):
                    for j in range(-self.r,self.r+1):
                        tempGrid=grid(x=self.r+i,y=self.r+j)
                        self.gridDict[tempGrid.x, tempGrid.y] = tempGrid

        if(self.shape=='circle'):
            if(self.r):
                for i in range(-self.r,self.r+1):
                    for j in range(-self.r,self.r+1):
                        if(i*i+j*j<self.r*self.r):
                            tempGrid = grid(x=self.r + i, y=self.r + j)
                            self.gridDict[tempGrid.x, tempGrid.y] = tempGrid

    def get_neighbors(self,x,y,neighbor=4):
        tempPointList=[]
        if (self.gridDict):
            if(neighbor==8):
                for i in range(-1,2,1):
                    for j in range(-1,2,1):
                        if(abs(i)+abs(j)):
                            if (x+i,y+j) in self.gridDict:
                                temp_value=self.gridDict[(x+i,y+j)]
                                tempPointList.append(temp_value)

            if(neighbor==4):
                xyList=[[x-1,y],[x+1,y],[x,y+1],[x,y-1]]
                for item in xyList:
                    if(tuple(item) in self.gridDict):
                        temp_value=self.gridDict[tuple(item)]
                        tempPointList.append(temp_value)

        else:
            tempPointList=[]
        return tempPointList

    def add_point(self,point,flag):
        '''
        当环境中加入一个点的时候，各个对象所进行的更新操作：
        '''
        #gridList的更新操作
        int_x,int_y=int(point[0]),int(point[1])
        self.gridDict[(int_x,int_y)].pop+=1
        if(self.gridDict[(int_x,int_y)].flag>0):
            if(self.gridDict[(int_x, int_y)].flag!=flag):
                print ('your should check the grid flag before add a point')
        self.gridDict[(int_x,int_y)].flag=flag
        self.pointlist.add_item(point)
        self.point_num+=1
        '''
        add the Memory kernal mechanism
        '''
        if self.pointlist.len_list()>self.Memory:
            self.pointlist.remove_item(self.pointlist.choose_random_item())
#             self.pointlist.pop(random.randrange(len(self.pointlist)))

    def get_empty_gridlist(self):
        temp_empty_grid=[]
        for tempgrid in self.gridDict.values():
            if(tempgrid.flag==0):
                temp_empty_grid.append(tempgrid)
        return temp_empty_grid

    def get_anchorpoint_number(self):
        return len(self.anchorPoint)

    def get_random_point(self):
        point=self.pointlist.choose_random_item()
        return point


    ###get the attribute for visulization
    def get_map(self):
        map=np.zeros((2*self.r+1,2*self.r+1))
        #这个赋值可能会初夏x，y反了的情况，注意甄别
        for row in range(0,2*self.r+1):
            for col in range(0,(2*self.r+1)):
                if((row,col) in self.gridDict):
                    map[row][col]=self.gridDict[(col,row)].flag
        return map

    def get_popmap(self):
        map = np.zeros((2 * self.r + 1, 2 * self.r + 1))
        # 这个赋值可能会初夏x，y反了的情况，注意甄别
        for row in range(0, 2 * self.r + 1):
            for col in range(0, 2 * self.r + 1):
                if ((row, col) in self.gridDict):
                    map[row][col] = self.gridDict[(col, row)].pop
        return map

    def get_Gridpop_distribution(self):
        popDict={} # 存储不同anchorpoint的人口
        for grid in self.gridDict.values():
            if grid.flag in popDict:
                popDict[grid.flag]+=grid.pop
            else:
                popDict[grid.flag]=grid.pop
        return popDict

    def get_boundary(self):
        BoundaryDict={}
        for grid in self.gridDict.values():
            if(grid.flag==0):
                continue
            neighlist=self.get_neighbors(grid.x,grid.y,neighbor=4)
            grid_length=0
            if(neighlist):
                for neigh in neighlist:
                    if(neigh):
                        if(neigh.flag!=grid.flag):
                            grid_length+=1
            if(grid.flag in BoundaryDict):
                BoundaryDict[grid.flag]+=grid_length
            else:
                BoundaryDict[grid.flag]=grid_length
        return BoundaryDict

    def get_boundary2(self):
        '''
        @discription: 返回研究边缘属性所需要的信息。返回值为dict，每个dict包含四维信息
            0、边缘的长度：当几何周边存至少一个非本类的格子的时候，该点定义为边界
            1、边缘格子的个数，用于后来计算每个类别边缘的平均人口密度
            2、边缘格子的人口总数，用于计算边缘格子的所有人口
            3、每个类内所有的人口，计算每个类中人口的总数，比较人口总数和边缘人口密度的关系
        '''
        BoundaryDict={}
        for grid in self.gridDict.values():
            if(grid.flag==0):
                continue
            neighlist=self.get_neighbors(grid.x,grid.y,neighbor=4)
            grid_length=0
            if(neighlist):
                for neigh in neighlist:
                    if(neigh):
                        if(neigh.flag!=grid.flag):
                            grid_length+=1
            if(grid.flag in BoundaryDict):
                BoundaryDict[grid.flag][3]+=grid.pop
            else:
                BoundaryDict[grid.flag]=[0,0,0,0]
                BoundaryDict[grid.flag][3]=grid.pop
            if(grid_length!=0):
                #计算每个类的边缘长度  
                if(grid.flag in BoundaryDict):
                    BoundaryDict[grid.flag][0]+=grid_length
                else:
                    BoundaryDict[grid.flag]=[0,0,0,0]
                    BoundaryDict[grid.flag][0]=grid_length
                #计算每个类的边缘格子数目
                BoundaryDict[grid.flag][1]+=1
                BoundaryDict[grid.flag][2]+=grid.pop
        return BoundaryDict

    def get_boundary2(self):
            '''
            @discription: 返回研究边缘属性所需要的信息。返回值为dict，每个dict包含四维信息
                0、边缘的长度：当几何周边存至少一个非本类的格子的时候，该点定义为边界
                1、边缘格子的个数，用于后来计算每个类别边缘的平均人口密度
                2、边缘格子的人口总数，用于计算边缘格子的所有人口
                3、每个类内所有的人口，计算每个类中人口的总数，比较人口总数和边缘人口密度的关系
            '''
            BoundaryDict={}
            for grid in self.gridDict.values():
                if(grid.flag==0):
                    continue
                neighlist=self.get_neighbors(grid.x,grid.y,neighbor=4)
                grid_length=0
                if(neighlist):
                    for neigh in neighlist:
                        if(neigh):
                            if(neigh.flag!=grid.flag):
                                grid_length+=1
                if(grid.flag in BoundaryDict):
                    BoundaryDict[grid.flag][3]+=grid.pop
                else:
                    BoundaryDict[grid.flag]=[0,0,0,0]
                    BoundaryDict[grid.flag][3]=grid.pop
                if(grid_length!=0):
                    #计算每个类的边缘长度  
                    if(grid.flag in BoundaryDict):
                        BoundaryDict[grid.flag][0]+=grid_length
                    else:
                        BoundaryDict[grid.flag]=[0,0,0,0]
                        BoundaryDict[grid.flag][0]=grid_length
                    #计算每个类的边缘格子数目
                    BoundaryDict[grid.flag][1]+=1
                    BoundaryDict[grid.flag][2]+=grid.pop
            return BoundaryDict

    def get_boundary3(self):
            '''
            @discription: 返回研究边缘属性所需要的信息。返回值为dict，每个dict包含四维信息
                0、边缘的长度：当几何周边存至少一个非本类的格子的时候，该点定义为边界
                1、边缘格子的个数，用于后来计算每个类别边缘的平均人口密度
                2、边缘格子的人口总数，用于计算边缘格子的所有人口
                3、每个类内所有的人口，计算每个类中人口的总数，比较人口总数和边缘人口密度的关系
                4、边缘格子的坐标
                5、所属的anchorpoint的坐标
            '''
            anchor_grid=self.__get_anchor_point_Grids()
            BoundaryDict={}
            for grid in self.gridDict.values():
                if(grid.flag==0):
                    continue
                neighlist=self.get_neighbors(grid.x,grid.y,neighbor=4)
                grid_length=0
                if(neighlist):
                    for neigh in neighlist:
                        if(neigh):
                            if(neigh.flag!=grid.flag):
                                grid_length+=1
                if(grid.flag in BoundaryDict):
                    BoundaryDict[grid.flag][3]+=grid.pop
                else:
                    BoundaryDict[grid.flag]=[0,0,0,0,[],0]
                    BoundaryDict[grid.flag][3]=grid.pop
                if((grid.x,grid.y) in anchor_grid):
                    BoundaryDict[grid.flag][5]=grid
                if(grid_length!=0):
                    #计算每个类的边缘长度  
                    if(grid.flag in BoundaryDict):
                        BoundaryDict[grid.flag][0]+=grid_length
                    else:
                        BoundaryDict[grid.flag]=[0,0,0,0]
                        BoundaryDict[grid.flag][0]=grid_length
                    #计算每个类的边缘格子数目
                    BoundaryDict[grid.flag][1]+=1
                    BoundaryDict[grid.flag][2]+=grid.pop
                    BoundaryDict[grid.flag][4].append([grid.x,grid.y])               
            return BoundaryDict
    def __get_anchor_point_Grids(self):
        return [(int(item[0]),int(item[1])) for item in self.anchorPoint]

    def get_area(self):
        AreaDict={}
        for grid in self.gridDict.values():
            if(grid.flag==0):
                continue
            if(grid.flag in AreaDict):
                AreaDict[grid.flag]+=1
            else:
                AreaDict[grid.flag]=1
        return AreaDict

if __name__=='__main__':

    Envir=Environment(shape='square',r=50)
    for grid in Envir.gridDict.values():
        grid.flag=grid.x+grid.y
        grid.pop=grid.x*10+grid.y
    map=Envir.get_map()
    popmap=Envir.get_popmap()

    plt.subplot(221)
    plt.imshow(X=map)
    plt.subplot(223)
    img=plt.imshow(X=popmap)
    plt.subplot(222)
    plt.colorbar(img)
    plt.subplot(224)


    areaDict = Envir.get_Gridpop_distribution()

    data = list(areaDict.values())
    # data=list(areaDict.reshape((-1,1)))
    data.sort(reverse=True)
    rank = [ran for ran in range(len(data))]
    plt.plot(rank, data)
    plt.show()
    print (len(Envir.gridDict))
    p=Envir.get_neighbors(0,0,8)
    print (len(p))