## getVisit.py - Extract detailed visit info from DM (sqlite3) registry file


## Python dependencies: sqlite3, tabulate

## T.Glanzman - Autumn 2019
__version__ = "0.1.0"

import sys,os
import sqlite3
#from tabulate import tabulate
import datetime
import argparse


class getVisitInfo(object):

    getVisitSQL='select visit from raw_visit order by visit;'
    getVisInfoSQL="select raftName,detectorName,detector,filter from raw where visit='$1' order by detector;"
    def __init__(self,dbpath='.',dbfile='registry.sqlite3',visitN=1):
        print("Hello from getVisitInfo.init()")
        ## Instance variables
        self.dbpath = dbpath
        self.dbfile = dbfile
        self.visitN = visitN
        print('dbpath = ',self.dbpath)
        print('dbfile = ',self.dbfile)
        print('visitN = ',self.visitN)
        self.dbInit = False
        return

    
    def __del__(self):
        ## Class destructor 
        self.con.close()
        self.dbInit = False
        return
    
    def initDB(self):
        ## Extract detailed data for specified visit
        ## sqlite3 database connection and cursor
        self.con = sqlite3.connect(os.path.join(self.dbpath,self.dbfile))  ## connect to sqlite3 file
        self.con.row_factory = sqlite3.Row           ## optimize output format
        self.cur = self.con.cursor()                 ## create a 'cursor'
        self.dbInit = True
        return

    def stdQuery(self,sql):
        if self.dbInit == False: return
        ## Perform a query, fetch all results and column headers
        result = self.cur.execute(sql)
        rows = result.fetchall()   # <-- This is a list of db rows in the result set
        ## This will generate a list of column headings (titles) for the result set
        titlez = result.description
        ## Convert silly 7-tuple title into a single useful value
        titles = []
        for title in titlez:
            titles.append(title[0])
            pass
        return (rows,titles)


    def getVisitList(self,dump=False):
        if self.dbInit == False: return
        ## Fetch list of visits
        visitList = []
        print('getVisitSQL = ',getVisitInfo.getVisitSQL)
        (rows,titles)=self.stdQuery(getVisitInfo.getVisitSQL)
        for row in rows:
            visitList.append(row[0])
            pass
        visitList.sort()
        if dump:
            for row in rows:
                print(row[0])
                pass
            pass
        return visitList

    
    def getVisitInfo(self,visit):
        ## Fetch info [raft,sensor,detector,filter] for specified visit
        if self.dbInit == False: return
        query = getVisitInfo.getVisInfoSQL.replace('$1',str(visit))
        (rows,titles)=self.stdQuery(query)

        raft,detector,flter=[],[],[]
        raftSensor = {}
        for row in rows:
            raft.append(row[0])
            if row[0] in raftSensor:
                raftSensor[row[0]].append(row[1])
            else:
                raftSensor[row[0]] = [row[1]]
                pass
            detector.append(row[2])
            flter.append(row[3])
        return raft,raftSensor, detector,flter

    
    def run(self):
        self.initDB()

        self.visit = 0

        ## Fetch list of all visits
        self.visitList = self.getVisitList()
        print('# visits returned = ',len(self.visitList))
        print('Looking for ',self.visitN,'th visit')
        if len(self.visitList) < self.visitN:
            raise Exception('Too few visits') # User has asked for
                                              # visit beyond list
                                              # length
        print('visitList[0:10] = ',self.visitList[0:10])

        ## Select desired visit
        self.visit = self.visitList[self.visitN]
        print('Selected visit = ',self.visit)

        ## Fetch detailed visit info
        self.rafts,self.rsList,self.detectorList,self.filterList \
            = self.getVisitInfo(self.visit)
        self.raftList = []
        for raft in self.rafts:
            if raft in self.raftList: continue
            self.raftList.append(raft)
            pass
        return len(self.visitList),self.visit,self.raftList,self.rsList,self.detectorList,self.filterList



raftIDs = ['R01','R02','R03','R10','R11','R12','R13','R14','R20','R21','R22','R23','R24','R30','R31','R32','R33','R34','R41','R42','R43']

def d2rs(detector):
    ## Convert a DM "detector number" to raft/sensor format, e.g.,
    ## "R22" "S11"
    det = int(detector)
    if det > 189 or det < 0: raise Exception("Bad detector number")
    raft = int(det/9)
    raftID = raftIDs[raft]
    s1 = det%9
    s2 = int(s1/3)
    s3 = s1 % 3
    sensorID = f'S{s2}{s3}'
    return raftID, sensorID


def rs2d(raftID,sensorID):
    # Convert a raft sensor string of form "Rnn" and "Smm" to a DM
    # "detector number" (int from 0 to 188)
    raft = raftIDs.index(raftID)
    det = int(raft)*9+int(sensorID[-2])*3+int(sensorID[-1])
    return det



if __name__ == '__main__':

    ## Define defaults
    defaultPath = '/global/cscratch1/sd/descdm/tomTest/sfd-2'
    defaultFile = 'registry.sqlite3'
    
    ## Parse command line arguments
    parser = argparse.ArgumentParser(description='Fetch visit data from DM sqlite registry file')
    parser.add_argument('registryPath',help='Path to registry file (default=%(default)s)',nargs='?',default=defaultPath)
    parser.add_argument('-r','--registryFile',default=defaultFile,help='Name of registry file (default = %(default)s)')
    parser.add_argument('-n','--nth',default=0,type=int,help='Desired visit, counting from beginning of sorted list (default=%(default)s)')
    parser.add_argument('-v','--version', action='version', version=__version__)
    args = parser.parse_args()

    myvisit = getVisitInfo(dbpath=args.registryPath,dbfile=args.registryFile,visitN=args.nth)
    nvisits,visit,raftList,rsList,detectorList,filterList = myvisit.run()
    print("\n===========================\nReturn from getVisitInfo.")
    print('There were ',nvisits,' visits in this repo.')
    print('Selected visitID = ',visit,':\n #rafts = ',len(raftList))
    print('raftList = ',raftList)
    print('\n #sensors = ',len(detectorList))
    for raft in rsList:
        print(raft,': ',rsList[raft])
        pass
    print('\ndetectorList = ',detectorList)
    sys.exit()



