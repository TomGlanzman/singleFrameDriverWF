## workflow.py - top-level Parsl workflow script to run singleFrameDriver

## T.Glanzman - July 2019

## Note: One must first have the proper python and DM environment to
## run this script.

##
## Initialization
##

import os,sys,datetime
import traceback

def checkConsecutive(l):
    # Check if list (of sensors) is consecutive (for parallelization)
    return sorted(l) == list(range(min(l), max(l)+1))


startTime = datetime.datetime.now()

## Say hello
print(startTime, ": Entering workflow.py")
print("Running python from: ",sys.prefix)
print("Python version: ",sys.version)



#import logging

## Quantities used by all steps in this workflow
workflowRoot = os.environ['PT_WORKFLOWROOT']

## Load Parsl
import parsl
from parsl.app.app    import  python_app, bash_app
print("parsl version = ",parsl.__version__)

## Configure Parsl **USER-SUPPLIED configuration!**
import pConfig

print(datetime.datetime.now(), ": Parsl configuration setup complete")
print("config = ",pConfig.config)

parsl.load(pConfig.config)
print(datetime.datetime.now(), ": Parsl config complete!")



#########################################################
#########################################################



##
## Define Generic Parsl-decorated workflow (bash) app
##    (one instance of calling this app generates one user 'task')
##

@bash_app(executors=['knlMj'],cache=True)
def pCmd(cmd, stdout=parsl.AUTO_LOGNAME, stderr=parsl.AUTO_LOGNAME, label=None):
    ## Generalized command processing for a given Parsl executor (defined in 'config')
    import os,sys,datetime
    print(datetime.datetime.now(),' Entering pCmd:\n',cmd)
    return f'{cmd}'



#########################################################
#########################################################

##
## Submit and Run the workflow steps
##

print(datetime.datetime.now(), ": Submit workflow steps")

## First bits
tasksk = []         ## List of Parsl KNL tasks
tasksh = []         ## List of Parsl Haswell tasks
ntasks = 0          ## Total number of tasks


## Read in list of visits to process
visitList = [line.rstrip('\n') for line in open(os.environ['PT_VISITLIST'])]
print('visitList contains ',len(visitList),' visits.')


## Loop over all visits  (visit rerundir nParallel nCores)
for visit in visitList:
    ntasks += 1
    cmd = workflowRoot+"/singleFrameDriver.sh "+str(visit)+" "+os.environ['PT_RERUNDIR']+" "+os.environ['PT_PARALLEL_MAX']+" "+os.environ['PT_NCORES']
    print('cmd = ',cmd)
    stdo = os.path.join(workflowRoot,'SFD'+str(ntasks)+'.log')
    stde = os.path.join(workflowRoot,'SFDerr'+str(ntasks)+'.log')

    ## Submit Parsl request for one visit
    print("Creating parsl task ",ntasks)
    tasksk.append(pCmd(cmd,label='singleFrameDrvr'))     # add new Parsl task to list
    pass

print(" Total number of parsl tasks created = ",ntasks)

#########################################################
#########################################################

## Uncomment the assert if running with "python -i"
#assert False,"Entering python interpreter"


## Wait for jobs to complete

print("Begin waiting for defined tasks to complete...")
try:
    parsl.wait_for_current_tasks()
except:         # Unhandled exception will cause script to abort
    print("Exception!  parsl.wait_for_current_tasks()   Bah!")
pass


print("Check return code for each task")
### Can the .result() function also cause an exception???
taskn = 0
rc = 0
try:
    for task in tasksh:
        print("waiting for Haswell job ",taskn)
        print("rc = ",task.result())
        taskn += 1
        pass
    for task in tasksk:
        print("waiting for KNL job ",taskn)
        print("rc = ",task.result())
        taskn += 1
        pass
except Exception as ex:
    print("Exception waiting for job ",taskn)
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print(message)
    print(traceback.format_exc())
    rc = 1
    pass



## Final bookkeeping
endTime = datetime.datetime.now()
elapsedTime = endTime-startTime
print("Time to complete this job = ",elapsedTime)
print(endTime,": Exiting workflow")

sys.exit(rc)




