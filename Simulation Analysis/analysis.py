import sys, os
from magnet_properties import MagnetProperties, read_movement_data
from magnet import Magnet, get_energy_movement
from field_calculations import calculate, compare_movement
import numpy


mag_length = 1.691
mag_mid = mag_length/2
QA_length = 0.249

def main():
    file1 = '\\\\cern.ch\\dfs\\Users\\m\\mwallin\\' \
        + 'Documents\\ROXIE\\Processed Data\Horizontal.csv'
    file2 = '\\\\cern.ch\\dfs\\Users\\m\\mwallin\\' \
        + 'Documents\\ROXIE\\Processed Data\Mid_Roll.csv'
    
    m_properties1 = read_movement_data(file1)
    m_properties2 = read_movement_data(file2)
    

    magnet = Magnet(m_properties1, [[mag_mid, 0.01]], 1000, 12000)
    magnet2 = Magnet(m_properties2, [[mag_mid, 0.1]], 1000, 12000)

    phi_move1 = magnet.get_Phi_in_QA((mag_length-QA_length)/2, \
            (mag_length+QA_length)/2, 36)

    phi_move2 = magnet2.get_Phi_in_QA((mag_length-QA_length)/2, \
            (mag_length+QA_length)/2, 36)



    magnet0 = Magnet(m_properties1, [[mag_mid, 0.0]], 1000, 12000)
    phi0 = magnet0.get_Phi_in_QA((mag_length-QA_length)/2, \
            (mag_length+QA_length)/2, 36)
    deltaI = magnet.get_new_I(magnet0)+magnet2.get_new_I(magnet0)-2*magnet0._I

    print('Integrated voltage from movement: ', 100*(phi_move1+phi_move2-2*phi0))
    print('Integrated voltage from current drop: ', 100*(deltaI*0.001*QA_length*0.011*36))

    Eleak = 0
    Ltot = 0
    for i in range(4):
        energy = get_energy_movement(i, magnet, magnet0)
        energy2 = get_energy_movement(i, magnet2, magnet0)
        print('Coilnr: ' + str(i) + ' ' + str(energy+energy2))
        Eleak += energy
        Ltot += magnet.get_L_self(i)


    #movement = list(numpy.linspace(-0.5,0.5, 100))
    
    #calculate(m_properties, movement)
    #compare_movement([0.025], m_properties)
    #phi = get_phi_from_movement(movement, m_properties)
    #plot_val_and_get_interpolation(movement, phi)
  


if __name__ == '__main__':
    main()
