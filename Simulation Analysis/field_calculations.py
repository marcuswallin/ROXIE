

from magnet import Magnet, trapezoidal_integration
import numpy
from matplotlib import pyplot

mag_length = 1.691
mag_mid = mag_length/2
QA_length = 0.249


def calculate(m_properties, movement):

    deltaI = get_current_drop(movement, m_properties)
    print(m_properties.get_M(0, 1, 0))
    print(m_properties.get_M(0, 1, 1))
    print(m_properties.get_M(0, 1, 2))
    print(m_properties.get_M(0, 1, 3))
    m_properties.get_M(0.5)
   # plot_val_and_get_interpolation(movement, deltaI)



#
def compare_movement(movement, properties):
    phi = get_phi_from_movement(movement, properties)
    QA = get_current_drop(movement, properties)
    phi0 = get_phi_from_movement([0], properties)
    QA0 = get_current_drop([0], properties)

    print(phi0[0]-phi[0])
    print(QA0[0]-QA[0])
#returns expected delta I, delta QA and delta E
#







def get_phi_from_movement(movement, properties):
    phi = []

    for m in movement:
        interprator = Magnet(properties, [[mag_mid, m]], 100, 10000)
        phi.append(interprator.get_Phi_in_QA((mag_length-QA_length)/2, \
            (mag_length+QA_length)/2, 100, 36))

    return phi

#change name
def get_current_drop(movement, properties):
    I = []
 #   interprator = Magnet(properties, [[mag_mid, movement[0]]])
 #   interprator.calculate_inductance(100)
    for m in movement:
        interprator = Magnet(properties, [[mag_mid, m]], 100, 10000)
        I.append(interprator.get_I_in_magnet(100,10000))
    
    return I





def plot_val_and_get_interpolation(movement, val ):
    k, m = numpy.polyfit(movement, val, 1)

    print(k,m)
    fitted = []
    for i in movement:
        fitted.append(i*k+m)
    pyplot.plot(movement, val, 'ro')
    pyplot.plot(movement, fitted)
    pyplot.show()
