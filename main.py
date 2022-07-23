from utils import *
from LaserWork import LaserWork
import sys
sys.setrecursionlimit(5000)


input_path = "input.txt"

input_data = read_input(input_path)

#print(len(input_data))


def place_input_data(input_data):

    Safe_obj_list = []
    input_index = 0
    for cur_line in input_data:
        cur_line_data = [int(x) for x in cur_line.split(' ')]
        if len(cur_line_data) == 4:
            row,col,m,n = cur_line_data
            input_index = 0

            laser_obj = LaserWork(row_r=row, col_c= col,mirror_m=m,mirror_n= n)
            Safe_obj_list.append(laser_obj)

        else:
            row,col = cur_line_data
            
            if input_index < m:
                row_mirror = (col,MIRROR_0)
                col_mirror = (row,MIRROR_0)
            else:
                row_mirror = (col,MIRROR_1)
                col_mirror = (row,MIRROR_1)

            if laser_obj.row_mirror_positions.get(row) is None:
                laser_obj.row_mirror_positions[row] = []
            laser_obj.row_mirror_positions[row].append(row_mirror)
                
            if laser_obj.col_mirror_positions.get(col) is None:
                laser_obj.col_mirror_positions[col] = []
            laser_obj.col_mirror_positions[col].append(col_mirror)


           
            
            input_index = input_index+1

        #print(safe_obj.row_mirror_positions)
        #print(safe_obj.col_mirror_positions)
        #("##################################")
        
    return Safe_obj_list


safe_obj_list = place_input_data(input_data)
#print(len(Safe_obj_list))
for i,safe_obj in enumerate(safe_obj_list):
    result = safe_obj.CheckLaser()
    str_out = "Case {}: {}".format(str(i+1),result)
    print(str_out)