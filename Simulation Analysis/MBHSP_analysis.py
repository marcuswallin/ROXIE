import sys, os
from magnet_properties import MagnetProperties, read_movement_data
from magnet import Magnet, get_energy_movement
import numpy
from print_results import print_results


mag_length = 1.691
mag_mid = mag_length/2
QA_length = 0.249
gain = 100
current = 11850
nturns = 36
movement1 = 0.01

settings_list = [QA_length,  0.01152, 36, gain, mag_length, movement1, current]
def main():

    file1 = '\\\\cern.ch\\dfs\\Users\\m\\mwallin\\' \
        + 'Documents\\ROXIE\\Processed Data\\MBHSP\\Vertical.csv'
 
    results_file = '\\\\cern.ch\\dfs\\Users\\m\\mwallin\\' \
        + 'Documents\\ROXIE\\Results Simulation\\MBHSP\\thesis\\vertical_3.csv'
    
    m_properties1 = read_movement_data(file1)
    magnet1 = Magnet(m_properties1, [[mag_mid, movement1]], movement1,1000, current, mag_length)

    phi_move1 = magnet1.get_Phi_in_QA((mag_length-QA_length)/2, \
            (mag_length+QA_length)/2, nturns)


    magnet0 = Magnet(m_properties1, [[mag_mid, 0.0]], 0,1000, current, mag_length)
    phi0 = magnet0.get_Phi_in_QA((mag_length-QA_length)/2, \
            (mag_length+QA_length)/2, 36)
    
    deltaLtot = magnet1._Ltot - magnet0._Ltot
    deltaI = (magnet1.get_new_I(magnet0)-current) 

    print(deltaI)

    Vmov = gain*(phi_move1-phi0)
    Vcurrdrop = gain*(deltaI*0.0009477*QA_length*0.011*nturns)

    energy_list = []
    for i in range(4):
        energy1 = get_energy_movement(i, magnet1, magnet0)

        energy_list.append(energy1)#+energy2)
    
    energy_list[0], energy_list[1] = energy_list[1], energy_list[0]
    energy_list = list(reversed(energy_list))
    print_results(results_file, settings_list, energy_list, Vcurrdrop, Vmov, deltaI, deltaLtot)



if __name__ == '__main__':
    main()
