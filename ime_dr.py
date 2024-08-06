''' Python script to check FTP connections are up for all active portals in ImE, for DR exercise '''
''' Written by Juan Boccia - 06/08/2024 '''

import sys, os, datetime

from csv import DictReader
from time import sleep
from ftplib import FTP


SOURCEFILE = 'portals_full_info.csv'
FIELDS = ['SYSTEM', 'PORTAL', 'HOSTNAME', 'USERNAME', 'PASSWORD', 'DIRECTORY'] # Only these fields are to be brought over
DIVIDER = "*-" * 20


def drExercise():
    ''' Main function for DR exercise. Checks for csv file, loads into memory and pings/ftp checks portals. 
    Submit 1 argument ('win' for a windows machine or 'dr' otherwise) for DR exercise
    or 5 arguments ('win'/'dr, hostname, user, password, directory) for test scenario. '''

    timeStamp = datetime.datetime.now()
    outputFile = f'DR_exercise_{timeStamp.strftime('%Y-%m-%d %H%M%S')}.txt'
    open(outputFile, 'w').close()
    stdout = sys.stdout
    print(f"\nDR exercise started on {timeStamp.strftime('%Y-%m-%d @ %X')}")

    if len(sys.argv) == 6:
        print("\nThis is a test scenario with the following parameters:")
        print(sys.argv[1:])

        if sys.argv[1].lower() == 'win': # Parameter needs to be -n for Windows os or -c for others
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

        with open(outputFile, 'a') as sys.stdout:
            # Test ping and ftp with test portal passed as argument
            pingPortal(portal, param)
            ftpPortal(portal)
            timeStamp = datetime.datetime.now().strftime('%Y-%m-%d @ %X')
            print(f"\n{DIVIDER}\nDR Exercise finished on {timeStamp}\n")
        sys.stdout = stdout

    elif len(sys.argv) == 2:
        # Check for csv file in directory
        if sys.argv[1].lower() == 'win':
            param = '-n'
        else:
            param = '-c'
        if not os.path.isfile(SOURCEFILE):
            print('Source CSV file not found. Please save file "portals_full_info.csv" in this directory and retry.')
        else:
            print('Source CSV file found, loading...')
            sleep(0.5)
            portals = loadCsv(SOURCEFILE) # Load portals from csv file
            print(f"\nPortals loaded: {len(portals)}")            
            with open(outputFile, 'a') as sys.stdout:
                print(f"\nDR exercise started on {timeStamp.strftime('%Y-%m-%d @ %X')}")
                print(f"\nPortals loaded: {len(portals)}")
                
                for i, portal in enumerate(portals): # One by one, ping and try FTP connection with the portals
                    print(f"\n{DIVIDER}\nPortal {i+1} of {len(portals)}")
                    print(f"\nPortal: {portal['SYSTEM']} | {portal['PORTAL']}")                
                    pingPortal(portal, param, i, tot=len(portals))
                    ftpPortal(portal)
                timeStamp = datetime.datetime.now().strftime('%Y-%m-%d @ %X')
                print(f"\n{DIVIDER}\nDR Exercise finished on {timeStamp}\n")
            sys.stdout = stdout
    else:
        print("Please submit 1 argument ('win' for a windows machine or 'dr' otherwise) for DR exercise or 5 arguments ('win'/'dr, hostname, user, password, directory) for test scenario.")
    
    timeStamp = datetime.datetime.now().strftime('%Y-%m-%d @ %X')
    print(f"\n{DIVIDER}\nDR Exercise finished on {timeStamp}\n")


def loadCsv(SOURCEFILE):
    ''' Function that loads portal details from portals_full_info.csv file. '''
    portals = []
    with open(SOURCEFILE, newline='') as csvfile:
        reader = DictReader(csvfile, delimiter=';')
        counter = 0
        for row in reader:
            if row['STATUS'] == 'A' and row['ROUTE STATUS'] =='Enabled' and row['HOSTNAME']: # Check for active portals with a hostname.
                counter += 1
                portal = {}
                for field in FIELDS:
                    portal[field] = row[field]
                portals.append(portal)
                print("\rPortals imported: {}". format(counter), end='')
                sleep(.025)
    return portals


def pingPortal(portal, param, i=None, tot=None):
    if i:
        os.system(f'echo: ')
        os.system(f'echo Portal {i+1} of {tot} ({i/tot:.1%})')

    hostname = portal['HOSTNAME']
    response = os.system(f'ping {param} 1 {hostname}')
    
    if response == 0:
        print(f"\nPortal {portal['SYSTEM']} | {portal['PORTAL']} is up!")
    else:
        print(f"\nPortal {portal['SYSTEM']} | {portal['PORTAL']} seems to be down. Please check!")

def ftpPortal(portal):
    try:
        with FTP(portal['HOSTNAME'], portal['USERNAME'], portal['PASSWORD']) as ftp: 
            print(ftp.getwelcome())           
    except Exception as e:
        print(f"\nIssue encountered, please see error:\n{e}")
        print('ftp connection failed')
    else:
        print('\nftp connection and login successful!')
        # Implement cd into target directory
        pass


if __name__ == '__main__':
    drExercise()
