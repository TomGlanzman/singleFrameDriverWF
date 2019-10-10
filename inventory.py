#!/usr/bin/env python

# inventory.py - Analyze a DM repo directory tree containing 'raw' (simulated) images
#   NOTE: this script is very sensitive to details of directory structure and file naming!

## User configs
defRawDir='/global/cscratch1/sd/descdm/tomTest/sfd-2/raw'

## 
import os,sys
import argparse
#import datetime
#import subprocess,shlex
#from operator import itemgetter
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import tabulate

## Command line parsing...  (NOTE: all cmd line args are **IGNORED** now...)
parser = argparse.ArgumentParser(description='Search repo for raw image files and create inventory')

## Positional argument
#parser.add_argument('command', help='pilotMon command', default='summary', choices=commandList)

## Optional arguments
parser.add_argument('-d','--directory',dest='dir',default=defRawDir,help="Directory to search (default=%(default)s)")
parser.add_argument('-p','--enablePlots',action='store_true',default=False,help="Enable histograms (default=%(default)s)")
parser.add_argument('-l','--lineLimit',dest='lineLimit',type=int,default=20,help="Limit lines in visit report (default=%(default)s)")
parser.add_argument('-v','--visitListFile',default=None,help="Name of visit list file to produce (default=%(default)s)")


## Unpack arguments
args = parser.parse_args()

debug = False

## Locate directory containing visit/image files
##  **NOTE** the 'rootdir' must point the a 'raw' repo directory containing visit dirs.
rootdir = args.dir
if rootdir[-1] == '/':rootdir = rootdir[0:-1]  # remove trailing '/', if present
print('Analyzing image directory: ',rootdir)
startDepth=rootdir.count(os.sep)
vDict = {}


## Walk directory tree, find data filesSearch for desired (FITS) files, parse file name, update statistics
## Dir name template:  .../raw/<visitID>/<Raft>/<File name>.fits
## File name template: <visitID>-<Raft>-<Sensor>-det<detector#>-<image#>.fits
## File name example: 00510445-R01-S22-det008-000.fits
##
## Fill data structure vDict{visitID:{raftID:[sensorIDs,...]}}
for root, dirs, files in os.walk(rootdir):
    depth = root.count(os.sep)-startDepth
    if depth != 2: continue   ## select only files in <visitID>/<raft> dirs
    visitID = os.path.split(root)[-2]
    visitID = root.split("/")[-2]
    raftID = os.path.split(root)[-1]
#    print('visitID = ',visitID,' raftID  = ',raftID)

    if visitID not in vDict:
        vDict[visitID]={}
        #print('vDict = ',vDict)
        pass
    if raftID not in vDict[visitID]:
        vDict[visitID][raftID]=[]
        #print('vDict = ',vDict)
        pass
    for file in files:
        pieces = file.split('-')
        if pieces[-1].split(".")[-1] != 'fits':
            print('NON FITS FILE! ',file)
            continue
        xVisit = str(int(pieces[0]))
        xRaft  = pieces[1]
        if xVisit != visitID or xRaft != raftID:  # Sanity check!
            print('Expected visitID ',visitID,', but got ',xVisit)
            print('Expected raftID  ',raftID, ', but got ',xRaft)
            raise Exception("Inconsistent visitID or raftID")
        sensorID = pieces[2]
        vDict[visitID][raftID].append(sensorID)
    pass

print('Raw image directory tree analyzed.')


##
## Summarize the visit dictionary
nVisits=0
nSensors=0
vList = list(vDict.keys())
vList.sort()
numSensorList = []
numRaftList = []
rows = []

for visit in vList:
    nVisits += 1
    nSenPerVis = 0
    numRaftList.append(len(vDict[visit]))
    for raft in vDict[visit]:
        nSens = len(vDict[visit][raft])
        nSensors += nSens
        nSenPerVis += nSens
        pass
    numSensorList.append(nSenPerVis)
    rows.append([nVisits,visit,len(vDict[visit]),nSenPerVis])
    pass


## Produce report
print('Image directory summary:')
print('nVisits = ',nVisits,', nSensors = ',nSensors)
print('Average sensors/visit = ',float(nSensors)/nVisits)

if debug:
    print('numSensorList = ',numSensorList)
    print('numRaftList = ',numRaftList)


## Pretty print out first "lineLimit" of: [visitID, #rafts, #sensors]
colnames = ['#','visitID','#rafts','#sensors']
tabFormat = "psql"
print(tabulate.tabulate(rows[0:args.lineLimit],headers=colnames,tablefmt=tabFormat))

## Produce a visit list file, if requested
##   A text file with "visitID #rafts #sensors" per line
if args.visitListFile != None:
    print('Create visit list file!')
    fd=open(args.visitListFile,'w')
    for row in rows:
        line = str(row[1])+' '+str(row[2])+' '+str(row[3])+'\n'
        fd.write(line)
        pass
    fd.close()
    pass
    

## Histogram #rafts and #sensors
if args.enablePlots:
    n,bins,patches = plt.hist(numSensorList,189)
    if debug:
        print('n = ',n)
        print('bins = ',bins)
        print('patches = ',patches)
        pass
    plt.show()
    n,bins,patches = plt.hist(numRaftList,21)
    plt.show()
    pass



