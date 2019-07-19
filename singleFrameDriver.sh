#/bin/bash

## singleFrameDriver.sh - driver to run singleFrameDriver (typically
## from within a Parsl workflow but, with care, can also be used
## stand-alone)

## NOTE: a proper DM environment AND repository must first be
## established prior to running this script


pid=$$
if [ ! -z "${SLURMD_NODENAME}" ]
then
    echo `date`"  $pid Entering singleFrameDriver.sh, running on "${SLURMD_NODENAME}
else
    echo `date`"  $pid Entering singleFrameDriver.sh, running on "${HOST}
fi


## command line args
visit=$1          # visit number to process
dir=$2            # name for /rerun subdirectory
nPar=$3           # number of parallel processes ('-j' option)
nCores=$4         # number of cores to use ('--ncores' options)

echo "$pid $0"

echo;echo;echo
echo "All environment variables:"
printenv |sort
echo "==========================="
echo "module list"
module list 2>&1
echo "==========================="
echo;echo;echo

## The following might be necessary to prevent DM repo initialization contention
# delay=$(($RANDOM % 300))  ## 0-299 seconds
# echo "INITIAL RANDOM DELAY OF $delay SEC"
# sleep $delay
# echo `date`"  << Wake up! >>"

PWDSAVE=$PWD

######################################
# Run singleFrameDriver

## Timing prefix
Tprefix="/usr/bin/time -v "

## Set Initialization and Parallelization parameters
# clobberParm=""
# if [ "$startDet" = "-1" ]; then
#     BFoptions=""
#     IDparm=""
#     clobberParm=" --clobber-config --clobber-version "
#     echo "Initialization run for seeding the config"
# elif [ "$startDet" = "$endDet" ]; then
#     BFoptions=""
#     IDparm=" --id detector=${startDet} "
#     echo "Single sensor [${startDet}], no parallelization"
# else
#     BFoptions=" -j "${nPar}    ## parallelization
#     IDparm=" --id detector=${startDet}..${endDet} "
#     echo "Multiple sensors [${startDet}..${endDet}], parallelization set to ${nPar}"
# fi


# ## Note that $CP_PIPE_DIR comes from the DM stack setup
# BFprefix=${CP_PIPE_DIR}/bin
echo `date`"  Starting singleFrameDriver"

## This is the DM code to generate the brighter-fatter kernels
## set "doCalcGains=True" to compute bf gains from flats
## set "doCalcGains=False" to use bf gains stored in <repo>/calibrations

set -x

## This is the command to generate the BF kernels
#${Tprefix} python ${BFprefix}/makeBrighterFatterKernel.py "${PT_REPODIR}" --rerun ${dir}  ${IDparm} --visit-pairs ${PT_BF_VISITPAIRS} -c xcorrCheckRejectLevel=2 doCalcGains=True isr.doDark=True isr.doBias=True isr.doCrosstalk=True isr.doDefect=False isr.doLinearize=False forceZeroSum=True correlationModelRadius=3 correlationQuadraticFit=True level=AMP ${clobberParm} ${BFoptions}

## This is the command to invoke the singleFrameDriver

#### TEMPORARY OVERRIDES
visit=500086
dir=test1
nCores=10
singleFrameDriver.py ${PT_REPODIR} --rerun ${dir} --id visit=${visit} --cores ${nCores} --timeout 999999999 --loglevel CameraMapper=warn


rc=$?
set +x
echo "$pid [singleFrameDriver rc = "$rc"]"


echo `date`"  $pid Exiting singleFrameDriver.sh"
 
## Exit with return code
exit $rc
