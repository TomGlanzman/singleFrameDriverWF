#!/bin/bash

## runSingleFrameDriver.sh - run one instance of singleFrameDriver


## This script is intended to be run interactively, just once and
## ideally from the workflow main directory.

## Define workflow root directory
workflowroot=$(dirname $(realpath $0))

## Define task-specific env-vars
source $workflowroot/configTask.sh

## DM setup
source $workflowroot/cvmfsSetup.sh

## Establish a repository for brighter-fatter generation (visit rerundir #procs #cores)
test=T`date +%Y%m%d.%H.%M.%S`
#visit="500131"    #sfd-1
visit="390560"    #sfd-2
$workflowroot/singleFrameDriver.sh $visit $test 5 5 |& tee $workflowroot/singleFrameDriver-${test}.log 

