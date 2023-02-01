# to be done for this script
# 1 : access the config.xml file in write mode
# 2 : access in read mode and loop thru transmitters in transmitter file
# 3 : replace the transmitter in the xml file with the transmitter from the file
# 4 : access the command line and run the ray tracer
# 5 : when the file is generated, rename the file

# for running shell commands
import os

# number passed in must be a float
# normally I'd include type handling but since we're using this for a very specific function it is a waste of time
def removeDecimal(num):
    if num is not int:
        num_parts = str(num).split('.')
        return(num_parts[0]+"p"+num_parts[1])

# grab entire content of xml file
# add in lo/hi fidelity specs

config = open("Config.xml", "r")
content_capture = config.readlines()
content_capture[118] = "\t<num_transmission_max>1</num_transmission_max>\n"
content_capture[119] = "\t<num_diffraction_max>1</num_diffraction_max>\n"
content_capture[132] = "\t<receiver_position_filename>ReceiverPositions.dat</receiver_position_filename>\n"
config.close()

# access transmitter locations
trans_file = open("TransmitterPositions.csv", "r")
current_trans_xyz = trans_file.readline().split()

# loop through all transmitters
while current_trans_xyz != []:

    trans_name = ['','','']
    # writing the filename
    for index in range(0,3):
        if float(current_trans_xyz[index])<0:
            trans_name[index] = "n"+removeDecimal(float(current_trans_xyz[index])*-1)

        else:
            trans_name[index] = removeDecimal(float(current_trans_xyz[index]))

    filename = "x"+str(trans_name[0])+"_y"+str(trans_name[1])+"_z"+str(trans_name[2])+".csv"
    
    print("lofi RT sim of transmitter at",current_trans_xyz)

    # reopen config file to set transmitter location
    config = open("Config.xml", "w")
    content_capture[117] = "\t<num_reflection_max>1</num_reflection_max>\n"
    content_capture[75] = "\t<source_position> <x>" +   current_trans_xyz[0]\
                          + "</x> <y>"              +   current_trans_xyz[1]\
                          + "</y> <z>"              +   current_trans_xyz[2]\
                          + "</z> </source_position>\n"
    config.writelines(content_capture)
    config.close()

    # run ray tracer and rename it
    os.system("RayTubeTracing.exe")
    os.system("rename ReceivedPowers.csv lofi_"+filename)
    os.system("move lofi_"+filename+" lofi_maps")

##    print("hifi RT sim of transmitter at",current_trans_xyz)
##    
##    # hifi section
##    config = open("Config.xml", "w")
##    content_capture[117] = "\t<num_reflection_max>5</num_reflection_max>\n"
##    config.writelines(content_capture)
##    config.close()
##
##    # run ray tracer and rename it
##    os.system("RayTubeTracing.exe")
##    os.system("rename ReceivedPowers.csv hifi_"+filename)
##    os.system("move hifi_"+filename+" hifi_maps")
    
    # collect next transmitter
    current_trans_xyz = trans_file.readline().split()

trans_file.close()
