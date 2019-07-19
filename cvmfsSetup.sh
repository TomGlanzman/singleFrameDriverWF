## cvmfsSetup.sh - from Heather Kelly (7/19/2019) to set up DMstack
## envrionment within which to run the singleFrameDriver.
## Work in progress!

export STACKCVMFS=/cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib
export LSST_STACK_VERSION=w_2019_20

export LOCALDIR=/global/common/software/lsst/cori-haswell-gcc/DC2/parsl/run2.1i

module unload python
module unload python3

module swap PrgEnv-intel PrgEnv-gnu
module load pe_archive
module swap gcc gcc/6.3.0
module rm craype-network-aries
module rm cray-libsci
module unload craype
export CC=gcc

source $STACKCVMFS/$LSST_STACK_VERSION/loadLSST.bash
setup lsst_distrib
setup -r $LOCALDIR/obs_lsst -j

export OMP_NUM_THREADS=1


