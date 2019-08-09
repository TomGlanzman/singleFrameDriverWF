## cvmfsSetup.sh - from Heather Kelly (7/19/2019) to set up DMstack
## envrionment within which to run the singleFrameDriver.
## Work in progress!

SECONDS=0   # start the clock
STARTTIME=$(date +%s)
export STACKCVMFS=/cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib
#export LSST_STACK_VERSION=w_2019_20
export LSST_STACK_VERSION=w_2019_19-dev   # post Cori-upgade 7/30/2019

export LOCALDIR=/global/common/software/lsst/cori-haswell-gcc/DC2/parsl/run2.1i

module unload python
#module unload python3

module swap PrgEnv-intel PrgEnv-gnu
# module load pe_archive
# module swap gcc gcc/6.3.0
module swap gcc gcc/7.3.0

module rm craype-network-aries
module rm cray-libsci
module unload craype
export CC=gcc

date;echo "source $STACKCVMFS/$LSST_STACK_VERSION/loadLSST.bash"
source $STACKCVMFS/$LSST_STACK_VERSION/loadLSST.bash

date;echo "setup lsst_distrib"
setup lsst_distrib

date;echo "setup -r $LOCALDIR/obs_lsst -j"
#setup -r $LOCALDIR/obs_lsst -j
setup -r $LOCALDIR/obs_lsst-gcc73/obs_lsst -j
echo "Done!";date
echo "Elapsed time (s) = $SECONDS"
sleep 5
ENDTIME=$(date +%s)
echo "Elapsed time (s) = $(($ENDTIME - $STARTTIME))"
export OMP_NUM_THREADS=1


