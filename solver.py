from mpi4py import MPI
import hashlib
import sys
import inspect
from queue import PriorityQueue
import logging
import time
import functools
# from enum import Enum

# Import game definition from file specified in command line
game_module = __import__(sys.argv[1].replace('.py', ''))

# Make sure the game is properly defined
assert(hasattr(game_module, 'initial_position'))
assert(hasattr(game_module, 'do_move'))
assert(hasattr(game_module, 'gen_moves'))
assert(hasattr(game_module, 'primitive'))
assert(inspect.isfunction(game_module.do_move))
assert(inspect.isfunction(game_module.gen_moves))
assert(inspect.isfunction(game_module.primitive))

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Set up our logging system
logging.basicConfig(filename='logs/solver_log' + str(rank) + '.log', filemode='w', level=logging.DEBUG)


WIN, LOSS, TIE, DRAW = "WIN", "LOSS", "TIE", "DRAW"
UNKNOWN_REMOTENESS = -1
PRIMITIVES = (WIN, LOSS, TIE, DRAW)

class GameState:
    """
    Wrapper for the idea of a GameState, not needed
    by the user, just makes things easier for the
    framework.
    """
    def __init__(self, pos):
        self.pos = pos
        self._state = None
        self._remoteness = None

    def get_hash(self):
        """
        Returns the appropriate hash of a given GameState object.
        Based off of the value of it's position.
        """
        return int(hashlib.md5(str(self.pos).encode('utf-8')).hexdigest(), 16) % size

    def expand(self):
        """
        Takes the current position and generates the
        children positions.
        """
        # Raw, in other words, not a GameState object.
        raw_states = map(lambda m: game_module.do_move(self.pos, m), game_module.gen_moves(self.pos))
        # Wrapped, in other words, a GameState object.
        wrapped_states = map(lambda m: GameState(m), raw_states)
        return wrapped_states

    @property
    def remoteness(self):
        """
        Determines returns remoteness if it
        has been found, returns UNKNOWN_REMOTENESS
        otherwise
        """
        if self._remoteness == None:
            return UNKNOWN_REMOTENESS
        else:
            return self._remoteness

    @remoteness.setter
    def remoteness(self, new_remoteness):
        self._remoteness = new_remoteness

    @property
    def state(self):
        """
        Determines whether the state is a:
        WIN, LOSS, TIE, DRAW or UNDECIDED
        """
        if self._state == None:
            return game_module.primitive(self.pos)
        else:
            return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

    def is_primitive(self):
        """
        Determines the difference between
        WLTD and UNDECIDED
        """
        # TODO: Don't violate abstraction barrier...
        # Notably: ("WIN", "LOSS", "TIE", "DRAW")
        return self.state in PRIMITIVES

class Job:
    """
    A job has a game state, parent, type, and also has a priority for placing
    jobs in a queue for the processes to work on.
    """
    # A list of possible job types.
    LOOK_UP           = "lookup"
    DISTRIBUTE        = "distribute"
    CHECK_FOR_UPDATES = "check_for_updates"
    SEND_BACK         = "send_back"
    FINISHED          = "finished"
    RESOLVE           = "resolve"

    _priority_table = {
            FINISHED          : 0,
            LOOK_UP           : 1,
            RESOLVE           : 2,
            SEND_BACK         : 3,
            DISTRIBUTE        : 4,
            CHECK_FOR_UPDATES : 5
    }

    def _assign_priority(self):
        self.priority = self._priority_table[self.job_type]

    def __init__(self, job_type, game_state=None, parent=None, job_id=None):
        self.job_type   = job_type
        self.game_state = game_state
        self.parent     = parent
        self.job_id     = job_id
        self._assign_priority()

    def __lt__(self, other):
        """
        Compares two Job objects based off the priority
        they have.
        """
        return self.priority < other.priority

class Process:
    """
    Class that defines the behavior what each process should do
    """
    IS_FINISHED = False

    INITIAL_POS = GameState(game_module.initial_position)
    ROOT = INITIAL_POS.get_hash()

    def dispatch(self, job):
        """
        Given a particular kind of job, decide what to do with
        it, this can range from lookup, to distributing, to
        checking for recieving.
        """
        _dispatch_table = {
                Job.FINISHED          : self.finished,
                Job.LOOK_UP           : self.lookup,
                Job.RESOLVE           : self.resolve,
                Job.DISTRIBUTE        : self.distribute,
                Job.SEND_BACK         : self.send_back,
                Job.CHECK_FOR_UPDATES : self.check_for_updates
        }
        return _dispatch_table[job.job_type](job)

    def _queue_to_str(self, q):
        """
        For debugging purposes.
        Prints the job type for each job in the job queue.
        """
        return ', '.join([str(j.job_type) for j in q.queue])

    def _log_work(self, work):
        check_for_updates = 'check_for_updates, check_for_updates'
        if not(self._queue_to_str(work) == '' or self._queue_to_str(work) == check_for_updates):
            logging.info("Machine " + str(self.rank) + " has " + self._queue_to_str(self.work) + " lined up to work on")
            logging.info("Machine " + str(self.rank) + " has resolved: " + str(self.resolved) + " " + str(self.remote))


    def run(self):
        """
        Main loop for each process
        """
        # TODO
        while not Process.IS_FINISHED:
            if __debug__:
                time.sleep(.05)
                self._log_work(self.work)
            if self.rank == Process.ROOT and Process.INITIAL_POS.pos in self.resolved:
                Process.IS_FINISHED = True
                logging.info('Finished')
                print (self.resolved[Process.INITIAL_POS.pos])
                comm.Abort()
            if self.work.empty():
                self.add_job(Job(Job.CHECK_FOR_UPDATES))
            job = self.work.get()
            result = self.dispatch(job)
            if result is None: # Check for updates returns nothing.
                continue
            self.add_job(result)

    def __init__(self, rank):
        self.rank = rank
        self.work = PriorityQueue()
        self.resolved = {}
        self.remote = {}
        # As for recieving, should test them when appropriate
        # in the run loop.
        self.received = []
        # Keep a dictionary of "distributed tasks"
        # Should contain an id associated with the length of task.
        # For example, you distributed rank 0 has 4, you wish to
        # distribute 3, 2. Give it an id, like 1 and associate it
        # with length 2. Then once all the results have been received
        # you can compare the length, and then reduce the results.
        # solving this particular distributed task.
        self._id = 0              # Job id tracker.
        self._counter = {}        # A job_id -> Number of results
                                  # remaining.
        self._pending = {}        # job_id -> [ Job, GameStates, ... ]
                                  # Resolved.
        # Main process will terminate everyone by bcasting the value of
        # finished to True.
        self.finished = False

    def add_job(self, job):
        """
        Adds a job to the priority queue so it may be worked on at an
        appropriate time
        """
        self.work.put(job)

    def finished(self, job):
        """
        Occurs when the root node has detected that the game has been solved
        """
        IS_FINISHED = True

    def lookup(self, job):
        """
        Takes a GameState object and determines if it is in the
        resolved list. Returns the result if this is the case, None
        otherwise.
        """
        logging.info("Machine " + str(rank) + " looking up " + str(job.game_state.pos))
        try:
            res = self.resolved[job.game_state.pos]
            logging.info("Position " + str(job.game_state.pos) + " has been resolved")
            job.game_state.state = res
            return Job(Job.SEND_BACK, job.game_state, job.parent, job.job_id)
        except KeyError: # Not in dictionary.
            # Try to see if it is_primitive:
            if job.game_state.is_primitive():
                logging.info("Position " + str(job.game_state.pos) + " is primitive")
                self.remote[job.game_state.pos] = 0
                job.game_state.remoteness = 0
                self.resolved[job.game_state.pos] = game_module.primitive(job.game_state.pos)
                return Job(Job.SEND_BACK, job.game_state, job.parent, job.job_id)
            return Job(Job.DISTRIBUTE, job.game_state, job.parent, job.job_id)

    def _add_pending_state(self, job, children):
        # Refer to lines 179-187 for an explanation of why this
        # is done.
        self._pending[self._id] = [job]
        self._counter[self._id] = len(list(children))

    def _update_id(self):
        """
        Changes the id so there is no collision.
        """
        self._id += 1

    def distribute(self, job):
        """
        Given a gamestate distributes the results to the appropriate
        children.
        """
        children = list(job.game_state.expand())
        # Add new pending state information.
        #logging.info('Found children ' + ', '.join([str(c.pos) for c in children]))
        self._add_pending_state(job, children)
        #logging.info('Found children ' + ', '.join([str(c.pos) for c in children]))
        # Keep a list of the requests made by isend. Something may
        # fail, so we will need to worry about error checking at
        # some point.
        for child in children:
            job = Job(Job.LOOK_UP, child, self.rank, self._id)
            logging.info("Machine " + str(rank)
                       + " found child " + str(job.game_state.pos)
                       + ", sending to " + str(child.get_hash()))

            comm.isend(job,  dest = child.get_hash())

        self._update_id()

    def check_for_updates(self, job):
        """
        Checks if there is new data from other Processes that needs to
        be received and prepares to recieve it if there is any new data.
        Returns True if there is new data to be recieved.
        Returns None if there is nothing to be recieved.
        """
        # Probe for any sources
        if comm.iprobe(source=MPI.ANY_SOURCE):
            # If there are sources recieve them.
            self.received.append(comm.recv(source=MPI.ANY_SOURCE))
            for job in self.received:
                self.add_job(job)

            self.recieved = [] # Clear recieved.

    def send_back(self, job):
        """
        Send the job back to the node who asked for the computation
        to be done.
        """
        logging.info("Machine " + str(rank) + " is sending back " + str(job.game_state.pos) + " to " + str(job.parent))
        resolve_job = Job(Job.RESOLVE, job.game_state, job.parent, job.job_id)
        comm.send(resolve_job, dest=resolve_job.parent)

    def _res_red(self, res1, res2):
        """
        Private method that helps reduce in resolve.
        """
        # Probably can be done in a "cleaner" way.
        if res1.state == LOSS and res2.state == LOSS:
            return WIN
        elif res1.state == WIN or res2.state == WIN:
            return LOSS
        elif res1.state == TIE or res2.state == TIE:
            return TIE
        elif res1.state == DRAW or res2.state == DRAW:
            return DRAW

    def _remoteness_reduce(self, rem1, rem2):
        """
        Private method that helps reduce remoteness
        """
        if rem1.state == WIN and rem2.state == WIN:
            return max(rem1.remoteness, rem2.remoteness) + 1
        elif rem2.state == WIN:
            return rem1.remoteness + 1
        elif rem1.state == WIN:
            return rem2.remoteness + 1
        else:
            return min(rem1.remoteness, rem2.remoteness) + 1


    def resolve(self, job):
        """
        Given a list of WIN, LOSS, TIE, (DRAW, well maybe for later)
        determine whether this position in the game tree is a WIN,
        LOSS, TIE, or DRAW.
        """
        self._counter[job.job_id] -= 1
        self._pending[job.job_id].append(job.game_state) # [Job, GameState, ... ]
        if self._counter[job.job_id] == 0: # Resolve _pending.
            to_resolve = self._pending[job.job_id][0] # Job
            resolve_data = self._pending[job.job_id][1:] # [GameState, GameState, ...]
            self.resolved[to_resolve.game_state.pos] = functools.reduce(self._res_red, resolve_data)
            self.remote[to_resolve.game_state.pos] = functools.reduce(self._remoteness_reduce, resolve_data)
            job.game_state.state = self.resolved[to_resolve.game_state.pos]
            job.game_state.remoteness = self.remote[to_resolve.game_state.pos]
            logging.info("Position " + str(job.game_state.pos) + " has been resolved, remoteness: " + str(self.remote[to_resolve.game_state.pos]))
            to = Job(Job.SEND_BACK, job.game_state, to_resolve.parent, to_resolve.job_id)
            self.add_job(to)

process = Process(rank)
if process.rank == Process.ROOT:
    initial_gamestate = GameState(game_module.initial_position)
    initial_job = Job(Job.LOOK_UP, initial_gamestate, process.rank, 0) # Defaults at zero, TODO: Fix abstraction violation.
    process.add_job(initial_job)

process.run()
