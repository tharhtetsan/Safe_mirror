class Laser:
    

    def __init__(self) :

        self.lastVisited_point = None
        self.current_direction = None

    
    def update_Current_direction(self,laser_direction):
        self.current_direction = laser_direction
    
    def update_lastVisited_point(self,last_visitedPoint):
        self.lastVisited_point = last_visitedPoint
