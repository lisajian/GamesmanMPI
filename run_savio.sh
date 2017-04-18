#!/bin/bash
# Job name:
#SBATCH --job-name=to_memfix
#
# Partition:
#SBATCH --partition=savio
# 
# QoS (put into debug mode:
#SBATCH --qos=savio_debug
#
# Processors:
# Based off of here: https://www.rosettacommons.org/node/3597
#SBATCH --ntasks=20
#
#SBATCH --time 00:15:00
#
# Requeue:
#SBATCH --requeue

## Command(s) to run:
module load intel
module load openmpi
module load python/3.5.1

GAME=test_games/mttt.py

pip install --user bitstring
pip install --user cachetools
pip install --user queuelib
pip install --user jsonpickle
pip install --user mpi4py==2.0.0

mpiexec -np $SLURM_NTASKS python3 -OO -B solver_launcher.py $GAME
