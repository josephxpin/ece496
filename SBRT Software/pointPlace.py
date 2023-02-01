import numpy as np
from decimal import Decimal

def format_e(n):
    a = '%E' % n
    return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]

end = "n"

while end == "n":
    acceptable = False
    while not acceptable:
        min_x = float(input("Minimum x-coordinate: "))
        max_x = float(input("Maximum x-coordinate: "))
        min_y = float(input("Minimum y-coordinate: "))
        max_y = float(input("Maximum y-coordinate: "))
        z = input("z-coordinate: ")

        if min_x > max_x:
            print("Invalid x entries")
        elif min_y > max_y:
            print("Invalid y entries")
        else:
            acceptable = True

    file = open("TransmitterPositions.csv","a")
    
    for x in np.arange(min_x,max_x+0.5,0.5):
        for y in np.arange(min_y,max_y+0.5,0.5):
            file.write('%s %s %s\n' %( format_e(Decimal(x)), format_e(Decimal(y)), format_e(Decimal(z)), ))

    file.close()   
    end = input("Done (y/n)? ")
