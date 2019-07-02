

class MutualInductance:
    
    
    def __init__(self, movement, inductances):
        self._nr_coils = len(inductances)
        self._M_values = inductances
        self._movement = movement


    def get_M_coil(self, coil1, coil2):
        
        return self._M_values[coil1][coil2]