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

def runCommand(cmdsh):
    cmdArgs = shlex.shlex(cmdsh)
    cmdArgs.whitespace_split = True
    rssh = Popen(cmdArgs, stdout = PIPE, stderr = PIPE)
    cmdOut = rssh.stdout.readlines()
    return cmdOut

def getVfilerRoot(vfiler):
    vfInfoCMD = 'ssh root@' + str(filer) + ' vfiler status -r ' + str(vfiler)
    vfInfo = runCommand(vfInfoCMD)
    for line in vfInfo:
        if '[/etc]' in line:
            # ex: Path: /vol/vol_name [/etc]
            volPath = line.strip().split()[1]
            rootVol = volPath.split("/")[2]
    return rootVol

def getFilerRoot(filer):
    filerInfoCMD = 'ssh root@' + str(filer) + ' vol status'
    filerInfo = runCommand(filerInfoCMD)
    for line in filerInfo:
        if 'root,' in line:
            # ex:   volume_name online          raid4, flex       root, create_ucode=on, 
            rootVol = line.strip().split()[0]
    return rootVol

def shareParse(exports):
    # TODO: analyze the NFS share line
    # ex: /vol/<volume_name>  -sec=<auth type>,rw=<IP1>:<IP2>,[ro=<IP1>:<IP2>,]root=<IP1>:<IP2>
    # save in a dict of dict of sets: key = volume, value = dict => keys = sec,rw,ro,root and values auth type and set(IP)
    # dodos = {'share_name' : {'sec' : sys, 'rw' : set([<IP1>,<IP2>]), ...}}
    for line in exports:
        # ex: /vol/volume_name      -sec=sys,rw=IP1:IP2,root=IP1:IP2,nosuid
        sharePath = line.strip().split()[0]
        exportOptions = line.lstrip("-").split(",")
    return dodos

def cmpShare():
    # TODO: compare 2 NFS shares
    # the data is structured in dodos, IPs are added in sets
    # compare 1st level keys to check if NFS shares are in the conf file
    # compare values for sec key
    # compare IPs, since they are sets then just diff   
    pass

def main():
    args = setupParser()
    filer = args.filerName
    vfiler = args.vfilerName
    volume = args.volumeName
    if vfiler:
        exportfsCMD = 'ssh root@' + str(filer) + ' vfiler run ' + str(vfiler) + ' exportfs'
        vfRootVol = getVfilerRoot(vfiler)
        exportsCMD = 'ssh root@' + str(filer) + ' rdfile /vol/' + str(vfRootVol) + '/etc/exports'
    else:
        exportfsCMD = 'ssh root@' + str(filer) + ' exportfs'
        rootVol = getFilerRoot(filer)
        exportsCMD = 'ssh root@' + str(filer) + ' rdfile /vol/' + str(rootVol) + '/etc/exports'
    #TODO: parse, compare, return result

if __name__ == "__main__":
    main()
