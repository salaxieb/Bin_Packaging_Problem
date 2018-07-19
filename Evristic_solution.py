from drawing import FLOOR_HEIGHT_PXL
from drawing import FLOOR_WIDTH_PXL
from Box import MAX_BOX_SIZE_PXL
import random
import copy


class Solution_Position(object): #gives the box the angle and the down & left or down & right position 
    def __init__(self, Boxes_list, solution, X=0, Y=0):
        Copy_Of_Boxes_List = copy.copy(Boxes_list)
        if len(solution) >= len(Copy_Of_Boxes_List):
            print "all boxes fitted in"
        for i in solution:
            for j in Copy_Of_Boxes_List:
                if j.box_Num == i.box_Num:
                    Copy_Of_Boxes_List.remove(j)
        box = random.choice(Copy_Of_Boxes_List)
        self.box_Num = box.box_Num
        self.angle = random.choice((0,1))
        self.position = random.choice((0,1)) #0 - down & left, 1- down & right
        self.width = box.width
        self.height = box.height
        self.X = X
        self.Y = Y
        self.color = box.color


        
class Evristic_solution(object):
    def __init__(self, Boxes_List):
        self.Boxes_List = Boxes_List
        self.positions = []
        self.solve_properly()
        self.Put_Cost_Value()
    
    def solve_properly(self):
        self.clear_copies()
        #flag_of_overfill = False
        #while not(flag_of_overfill):
        self.positions.append(Solution_Position(self.Boxes_List,self.positions))
        self.Put_X_Y_to_positions()
        self.Put_Cost_Value()
        
    def copy(self,positions):
        self.positions = []
        for i in positions:
            self.positions.append(copy.copy(i))
        self.Put_Cost_Value()
        
    def sort_By_X(self,positions):
        return positions.X
    
    def clear_copies(self):
        boxes = []
        for position in self.positions:
            boxes.append(position.box_Num)
            if boxes.count(position.box_Num) > 1:
                self.positions.remove(position)
                
                
    def Put_X_Y_to_positions(self):
        for j in self.positions:
            if j.angle:
                j.height, j.width = j.width, j.height #turn

        list_of_Y = []
        positions_with_X_Y = []
        flag_of_overfill = False
        for current_box in self.positions: #here begins looking for empty space
            flag_put_in_place = False
            #if not(flag_of_overfill):
            list_of_Y = [1]
            for position in positions_with_X_Y:
                list_of_Y.append(position.Y+position.height + 2) #+2 is to avoid pixels crosses
            list_of_Y.sort()
            
            for Y in list_of_Y:
                if not(flag_put_in_place):   #to see if we have found space
                    possible_positions_list_in_Y_line = [0]
                    for position in positions_with_X_Y:
                        if (position.Y <= Y + current_box.height and position.Y+position.height > Y): #pay attention to this place with <= or <
                            possible_positions_list_in_Y_line.append(position.X)
                            possible_positions_list_in_Y_line.append(position.X+position.width)
                    possible_positions_list_in_Y_line.append(FLOOR_WIDTH_PXL)
                    if len(possible_positions_list_in_Y_line)>0:
                        possible_positions_list_in_Y_line.sort(reverse=current_box.position)
                        
                
                        for current_X in possible_positions_list_in_Y_line:
                            if current_box.position:
                                possible_X = current_X - current_box.width
                            else:
                                possible_X = current_X
                            if not(flag_put_in_place):
                                if self.Check_for_crosses_of_list(positions_with_X_Y, possible_X, Y, current_box.width, current_box.height):
                                    flag_of_overfill, positions_with_X_Y = self.Put_in_X_Y_Position_Down_Right_or_Down_Left(current_box.position, flag_put_in_place, Y, current_box, possible_X, positions_with_X_Y, flag_of_overfill)
                                    flag_put_in_place = True
            #else:
                #self.positions.remove(current_box)
                #print "removed"
        self.positions = []
        for i in positions_with_X_Y:
            self.positions.append(i)
        return flag_of_overfill
                

    def Put_in_X_Y_Position_Down_Right_or_Down_Left(self, Right_Or_Left, flag_put_in_place,Y, current_box, possible_X, positions_with_X_Y, flag_of_overfill):
        if Y + current_box.height < FLOOR_HEIGHT_PXL:
            if Right_Or_Left: #true means to right
                current_box.X = possible_X
            else:
                current_box.X = possible_X
            current_box.Y = Y
            positions_with_X_Y.append(current_box)
        else:
            flag_of_overfill = True
            '''self.positions.remove(current_box)'''
        return flag_of_overfill, positions_with_X_Y
    

    
    def Check_for_crosses_of_list(self,positions_with_X_Y, X, Y, width, height):
        if (X < 0 or X + width > FLOOR_WIDTH_PXL):
            return False
        for position in positions_with_X_Y:
            if self.Check_for_crosses (position.X, position.Y, 
                                       position.X+position.width, position.Y+ position.height, 
                                       X, Y, 
                                       X + width, Y + height):
                return False
        return True
    
    def Check_for_crosses (self, AX1, AY1, AX2, AY2, BX1, BY1 , BX2, BY2):
        if (abs(AX1 - BX1) > MAX_BOX_SIZE_PXL or abs(AY1 - BY1) > MAX_BOX_SIZE_PXL):
            return False
        if self.Dot_inside_recktangle(AX1 + 1, AY1 + 1, BX1, BY1, BX2, BY2):
            return True
        if self.Dot_inside_recktangle(AX1 + 1, AY2 - 1, BX1, BY1, BX2, BY2):
            return True
        if self.Dot_inside_recktangle(AX2 - 1, AY1 + 1, BX1, BY1, BX2, BY2):
            return True
        if self.Dot_inside_recktangle(AX2 - 1, AY2 - 1, BX1, BY1, BX2, BY2):
            return True
        
        if self.Dot_inside_recktangle(BX1 + 1, BY1 + 1, AX1, AY1, AX2, AY2):
            return True
        if self.Dot_inside_recktangle(BX1 + 1, BY2 - 1, AX1, AY1, AX2, AY2):
            return True
        if self.Dot_inside_recktangle(BX2 - 1, BY1 + 1, AX1, AY1, AX2, AY2):
            return True
        if self.Dot_inside_recktangle(BX2 - 1, BY2 - 1, AX1, AY1, AX2, AY2):
            return True
        
        if (AX1 < BX1 and AX2 > BX2 and AY1 > BY1 and AY2 < BY2):
            return True
        if (BX1 < AX1 and BX2 > AX2 and BY1 > AY1 and BY2 < AY2):
            return True
        
        return False
    
    def Dot_inside_recktangle(self,X,Y,AX,AY,BX,BY):
        return (X >= AX and X <= BX and Y >= AY and Y <= BY) 
        
    def Put_Cost_Value(self):
        Cost = 0.0
        for i in self.positions:
            Cost = Cost + i.width * i.height
        self.cost = Cost/(FLOOR_HEIGHT_PXL * FLOOR_WIDTH_PXL)
    


        
class Solutions_List(object):
    def __init__(self, count, Boxes_List):
        self.count = count
        self.Boxes_List = Boxes_List
        self.solutions = []
        for i in range(count):
            self.solutions.append(Evristic_solution(Boxes_List))
            
    def Cycle(self):
        self.solutions.sort(key=self.sort_By_Cost, reverse = True) 
        spliting_percent = 0.4

        to_Mutation = int(self.count * spliting_percent)
        i = 0
        while i < self.count-1:
            if  i < to_Mutation:
                self.solutions.append(self.Mutation_of_solution(self.solutions[i]))
            else:
                solution1, solution2 = self.Crossbreeding(self.solutions[i], self.solutions[i + 1])
                self.solutions.append(solution1)
                self.solutions.append(solution2) 
                i = i + 1
            i = i + 1
               
        #taking best solutions      
        solutions_new = []
        while len(solutions_new) < self.count and len(self.solutions) > 1:
            num = random.randint(0,len(self.solutions)-1)
            solution1 = self.solutions[num]
            self.solutions.remove(solution1)
            solution2 = self.solutions[random.randint(0,len(self.solutions)-1)]
            self.solutions.remove(solution2)
            solutions_new.append(self.Selection(solution1,solution2))
        self.solutions = solutions_new  
        self.solutions.sort(key=self.sort_By_Cost, reverse = True)

        
    def Mutation_of_solution (self, solution):
        mutation_rate = 0.1
        mutated_solution = Evristic_solution(self.Boxes_List)
        mutated_solution.copy(solution.positions) 
            
        for i in mutated_solution.positions:
            if random.random() <= mutation_rate:
                mutated_solution.positions.insert(mutated_solution.positions.index(i),Solution_Position(self.Boxes_List, mutated_solution.positions))
                mutated_solution.positions.remove(i)    
            if random.random() <= mutation_rate:
                i.angle = not(i.angle)
            if random.random() <= mutation_rate:
                i.position = not(i.position)
        
        mutated_solution.solve_properly()
        return mutated_solution
     
    def Crossbreeding (self, s1, s2):
        crossbreeding_points = 1
        point = 0
        solution1 = copy.copy(s1)
        solution2 = copy.copy(s2)
        solution1.copy(s1.positions)
        solution2.copy(s2.positions)
        min_length = min(len(solution1.positions),len(solution2.positions))
        for crosbreeding_point in range(crossbreeding_points):
            point = random.randint(0, min_length)
            for position in range(point):
                solution1.positions[position], solution2.positions[position] = solution2.positions[position], solution1.positions[position]
        
        solution1.solve_properly()
        solution2.solve_properly()
        return solution1, solution2
    
    def Selection (self, solution1, solution2):
        if solution1.cost > solution2.cost:
            return solution1
        else:
            return solution2
    
    def sort_By_Cost(self,solution):
        return solution.cost
    
        