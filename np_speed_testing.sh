#!/bin/bash
# This script takes four command line arguments: regular (non-NumPy) gamefile,
# NumPy gamefile, number of processes, and number of times to run. Dumps to
# tests/time_results_np.txt and tests/solve_results_np.txt
echo Beginning testing for $1 and $2, $3 processes, $4 tests > tests/solve_results_np.txt
echo Beginning testing for $1 and $2, $3 processes, $4 tests > tests/time_results_np.txt
echo -ne "0%\r"
TOTAL=$4
for testnum in `seq 0 $4`
  do
    echo -ne "\n" >> tests/time_results_np.txt
    echo -ne "\n" >> tests/solve_results_np.txt
    echo Test $i with NumPy>> tests/time_results_np.txt
    echo Test $i with NumPy>> tests/solve_results_np.txt
    echo --------- >> tests/time_results_np.txt
    echo --------- >> tests/solve_results_np.txt
    (time mpiexec -n $3 python solver_launcher.py $2 -np) >> tests/solve_results_np.txt 2>> tests/time_results_np.txt
    echo -ne "\n" >> tests/time_results_np.txt
    echo -ne "\n" >> tests/solve_results_np.txt
    echo Test $i with Pickling>> tests/time_results_np.txt
    echo Test $i with Pickling>> tests/solve_results_np.txt
    echo --------- >> tests/time_results_np.txt
    echo --------- >> tests/solve_results_np.txt
    (time mpiexec -n $3 python solver_launcher.py $1) >> tests/solve_results_np.txt 2>> tests/time_results_np.txt
    step=$((testnum * 100))
    percent=$((step / TOTAL))
    echo -ne "$percent%\r"

  done
