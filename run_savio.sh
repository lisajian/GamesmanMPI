#!/bin/bash
# Job name:
#SBATCH --job-name=gamesmanMPI-solve
#
# Partition:
#SBATCH --partition=PARTITION NAME
#
# Processors:
#SBATCH --nodes=24
#SBATCH --exclusive
#
# Num. Processors per Node
#SBATCH --ntasks-per-node=4
#
# Constraint:
#SBATCH --constraint=highmem
#
# Mail type:
#SBATCH --mail-type=all
#
# Mail user:
#SBATCH --mail-user=sbw@berkeley.edu

## Command(s) to run:
module load openmpi
mpirun python solve_launcher.py test_games/toot_and_otto_np.py -np -s
