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

settings_list = [QA_length,  0.011, 36, gain, mag_length, 0.008, current]

def main():
    name = 'Horizontal_2coils.csv'
    file = '\\\\cern.ch\\dfs\\Users\\m\\mwallin\\' \
        + 'Documents\\ROXIE\\Processed Data\\FRESCA2\\'+name
    results_file = '\\\\cern.ch\\dfs\\Users\\m\\mwallin\\' \
        + 'Documents\\ROXIE\\Results Simulation\\FRESCA2\\'+ 'top_roll_double.csv'
    file2 = '\\\\cern.ch\\dfs\\Users\\m\\mwallin\\' \
        + 'Documents\\ROXIE\\Processed Data\\FRESCA2\\Outer_Roll_2coils.csv'
    
    m_properties1 = read_movement_data(file)
    m_properties2 = read_movement_data(file2)
    
    #movements in mm
    movement1 = 0.5
    movement2 = 0.0000

    magnet = Magnet(m_properties1, [[mag_mid, movement1]], movement1, 1000, current, mag_length)
    magnet2 = Magnet(m_properties2, [[mag_mid, movement2]], movement2, 1000, current, mag_length)
 

    phi_move1 = magnet.get_Phi_in_QA((mag_length-QA_length)/2, \
            (mag_length+QA_length)/2, 36)
    phi_move2 = magnet2.get_Phi_in_QA((mag_length-QA_length)/2, \
            (mag_length+QA_length)/2, 36)


    magnet0 = Magnet(m_properties1, [[mag_mid, 0.0]], 0, 1000, current, mag_length)
    phi0 = magnet0.get_Phi_in_QA((mag_length-QA_length)/2, \
            (mag_length+QA_length)/2, 36)
    deltaI = ((magnet.get_new_I(magnet0)-current) + \
        (magnet2.get_new_I(magnet0)-current))

 #   print('Integrated voltage from movement: ', 100*(phi_move1-phi0))
  #  print('Integrated voltage from current drop: ', 100*(deltaI*0.001*QA_length*0.011*36))

    Vmov = gain*((phi_move1-phi0)+(phi_move2-phi0))
    Vcurrdrop = gain*(deltaI*0.001*QA_length*0.011*nturns)
    print(deltaI)
 #   Eleak = 0
  #  Ltot = 0
    energy_list = []
    for i in range(4):
        energy1 = get_energy_movement(i, magnet, magnet0)
        energy2 = get_energy_movement(i, magnet2, magnet0)
        energy_list.append(energy1+energy2)
    #    print('Coilnr: ' + str(i) + ' ' + str(energy))
     #   Eleak += energy
    #    Ltot += magnet.get_L_self(i)
    energy_list[0], energy_list[1] = energy_list[1], energy_list[0]

    energy_list = list(reversed(energy_list))
    print_results(results_file, settings_list, energy_list, Vcurrdrop, Vmov)

    


if __name__ == '__main__':
    main()
