from ast import Pass
from turtle import backward, right
from Laser import Laser
from constants import *
import operator
from bst import BinarySearchTree
from utils import run_binary_search
from utils import calculate_nextDirection

class LaserWork:
    


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
        self.bst = BinarySearchTree()


    def compute_LinesIntersections(self, events):
        intersections = []
        try:
            for event in events:
                if type(event) is not tuple:
                    x, y, event_flag = event
                    if event_flag == 0:
                        self.bst[x] = x
                    elif event_flag == 1:
                        del self.bst[x]
              
                else:
                    x_range, y = event
                    for i in range(x_range[0] + 1, x_range[1]):
                        if self.bst[i] is not None:
                            intersections.append((self.bst[i], y))
        except :
                Pass
        return intersections   


    def create_events_queue(self, horizontal_segments, vertical_segments):
        events = []
        for segment in horizontal_segments:
            start, stop = segment

            # Markers for start and stop events.
            start.append(0)
            stop.append(1)

            events.append(start)
            events.append(stop)

        for segment in vertical_segments:
            events.append(segment)

        events.sort(key=operator.itemgetter(1)) 

        return events


    def CheckLaser(self):
        done, forward_trace = self.laserBeam_travel_forward()
        if done:    
            return 0
        else:
            back_done, backward_trace = self.laser_Backward_travel()
            

        intersection_points, lexi_candidates = [], []


        events = self.create_events_queue(forward_trace.horizontal_lines,
                                          backward_trace.vertical_lines)
        
        intersections = self.compute_LinesIntersections(events)
        
        if len(intersections) > 0:
            lexi_candidates.append(intersections[0])
        intersection_points.extend(intersections)
       
        #print()
        #print(events)
        #print("intersections_ f_h and b_V : ",intersections)
        #print()
 
    

        events = self.create_events_queue(backward_trace.horizontal_lines,
                                          forward_trace.vertical_lines)
        intersections = self.compute_LinesIntersections(events)
        #print()
        #print(events)
        #print("intersections_ f_v and b_h : ",intersections)
        #print()


        if len(intersections) > 0:
            lexi_candidates.append(intersections[0])
        intersection_points.extend(intersections)

        n_intersections = len(intersection_points)
        #print("lexi_candidates", lexi_candidates)
        #print("n_intersections : ",n_intersections)
        lexi_first = None
        if n_intersections > 0:
            if len(lexi_candidates) > 1:
                lexi_first = self.choose_closedPoint_forward_trace(lexi_candidates)
                
            else:
                lexi_first = lexi_candidates[0]
        else:
            return "impossible"

        result = str(n_intersections) + " " + str(lexi_first[0]) +" " + str(lexi_first[1])
        return result
        #print("done : ",done)

    def choose_closedPoint_forward_trace(self, lexi_candidates):
        point_a, point_b = lexi_candidates

        if (point_a[0] < point_b[0]):
            return point_a
        elif (point_a[0] == point_b[0]):
            if (point_a[1] < point_b[1]):
                return point_a
            else:
                return point_b
        else:
            return point_b


    def laser_Backward_travel(self):
        start_point = [self.row,self.col+1]
        end_point = [1,0]
        init_direction = LEFT
        ## initially laser start from row,col+1 with the left direction
        backward_laser_obj = Laser()
        backward_laser_obj.update_lastVisited_point(last_visitedPoint=start_point)
        backward_laser_obj.update_Current_direction(laser_direction=init_direction)
        
        done,backward_trace = self.travel_the_grip(backward_laser_obj,end_point)
        return done, backward_trace




    def laserBeam_travel_forward(self):
        start_point = [1,0]
        end_point = [self.row,self.col+1]
        init_direction = RIGHT
        ## initially laser start from 1,0 with the right direction
        forward_laser_obj = Laser()
        forward_laser_obj.update_lastVisited_point(last_visitedPoint=start_point)
        forward_laser_obj.update_Current_direction(laser_direction=init_direction)
        
        done,forward_trace = self.travel_the_grip(forward_laser_obj,end_point)

        #print("laser_travelForward status : ",done)
        return  done,forward_trace
    

    
    def  travel_the_grip(self, laser_beam_trace,end):
        done = False
        while True:
            next_trace, mirror_orientation,laser_beam_trace = self.get_next_point(laser_beam_trace)
            laser_beam_trace.update_lastVisited_point(next_trace)
            #print("horizontal_lines : ",laser_beam_trace.horizontal_lines)
            #print("veticle_lines : ",laser_beam_trace.vertical_lines)
            
            if next_trace == end:
                done = True
                break
            elif  (next_trace[0] > self.row) or (next_trace[1] > self.col) or  (next_trace[0] < 1) or (next_trace[1] < 1):
                break

            else:

                
                new_direction = calculate_nextDirection(laser_beam_trace.current_direction, mirror_orientation)
                laser_beam_trace.update_Current_direction(new_direction)
                
                #print("New direction : ",new_direction)
                #print(".........................................................")

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
        
        #print("current_point_trace : ",current_point_trace)
        #print("col_mirror_positions : ",self.col_mirror_positions)
        #print("row_mirror_positions : ",self.row_mirror_positions)
        #print("cols_with_mirrors : ",cols_with_mirrors)
        #print("rows_with_mirrors : ",rows_with_mirrors)


        if (laser_obj.current_direction == LEFT ) or (laser_obj.current_direction == RIGHT):
            
            if cols_with_mirrors is not None:
                cols_with_mirrors_position =[ cur_col for cur_col,cur_mirror in cols_with_mirrors]
                nearest_mirror_interval =  run_binary_search(cols_with_mirrors_position,current_point_trace[1])
                #print("closest_mirror_interval : ",nearest_mirror_interval)

                if laser_obj.current_direction == RIGHT:
                    # go to right direction
                    next_point = [current_point_trace[0],cols_with_mirrors_position[nearest_mirror_interval+1]]
                    mirror_orientation =  cols_with_mirrors[nearest_mirror_interval+1][1]


                else: #laser_obj.current_direction  == LEFT:
                    # go to left direction
                    next_point = [current_point_trace[0],cols_with_mirrors_position[nearest_mirror_interval-1]]
                    mirror_orientation =  cols_with_mirrors[nearest_mirror_interval-1][1]
                    #print(nearest_mirror_interval-1)
                    #print("left next point",cols_with_mirrors)
            
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

        #print("mirror_orientation : ",mirror_orientation)
        #print("cur direction : ",laser_obj.current_direction)
        #print("next_point : ",next_point)
       
        return next_point,mirror_orientation,laser_obj 
                   
