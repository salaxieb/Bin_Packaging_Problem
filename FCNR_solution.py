from drawing import FLOOR_WIDTH_PXL, FLOOR_HEIGHT_PXL
from copy import copy

class Level(object):
    def __init__(self, floor, Solution_Position):
        self.floor = floor
        self.previous_X_floor = 0
        self.previous_X_ceiling = FLOOR_WIDTH_PXL
        self.ceiling = self.floor + Solution_Position.height
        self.positions_floor = []

        #return Solution_Position
        
    def Put_the_Box_Floor (self, Solution_Position):
        Solution_Position.Y = self.floor
        Solution_Position.X = self.previous_X_floor
        self.previous_X_floor = self.previous_X_floor + Solution_Position.width
        self.positions_floor.append(Solution_Position)
        return Solution_Position
    
    def Put_the_Box_Ceiling (self, Solution_Position):
        Solution_Position.Y = self.ceiling - Solution_Position.height
        Solution_Position.X = self.previous_X_ceiling - Solution_Position.width
        self.previous_X_ceiling = self.previous_X_ceiling - Solution_Position.width
        return Solution_Position
    
    def Get_Left_Value_Floor(self, Solution_Position):
        return FLOOR_WIDTH_PXL - self.previous_X_floor - Solution_Position.width
    
    def Get_Left_Value_Ceiling(self, Solution_Position):
        for position in self.positions_floor:
            if self.ceiling - Solution_Position.height < position.Y + position.height:
                last_crossing = position            
        return self.previous_X_ceiling - (last_crossing.X + last_crossing.width) - Solution_Position.width

class FCNR(object):
    def __init__ (self):
        self.positions = []
        self.overfill = False
        self.cost = 0.0
    
    def solve(self, positions):
        self.positions = []
        for position in positions:
            self.positions.append(copy(position))
            
        for j in self.positions:
            if j.angle:
                j.height, j.width = j.width, j.height #turn
                
        self.positions.sort(key = self.sort_Height, reverse = True)
        
        Levels = []
        level = Level(0, self.positions[0])
        Levels.append(level)
        
        for position in self.positions:
            flag_of_solution_floor = False
            flag_of_solution_ceiling = False
            for level in Levels:
                if level.Get_Left_Value_Floor(position) >= 0 and not(flag_of_solution_floor):
                    min_level = level
                    flag_of_solution_floor = True
                else:
                    if level.Get_Left_Value_Floor(position) < min_level.Get_Left_Value_Floor(position) and level.Get_Left_Value_Floor(position) >= 0:
                        min_level = level
            
            if not(flag_of_solution_floor):            
                for level in Levels:
                    if level.Get_Left_Value_Ceiling(position) >= 0 and not(flag_of_solution_ceiling):
                        min_level = level
                        flag_of_solution_ceiling = True
                    else:
                        if level.Get_Left_Value_Ceiling(position) < min_level.Get_Left_Value_Ceiling(position) and level.Get_Left_Value_Ceiling(position) >= 0:
                            min_level = level
                            
                if not(flag_of_solution_floor) and not(flag_of_solution_ceiling):
                    min_level = Level(Levels[len(Levels)-1].ceiling, position)
                    Levels.append(min_level)
                    
            if flag_of_solution_ceiling:                       
                position = min_level.Put_the_Box_Ceiling(position) 
            else:
                position = min_level.Put_the_Box_Floor(position)
                
            self.put_Cost_Value()
             
    def sort_Height(self, Solution_Position):
        return Solution_Position.height
    
    def put_Cost_Value(self):
        Cost = 0.0
        for i in self.positions:
            if (i.Y+i.height <= FLOOR_HEIGHT_PXL):
                Cost = Cost + i.width * i.height
        self.cost = Cost/(FLOOR_HEIGHT_PXL * FLOOR_WIDTH_PXL)

    