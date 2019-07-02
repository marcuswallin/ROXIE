import csv

def print_results(file_name, settings_list, energy_list, Vcurrdrop, Vmov, deltaI, deltaLtot):

    with open(file_name, mode='w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, lineterminator="\n")
       
        
        writer.writerow(['CoilNr','Energy [J]'])
        for i, energy in enumerate(energy_list):
            writer.writerow([str(i+1), str(energy)])
        

        writer.writerow(['delta L', str(deltaLtot)])
        writer.writerow(['delta I', str(deltaI)])

        writer.writerow(['Integrated Voltage from Movement', str(Vmov)])
        writer.writerow(['Integrated Voltage from Current Drop', str(Vcurrdrop)])

        writer.writerow(['Settings'])
        writer.writerow(['QA length', 'QA width', 'QA nr turns', \
            'Voltage Gain', 'Magnet length', 'Movement', 'Current [A]'])
        writer.writerow(settings_list)
            



