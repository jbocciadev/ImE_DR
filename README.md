# ImE_DR
Repository for script that checks all ImE portals FTP

## Instructions:

### Testing:
    1. Run the file as python3 ime_dr.py <win/dr> <hostname> <username> <password> <destination directory>
    2. The ping information will be visible in the commend line, and the FTP connection details will be stored in a new .txt file in the same directory.

### Production:
    1. Check that the current folder contains the script file AND a current version of the portal_report.csv file.
    2. Run the file as python3 ime_dr.py <win/dr>.
    3. The ping information will be visible in the commend line, and the FTP connection details will be stored in a new .txt file in the same directory. A running progress can be seen in the command line.