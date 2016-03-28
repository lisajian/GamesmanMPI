from .utils import *
from src.game_state import GameState
import numpy as np
import logging

class Job:
    """
    A job has a game state, parent, type, and also has a priority for placing
    jobs in a queue for the processes to work on.
    """
    # A list of possible job types.
    FINISHED          = 0
    LOOK_UP           = 1
    RESOLVE           = 2
    SEND_BACK         = 3
    DISTRIBUTE        = 4
    CHECK_FOR_UPDATES = 5

    # Special number associated with the initial job id.
    INITIAL_JOB_ID = 0

    def _assign_priority(self):
        self.priority = self.job_type

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

    @staticmethod
    def construct_job(numpy_rep):
        logging.debug("Constructing job from " + str(numpy_rep))
        pos_length = numpy_rep.size - POS_START_INDEX
        pos = numpy_rep[(-1 * pos_length):]
        gs = GameState(pos, remoteness=numpy_rep[REMOTENESS_INDEX], state=numpy_rep[STATE_INDEX])
        to_ret = Job(int(numpy_rep[JOB_TYPE_INDEX]), game_state=gs, parent=int(numpy_rep[PARENT_INDEX]), job_id=int(numpy_rep[JOB_ID_INDEX]))
        logging.debug("Constructed job with following data: " + str(to_ret.__dict__))
        logging.debug("GameState: " + str(gs.__dict__))
        return to_ret

    def construct_numpy_representation(self):
        metadata = np.array([self.job_type, self.parent, self.job_id, self.game_state.remoteness, self.game_state.state])
        return np.append(metadata, self.game_state.pos)
