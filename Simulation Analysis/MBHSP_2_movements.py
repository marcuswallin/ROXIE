import sys, os
from magnet_properties import MagnetProperties, read_movement_data
from magnet import Magnet, get_energy_movement
#from field_calculations import calculate, compare_movement
import numpy
from print_results import print_results


mag_length = 1.691
mag_mid = mag_length/2
QA_length = 0.249
gain = 100
current = 12900
nturns = 36
movement1 = 0.00013
movement2 = 0.00018
settings_list = [QA_length,  0.01152, 36, gain, mag_length, movement1, current]
def main():
    #name = 'horizontal.csv'
    file1 = '\\\\cern.ch\\dfs\\Users\\m\\mwallin\\' \
        + 'Documents\\ROXIE\\Processed Data\\MBHSP\\Horizontal.csv'
 
    file2 = '\\\\cern.ch\\dfs\\Users\\m\\mwallin\\' \
        + 'Documents\\ROXIE\\Processed Data\\MBHSP\\Mid_Roll.csv'

    results_file = '\\\\cern.ch\\dfs\\Users\\m\\mwallin\\' \
        + 'Documents\\ROXIE\\Results Simulation\\MBHSP\\transient39.csv'
    
    m_properties1 = read_movement_data(file1)
    m_properties2 = read_movement_data(file2)
    magnet1 = Magnet(m_properties1, [[mag_mid, movement1]], movement1,1000, current, mag_length)
    magnet2 = Magnet(m_properties2, [[mag_mid, movement2]], movement2,1000, current, mag_length)

    phi_move1 = magnet1.get_Phi_in_QA((mag_length-QA_length)/2, \
            (mag_length+QA_length)/2, nturns)
    phi_move2 = magnet2.get_Phi_in_QA((mag_length-QA_length)/2, \
            (mag_length+QA_length)/2, 36)

    magnet0 = Magnet(m_properties1, [[mag_mid, 0.0]], 0,1000, current, mag_length)
    phi0 = magnet0.get_Phi_in_QA((mag_length-QA_length)/2, \
            (mag_length+QA_length)/2, 36)
    
    deltaI = ((magnet1.get_new_I(magnet0)-current) + \
        (magnet2.get_new_I(magnet0)-current))
    print(deltaI)

    Vmov = gain*((phi_move1-phi0)+(phi_move2-phi0))
    Vcurrdrop = gain*(deltaI*0.001*QA_length*0.011*nturns)

    energy_list = []
    for i in range(4):
        energy1 = get_energy_movement(i, magnet1, magnet0)
        energy2 = get_energy_movement(i, magnet2, magnet0)
        energy_list.append(energy1+energy2)
    
    energy_list[0], energy_list[1] = energy_list[1], energy_list[0]
    energy_list = list(reversed(energy_list))
    print_results(results_file, settings_list, energy_list, Vcurrdrop, Vmov)



if __name__ == '__main__':
    main()
