''' Python script to check FTP connections are up for all active portals in ImE, for DR exercise '''

import sys, os, datetime

from csv import DictReader
from time import sleep


sourceFile = 'portals_full_info.csv'
fields = ['SYSTEM', 'PORTAL', 'HOSTNAME', 'USERNAME', 'PASSWORD', 'DIRECTORY'] # Only these fields are to be brought over
divider = "*-" * 20


def drExercise():
    ''' Main function for DR exercise. Checks for csv file, loads into memory and pings/ftp checks portals. 
    If test scenario, run python3 (ime_dr win or dr) (ip to check) (username) (password)'''

    timeStamp = datetime.datetime.now().strftime('%Y-%m-%d @ %X')
    print(f"\nDR exercise started on {timeStamp}")
    # In future, implement output to file.
    # destfile = f'DR_exercise_{timeStamp}'

    # Implement test scenario with cmd arguments
    if len(sys.argv) == 6:
        print("\nThis is a test scenario with the following parameters:")
        print(sys.argv[1:])

        if sys.argv[1].lower() == 'win':
            param = '-n'
        else:
            param = '-c'
        hostname = sys.argv[2]
        user = sys.argv[3]
        password = sys.argv[4]
        directory = sys.argv[5]
        portal = {
            'SYSTEM': 'TEST',
            'PORTAL': 'TEST',
            'HOSTNAME': hostname,
            'USERNAME': user,
            'PASSWORD': password,
            'DIRECTORY': directory
        }
        pingPortal(portal, param)
    elif len(sys.argv) == 1:
        # Check for csv file in directory
        if not os.path.isfile(sourceFile):
            print('Source CSV file not found. Please save file "portals_full_info.csv" in this directory and retry.')
        else:
            print('Source CSV file found, loading...')
            sleep(0.5)
            portals = loadCsv(sourceFile) # Load portals from csv file
            print(f"\nPortals loaded: {len(portals)}")
            
            for portal in portals: # Ping portals 1 by 1
                param = '-c'
                pingPortal(portal)
                pass # Implement ftp connection check
    else:
        print("Please submit 0 arguments for DR exercise or 5 arguments for test scenario")
    
    timeStamp = datetime.datetime.now().strftime('%Y-%m-%d @ %X')
    print(f"\n{divider}\nDR Exercise finished on {timeStamp}.\n")


def loadCsv(sourceFile):
    ''' Function that loads portal details from portals_full_info.csv file. '''
    portals = []
    with open(sourceFile, newline='') as csvfile:
        reader = DictReader(csvfile, delimiter=';')
        # fields = ['SYSTEM', 'PORTAL', 'HOSTNAME', 'USERNAME', 'PASSWORD', 'DIRECTORY'] # Only these fields are to be brought over
        counter = 0
        for row in reader:
            if row['STATUS'] == 'A' and row['ROUTE STATUS'] =='Enabled' and row['HOSTNAME']: # Check for active portals with a hostname.
                counter += 1
                portal = {}
                for field in fields:
                    portal[field] = row[field]
                    print(portal)
                portals.append(portal)
                print("\rPortals imported: {}". format(counter), end='')
                sleep(.025)
    return portals


def pingPortal(portal, param):
    # param = '-c'  # Parameter needs to be -n for Windows os or -c for others
    hostname = portal['HOSTNAME']
    print(f"\n{divider}\nPortal: {portal['SYSTEM']} | {portal['PORTAL']}")
    response = os.system(f'ping {param} 1 {hostname}')
    
    if response == 0:
        print(f"\nPortal {portal['SYSTEM']} | {portal['PORTAL']} is up!")
    else:
        print(f"\nPortal {portal['SYSTEM']} | {portal['PORTAL']} seems to be down. Please check!")


if __name__ == '__main__':
    drExercise()
