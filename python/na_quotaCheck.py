#!/usr/bin/python
import argparse
from subprocess import Popen, PIPE
import shlex

def setupParser():
    parser = argparse.ArgumentParser(prog = 'na_quotaCheck.py',
                                     description = 'This script checks if the volume filesystem size can accomodate the specified quota.')
    parser.add_argument('-f', '--filer', action = "store", type = str, dest = "filerName", required = True)
    parser.add_argument('-vf', '--vfiler', action = "store", type = str, dest = "vfilerName", required = False)
    parser.add_argument('-vol', '--volume', action = "store", type = str, dest = "volumeName", required = True)
    args = parser.parse_args()
    return args

#nice convertion function found on stackoverflow
def GetHumanReadable(size, precision = 2):
    suffixes = ['KB', 'MB', 'GB', 'TB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f%s"%(precision,size,suffixes[suffixIndex])

def runCommand(cmdsh):
    cmdArgs = shlex.shlex(cmdsh)
    cmdArgs.whitespace_split = True
    rssh = Popen(cmdArgs, stdout = PIPE, stderr = PIPE)
    cmdOut = rssh.stdout.readlines()
    return cmdOut

def main():
    quotaSize = 0
    volSize = 0
    args = setupParser()
    filer = args.filerName
    vfiler = args.vfilerName
    volume = args.volumeName
    if vfiler:
        quotaCmd = 'ssh root@' + str(filer) + ' vfiler run ' + str(vfiler) + ' quota report'
    else:
        quotaCmd = 'ssh root@' + str(filer) + ' quota report'
    volSpaceCmd = 'ssh root@' + str(filer) + ' df'
    volInfo = runCommand(volSpaceCmd)
    for line in volInfo:
        if volume in line and "snapshot" not in line:
            #read the size of the volume
            volSize = int(line.split()[1])
    quotaInfo = runCommand(quotaCmd)
    for line in quotaInfo:
        if volume in line:
            #sum up the quota size for the volume
            quotaSize += int(line.split()[5])
    print "Checking quota on volume", volume
    if volSize < quotaSize:
        print "WARNING: the total quota size is greater than the volume!"
        print "         increase the volume to accomodate for the set quota size."
    print "\tVolume size:", GetHumanReadable(volSize)
    print "\tQuota size:", GetHumanReadable(quotaSize)

if __name__ == "__main__":
    main()
