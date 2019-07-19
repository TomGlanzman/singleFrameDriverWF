#!/bin/bash
## buildFileList.sh - create a list of FITS files to be processed with singleFrameDriver
##    This is Y3-WFD (347 visits)
##    Needs python3

## (From Heather, 7/19/2019)

/global/common/software/lsst/cori-haswell-gcc/DC2/parsl/run2.1i/ImageProcessingPipelines/workflows/srs/pipe_scripts/createIngestFileList.py /global/projecta/projectdirs/lsst/production/DC2_ImSim/Run2.1i/sim/y3-wfd/00497969to00560434 --ext .fits --recursive --filename ingestFileTest.txt
