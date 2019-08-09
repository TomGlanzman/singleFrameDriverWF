## configTask.sh 
##
## This file must be source'd by both the One-time Setup and
## Production Running steps
##
## Define environment variables to drive the generation of one set of
## brighter-fatter kernels on Cori at NERSC using SLURM and Parsl.
##
## Most variables defined herein will be prefixed with "PT_"
## ("ParslTask" or "PipelineTask", take your pick)
##

## This script *must* be sourced to have any value!
if [[ x$BASH_SOURCE =~ x$0 ]]; then
    echo "You must source this script: $BASH_SOURCE"
    exit
fi

## Needed only until the most recent version of parsl is made part of the DM conda installation
export PATH="'${PATH}:${HOME}'"/.local/bin


#####################################################
###########  Global variables
#####################################################

##     PT_WORKFLOWROOT is where the workflow scripts live (must be same dir as this config script)
export PT_WORKFLOWROOT="$(realpath $(dirname $BASH_SOURCE))"

export PT_SCRATCH='/global/cscratch1/sd/descdm'

##     PT_OUTPUTDIR is the general area where the output goes, e.g., $SCRATCH or projecta
export PT_OUTPUTDIR=$PT_SCRATCH

##      PT_DEBUG is a global flag for workflow development & debugging
export PT_DEBUG=False


#####################################################
###########  One-time Setup
#####################################################

### The following values are required to establish a working DM-style
### repository

##     PT_CALIBS points to a "CALIB" tar ball to populate the repository (is this needed??)
export PT_CALIBS='/global/projecta/projectdirs/lsst/production/DC2_ImSim/Run1.2i/CALIB/CALIB_Run1.2i.tar.gz'

##     PT_REPODIR is the location of output repository
export PT_REPODIR=${PT_OUTPUTDIR}'/tomTest/sfd-1'   # singleFrameDriver test repo(s)


###################################################
###########  Production running
###################################################

## makeBrighterFatterKernel parameters

##     PT_RERUNDIR is the subdirectory under <repo>/rerun into which results are stored
##                 Note that this value may be adjusted later with a numeric postfix.
export PT_RERUNDIR='20190730'

export PT_VISITLIST="$PT_WORKFLOWROOT/visitList.txt"

export PT_PARALLEL_MAX=25  # "-j" DM parallelization parameter [NOT CURRENTLY USED]

export PT_NCORES=25      # number of cores one invocation may use

#----------------------------------------------------------------

## The following is used in association with the Parsl "Config" object

##     PT_ENVSETUP is a script run by the batch script prior to the main event
export PT_ENVSETUP="source ${PT_WORKFLOWROOT}/configTask.sh;export PATH="'${PATH}:${HOME}'"/.local/bin;source ${PT_WORKFLOWROOT}/cvmfsSetup.sh;"


## Dump all the "PT_" environent variables to screen
printenv |sort |grep "^PT_"

echo;echo;echo
echo "==========================================================================="
#echo "  ALL ENVIRONMENT VARIABLES "
## Dump all env-vars for debugging 
#printenv|sort
echo "==========================================================================="
echo;echo;echo
