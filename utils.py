from constants import * 


def calculate_nextDirection(laser_direction, mirror_status):
    """    
    laser_direction (str) : direction of incomming laser
    mirror_status (int) :  / = 0 and \ = 1


    / =  MIRROR_0 = 0 
    \ = MIRROR_1 = 1 
    """


    next_direction = None
    if laser_direction == LEFT:
        if mirror_status ==  MIRROR_1:
             next_direction = UP
        else:
            next_direction = DOWN

    elif laser_direction == RIGHT:
        if  mirror_status == MIRROR_1 :
            next_direction = DOWN
        else:
            next_direction = UP
    
    elif laser_direction == UP :
        if mirror_status == MIRROR_1:
            next_direction= LEFT
        else:
            next_direction = RIGHT
    

    elif laser_direction == DOWN:
        if mirror_status == MIRROR_1:
            next_direction = RIGHT
        else:
            next_direction = LEFT
    
    return next_direction




def run_binary_search(list_nums, target):
    """
    list_nums : sorted list
    """
    lower = 0
    upper = len(list_nums)
    while lower < upper:
        mid = lower + (upper - lower) // 2
        val = list_nums[mid]
        if target == val:
            return mid
        elif target > val:
            if lower == mid:
                break
            lower = mid
        elif target < val:
            upper = mid




def read_input(file_path):
    with open(file_path, 'r') as f:
        contents = [line.strip() for line in f.readlines()]

    return contents