## pConfig.py - Define Parsl configuration for use in a top-level workflow script

##  To use this file, create the desired executor(s), giving each a
##  unique name.  Activate the needed executors at the *end* of this
##  file in the "Config" object.  Note that each activated executor
##  has some associated overhead so it is recommended to activate only
##  those you will use.

## T.Glanzman - May 2019

##
## import Parsl elements
##

import sys,os,logging
import parsl
from parsl.providers  import  SlurmProvider
from parsl.providers  import  LocalProvider
from parsl.channels   import  LocalChannel
from parsl.launchers  import  SingleNodeLauncher
from parsl.launchers  import  SrunLauncher
from parsl.launchers  import  SimpleLauncher
from parsl.executors  import  HighThroughputExecutor
from parsl.executors  import  ThreadPoolExecutor
from parsl.config     import  Config

## Parsl monitoring
from parsl.monitoring.monitoring import MonitoringHub
from parsl.addresses import address_by_hostname


##
##   Configure Parsl
##
hostName = address_by_hostname()


##
##  Define Parsl executors
##

## The following Executors are all based on the "High Throughput
## Executor" (or "HTEX") as recommended by the Parsl team.  They can
## operate on configuration ranging from a single login (or batch)
## node to many batch nodes.  These executors have been tuned for the
## makeBrighterFatterKernel.py DM tool.
#####################


## EXPERIMENTAL executor that runs on a single batch node and bypasses 'srun'

knl1 = HighThroughputExecutor(
    label='knl1',
    address=address_by_hostname(),   # node upon which the top-level parsl script is running
    cores_per_worker=10,             # threads per user task (managed by a 'worker')
    max_workers=3,                   # user tasks/node
    poll_period=5000,                # (ms)
    provider=SlurmProvider(          ## Dispatch tasks via SLURM
        partition='regular',         # SLURM job "queue"
        walltime='04:00:00',         # max time for batch job
        cmd_timeout=300,             # (s) Extend time waited in response to 'sbatch' command
        nodes_per_block=1,           # Nodes per batch job
        init_blocks=0,               # of batch jobs to submit in anticipation of future demand
        min_blocks=1,                # limits on # batch job requests
        max_blocks=1, 
        parallelism=0.1,             # reduce "extra" (excessive) batch jobs
        scheduler_options="#SBATCH -L SCRATCH,projecta \n#SBATCH --constraint=knl",
        worker_init=os.environ['PT_ENVSETUP'],          # Initial ENV setup
        channel=LocalChannel(),      # batch communication is performed on this local machine
        launcher=SimpleLauncher()    # One node only
    ),
)

## This executor is intended for large-scale KNL batch work with
## *multiple* nodes & workers/node and employing significant
## parallelism within the DM code ("-j") or not

knlM = HighThroughputExecutor(
    label='knl',
    address=address_by_hostname(),   # node upon which the top-level parsl script is running
    cores_per_worker=10,             # threads per user task (managed by a 'worker')
    max_workers=3,                   # user tasks/node
    poll_period=5000,                # (ms)
    provider=SlurmProvider(          ## Dispatch tasks via SLURM
        partition='regular',         # SLURM job "queue"
        walltime='04:00:00',         # max time for batch job
        cmd_timeout=300,             # (s) Extend time waited in response to 'sbatch' command
        nodes_per_block=1,           # Nodes per batch job
        init_blocks=0,               # of batch jobs to submit in anticipation of future demand
        min_blocks=1,                # limits on batch job requests
        max_blocks=1, 
        parallelism=0.1,             # reduce "extra" batch jobs
        scheduler_options="#SBATCH -L SCRATCH,projecta \n#SBATCH --constraint=knl",
        worker_init=os.environ['PT_ENVSETUP'],          # Initial ENV setup
        channel=LocalChannel(),      # batch communication is performed on this local machine
        launcher=SrunLauncher()      # SrunLauncher necessary for multi-node batch jobs
    ),
)



## This executor is intended to be used for interactive work on a
## single (haswell) login node

haswellInt = HighThroughputExecutor(
    label='haswellInt',
    address=address_by_hostname(),  # node upon which the top-level parsl script is running
    cores_per_worker=10,
    max_workers=1,                            # user tasks/node (small number to avoid hogging machine)
    poll_period=30,
    provider=LocalProvider(                 # Dispatch tasks on local machine only
        channel=LocalChannel(),
        init_blocks=1,
        max_blocks=1,
        worker_init=os.environ['PT_ENVSETUP'],          # Initial ENV setup
    )
)


## This executor is intended to be used for work on a single
## interactive (haswell or knl) batch node

coriBint = HighThroughputExecutor(
    label='coriBint',
    address=address_by_hostname(),  # node upon which the top-level parsl script is running
    cores_per_worker=1,
    max_workers=5,                            # user tasks/node (up to capacity of machine)
    poll_period=30,
    provider=LocalProvider(                 # Dispatch tasks on local machine only
        channel=LocalChannel(),
        init_blocks=1,
        max_blocks=1,
        worker_init=os.environ['PT_ENVSETUP'],          # Initial ENV setup
    )
)


## This is based on the *default* executor (*DO NOT USE* due to this
## executor is not recommended by Yadu)
coriLogin=ThreadPoolExecutor(
    label='coriLogin',
    managed=True,
    max_threads=2,
    storage_access=[],
    thread_name_prefix='',
    working_dir=None
)


###################################################
###################################################
###################################################

##
## Finally, assemble the full Parsl configuration 
##   [Be sure to specify your needed executor(s)]

config = Config(
    app_cache=True, 
    checkpoint_mode='task_exit', 
    executors=[knl1],
    monitoring=MonitoringHub(
        hub_address=address_by_hostname(),
        hub_port=55055,
        logging_level=logging.INFO,
        resource_monitoring_interval=60,
    ),
    retries=1
)


