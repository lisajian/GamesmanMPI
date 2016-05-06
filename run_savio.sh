#!/bin/bash
# Job name:
#SBATCH --job-name=tootnottolru
#
# Partition:
#SBATCH --partition=savio
# 
# QoS (put into debug mode:
#SBATCH --qos=savio_debug
#
# Processors:
#SBATCH --nodes=4
#
# Mail user:
#SBATCH --mail-user=csumnicht@berkeley.edu

## Command(s) to run:
module load openmpi
module load python/3.2.3
module load mpi4py
module load pip
module load virtualenv/1.7.2

#Start virtual env
virtualenv venv
source venv/bin/activate

ICC=/global/software/sl-6.x86_64/modules/langs/intel/2013_sp1.4.211/bin/intel64/icc
STATS_DIR=/global/scratch/kzentner/tootnottolru
GAME=test_games/toot_and_otto_bitstring.py

# env CC=$ICC pip-3.2 install bitarray
pip-3.2 install bitstring
pip-3.2 install cachetools

mpiexec python3 solver_launcher.py -sd $STATS_DIR $GAME
