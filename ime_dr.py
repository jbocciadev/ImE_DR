''' Python script to check FTP connections are up for all active portals in ImE, for DR exercise '''

import os, datetime

from csv import DictReader
from time import sleep


sourceFile = 'portals_full_info.csv'
divider = "*-" * 20


def drExercise():
    ''' Main function for DR exercise. Checks for csv file, loads into memory and pings/ftp checks portals. '''
    # In future, implement output to file.
    # timeStamp = datetime.datetime.now().strftime('%Y%m%d-%X')
    # destfile = f'DR_exercise_{timeStamp}'

    # Check for csv file in directory
    if not os.path.isfile(sourceFile):
        print('Source CSV file not found. Please save file "portals_full_info.csv" in this directory and retry.')
    else:
        print('Source CSV file found, loading...')
        sleep(0.5)
        portals = loadCsv(sourceFile)
        print(f"\nPortals loaded: {len(portals)}")
        
        for portal in portals:
            pingPortal(portal)
            pass # Implement ftp connection check

    print(f"\n{divider}\nDR Exercise finished.\n")


def loadCsv(sourceFile):
    ''' Function that loads portal details from portals_full_info.csv file. '''
    portals = []
    with open(sourceFile, newline='') as csvfile:
        reader = DictReader(csvfile, delimiter=';')
        fields = ['SYSTEM', 'PORTAL', 'HOSTNAME', 'USERNAME', 'PASSWORD', 'DIRECTORY'] # Only these fields are to be brought over
        counter = 0
        for row in reader:
            if row['STATUS'] == 'A' and row['ROUTE STATUS'] =='Enabled' and row['HOSTNAME']: # Check for active portals with a hostname.
                counter += 1
                portal = {}
                for field in fields:
                    portal[field] = row[field]
                portals.append(portal)
                print("\rPortals imported: {}". format(counter), end='')
                sleep(.025)
        # print("")
    return portals


def pingPortal(portal):
    # param = '-n' if os.sys.platform().lower()=='win32' else '-c'
    param = '-c'
    hostname = portal['HOSTNAME']
    print(f"\n{divider}\nPortal: {portal['SYSTEM']} | {portal['PORTAL']}")
    response = os.system(f'ping -c 1 {hostname}')
    
    if response == 0:
        print(f"\nPortal {portal['SYSTEM']} | {portal['PORTAL']} is up!")
    else:
        print(f"\nPortal {portal['SYSTEM']} | {portal['PORTAL']} seems to be down. Please check!")


if __name__ == '__main__':
    drExercise()
