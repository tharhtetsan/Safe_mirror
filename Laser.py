class Laser:
    

    def __init__(self) :

        self.horizontal_lines = []
        self.vertical_lines = []
        self.lastVisited_point = None
        self.current_direction = None

    
    def update_Current_direction(self,laser_direction):
        self.current_direction = laser_direction
    
    def update_lastVisited_point(self,last_visitedPoint):
        self.lastVisited_point = last_visitedPoint

    
    def add_horizontal_line(self, line):
        
        line.sort()
        self.horizontal_lines.append(line)

    def add_vertical_line(self,line):
        row_range = tuple(sorted([line[0][0], line[1][0]]))
        col = line[0][1]
        self.vertical_lines.append(((row_range), col))


