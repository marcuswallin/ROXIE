import numpy
import math

class Magnet:

    '''Class that interprates the simulation data, and can calculate
    properties for analysis.'''

    def __init__(self, magnet_properties, displacement, full_movement, n_calculations, start_current, mag_length):
        self._properties = magnet_properties
        
        #changes for all magnets
        self._magnet_length = mag_length
        self._I = start_current

        self._n_calculations = n_calculations
        #contains information on how much and where the displacement has occured
        #list of list containing x,y coordinates
        self._full_movement = full_movement
        self._displacement = displacement
        self._x_values = numpy.linspace(0, self._magnet_length, n_calculations)

        self._y_values = [self._full_movement for i in range(n_calculations)]#list(map(self.get_y, self._x_values))
       
        #self._Ltot = self.calculate_inductance(n_calculations)
        self._M_values = self.calculate_M(magnet_properties)
        for row in self._M_values:
            print(row)
        self._Ltot = 0
        for i in range(self._properties.get_nr_coils()):
            self._Ltot += self.get_L_self(i)
        #    print(self.get_L_self(i))
        
    

    ''' def calculate_inductance(self, n_calculations):
        
        x_vals = self._x_values
        y_vals = self._y_values
        #y_val = self._full_movement
        L_vals = list(map(self._properties.get_L, y_vals))
        print(L_vals)
        Ltot = trapezoidal_integration(x_vals, L_vals)
        return Ltot
    '''

    def Ltot(self):
        return self._Ltot


    def get_new_I(self, magnet0 ):
        '''   '''
        Lzero = magnet0.Ltot()
        
        deltaL = self._Ltot - Lzero
        print('deltaL = '+str(self._Ltot ))
        if deltaL == 0:
            return self._I
        alpha = self._Ltot/deltaL
      #  print(1/alpha)
        deltaI = -self._I/alpha
        Inew = self._I + deltaI
        #Inew = math.sqrt(Lzero/self._Ltot)*self._I
      
        return Inew


    #def get_L_no_movement(self):
    #    x_vals = numpy.linspace(0, self._magnet_length, self._n_calculations)
    #    y_vals = [0]*self._n_calculations
    #    L_vals = list(map(self._properties.get_L, y_vals))
    #    Lzero = trapezoidal_integration(x_vals, L_vals)
    #    return Lzero

    def calculate_M(self, m_properties):

        nr_coils = m_properties.get_nr_coils()
        M = []
        for coil1 in range(nr_coils):
            Mrow = []
            for coil2 in range(nr_coils):
                M_local = [self._properties.get_M(y, coil1, coil2) for y in self._y_values]

                #M_local = [self._properties.get_M(self._full_movement, coil1, coil2 for )]
                Mrow.append(trapezoidal_integration(self._x_values, M_local))
            
            M.append(Mrow)
        return M

        
    def get_L_self(self, coil):
        Lself  = 0
        for i in range(self._properties.get_nr_coils()):
            Lself += self._M_values[coil][i]
        return Lself



    def get_y(self, x):
        '''Returns y-value, based on x-value
        
        For a given x position, interpolates the displacement 
        and returns a y-value.
        The unit of the y-value is depending omn the input, 
        but mostly mm and degrees
        '''
        if x < 0  or x > self._magnet_length:
            raise ValueError(str(x) + ' is not a valid x input.')
        start = [0, 0]
        end = [self._magnet_length, 0]
        positions = [start, end]

        for displ in self._displacement:
            positions.append(displ)
        positions.sort(key=lambda x: x[0], reverse=False)

        #returns the index of interpolation
        for i, pos in enumerate(positions):
            if x < pos[0]:
                break

        x1 = positions[i-1][0]
        y1 = positions[i-1][1]
        x2 = positions[i][0]
        y2 = positions[i][1]
        
        k = (y2-y1)/(x2-x1)
        m = y1 - k*x1
        return k*x+m
    

    def get_Phi_in_QA(self, QA_xstart, QA_xend, n_turns):
        '''Integrates the B-value over the quench antenna.

        Inputs: QA_xstart - xposition for the start of the QA
                QA_xstart - xposition for the end of the QA
                n_calculations - number of integration points in the QA
                n_turns - How many turns the QA has.

        Returns the magnetic field inside the quench antenna.
        '''
        properties = self._properties
      #  QAlength = QA_xend-QA_xstart
       
        x_vals = numpy.linspace(QA_xstart, QA_xend, self._n_calculations)
        #y_vals = list(map(self.get_y, x_vals))
        y_vals = [self._full_movement for i in range(self._n_calculations)]
        Bm_vals = list(map(properties.get_Bm, y_vals))
        phi  = trapezoidal_integration(x_vals, Bm_vals)

        return phi*n_turns

#move to other module
def get_energy_movement(coil, magnet_new, magnet0 ):
    deltaL = (magnet_new.get_L_self(coil) - magnet0.get_L_self(coil))
    midL = (magnet_new.get_L_self(coil) + magnet0.get_L_self(coil))/2
    
    deltaI = magnet_new.get_new_I(magnet0) - magnet0._I
    midI = (magnet_new.get_new_I(magnet0) + magnet0._I)/2

    return midI * (midI * deltaL + midL * deltaI)


def trapezoidal_integration(x, y):
    '''Integrates the y-values with the trapezoidal rule.
    Currently requires the x values to have equal steplength.

    If needed can be extended to integrate with varying steplength.'''
    if len(x) < 2 or len(y) < 2:
        raise ValueError('Values must be 2 or more.')

    if len(x) != len(y):
        raise ValueError('X and Y must be same length.')

    dx = x[1]-x[0]
    y_right = y[1:]
    y_left = y[:-1]

    tot = (dx/2)*(sum(y_right)+sum(y_left))
    return tot





    


