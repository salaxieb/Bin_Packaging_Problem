import random
random.seed(1234567890)
from drawing import FLOOR_HEIGHT_PXL
from drawing import SCREEN_HIGHT_PXL
from drawing import SCREEN_WIDTH_PXL
from drawing import WHITE
from FCNR_solution import FCNR
from Evristic_solution import Evristic_solution, Solutions_List
import pygame,  sys
from pygame.locals import QUIT
from Box import Box
from drawing import Floor_Drawing
from drawing import Box_Drawing
from drawing import Graph
import time
Boxes_List = []
print "0"
for i in range(30): 
    Boxes_List.append(Box())

pygame.init()
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH_PXL, SCREEN_HIGHT_PXL))
pygame.display.set_caption('Drawing')
print "1"
''''E = Evristic_solution(Boxes_List)'''
M = Evristic_solution(Boxes_List)

    

Solutions = Solutions_List(100,Boxes_List)
i = 0
while i < 15:    
    Solutions.Cycle()
    i = i + 1

R = FCNR()

print "done"

def Drawing(Boxes_List):    
    DISPLAYSURF.fill(WHITE)  
    Floor_Drawing(DISPLAYSURF, 1)
    Floor_Drawing(DISPLAYSURF, 0)
    
    cycle = 0
    costs = []
    while cycle < 200:
        DISPLAYSURF.fill(WHITE)  
        Floor_Drawing(DISPLAYSURF, 1)
        Floor_Drawing(DISPLAYSURF, 0)

        Solutions.Cycle()
        E = Solutions.solutions[0]  
        print E.cost         
            
        for i in E.positions:
            Box_Drawing(DISPLAYSURF,0,i.box_Num, i.X, i.Y, i.width, i.height, i.color, i.angle)
        costs.append(E.cost)
        
        Graph(DISPLAYSURF,costs)
        R.solve(E.positions)
        
        for i in R.positions:
            Box_Drawing(DISPLAYSURF,1,i.box_Num, i.X, i.Y, i.width, i.height, i.color, i.angle, out_of_box= (i.Y+i.height > FLOOR_HEIGHT_PXL))
        
        
           
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        cycle = cycle+1
        print cycle
    print E.cost
    print R.cost
    print time.clock()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
    
    

 
Drawing(Boxes_List)      
