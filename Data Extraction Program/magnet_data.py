import csv
import os
class MagnetData:
    '''Class for containing data from a simulation in ROXIE
    '''
    def __init__(self, file_name, inductance, B_values, M_values):
        self._file_name = file_name
        self._inductance = inductance
        self._B_values = B_values
        self._M_values = M_values
        filename, file_extension = os.path.splitext(file_name)
        self._movement = float(filename.split(' ')[-1])
        self._QA_width = 0
        
    def movement(self):
        return self._movement


    def file_name(self):
        return self._file_name

    def inductance(self):
        return self._inductance

    def B_values(self):
        '''List of tuples where the first value in the tuple is the x-position 
        of the measurement, and the second is the B-value.'''
        return self._B_values

    def M_values(self):
        return self._M_values

    def QA_width(self):
        return self._QA_width

    '''MBHSP:
       Total magnet inductance 10.487-11.698 mH
       in testdata file 9.63 mH
       Measurements: 5.3781 mH/m
       Magnetic length: 1.691 m
    
    '''
    def get_B_in_QA(self):
        Bm = 0
        x = []
        B = []
        
        for B_tuple in self._B_values:
            x.append(B_tuple[0]*0.01)
            B.append(B_tuple[1])
        Bm = trapezoidal_integration(x,B)
        
        self._QA_width = x[-1]-x[0]
        print('QA width: '+ str(self._QA_width))

         #   xdif = self._B_values[i][0]-self._B_values[i-1][0]
        #    B = self._B_values[i][1]
         #   Bm += xdif*B
        return Bm


def write_magnet_file(magnetdata, file_name):
    
    magnetdata.sort(key=lambda x: x._movement, reverse=False)

    with open(file_name, mode='w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, lineterminator="\n")
        magnetdata[0].get_B_in_QA()
        QA = magnetdata[0].QA_width()
        writer.writerow(['LinkNr','Movement', 'L', \
             f'Bm, QAwidth = {QA:.5f}m'])
        for i,data in enumerate(magnetdata):
            writer.writerow([str(i), \
                data.movement(), \
                data.inductance(), 
                data.get_B_in_QA()])
        
        for i1, data in enumerate(magnetdata):
            writer.writerow(['Mutual Inductance index ' + str(i1)])
            for Mrow in data.M_values():
                writer.writerow([' ', Mrow[0], Mrow[1], Mrow[2], Mrow[3]])
            

        # readCSV = csv.reader(csvfile, delimiter=',')

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

            





def extract_magnetdata(file_list, directory):
    '''Extracts data from ROXIE files. 
    Returns a list containing MagnetData objects with that data. 

    Arguments: file_list: string list of all files in the directory folder
               directory: directory containing the files.

    '''
    magnetdata_list = []
    for f in file_list:
        inductance = 0
        extracting_B_values = False
        extracting_M_values = False
        B_values = []
        M_values = []

        with open(directory+'\\'+f, mode = 'r') as magnetfile:
          data = magnetfile.readlines()
        
        for i, line in enumerate(data):
            
            if 'TOTAL INDUCTANCE' in line:
                line_content = line.split()
                inductance = float(line_content[-1])

            if 'GRAPH' in line:
                extracting_B_values = True

            if extracting_B_values:
                line_content = line.split()
                if len(line_content) < 1:
                    extracting_B_values = False  
                elif line_content[0].isdigit():
                    B_values.append((float(line_content[2]), float(line_content[4])))
                
            if 'SELF AND MUTUAL INDUCTANCES' in line:
                extracting_M_values = True

            if extracting_M_values:
                line_content = line.split()
                if extracting_B_values:
                    extracting_M_values = False  
                elif len(line_content) > 4 and line_content[0].isdigit():
                    M_values.append(
                        [float(line_content[1]),  \
                        float(line_content[2]),   \
                        float(line_content[3]),   \
                        float(line_content[4])])
                

        magnetdata_list.append(MagnetData(f, inductance, B_values, M_values))

    return magnetdata_list

