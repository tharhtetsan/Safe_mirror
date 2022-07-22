from ast import Pass
from turtle import right
from Laser import Laser
from constants import *
import operator

from utils import run_binary_search
from utils import calculate_nextDirection

class SafeLaser:
    


    def __init__(self,row_r,col_c,mirror_m,mirror_n) :

        """
            row_r (int) : row index
            col_c (int) : col index
            / =  MIRROR_0 = 0 
            \ = MIRROR_1 = 1 
        """

        self.row = row_r
        self.col = col_c
        self.mirror_0 = mirror_m
        self.mirror_1 = mirror_n

        self.row_mirror_positions = {}
        self.col_mirror_positions = {}

        self.init_direction = RIGHT
        self.start_point = [1,0]
        self.end_point = [self.row,self.col+1]


    
    def searchSafe(self):
        Pass


    def solve(self):
        done, forward_trace = self.laser_travelForward()

        print("done : ",done)


    def laser_travelForward(self):

        ## initially laser start from 1,0 with the right direction
        laser_obj = Laser()
        laser_obj.update_lastVisited_point(last_visitedPoint=self.start_point)
        laser_obj.update_Current_direction(laser_direction=self.init_direction)
        
       

        done,forward_trace = self.run_trace(laser_obj,self.end_point)

        print("laser_travelForward",done)

        return  done,forward_trace
    

    
    def  run_trace(self, laser_beam_trace,end):
        done = False
        while True:
            next_trace, mirror_orientation,laser_beam_trace = self.get_next_point(laser_beam_trace)
            laser_beam_trace.update_lastVisited_point(next_trace)
            
            if next_trace == end:
                done = True
                break
            elif  (next_trace[0] > self.row) or (next_trace[1] > self.col) or  (next_trace[0] < 1) or (next_trace[1] < 1):
                break

            else:

                
                new_direction = calculate_nextDirection(laser_beam_trace.current_direction, mirror_orientation)
                laser_beam_trace.update_Current_direction(new_direction)
                print("horizontal_lines : ",laser_beam_trace.horizontal_lines)
                print("veticle_lines : ",laser_beam_trace.vertical_lines)
                print("New direction : ",new_direction)
                print(".........................................................")
        
        
        return done, laser_beam_trace

    
    def insert_range(self, list_mirrors, end):
        list_mirrors = [item for item in list_mirrors]
        list_mirrors.insert(0, (0, None))
        list_mirrors.append((end, None))

        return list_mirrors


    def get_next_point(self,laser_obj: Laser):
        
        current_point_trace = laser_obj.lastVisited_point
       
        

        cols_with_mirrors = self.row_mirror_positions.get(current_point_trace[0], [])
        cols_with_mirrors.sort(key=operator.itemgetter(0))
        cols_with_mirrors = self.insert_range(cols_with_mirrors, self.col + 1)

        rows_with_mirrors = self.col_mirror_positions.get(current_point_trace[1], [])
        rows_with_mirrors.sort(key=operator.itemgetter(0))
        rows_with_mirrors = self.insert_range(rows_with_mirrors, self.row + 1)
        
        print("current_point_trace : ",current_point_trace)
        print("col_mirror_positions : ",self.col_mirror_positions)
        print("row_mirror_positions : ",self.row_mirror_positions)
        print("cols_with_mirrors : ",cols_with_mirrors)
        print("rows_with_mirrors : ",rows_with_mirrors)


        if (laser_obj.current_direction == LEFT ) or (laser_obj.current_direction == RIGHT):
            
            if cols_with_mirrors is not None:
                cols_with_mirrors_position =[ cur_col for cur_col,cur_mirror in cols_with_mirrors]
                nearest_mirror_interval =  run_binary_search(cols_with_mirrors_position,current_point_trace[1])
                print("closest_mirror_interval : ",nearest_mirror_interval)

                if laser_obj.current_direction == RIGHT:
                    # go to right direction
                    next_point = [current_point_trace[0],cols_with_mirrors_position[nearest_mirror_interval+1]]
                    mirror_orientation =  cols_with_mirrors[nearest_mirror_interval+1][1]


                else: #laser_obj.current_direction  == LEFT:
                    # go to left direction
                    next_point = [current_point_trace[0],cols_with_mirrors_position[nearest_mirror_interval-1]]
                    mirror_orientation =  cols_with_mirrors[nearest_mirror_interval-1][1]
                    print(nearest_mirror_interval-1)
                    print("left next point",cols_with_mirrors)
            
            else:
                # laser leave grid.
                next_point = [current_point_trace[0],self.col]
            laser_obj.add_horizontal_line([current_point_trace,next_point])
        
        else:
            if rows_with_mirrors is not None:
                rows_with_mirrors_position =[ cur_row for cur_row,cur_mirror in rows_with_mirrors]
                nearest_mirror_interval =  run_binary_search(rows_with_mirrors_position,current_point_trace[0])

                if laser_obj.current_direction ==  DOWN:
                    next_point = [rows_with_mirrors_position[nearest_mirror_interval+1],current_point_trace[1]]
                    mirror_orientation =  rows_with_mirrors[nearest_mirror_interval+1][1]

                
                else:# laser_obj.current_direction == UP :
                    next_point = [rows_with_mirrors_position[nearest_mirror_interval-1],current_point_trace[1]]
                    mirror_orientation =  rows_with_mirrors[nearest_mirror_interval-1][1]
            else:
                ## Laser leave grid
                next_point =[self.row, current_point_trace[1]]

            laser_obj.add_vertical_line([current_point_trace,next_point])

        print("mirror_orientation : ",mirror_orientation)
        print("cur direction : ",laser_obj.current_direction)
        print("next_point : ",next_point)
       
        return next_point,mirror_orientation,laser_obj         
                   
