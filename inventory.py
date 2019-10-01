#!/usr/bin/env python

# inventory.py - Analyze a DM repo directory tree containing 'raw' (simulated) images
#   NOTE: this script is very sensitive to details of directory structure and file naming!

import os,sys
import argparse
#import datetime
#import subprocess,shlex
#from operator import itemgetter
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

## Command line parsing...  (NOTE: all cmd line args are **IGNORED** now...)
parser = argparse.ArgumentParser(description='Search repo for raw image files and create inventory')

## Positional argument
#parser.add_argument('command', help='pilotMon command', default='summary', choices=commandList)

## Optional arguments
parser.add_argument('-d','--directory',dest='dir',help="Directory to search")
#parser.add_argument('-u','--userid',default='descpho',help="Specify userid running Pilot (default: %(default)s)")
#parser.add_argument('-p','--prefix',default='phoSim',help="Specify pilot jobname prefix (default: %(default)s)")

## Unpack arguments
args = parser.parse_args()



## Locate directory containing visit/image files
##  **NOTE** the 'rootdir' must point the a 'raw' repo directory containing visit dirs.
rootdir='/global/cscratch1/sd/descdm/tomTest/sfd-1/raw/'
rootdir=os.path.dirname(rootdir)
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
numSensorList = []
numRaftList = []

for visit in vDict:
    nVisits += 1
    nSenPerVis = 0
    numRaftList.append(len(vDict[visit]))
    for raft in vDict[visit]:
        nSens = len(vDict[visit][raft])
        nSensors += nSens
        nSenPerVis += nSens
        pass
    numSensorList.append(nSenPerVis)
    pass



## Produce report
print('Image directory summary:')
print('nVisits = ',nVisits,', nSensors = ',nSensors)
print('Average sensors/visit = ',float(nSensors)/nVisits)
    
print('numSensorList = ',numSensorList)
print('numRaftList = ',numRaftList)
      

## Histogram #rafts and #sensors
n,bins,patches = plt.hist(numSensorList,189)
print('n = ',n)
print('bins = ',bins)
print('patches = ',patches)
plt.show()
n,bins,patches = plt.hist(numRaftList,21)
plt.show()



