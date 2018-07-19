from random import uniform
from drawing import FLOOR_WIDTH_PXL
MAX_BOX_SIZE_PXL = int (FLOOR_WIDTH_PXL * 0.35)

counter = 0

class Box(object):
    def __init__(self):
        self.height = int(uniform(0.4,1)*MAX_BOX_SIZE_PXL)
        self.width = int(uniform(0.4,1)*MAX_BOX_SIZE_PXL)
        coefficient = float((self.width*self.height))/(MAX_BOX_SIZE_PXL**2)
        self.color = (int(uniform(0.1,1)*(70+150*coefficient)), int(110 + 145*coefficient), int(uniform(0.1,1)*(70+150*coefficient)))
        global counter
        self.box_Num = counter
        counter += 1
        print" Box Number: "+ str(counter) + " Height: " + str(self.height) + " Width: " + str(self.width)
    