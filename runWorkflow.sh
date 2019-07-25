#!/bin/bash

## runWorkflow.sh - run the workflow.sh script after setting up environment(s)

## This script is intended to be run interactively, ideally from the
## workflow main directory.

## NOTE: if invoked with a single parameter, "int", then python will
## exit into an interpreter.  This assumes an "assert" is present in
## workflow.py.

## Define root workflow directory
##   Note: this will assume this script resides in the top-level task directory
workflowroot="$(realpath $(dirname $BASH_SOURCE))"
echo 'workflowroot= '$workflowroot

## This is needed if parsl (or some other package) is installed locally
export PATH=$HOME/.local/bin:$PATH

## Define the workflow-specific env-vars
echo "source workflowroot/configTask.sh"
source $workflowroot/configTask.sh

## DM setup
echo "source workflowroot/cvmfsSetup.sh"
source $workflowroot/cvmfsSetup.sh

## Run the workflow
echo "python workflowroot/workflow.py"
if [ "$1" == "int" ]; then
    python -i $workflowroot/workflow.py
else
    python $workflowroot/workflow.py
fi
