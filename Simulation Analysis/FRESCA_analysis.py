import sys, os
from magnet_properties import MagnetProperties, read_movement_data
from magnet import Magnet, get_energy_movement
from print_results import print_results
import numpy


mag_length = 1.6
mag_mid = mag_length/2
QA_length = 0.249
gain = 100
current = 11850
nturns = 36
movement1 = -0.005

settings_list = [QA_length,  0.011, 36, gain, mag_length, movement1, current]

def main():
    name = 'Vertical.csv'
    file = '\\\\cern.ch\\dfs\\Users\\m\\mwallin\\' \
        + 'Documents\\ROXIE\\Processed Data\\FRESCA2\\'+name
    results_file = '\\\\cern.ch\\dfs\\Users\\m\\mwallin\\' \
        + 'Documents\\ROXIE\\Results Simulation\\FRESCA2\\thesis new cB\\'+ 'v_single.csv'

    m_properties1 = read_movement_data(file)

    magnet = Magnet(m_properties1, [[mag_mid, movement1]], movement1, 1000, current, mag_length)


    phi_move1 = magnet.get_Phi_in_QA((mag_length-QA_length)/2, \
            (mag_length+QA_length)/2, 36)


    magnet0 = Magnet(m_properties1, [[mag_mid, 0.0]], 0, 1000, current, mag_length)
    phi0 = magnet0.get_Phi_in_QA((mag_length-QA_length)/2, \
            (mag_length+QA_length)/2, 36)
    
    deltaLtot = magnet._Ltot - magnet0._Ltot
    deltaI = (magnet.get_new_I(magnet0)-current) 

    Vmov = gain*(phi_move1-phi0)
    Vcurrdrop = gain*(deltaI*0.0011384*QA_length*0.011*nturns)
    print(deltaI)

    energy_list = []
    for i in range(4):
        energy1 = get_energy_movement(i, magnet, magnet0)

        energy_list.append(energy1)

    energy_list[0], energy_list[1] = energy_list[1], energy_list[0]

    energy_list = list(reversed(energy_list))
    print_results(results_file, settings_list, energy_list, Vcurrdrop, Vmov, deltaI, deltaLtot )

    


if __name__ == '__main__':
    main()
