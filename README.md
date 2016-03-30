# GamesmanMPI
### MPI-Based Solver for Two Player Abstract Strategy Games

(More project description here)

## Loading a Game
Games to be solved are loaded via the command line, with the following syntax:
```
mpiexec -n <number of processes> python solver_launcher.py <your game file>
```
For example, you could load our example game, Four-To-One, by running
```
mpiexec -n 5 python solver_launcher.py test_games/four_to_one.py
```
Your game file must follow the conventions outlined in the API

### <a name="optimize-desc"></a>(Optional) Optimization with NumPy
Communication between processes can be greatly sped up if board state are stored as certain datatypes. Specifically, if your Gamestate object is a NumPy array in which the elements are of an [MPI Elementary data type](https://computing.llnl.gov/tutorials/mpi/#Routine_Arguments "MPI Primitives"), you can use the `-np` or `--numpy` flag to run an optimized version of the solver. Note that you must add an additional method to your game file to specify the specific data type you are using. See [API Description](#optimize-api)

## Testing
Also included is a very simple testing script, `testing.sh`, which allows you to time the game solver within a certain range of process counts, and also compare that to local solver performance. Use the following syntax:
```
bash testing.sh <your game file> <min # of processes> <max # of processes> <# of runs per process> <-l> <-np>
```
Where the `-l` tag includes testing with the local solver, and the `-np` flag runs the process with NumPy optimizations. Flags can occur in any order. To test Four-To-One with process counts ranging from 4 to 12, running each option 3 times, including the local solver, with the NumPy optimization, we would run
```
bash testing.sh test_games/four_to_one.py 4 12 3 -l -np
```
The results of the test are dumped to two files: `tests/solve_results.txt` and `tests/time_results.txt`

## Description of API
There are four elements which a game class must implement:
- initial_position
2. gen_moves
3. do_moves
4. primitive

The exact way in which you represent a game state or moves (ints, lists, etc.) does not matter, as long as you are consistant. For the puposes of this guide, we'll use an integer to represent our gamestate and moves, since we our example is Four-To-One.

#### initial_position( )
###### Parameters
- returns: *gamestate-type*
  - The initial position for game

###### Example
```python
def initial_position(x):
    return 4
```

#### gen_moves( *gs* )
###### Parameters
- gs: *gamestate-type*
  - The gamestate for which you are generating moves
- returns: *list of move-type*
  - All legal moves from that gamestate

###### Example
```python
def gen_moves(x):
    if x == 1:
        return [-1]
    return [-1, -2]
```

#### do_move( *gs*, *m* )
###### Parameters
- gs: *gamestate-type*
  - The gamestate from which you are making a move
- m: *move-type*
  - The move that you are making
- returns: *gamestate-type*
  - The new gamestate after the move has been made

###### Example
```python
def do_move(x, move):
    return x + move
```
#### primitive( *gs* )
###### Parameters
- gs: *gamestate-type*
  - The gamestate that you are analyzing
- returns: *list of move-type*
  - The primitive type for *gs*, if it is a pimitive (WIN, LOSS, TIE, DRAW)

###### Example
```python
def primitive(x):
    if x <= 0:
        return LOSS
```

#### <a name="optimize-api"></a> board_state_element_type (Optional)
The type associated with the NumPy arrays used to represent a board state. See [optimization](#optimize-desc)

###### Example
```python
board_state_element_type = MPI.INT
```
