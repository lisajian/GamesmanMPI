from .utils import *
import numpy as np

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
        pos_length = numpy_rep.size - utils.POS_START_INDEX
        pos = numpy_rep[(-1 * pos_length):]
        gs = GameState(pos, remoteness=numpy_rep[utils.REMOTENESS_INDEX], state=numpy_rep[utils.STATE_INDEX])
        return Job(numpy_rep[utils.JOB_TYPE_INDEX], game_state=gs, parent=numpy_rep[utils.PARENT_INDEX], job_id=numpy_rep[utils.JOB_ID_INDEX])

    def construct_numpy_representation(self):
        metadata = np.array([self.job_type, self.parent, self.job_id, self.game_state.state, self.game_state.remoteness])
        return np.append(metadata, self.game_state.pos)
