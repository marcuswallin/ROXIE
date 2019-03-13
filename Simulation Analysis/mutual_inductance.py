

class MutualInductance:
    
    
    def __init__(self, movement, inductances):
        self._nr_coils = len(inductances)
        self._M_values = inductances

        #do not work properly now
        self._movement = movement


    def get_M_coil(self, coil1, coil2):
        
        return self._M_values[coil1][coil2]