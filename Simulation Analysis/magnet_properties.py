
from numpy import interp
import csv
from mutual_inductance import MutualInductance

class MagnetProperties:

    def __init__(self, movement, inductance, Bm, M_list):
        self._movement = movement
        self._inductance = inductance
        self._Bm = Bm
        self._M_list = M_list
    

        self._min_y = min(movement)
        self._max_y = max(movement)

    def min_y(self):
        return self._min_y

    def max_y(self):
        return self._min_y
      
    def get_M(self, y, coil1, coil2):
        '''calculates the expected M (mH/m), with a movement according to the 
        y parameter.
    
        Returns a float value. Only possible to call if the movement is within 
        the outer bounds of the input file.'''

        if y < self._min_y or y > self._max_y:
            raise ValueError('Y-Value: '+ str(y) + ' is outside of bounds, should be within: ' + \
                str(self._min_y) +' - +' + str(self._max_y))

        Mlist = []
        for M in self._M_list:
            Mlist.append(M.get_M_coil(coil1, coil2))
        
        return interp(y, self._movement, Mlist) 

    def get_Bm(self, y):
        '''calculates the expected Bm (mH/m), with a movement according to the 
        y parameter.
    
        Returns a float value. Only possible to call if the movement is within 
        the outer bounds of the input file.'''
        if y < self._min_y or y > self._max_y:
            raise ValueError('Y-Value: '+ str(y) + ' is outside of bounds, should be within: ' + \
                str(self._min_y) +' - +' + str(self._max_y))

        return interp(y, self._movement, self._Bm)

    def get_nr_coils(self):
        return self._M_list[0]._nr_coils


    def get_L(self, y):
        '''calculates the expected L/m (mH/m), with a movement accoriding to the 
        movement parameter.
    
        Returns a float value. Only possible to call if the movement is within 
        the outer bounds of the input file.'''
        if y < self._min_y or y > self._max_y:
            raise ValueError('Y-Value is outside of bounds, should be within: ' + \
                str(self._min_y) +' - +' + str(self._max_y))

        return interp(y, self._movement, self._inductance)



#currently only reads movement, inductance and Bm
def read_movement_data(file):

    movement = []
    inductance = []
    Bm = []
    M = []
    Mlist = []

    with open(file, mode='rt', encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        for row in readCSV:
            if row[0].isdigit():
                movement.append(float(row[1]))
                inductance.append(float(row[2])*0.001)
                Bm.append(float(row[3]))
            elif(row[0] == " "):
                vals = list(map(lambda x : float(x)*0.001, row[1:]))
               
                M.append(vals)


            if len(M) == 4:
                Mlist.append(MutualInductance(movement, M))
                M = [] 
            

           # print(row[0] + "...")

            #else if (len(row)>)

    #for M in Mlist:      
     #   print(M._M_values)
    return MagnetProperties(movement, inductance, Bm, Mlist)

        



