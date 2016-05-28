from mpi4py import MPI
import logging
import imp
import argparse

import src.utils

parser = argparse.ArgumentParser()
parser.add_argument(
    "game_file",
    help="game to solve for"
)

parser.add_argument(
    "--debug",
    help="Enables or disables logging",
    action="store_true"
)

parser.add_argument(
    "-sd",
    "--statsdir",
    help="location to store statistics about game",
    action="store"
)

args = parser.parse_args()

comm = MPI.COMM_WORLD

# Load file and give it to each process.
game_module = imp.load_source('game_module', args.game_file)
src.utils.game_module = game_module

# Make sure every process has a copy of this.
comm.Barrier()

# Now it is safe to import the classes we need as everything
# has now been initialized correctly.
from src.game_state import GameState  # NOQA
from src.job import Job  # NOQA
from src.process import Process  # NOQA


def validate(mod):
    try:
        getattr(mod, 'initial_position')
        getattr(mod, 'do_move')
        getattr(mod, 'gen_moves')
        getattr(mod, 'primitive')
    except AttributeError as e:
        print("Could not find method"), e.args[0]
        raise

# Make sure the game is properly defined
validate(src.utils.game_module)

# Set up our logging system
lvl = logging.CRITICAL
if args.debug:
    lvl = logging.DEBUG

logging.basicConfig(
    filename='logs/solver_log' + str(comm.Get_rank()) + '.log',
    filemode='w',
    level=lvl
)

initial_position = src.utils.game_module.initial_position()

process = Process(
    comm.Get_rank(),
    comm.Get_size(),
    comm,
    stats_dir=args.statsdir
)

if process.rank == process.root:
    initial_gamestate = GameState(GameState.INITIAL_POS)
    initial_job = Job(
        Job.LOOK_UP,
        initial_gamestate,
        process.rank,
        Job.INITIAL_JOB_ID
    )
    process.add_job(initial_job)

process.run()
