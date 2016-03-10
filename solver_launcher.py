from mpi4py import MPI
import inspect
import logging
import imp
import argparse
import src.utils

parser = argparse.ArgumentParser()
parser.add_argument("game_file", help="game to solve for")
parser.add_argument("-np", "--numpy", help="optimize for numpy array usage",
                               action="store_true")

args = parser.parse_args()

comm = MPI.COMM_WORLD

# Load file and give it to each process.
game_module = imp.load_source('game_module', args.game_file)
src.utils.game_module = game_module

# Make sure every process has a copy of this.
comm.Barrier()

# Now it is safe to import the classes we need as everything
# has now been initialized correctly.
from src.game_state import GameState
from src.job import Job
from src.process import Process

# Make sure the game is properly defined
assert(hasattr(src.utils.game_module, 'initial_position'))
assert(hasattr(src.utils.game_module, 'do_move'))
assert(hasattr(src.utils.game_module, 'gen_moves'))
assert(hasattr(src.utils.game_module, 'primitive'))
assert(inspect.isfunction(src.utils.game_module.initial_position))
assert(inspect.isfunction(src.utils.game_module.do_move))
assert(inspect.isfunction(src.utils.game_module.gen_moves))
assert(inspect.isfunction(src.utils.game_module.primitive))
if args.numpy:
    assert(hasattr(src.utils.game_module, 'board_state_element_type'))


# Set up our logging system
logging.basicConfig(filename='logs/solver_log' + str(comm.Get_rank()) + '.log', filemode='w', level=logging.DEBUG)

initial_position = src.utils.game_module.initial_position()

process = Process(comm.Get_rank(), comm.Get_size(), comm, NP=args.numpy)
if process.rank == process.root:
    initial_gamestate = GameState(GameState.INITIAL_POS)
    initial_job = Job(Job.LOOK_UP, initial_gamestate, process.rank, 0) # Defaults at zero, TODO: Fix abstraction violation.
    process.add_job(initial_job)
process.run()
